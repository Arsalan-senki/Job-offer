from django.forms import ModelForm
from .models import Company, Job, Cities
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class CompanyForm(forms.ModelForm):
    city = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'city-autocomplete'}))

    class Meta:
        model = Company
        fields = ['name', 'email', 'telephone_number', 'city', 'manager']

    def clean_city(self):
        city_name = self.cleaned_data['city']
        if city_name:
            city, created = Cities.objects.get_or_create(name=city_name.lower())
            return city
        return None

class CompanyEditForm(forms.ModelForm):
    city = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'city-autocomplete'}))

    class Meta:
        model = Company
        fields = ['name', 'email', 'telephone_number', 'city', 'manager']

    def clean_city(self):
        city_name = self.cleaned_data['city']
        if city_name:
            city, created = Cities.objects.get_or_create(name=city_name.lower())
            return city
        return None


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['subject', 'talents', 'company', 'description']


class JobEditForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['subject', 'talents', 'company', 'description']