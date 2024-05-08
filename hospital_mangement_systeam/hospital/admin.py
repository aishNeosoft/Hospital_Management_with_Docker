# admin.py in hospital app
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Doctor, Patient, MedicalReport


admin.site.register(CustomUser)
admin.site.register(Doctor)
admin.site.register(Patient)

class ReportAdmin(admin.ModelAdmin):
    list_display = ['type', 'value', 'recorded_at']

admin.site.register(MedicalReport, ReportAdmin)
