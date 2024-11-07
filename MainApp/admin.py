from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(patient_details)
admin.site.register(patient_history)
admin.site.register(patienttodoctor)
admin.site.register(doctor_remarks)
admin.site.register(availabledoctors)
admin.site.register(admin_details)

