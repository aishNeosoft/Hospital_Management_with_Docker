from django.urls import path
from .views import *


urlpatterns = [
    #Boarding Pages
    path('', dashboard_page, name='dashboard'),
    path('patient/dashboard/', patient_dashboard, name='patient_dashboard'),
    
    #Authentication Pages
    path('login/', login_page, name='login'),
    path('logout/', logout_page, name='logout'),
    path('sign-up/', sign_up_page, name='sign_up_page'),

    #Doctor Pages
    path('add/patient/', add_patient, name='add_patient'),
    path('listing/patient/', patient_listing, name='patient_listing'),
    path('update/patient/<int:id>/', update_patient, name='update_patient'),
    path('delete/patient/<int:id>/', delete_patient, name='delete_patient'),

    #Medical Reports
    path('show/report/', show_reports_count, name='show_reports_count'),
    path('delete/report/<int:id>/', delete_report, name='delete_report'),
    path('generate/report/<int:id>/', generate_report_csv, name='generate_report'),
    path('patient/medical/reports/<int:id>/', check_reports, name='medical_reports'),
    path('patient/medical/reports/', only_check_reports, name='medical_patient_reports'),
]
