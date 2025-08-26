from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


class User(AbstractUser):
    """Custom User model with role-based authentication"""
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
        ('receptionist', 'Receptionist'),
    ]
    
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='patient')
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'role']
   
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"
    
    def get_role_display(self):
        return dict(self.ROLE_CHOICES)[self.role]


class DoctorProfile(models.Model):
    """Doctor profile model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    specialization = models.CharField(max_length=100, blank=True)
    license_number = models.CharField(max_length=50, blank=True)
    years_experience = models.PositiveIntegerField(default=0)
    bio = models.TextField(blank=True)
    
    def __str__(self):
        return f"Dr. {self.user.get_full_name()}"


class PatientProfile(models.Model):
    """Patient profile model"""
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    date_of_birth = models.DateField(blank=True,null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    address = models.TextField(blank=True)
    emergency_contact = models.CharField(max_length=15, blank=True)
    medical_history = models.TextField(blank=True)
    allergies = models.TextField(blank=True)
    blood_group = models.CharField(max_length=5, blank=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.date_of_birth}"
   
    @property
    def age(self):
        from datetime import date
        """Return patient age in years, or None if DOB not set"""
        if not self.date_of_birth:
            return None
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )

class Patient(models.Model):
    """Patient model for ultrasound records"""
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    full_name = models.CharField(max_length=200)
    date_of_birth = models.DateField(blank=True,null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=15)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Link to user profile if exists
    user_profile = models.OneToOneField(PatientProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='patient_record')
    
    def __str__(self):
        return f"{self.full_name} ({self.date_of_birth})"
    
    @property
    def age(self):
        from datetime import date
        """Return patient age in years, or None if DOB not set"""
        if not self.date_of_birth:
            return None
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )

class Appointment(models.Model):
    """Appointment model"""
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'doctor'})
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-appointment_date', '-appointment_time']
    
    def __str__(self):
        return f"{self.patient.full_name} - {self.appointment_date} {self.appointment_time}"


class UltrasoundReport(models.Model):
    """Ultrasound report model"""
    PREGNANCY_TYPE_CHOICES = [
        ('singleton', 'Singleton'),
        ('twins', 'Twins'),
        ('triplets', 'Triplets'),
    ]
    
    SCAN_TYPE_CHOICES = [
        ('longitudinal', 'Longitudinal'),
        ('transverse', 'Transverse'),
        ('oblique', 'Oblique'),
    ]
    
    FETAL_POSITION_CHOICES = [
        ('cephalic', 'Cephalic'),
        ('breech', 'Breech'),
        ('floating', 'Floating'),
    ]
    
    FETAL_STATUS_CHOICES = [
        ('live', 'Live'),
        ('not_live', 'Not Live'),
    ]
    
    PLACENTA_POSITION_CHOICES = [
        ('anterior', 'Anterior'),
        ('posterior', 'Posterior'),
        ('fundal', 'Fundal'),
        ('left_lateral', 'Left Lateral'),
        ('right_lateral', 'Right Lateral'),
    ]
    
    PLACENTA_MATURITY_CHOICES = [
        ('mature', 'Mature'),
        ('immature', 'Immature'),
    ]
    
    CERVICAL_OS_CHOICES = [
        ('closed', 'Closed'),
        ('open', 'Open'),
    ]
    
    LIQUOR_VOLUME_CHOICES = [
        ('adequate', 'Adequate'),
        ('increased', 'Increased'),
        ('reduced', 'Reduced'),
    ]
    
    FETAL_ANOMALY_CHOICES = [
        ('nil_obvious', 'Nil Obvious'),
        ('specific', 'Specific'),
        ('normal', 'Normal'),
        ('abnormal', 'Abnormal'),
    ]
    STATUS_CHOICES = [
        ('ready', 'Ready'),
        ('printed', 'Printed'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ready')
    
    # Basic Information
    report_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='ultrasound_reports')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'doctor'})
    scan_date = models.DateField()
    indication = models.CharField(max_length=200, default="F W B & G A")
    hospital = models.CharField(max_length=200, default="God's Grace Ultrasound")
    
    # Pregnancy Details
    pregnancy_type = models.CharField(max_length=20, choices=PREGNANCY_TYPE_CHOICES, blank=True)
    scan_type = models.CharField(max_length=20, choices=SCAN_TYPE_CHOICES, blank=True)
    fetal_position = models.CharField(max_length=20, choices=FETAL_POSITION_CHOICES, blank=True)
    fetal_status = models.CharField(max_length=20, choices=FETAL_STATUS_CHOICES, blank=True)
    
    # Fetal Measurements
    bdp = models.CharField(max_length=50, blank=True)  
    crl = models.CharField(max_length=50, blank=True)  
    fl = models.CharField(max_length=50, blank=True)   
    hc = models.CharField(max_length=50, blank=True)   
    ac = models.CharField(max_length=50, blank=True)   
    suspected_sex = models.CharField(max_length=20, blank=True)
    average_fetal_age = models.CharField(max_length=20, blank=True)
    
    # Placenta
    placenta_position = models.CharField(max_length=20, choices=PLACENTA_POSITION_CHOICES, blank=True)
    placenta_maturity = models.CharField(max_length=20, choices=PLACENTA_MATURITY_CHOICES, blank=True)
    
    # Cervix & Liquor
    distance_from_cervix = models.CharField(max_length=50, blank=True)
    pravaria = models.CharField(max_length=50, blank=True)
    cervical_os = models.CharField(max_length=20, choices=CERVICAL_OS_CHOICES, blank=True)
    cervical_os_measurement = models.CharField(max_length=50, blank=True)
    intact_cervix_length = models.CharField(max_length=50, blank=True)
    
    # Liquor & EFW
    liquor_volume = models.CharField(max_length=20, choices=LIQUOR_VOLUME_CHOICES, blank=True)
    afi = models.CharField(max_length=50, blank=True)  
    efw = models.CharField(max_length=50, blank=True) 
    
    # Dates & Anomalies
    uss_lmp = models.CharField(max_length=50, blank=True)  
    edd = models.CharField(max_length=50, blank=True)      
    fetal_anomalies = models.CharField(max_length=20, choices=FETAL_ANOMALY_CHOICES, blank=True)
    
    # Additional Information
    remarks = models.TextField(blank=True)
    signature = models.CharField(max_length=255, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    exclude = ['patient', 'doctor', 'signature'] 
    
    class Meta:
        ordering = ['-scan_date', '-created_at']
    
    def __str__(self):
        return f"Report {self.report_id} - {self.patient.full_name} - {self.scan_date}"
    
    def get_absolute_url(self):
        return f'/reports/{self.report_id}/'


# Signals to automatically create profiles
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create profile when user is created"""
    if created:
        if instance.role == 'doctor':
            DoctorProfile.objects.create(user=instance)
        elif instance.role == 'patient':
            PatientProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save profile when user is saved"""
    if instance.role == 'doctor' and hasattr(instance, 'doctor_profile'):
        instance.doctor_profile.save()
    elif instance.role == 'patient' and hasattr(instance, 'patient_profile'):
        instance.patient_profile.save()

@receiver(post_save, sender=PatientProfile)
def sync_patient_data(sender, instance, created, **kwargs):
    """Sync patient profile data with Patient model"""
    if created:
        # Create a Patient record when PatientProfile is created
        Patient.objects.create(
            full_name=instance.user.get_full_name(),
            date_of_birth=instance.date_of_birth,
            gender=instance.gender,
            phone=instance.user.phone,
            user_profile=instance
        )
    else:
        # Update existing Patient record
        if hasattr(instance, 'patient_record'):
            patient = instance.patient_record
            patient.full_name = instance.user.get_full_name()
            patient.date_of_birth = instance.date_of_birth
            patient.gender = instance.gender
            patient.phone = instance.user.phone
            patient.save()


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.message}"
    
