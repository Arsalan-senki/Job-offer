from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True, blank=False,error_messages={'unique': "A user with that email already exists.",})
    
    telephone_number = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1)
    certificate = models.CharField(max_length=100, blank=True, null=True)
    degree = models.CharField(max_length=50, blank=True, null=True)
    age = models.IntegerField(default=20, blank=True, null=True)
    is_employer = models.BooleanField(default=False)
    # city = models.CharField(max_length=100, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    objects = CustomUserManager()