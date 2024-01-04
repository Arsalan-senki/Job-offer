from django.contrib import admin

# Register your models here.

from .models import *



# admin.site.register(Employer)
# admin.site.register(Employee)
admin.site.register(Company)
admin.site.register(JobCommercial)
admin.site.register(Message)
admin.site.register(Cities)