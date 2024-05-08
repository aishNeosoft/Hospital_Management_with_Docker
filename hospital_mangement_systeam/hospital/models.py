from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of usernames.
    """
    def create_user(self, email, role, password=None, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, role, password=None, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, role, password, **extra_fields)

ROLE_CHOICES = (
    ('Doctor', 'Doctor'),
    ('Patient', 'Patient'),
)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["role"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'custom_user'


class Doctor(models.Model):
    doctor_first_name = models.CharField(max_length=100)
    doctor_last_name = models.CharField(max_length=100)
    doctor_email = models.EmailField()
    doctor_phone_number = models.CharField(max_length=15)
    doctor_address = models.CharField(max_length=255)
    doctor_department = models.CharField(max_length=200)
    doctor_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='doctor_user', default=1)

    def __str__(self):
        return self.doctor_user.email
    

class Patient(models.Model):
    patient_first_name = models.CharField(max_length=100)
    patient_last_name = models.CharField(max_length=100)
    patient_email = models.EmailField()
    patient_phone_number = models.CharField(max_length=15)
    patient_address = models.CharField(max_length=255)
    patient_status = models.BooleanField(default=False)
    check_patient_report = models.BooleanField(default=False)
    patient_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='patient_user', default=2)

    def __str__(self):
        return f"{self.patient_user.email}"
    

class MedicalReport(models.Model):
    TEMPERATURE = 'temperature'

    TYPE_CHOICES = [
        ('Temperature', _('Body Temperature')),
        ('Blood Pressure', _('Blood Pressure')),
        ('Pulse Rate', _('Pulse Rate')),
        ('Respiratory Rate', _('Respiratory Rate')),
        ('Weight', _('Weight')),
        ('Height', _('Height')),
        ('Blood Sugar Level', _('Blood Sugar Level')),
        ('Cholesterol Level', _('Cholesterol Level')),
        ('Oxygen Saturation', _('Oxygen Saturation')),
        ('Pain Level', _('Pain Level')),
        ('Allergy', _('Allergy')),
        ('Medication', _('Medication')),
        ('Symptoms', _('Symptoms')),
        ('Diagnosis', _('Diagnosis')),
        ('Treatment Plan', _('Treatment Plan'))
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_reports')
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, verbose_name=_('Type'))
    value = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_('Value'))
    recorded_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Recorded At'))

    class Meta:
        verbose_name = _('Medical Report')
        verbose_name_plural = _('Medical Reports')

    def __str__(self):
        return f"{self.get_type_display()} - {self.value} ({self.patient.patient_first_name} {self.patient.patient_last_name})"
    

# class Appointment(models.Model):
#     STATUS_CHOICES = [
#         ("requested", _("Requested")),
#         ("accepted", _("Accepted")),
#         ("declined", _("Declined")),
#     ]

#     patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='patient_appointments')
#     doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE, related_name='doctor_appointments')
#     reason_for_appointment = models.TextField(max_length=2500)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='requested')

#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ["-created_at"]

#     def __str__(self):
#         return f"{self.patient} -> {self.doctor} (Status: {self.get_status_display()})"


# class AppointmentRequest(models.Model):
#     patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='patient_requests')
#     doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE, related_name='doctor_requests')
#     reason_for_appointment = models.TextField(max_length=2500)
#     status = models.CharField(max_length=20, choices=Appointment.STATUS_CHOICES, default='requested')

#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ["-created_at"]

#     def __str__(self):
#         return f"{self.patient} -> {self.doctor} (Status: {self.get_status_display()})"
