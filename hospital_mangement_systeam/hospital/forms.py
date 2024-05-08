from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import *


ROLE_CHOICES = (
    ('Doctor', 'Doctor'),
    ('Patient', 'Patient'),
)

class NewUserForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hide specific password validation messages
        for fieldname in ['password1', 'password2', 'username']:
            self.fields[fieldname].help_text = None

    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone_number = forms.CharField(max_length=15, required=True)  
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'phone_number', 'role']

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone_number = self.cleaned_data['phone_number']
        user.role = self.cleaned_data['role']

        if commit:
            user.save()
        return user
    
class CustomUserSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = CustomUser
        fields = ['email', 'role', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            if user.role == 'Doctor':
                Doctor.objects.create(doctor_user=user)
            elif user.role == 'Patient':
                Patient.objects.create(patient_user=user)
        return user
    

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['patient_first_name', 'patient_last_name', 'patient_email', 'patient_phone_number', 'patient_address', 'patient_status']



class MedicalReportForm(forms.ModelForm):
    class Meta:
        model = MedicalReport
        fields = ['type', 'value']

    def __init__(self, patient_id, *args, **kwargs):
        super(MedicalReportForm, self).__init__(*args, **kwargs)
        self.initial['patient'] = patient_id  

    def clean_value(self):
        value = self.cleaned_data['value']
        # Add custom validation logic if needed
        return value
