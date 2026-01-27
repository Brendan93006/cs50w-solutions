from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Order, Trade, Account, Market, PriceSnapshot, Asset

# Create your views here.

def index(request):
    return render(request, 'trading/index.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')

        email = request.POST.get('email')

        password = request.POST.get('password')
        confirmation = request.POST.get('comfirmation')
        if password != confirmation:
            return render(request, 'trading/register.html', { "message": 'Passwords must match.'})
        
        try:
            user = User.objects.create_user(email=email, username=username, password=password)
            user.save()
        except IntegrityError:
            return render(request, 'trading/register.html', { 'message': 'Username already taken' })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, 'trading/register.html')
