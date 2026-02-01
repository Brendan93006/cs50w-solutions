from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.

class User(AbstractUser):
    pass

class Employee(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    name = models.CharField(max_length=30, default="")
    position = models.CharField(max_length=30)
    hire_date = models.DateField(auto_now_add=True)
    hourly_rate = models.DecimalField(max_digits=5, decimal_places=2)

class Shift(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="shifts")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

