from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Employee, Shift

# Create your views here.

def index(request):
    return render(request, 'schedulr/index.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')

        email = request.POST.get('email')

        password = request.POST.get('password')
        confirmation = request.POST.get('comfirmation')
        if password != confirmation:
            return render(request, 'schedulr/register.html', { "message": 'Passwords must match.'})
        
        try:
            user = User.objects.create_user(email=email, username=username, password=password)
            user.save()
        except IntegrityError:
            return render(request, 'schedulr/register.html', { 'message': 'Username already taken' })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, 'schedulr/register.html')
    
def login_view(request):
    if request == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'schedulr/login.html', { "message": "Invalid username and/or password" })
    else:
        return render(request, 'schedulr/login.html')
    
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
            return render(request, 'schedulr/add_employee.html', { "message": "Must provide name/position/hourly rate." })
        else:
            employee = Employee.objects.create(name=name, position=position, hourly_rate=hourly_rate)
            employee.save()
        
        return render(request, 'schedulr/employees.html')
    
    else:
        return render(request, 'schedulr/add_employee.html')

@login_required
def employees_view(request):
    if request.method == 'GET':
        employees = Employee.objects.get(owner=request.user).all()

        return render(request, 'schedulr/employees.html', { "employees": employees })