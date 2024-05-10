#Django Imports
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

#Python Imports
import json

#Third Party Imports
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

#Projects Imports
from .utils import (check_value, 
                    prepare_line_chart_data,
                    validate_user_registration)

from .forms import (Doctor,
                    Patient, 
                    CustomUser,
                    PatientForm, 
                    MedicalReport, 
                    MedicalReportForm)


# Dashboard Page
@login_required(login_url='login')
def dashboard_page(request):
    user = request.user
    if request.user.is_authenticated:
        if user.role == 'Patient':
            return redirect('patient_dashboard')
    
    report_count = MedicalReport.objects.all().count()
    report_type_count = (
        MedicalReport.objects
        .values('type')
        .annotate(count=Count('type'))
        .order_by('type')
    )
    labels_json = json.dumps([item['type'] for item in report_type_count])
    data_json = json.dumps([item['count'] for item in report_type_count])

    active_reports_count = (
        MedicalReport.objects
        .filter(patient__patient_status=True) 
        .count()
    )
    inactive_reports_count = (
        MedicalReport.objects
        .filter(patient__patient_status=False)  
        .count()
    )

    active_data_json = json.dumps([active_reports_count, inactive_reports_count])

    patients = Patient.objects.all()
    user_instance = request.user

    msg1 = ''
    if "msg1" in request.session:
        msg1 = request.session["msg1"]
        del request.session["msg1"]

    return render(request, 'management/hospital/dashboard-page.html', {
        'patients': patients,
        'user': user_instance,
        'role': '',
        'count': len(patients),
        'labels_json': labels_json,
        'data_json': data_json,
        'active_data_json': active_data_json,
        'msg1': msg1,
        'report_count':report_count
    })


@login_required(login_url='login')
def patient_dashboard(request):
    patient_user = request.user
    patient = patient_user.patient_user

    line_chart_data = prepare_line_chart_data(patient)
    
    msg1 = ''
    if "msg1" in request.session:
        msg1 = request.session["msg1"]
        del request.session["msg1"]

    return render(request, 'management/hospital/patient_dashboard.html', {
        'line_chart_data': line_chart_data,
        'user': patient_user,
        'role': patient_user.role,
        'patients': Patient.objects.all(),
        'msg1':msg1
    })


# Authentication 

def login_page(request):
    if request.method == 'POST':
       email = request.POST['email']
       password = request.POST['password']
       user = authenticate(request,username=email,password=password)
       if user is not None:
           login(request,user)
           return redirect('dashboard')
    return render(request,'management/common/Login.html')


def sign_up_page(request):
    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        address = request.POST['address']
        phone = request.POST['phone_number']

        validate_user = validate_user_registration(first_name, last_name, email, phone, password)
        if validate_user != True:
            return render(request, 'management/common/register-user.html', {'msg1':validate_user})

        user = CustomUser.objects.create_user(email=email, password=password, role=role)

        if role == 'Doctor':
            doctor = Doctor.objects.create(doctor_user=user)
            doctor.doctor_first_name = first_name
            doctor.doctor_last_name = last_name
            doctor.doctor_address = address
            doctor.doctor_phone_number = phone
            doctor.doctor_email = email
            doctor.save()

        elif role == 'Patient':
            patient = Patient.objects.create(patient_user=user)
            patient.patient_first_name = first_name
            patient.patient_last_name = last_name
            patient.patient_address = address
            patient.patient_phone_number = phone
            patient.patient_email = email
            patient.save()
        return redirect('login')
    
    return render(request, 'management/common/register-user.html')


@login_required(login_url='login')
def logout_page(request):
    logout(request)
    return redirect('login')


# Doctors View
@login_required(login_url='login')
def add_patient(request):
    patients = Patient.objects.all()
    form = PatientForm()
    if request.method == 'POST':
        email = request.POST['patient_email']
        password = 'Pass@1234'
        role = 'Patient'
        first_name = request.POST['patient_first_name']
        last_name = request.POST['patient_last_name']
        address = request.POST['patient_address']
        phone = request.POST['patient_phone_number']
        status = True if request.POST['patient_status'] == 'active' else False

        validate_user = validate_user_registration(first_name, last_name, email, phone, password)
        if validate_user != True:
            return render(request, 'management/hospital/patient_listing.html', {'msg1':validate_user,'patients':patients, 'form':form })
        user = CustomUser.objects.create_user(email=email, password=password, role=role)

        patient = Patient.objects.create(patient_user=user)
        patient.patient_first_name = first_name
        patient.patient_last_name = last_name
        patient.patient_address = address
        patient.patient_phone_number = phone
        patient.patient_email = email
        patient.patient_status = status
        patient.save()
        return redirect('patient_listing') 
    
    return render(request, 'management/hospital/patient_listing.html')


