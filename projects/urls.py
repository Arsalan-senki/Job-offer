
from django.contrib import admin
from django.urls import path
from . import views
app_name = 'website'

urlpatterns = [
    path('',views.home,name='home'),
    path('Jobs/<str:pk>',views.Jobs,name='jobs'),
    path('company/<str:pk>',views.company,name='companies'),
    path('create-company/',views.createCompany,name='create-Company'),
    path('delete-job/<str:pk>/',views.deletecompany,name='delete-company'),
    path('update-job/<str:pk>/',views.updatecompany,name='update-company'),
    path('create-commercials/', views.createCommercials, name='create-commercials'),
    path('jobs/', views.listCommercials, name='job-list'),
    path('delete-message/<str:pk>/',views.deleteMessage,name='delete-message'),
    path('result/', views.searchview, name='search'),
    path('create-job/', views.createCommercials, name='create-job'),
    path('dashboard/', views.home, name='dashboard'),
    
]
