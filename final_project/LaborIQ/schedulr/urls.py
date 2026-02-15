from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('add_employee', views.add_employee, name='add_employee'),
    path('employees', views.employees_view, name='employees'),
    path('shifts', views.shifts_view, name='shifts'),
    path('add_shift', views.add_shift, name='add_shift'),
    path('shifts/<int:employee_id>/delete/', views.delete_employee)
]