@login_required(login_url='login')
def update_patient(request, id):
    patient = Patient.objects.get(id=id)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('patient_listing')
    else:
        form = PatientForm(instance=patient)
    
    return render(request, 'management/hospital/update_patient.html', {'form': form})


@login_required(login_url='login')
def delete_patient(request, id):
    patient = Patient.objects.get(id=id)
    patient_user = patient.patient_user
    patient.delete()
    patient_user.delete()
    return redirect('patient_listing') 


@login_required(login_url='login')
def patient_listing(request):
    patients = Patient.objects.all()
    form = PatientForm()
    return render(request,'management/hospital/patient_listing.html', {'patients':patients, 'form':form})


@login_required(login_url='login')
def check_reports(request, id):
    patient = Patient.objects.get(id=id)
    medical_reports = patient.medical_reports.all().order_by('-recorded_at')
    if request.method == 'POST':
        valid_report_value = check_value(int(request.POST['value']))
        if valid_report_value != True:
            request.session["msg1"] = valid_report_value
            return redirect('medical_reports', id=patient.id)
        form = MedicalReportForm(patient.id, request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.patient = patient
            report.save()
            return redirect('medical_reports', id=patient.id)
    else:        
        form = MedicalReportForm(patient_id=patient.id)
    msg1 = ''
    if "msg1" in request.session:
        msg1 = request.session["msg1"]
        del request.session["msg1"]

    return render(request, 'management/hospital/medical-report.html', {'form': form, 'reports':medical_reports, 'patient':patient, "msg1":msg1})


@login_required(login_url='login')
def delete_report(request, id):
    report = MedicalReport.objects.get(id=id)
    patient = report.patient
    report.delete()
    return redirect('medical_reports', id=patient.id)


# Patient View
@login_required(login_url='login')
def only_check_reports(request):
    user = request.user
    patient = user.patient_user
    medical_reports = patient.medical_reports.all().order_by('-recorded_at')
    if not patient.check_patient_report:
        request.session["msg1"] = "You are not authorized to check medical reports."
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = MedicalReportForm(patient.id, request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.patient = patient
            report.save()
            return redirect('medical_reports', id=patient.id)
    else:
        form = MedicalReportForm(patient_id=patient.id)
    
    return render(request, 'management/hospital/medical-report.html', {'form': form, 'reports':medical_reports, 'patient':patient})


@login_required(login_url='login')
def show_reports_count(request):
    report_type_count = (
        MedicalReport.objects
        .values('type')
        .annotate(count=Count('type'))
        .order_by('type')
    )
    report_count_dict = {item['type']: item['count'] for item in report_type_count}   

    return render(request, 'management/hospital/check_reports.html', {'report_count_dict': report_count_dict})


@login_required(login_url='login')
def generate_report_csv(request, id):
    patient = Patient.objects.get(id=id)
    reports = patient.medical_reports.all()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="medical_report_{patient.patient_first_name}_{patient.patient_last_name}.pdf"'

    # Create PDF document using ReportLab
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)

    # Set PDF Title
    pdf.setTitle(f"Medical Report for {patient.patient_first_name} {patient.patient_last_name}")

    # Set PDF Content
    y_position = 750  # Start writing content from this y-position
    pdf.drawString(100, y_position, "Medical Report")
    y_position -= 20  # Move y-position up for next line

    # Write patient information
    pdf.drawString(100, y_position, f"Patient Name: {patient.patient_first_name} {patient.patient_last_name}")
    y_position -= 20

    # Write medical reports
    pdf.drawString(100, y_position, "Medical Reports:")
    y_position -= 20

    for report in reports:
        pdf.drawString(120, y_position, f"Type: {report.type}")
        y_position -= 15
        pdf.drawString(120, y_position, f"Value: {report.value}")
        y_position -= 20

    # Save the PDF content
    pdf.save()

    # Get the value of the BytesIO buffer and write it to the response
    pdf_bytes = buffer.getvalue()
    buffer.close()
    response.write(pdf_bytes)

    return response
