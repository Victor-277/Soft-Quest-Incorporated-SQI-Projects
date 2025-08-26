from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, DoctorProfile, PatientProfile, Patient, UltrasoundReport, Appointment


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Custom admin for User model"""
    list_display = ('email', 'first_name', 'last_name', 'role', 'phone', 'is_active', 'date_joined')
    list_filter = ('role', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name', 'phone')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'phone', 'role', 'password1', 'password2'),
        }),
    )


@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    """Admin for DoctorProfile model"""
    list_display = ('user', 'specialization', 'license_number', 'years_experience')
    list_filter = ('specialization', 'years_experience')
    search_fields = ('user__first_name', 'user__last_name', 'user__email', 'specialization')
    ordering = ('user__first_name', 'user__last_name')


@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    """Admin for PatientProfile model"""
    list_display = ('user', 'date_of_birth', 'gender', 'blood_group', 'emergency_contact')
    list_filter = ('gender', 'blood_group')
    search_fields = ('user__first_name', 'user__last_name', 'user__email', 'emergency_contact')
    ordering = ('user__first_name', 'user__last_name')


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    """Admin for Patient model"""
    list_display = ('full_name', 'date_of_birth', 'gender', 'phone', 'age', 'created_at')
    list_filter = ('gender', 'created_at')
    search_fields = ('full_name', 'phone', 'notes')
    ordering = ('-created_at',)
    readonly_fields = ('age', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('full_name', 'date_of_birth', 'gender', 'phone')
        }),
        ('Additional Information', {
            'fields': ('notes', 'user_profile')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(UltrasoundReport)
class UltrasoundReportAdmin(admin.ModelAdmin):
    """Admin for UltrasoundReport model"""
    list_display = ('report_id', 'patient', 'doctor', 'scan_date', 'pregnancy_type', 'average_fetal_age')
    list_filter = ('scan_date', 'pregnancy_type', 'fetal_status', 'created_at')
    search_fields = ('patient__full_name', 'doctor__first_name', 'doctor__last_name', 'report_id')
    ordering = ('-scan_date', '-created_at')
    readonly_fields = ('report_id', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Report Information', {
            'fields': ('report_id', 'patient', 'doctor', 'scan_date', 'indication', 'hospital')
        }),
        ('Pregnancy Details', {
            'fields': ('pregnancy_type', 'scan_type', 'fetal_position', 'fetal_status')
        }),
        ('Fetal Measurements', {
            'fields': ('bdp', 'crl', 'fl', 'hc', 'ac', 'suspected_sex', 'average_fetal_age')
        }),
        ('Placenta', {
            'fields': ('placenta_position', 'placenta_maturity')
        }),
        ('Cervix & Liquor', {
            'fields': ('distance_from_cervix', 'pravaria', 'cervical_os', 'cervical_os_measurement', 'intact_cervix_length')
        }),
        ('Liquor & EFW', {
            'fields': ('liquor_volume', 'afi', 'efw')
        }),
        ('Dates & Anomalies', {
            'fields': ('uss_lmp', 'edd', 'fetal_anomalies')
        }),
        ('Additional Information', {
            'fields': ('remarks', 'signature')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    """Admin for Appointment model"""
    list_display = ('patient', 'doctor', 'appointment_date', 'appointment_time', 'status', 'created_at')
    list_filter = ('appointment_date', 'status', 'created_at')
    search_fields = ('patient__full_name', 'doctor__first_name', 'doctor__last_name', 'reason')
    ordering = ('-appointment_date', '-appointment_time')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Appointment Details', {
            'fields': ('patient', 'doctor', 'appointment_date', 'appointment_time', 'status')
        }),
        ('Additional Information', {
            'fields': ('reason', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


# Customize admin site
admin.site.site_header = "God's Grace Ultrasound Admin"
admin.site.site_title = "God's Grace Ultrasound"
admin.site.index_title = "Welcome to God's Grace Ultrasound Administration"

