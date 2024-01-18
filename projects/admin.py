from django.contrib import admin

# Register your models here.

from .models import *



# admin.site.register(Employer)
# admin.site.register(Employee)
admin.site.register(Company)
admin.site.register(Job)
admin.site.register(Cities)
admin.site.register(ApplyJob)