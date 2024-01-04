from collections import Counter
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .form import *
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .premissions import *
from django.core.paginator import Paginator
# from .utils import create_user



def home(request):
    context = {'object' : None}
    return render(request, 'home.html', context)


def Jobs(request, pk):
    # jobs = Job.objects.get(id=pk)
    pass


def company(request, pk):
    company = Company.objects.get(id=pk)
    messages = Message.objects.filter(company=company)
    participants = company.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            company=company,
            body=request.POST.get('body')
        )
        return redirect('companies', pk=company.pk)
    
    context = {'company': company, 'messages': messages,'participants': participants}
    return render(request, 'company.html', context)


@login_required(login_url='login')
@user_is_employer
def createCompany(request):

    form = CompanyForm()
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            company.employer = request.user
            company.save()
            return redirect('website:home')
    cities = Cities.objects.all()

    context = {'form': form, 'cities': cities}
    return render(request, 'create-company.html', context)


@login_required(login_url='login')
def updatecompany(request, pk):
    company = Company.objects.get(id=pk)
    form = CompanyForm(instance=company)

    if request.user != company.user:
        return HttpResponse('You are not the user of this company')

    if request.method == 'POST':
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            return redirect('website:home')

    context = {'form': form}
    return render(request, "Company-form.html", context)


@login_required(login_url='login')
def deletecompany(request, pk):
    job = Job.objects.get(id=pk)
    if request.method == 'POST':
        job.delete()
        return redirect('website:home')

    return render(request, 'delete.html', {'obj': job})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse("You are not allowed ")

    if request.method == 'POST':
        message.delete()
        return redirect('website:home')

    return render(request, 'delete.html', {'obj': message})


@login_required(login_url='account:login')
@user_is_employer
def createCommercials(request):
    if request.method == 'POST':
        form = JobCommercialForm(request.POST)
        if form.is_valid():
            commercial = form.save(commit=False)
            commercial.save()
            return redirect('website:home')
    
    else:
        form = JobCommercialForm()
    companies = Company.objects.filter(employer= request.user)
    context = {'form': form, 'companies': companies}
    return render(request, 'create-job.html', context)


def listCommercials(request):
    commercials = JobCommercial.objects.all()
    for com in commercials:
        com.talents = com.talents.strip().split(',')[:3]

    context = {'commercials' : commercials}
    return render(request, 'commercials_list.html', context)


def searchview(request):
    if 'q' in request.GET:
        jobs = JobCommercial.objects.order_by('created_date')
        job_title_or_city = request.GET['q']
        if job_title_or_city:
            jobs = jobs.filter(subject__icontains=job_title_or_city) | jobs.filter(company__city__name__icontains=job_title_or_city)
            for job in jobs : 
                job.talents = job.talents.strip().split(',')[:3]
            context = {'commercials' : jobs}
            return render(request, 'commercials_list.html', context)
        else:
            return redirect('website:home')
