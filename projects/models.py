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
    manager = models.CharField(blank=True, max_length=255, null=True)


    def __str__(self):
        return self.name


class Job(models.Model):
    subject = models.CharField(max_length=100)
    talents=models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    company = models.ForeignKey('Company', related_name='job_companie', blank=True, on_delete=models.SET_NULL, null=True)
    manager = models.ForeignKey(CustomUser, related_name='job_manager', on_delete=models.CASCADE, blank=True, null=True) 

    def __str__(self):
        return self.subject



class ApplyJob(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'name: {self.user.first_name} {self.user.last_name}, job: {self.job.subject}'


