from collections import Counter
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from .models import *
from .form import *
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .premissions import *
from django.core.paginator import Paginator
# from .utils import create_user


#home:
def home_view(request):

    return render(request, 'home.html')


#company:
@login_required(login_url='account:login')
@if_user_is_employer
def company_create_view(request):

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
    return render(request, 'company-create.html', context)

@login_required(login_url=('account:login'))
@if_user_is_employer
def company_manage_view(request):
    """
    """
    companies = []
    if request.user.is_employer:
        companies = Company.objects.filter(employer=request.user.id)
    context = {
        'companies': companies,
    }

    return render(request, 'company-manager.html', context)


@login_required(login_url=('account:login'))
@if_user_is_employer
def company_edit_view(request, pk):

    company = get_object_or_404(Company, pk=pk, employer=request.user.id)
    form = CompanyEditForm(request.POST or None, instance=company)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Your Job Post Was Successfully Updated!')
        return redirect('website:company-manage')
    context = {
        'form': form,
        'city_name':company.city.name
    }

    return render(request, 'company-edit.html', context)


@login_required(login_url=('account:login'))
@if_user_is_employer
def company_delete_view(request, pk):
    Company.objects.get(pk=pk).delete()
    return redirect('website:company-manage')



#jobs:
def job_list_view(request):
    jobs = Job.objects.all()
    for com in jobs:
        com.talents = com.talents.strip().split(',')[:3]

    paginator= Paginator(jobs, 6)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    context = {'page_obj' : page_obj}
    return render(request, 'job_list.html', context)


def search_view(request):
    jobs = Job.objects.order_by('created_date')
    if 'q' in request.GET:
        subject_city_company = request.GET['q']
        if subject_city_company:
            jobs = jobs.filter(
                subject__icontains = subject_city_company) | jobs.filter(
                company__city__name__icontains = subject_city_company) | jobs.filter(
                company__name__icontains = subject_city_company)
    for job in jobs : 
        job.talents = job.talents.strip().split(',')[:3]
    paginator= Paginator(jobs, 12)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    context = {'page_obj' : page_obj}
    return render(request, 'job_list.html', context)


@login_required(login_url='account:login')
def single_job_view(request, pk):
    if request.method == 'POST':
        pass
    else :
        if Job.objects.filter(pk=pk).exists():
            job = Job.objects.get(pk=pk)
            signed_details = None
            if ApplyJob.objects.filter(user=request.user, job=job).exists():
                signed_details = ApplyJob.objects.get(user=request.user, job=job)
            applied_employees = ApplyJob.objects.filter(job=job)
            context = {
                'job' : job,
                'signed_details' : signed_details,
                'applied_employees': applied_employees}
            return render(request, 'job-single.html', context)
        else:
            return redirect('website:home')


@login_required(login_url='account:login')
@if_user_is_employer
def create_Job_view(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.manager= request.user
            job.save()
            return redirect('website:home')
    
    else:
        form = JobForm()
    companies = Company.objects.filter(employer= request.user)
    if companies.count() == 0 : 
        messages.error(request, 'You should create a company first')
        return redirect('website:company-create')
    context = {'form': form, 'companies': companies}
    return render(request, 'job-create.html', context)  


@login_required(login_url=('account:login'))
def jobs_manage_view(request):
    """
    """
    jobs = []
    applied_jobs = []
    signs_count = {}
    if request.user.is_employer:
        jobs = Job.objects.filter(manager=request.user.id)
        for job in jobs:
            count = ApplyJob.objects.filter(job=job).count()
            signs_count[job.id] = count
    if not request.user.is_employer:
        applied_jobs = ApplyJob.objects.filter(user=request.user.id)
    context = {
        'jobs': jobs,
        'appliedjobs':applied_jobs,
        'signs_count': signs_count
    }

    return render(request, 'job-manager.html', context)


@login_required(login_url=('account:login'))
@if_user_is_employer
def job_edit_view(request, pk):

    job = get_object_or_404(Job, pk=pk, manager=request.user.id)
    form = JobEditForm(request.POST or None, instance=job)
    companies = Company.objects.filter(employer=request.user.id)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Your Job Post Was Successfully Updated!')
        return redirect('website:job-manage')
    context = {
        'companies' : companies,
        'form': form,
    }

    return render(request, 'job-edit.html', context)


@login_required(login_url=('account:login'))
@if_user_is_employer
def job_delete_view(request, pk):
    Job.objects.get(pk=pk).delete()
    return redirect('website:job-manage')


@login_required(login_url=('account:login'))
@if_user_is_employee
def job_apply_view(request, pk):
    if request.method == 'POST':
        job = Job.objects.get(pk=pk)
        ApplyJob.objects.get_or_create(user=request.user, job=job)
        messages.success(request, 'Job applied successfully')
        return redirect(reverse('website:job-single', kwargs={'pk': pk}))


@login_required(login_url=('account:login'))
@if_user_is_employee
def job_remove_apply_view(request, pk):
    if request.method == 'POST':
        job = Job.objects.get(pk=pk)
        ApplyJob.objects.filter(user=request.user, job=job).delete()                    
        messages.success(request, 'Job applicant removed successfully') 
        return redirect(reverse('website:job-single', kwargs={'pk': pk}))              





