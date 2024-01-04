from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

from account.models import CustomUser

class Cities(models.Model):
    name = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name
    

class Company(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    telephone_number = models.CharField(blank=True, max_length=15)
    city = models.ForeignKey(Cities, on_delete=models.CASCADE, blank=True, max_length=50)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    employer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return self.name


class JobCommercial(models.Model):
    subject = models.CharField(max_length=100)
    talents=models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    company = models.ForeignKey('Company', related_name='commercials_companies', blank=True, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.subject


class Message(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)  # Add this line
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[:50]





