
from django.contrib import admin
from django.urls import path
from . import views
app_name = 'website'

urlpatterns = [
    path('',views.home_view,name='home'),

    path('company-create/', views.company_create_view, name='company-create'),
    path('company-manage/', views.company_manage_view, name='company-manage'),
    path('company-edit/<int:pk>', views.company_edit_view, name='company-edit'),
    path('company-delete/<int:pk>', views.company_delete_view, name='company-delete'),

    path('search/', views.search_view, name='search'),

    path('jobs/', views.job_list_view, name='job-list'),
    path('job-create/', views.create_Job_view, name='job-create'),
    path('job-manager/', views.jobs_manage_view, name='job-manage'),
    path('job-single/<int:pk>', views.single_job_view, name='job-single'),
    path('job-edit/<int:pk>', views.job_edit_view, name='job-edit'),
    path('job-delete/<int:pk>', views.job_delete_view, name='job-delete'),
    path('job-sign/<int:pk>', views.job_apply_view, name='job-apply'),
    path('job-remove-apply/<int:pk>', views.job_remove_apply_view, name='job-remove-apply'),
    
]
