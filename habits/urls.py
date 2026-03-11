from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add/', views.add_habit, name='add_habit'),
    path('edit/<int:pk>/', views.edit_habit, name='edit_habit'),
    path('delete/<int:pk>/', views.delete_habit, name='delete_habit'),
    path('toggle/<int:pk>/', views.toggle_habit, name='toggle_habit'),
    path('report/', views.report_view, name='report'),
    path('detail/<int:pk>/', views.habit_detail, name='habit_detail'),
]
