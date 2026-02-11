from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError, OperationalError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import User, Employee, Shift

from datetime import date, timedelta, time, datetime

# Create your views here.

def index(request):

    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')

        email = request.POST.get('email')

        password = request.POST.get('password')
        confirmation = request.POST.get('confirmation')
        if password != confirmation:
            return render(request, 'register.html', { "message": 'Passwords must match.'})
        
        try:
            user = User.objects.create_user(email=email, username=username, password=password)
            user.save()
        except IntegrityError:
            return render(request, 'register.html', { 'message': 'Username already taken' })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, 'register.html')
    
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'login.html', { "message": "Invalid username and/or password" })
    else:
        return render(request, 'login.html')
    
@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def add_employee(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        position = request.POST.get('position')
        hourly_rate = request.POST.get('hourly_rate')

        if not name or not position or not hourly_rate:
            return render(request, 'add_employee.html', { "message": "Must provide name/position/hourly rate." })
        else:
            employee = Employee.objects.create(name=name, position=position, hourly_rate=hourly_rate, owner=request.user)
            employee.save()
            return HttpResponseRedirect(reverse('employees'))
    
    else:
        return render(request, 'add_employee.html')

@login_required
def employees_view(request):
    if request.method == 'GET': 
        employees = Employee.objects.filter(owner=request.user).all()
        if employees.count() == 0:
            return render(request, 'employees.html', { "employees": employees, "message": "No employees available" })
        else:
            return render(request, 'employees.html', { "employees": employees })
        
@login_required
def shifts_view(request):
    if request.method == 'GET':
        today = timezone.localdate()

        start_of_week = today - timedelta(days=today.weekday())
        week_start = datetime.combine(start_of_week, time.min)
        week_end = week_start + timedelta(days=7)

        tz = timezone.get_current_timezone()
        week_start = timezone.make_aware(week_start, timezone=tz)
        week_end = timezone.make_aware(week_end, timezone=tz)

        shifts = Shift.objects.filter(start_time__lt=week_end, end_time__gte=week_start).order_by("start_time")

        return render(request, 'shifts.html', {"shifts": shifts})
    elif request.method == 'POST':
        return render(request, 'add_shift.html')

    
@login_required
def add_shift(request):
    if request.method == 'POST':
        employee = get_object_or_404(Employee, id=request.POST.get("employee_id"))

        start_time = request.POST.get("start_time")

        end_time = request.POST.get("end_time")

        if not employee or not start_time or not end_time:
            return render(request, 'add_shift.html', { "message": "Must provide employee/start time/end time." })
        else:
            shift = Shift.objects.create(employee=employee, start_time=start_time, end_time=end_time)
            shift.save()
            return HttpResponseRedirect(reverse('shifts'))
    elif request.method == 'GET':
        employees = Employee.objects.filter(owner=request.user).all()
        return render(request, 'add_shift.html', { "employees": employees })
