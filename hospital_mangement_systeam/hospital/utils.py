import json
from decimal import Decimal
from django.core.serializers.json import DjangoJSONEncoder

from .models import CustomUser, Doctor, Patient, MedicalReport

def get_medical_report_data(patient):
    # Fetch all medical reports for the specified patient
    reports = MedicalReport.objects.filter(patient=patient).order_by('recorded_at')
    
    report_data = {}
    
    for report in reports:
        report_type = report.type
        if report_type not in report_data:
            report_data[report_type] = {
                'timestamps': [],
                'values': []
            }
        
        recorded_date = report.recorded_at.date()
        # Append timestamp and value to the corresponding report type
        report_data[report_type]['timestamps'].append(str(recorded_date))
        report_data[report_type]['values'].append(float(report.value))
    
    return report_data


def prepare_line_chart_data(patient):
    report_data = get_medical_report_data(patient)
    
    if not report_data:
        # Handle case where no report data is available
        return json.dumps({'labels': [], 'datasets': []})
    
    # Extract timestamps from the first report type, if available
    first_report_type = next(iter(report_data))
    if 'timestamps' in report_data[first_report_type]:
        labels = report_data[first_report_type]['timestamps']
    else:
        # Handle case where no timestamps are available for the first report type
        labels = []
    
    # Prepare datasets for Chart.js
    datasets = []
    for report_type, data in report_data.items():
        dataset = {
            'label': report_type,
            'data': data['values'],
            'borderColor': 'rgb(75, 192, 192)',
            'lineTension': 0.1
        }
        datasets.append(dataset)
    
    # Assemble the complete chart data
    chart_data = {
        'labels': labels,
        'datasets': datasets
    }
    
    # Convert data to JSON format for JavaScript usage
    return json.dumps(chart_data, cls=DjangoJSONEncoder)

#User Validation 
def validate_user_registration(first_name, last_name, email, phone, password):

    # Validate first_name
    if not first_name:
        return 'First Name cannot be empty'
    else:
        pass
    
    # Validate last_name
    if not last_name:
        return 'Last Name cannot be empty'
    else:
        pass
    
    # Validate email
    if not email:
        return 'Email cannot be empty'
    elif CustomUser.objects.filter(email=email).exists():
        return 'Email already exists'
    elif '@' not in email or '.' not in email:
        return 'Invalid email format'
    else:
        pass
    
    # Validate Phone Number
    if len(phone) != 10:
        return 'Phone number must be 10 digits'
    elif not phone.isdigit():
        return 'Phone number should only contain digits'
    elif Patient.objects.filter(patient_phone_number=phone).exists() or Doctor.objects.filter(doctor_phone_number=phone).exists():
        return 'Phone number already exist'

    # Validate password
    if not password:
        return 'Password cannot be empty'
    elif len(password) <= 8:
        return 'Password should be at least 8 characters long'
    else:
        pass
    
    return True


def check_value(value):
    # Validate Reading value
    if value < 79 or value > 121:
        return 'Reading Range Between 80 to 120'

    return True
