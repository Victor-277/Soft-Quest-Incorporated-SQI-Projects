from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import User, Patient, UltrasoundReport, Appointment, DoctorProfile, PatientProfile


class UserRegistrationForm(UserCreationForm):
    """Form for user registration"""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone = forms.CharField(max_length=15, required=True)
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone', 'role', 'password1', 'password2')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email is already registered.')
        return email


class UserLoginForm(AuthenticationForm):
    """Form for user login"""
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter username"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    
    class Meta:
        model = User
        fields = ('username', 'password')


class PatientForm(forms.ModelForm):
    """Form for adding/editing patients"""
    class Meta:
        model = Patient
        fields = ['full_name', 'date_of_birth', 'gender', 'phone', 'notes']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Additional information'}),
        }

class UltrasoundReportForm(forms.ModelForm):
    """Form for ultrasound reports"""
    patient = forms.ModelChoiceField(queryset=Patient.objects.all(), required=True)

    class Meta:
        model = UltrasoundReport
        fields = [
            'patient', 'scan_date', 'indication', 'hospital',
            'pregnancy_type', 'scan_type', 'fetal_position', 'fetal_status',
            'bdp', 'crl', 'fl', 'hc', 'ac', 'suspected_sex', 'average_fetal_age',
            'placenta_position', 'placenta_maturity',
            'distance_from_cervix', 'pravaria', 'cervical_os', 'cervical_os_measurement', 'intact_cervix_length',
            'liquor_volume', 'afi', 'efw',
            'uss_lmp', 'edd', 'fetal_anomalies',
            'remarks', 'signature'
        ]
        widgets = {
            'patient': forms.HiddenInput(),
            'hospital': forms.HiddenInput(),
            'indication': forms.HiddenInput(),
            'scan_date': forms.DateInput(attrs={'type': 'date'}),
            'remarks': forms.Textarea(attrs={'rows': 4}),
            'bdp': forms.TextInput(attrs={'placeholder': 'mm / weeks'}),
            'crl': forms.TextInput(attrs={'placeholder': 'mm / weeks'}),
            'fl': forms.TextInput(attrs={'placeholder': 'mm / weeks'}),
            'hc': forms.TextInput(attrs={'placeholder': 'mm / weeks'}),
            'ac': forms.TextInput(attrs={'placeholder': 'mm / weeks'}),
            'distance_from_cervix': forms.TextInput(attrs={'placeholder': 'mm'}),
            'intact_cervix_length': forms.TextInput(attrs={'placeholder': 'cm'}),
            'afi': forms.TextInput(attrs={'placeholder': 'mm'}),
            'efw': forms.TextInput(attrs={'placeholder': '+/-0.1KG'}),
        }

    def __init__(self, *args, **kwargs):
        patient_instance = kwargs.pop('patient', None)
        super().__init__(*args, **kwargs)

        # Default values
        self.fields['indication'].initial = "F W B & G A"
        self.fields['hospital'].initial = "God's Grace Ultrasound"
        self.fields['signature'].initial = "God's Grace"

        if patient_instance:
            self.fields['patient'].initial = patient_instance
            self.fields['patient'].disabled = True  
class AppointmentForm(forms.ModelForm):
    """Form for appointments"""
    class Meta:
        model = Appointment
        fields = ['patient', 'appointment_date', 'appointment_time', 'reason', 'notes']
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date'}),
            'appointment_time': forms.TimeInput(attrs={'type': 'time'}),
            'reason': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Additional notes'}),
        }


class DoctorProfileForm(forms.ModelForm):
    """Form for doctor profile"""
    class Meta:
        model = DoctorProfile
        fields = ['specialization', 'license_number', 'years_experience', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }


class PatientProfileForm(forms.ModelForm):
    """Form for patient profile"""
    class Meta:
        model = PatientProfile
        fields = ['date_of_birth', 'gender', 'address', 'emergency_contact', 'medical_history', 'allergies', 'blood_group']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
            'medical_history': forms.Textarea(attrs={'rows': 3}),
            'allergies': forms.Textarea(attrs={'rows': 2}),
        }


class UserProfileForm(forms.ModelForm):
    """Form for user profile updates"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise ValidationError('This email is already registered.')
        return email


class SearchForm(forms.Form):
    """Form for searching patients and reports"""
    search_query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search by name, phone, or report ID...',
            'class': 'form-control'
        })
    )
    search_type = forms.ChoiceField(
        choices=[
            ('all', 'All'),
            ('patients', 'Patients'),
            ('reports', 'Reports'),
        ],
        initial='all',
        widget=forms.Select(attrs={'class': 'form-select'})
    )


class StaffEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'role']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
        }