from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils import timezone
from .models import Habit, HabitLog
from .forms import HabitForm, HabitLogForm

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'habits/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'habits/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    today = timezone.now().date()
    habits = Habit.objects.filter(user=request.user, is_active=True)
    habit_data = []
    for habit in habits:
        log, created = HabitLog.objects.get_or_create(habit=habit, date=today)
        habit_data.append({
            'habit': habit,
            'log': log,
            'streak': habit.get_streak(),
        })
    return render(request, 'habits/dashboard.html', {'habit_data': habit_data, 'today': today})

@login_required
def add_habit(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            return redirect('dashboard')
    else:
        form = HabitForm()
    return render(request, 'habits/habit_form.html', {'form': form, 'title': 'Add Habit'})

@login_required
def edit_habit(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    if request.method == 'POST':
        form = HabitForm(request.POST, instance=habit)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = HabitForm(instance=habit)
    return render(request, 'habits/habit_form.html', {'form': form, 'title': 'Edit Habit'})

@login_required
def delete_habit(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    if request.method == 'POST':
        habit.is_active = False
        habit.save()
        return redirect('dashboard')
    return render(request, 'habits/confirm_delete.html', {'habit': habit})

@login_required
def toggle_habit(request, pk):
    today = timezone.now().date()
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    log, created = HabitLog.objects.get_or_create(habit=habit, date=today)
    log.completed = not log.completed
    log.save()
    return redirect('dashboard')

@login_required
def habit_detail(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    logs = HabitLog.objects.filter(habit=habit).order_by('-date')[:30]
    return render(request, 'habits/habit_detail.html', {
        'habit': habit,
        'logs': logs,
        'streak': habit.get_streak()
    })


def report_view(request):
    from django.contrib.auth.decorators import login_required
    from django.utils import timezone
    today = timezone.now().date()
    start_week = today - timezone.timedelta(days=7)
    start_month = today - timezone.timedelta(days=30)
    habits = Habit.objects.filter(user=request.user, is_active=True)
    report_data = []
    for habit in habits:
        weekly_done = HabitLog.objects.filter(habit=habit, date__gte=start_week, completed=True).count()
        monthly_done = HabitLog.objects.filter(habit=habit, date__gte=start_month, completed=True).count()
        report_data.append({
            'habit': habit,
            'weekly_done': weekly_done,
            'weekly_percent': int((weekly_done / 7) * 100),
            'monthly_done': monthly_done,
            'monthly_percent': int((monthly_done / 30) * 100),
            'streak': habit.get_streak(),
        })
    return render(request, 'habits/report.html', {
        'report_data': report_data,
        'today': today,
        'user': request.user,
    })
