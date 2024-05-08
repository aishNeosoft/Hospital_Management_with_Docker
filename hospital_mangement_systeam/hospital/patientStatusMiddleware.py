from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect

from .models import Patient 


class PatientStatusMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # breakpoint()
            if hasattr(request.user, 'role') and request.user.role == 'Patient':
                try:
                    patient = Patient.objects.get(patient_user=request.user)
                    if not patient.patient_status:
                        patient.check_patient_report = False
                        patient.save()
                    else:
                        patient.check_patient_report = True
                        patient.save()

                except Patient.DoesNotExist:
                    pass

        response = self.get_response(request)
        return response
