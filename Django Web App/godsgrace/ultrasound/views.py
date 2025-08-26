from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.utils import timezone
from django import forms
from datetime import date, timedelta
import json
from django.views.decorators.http import require_POST

from .models import User, Patient, UltrasoundReport, Appointment, DoctorProfile, PatientProfile,Notification
from .forms import (
    UserRegistrationForm, UserLoginForm, PatientForm, UltrasoundReportForm,
    AppointmentForm, DoctorProfileForm, PatientProfileForm, UserProfileForm, SearchForm,StaffEditForm
)


def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

def is_doctor(user):
    return user.is_authenticated and user.role == 'doctor'

def is_patient(user):
    return user.is_authenticated and user.role == 'patient'

def is_staff_member(user):
    return user.is_authenticated and user.role in ['admin', 'doctor']

def is_receptionist(user):
    return user.role == 'receptionist'


# Authentication Views
def home(request):
    """Home page view"""
    
    if request.user.is_authenticated:
        return redirect('ultrasound:dashboard')
    
    # Get some statistics for the home page
    total_patients = Patient.objects.count()
    total_reports = UltrasoundReport.objects.count()
    today_reports = UltrasoundReport.objects.filter(scan_date=date.today()).count()
    upcoming_appointments = Appointment.objects.filter(
        appointment_date__gte=date.today(),
        status='scheduled'
    ).count()
    
    # Only get unread notifications if the user is authenticated
    unread_notifications_count = 0
    if request.user.is_authenticated:
        unread_notifications_count = request.user.notifications.filter(is_read=False).count()
    
    context = {
        'total_patients': total_patients,
        'total_reports': total_reports,
        'today_reports': today_reports,
        'upcoming_appointments': upcoming_appointments,
        'unread_notifications_count': unread_notifications_count,
    }
    
    return render(request, "ultrasound/index.html", context)



def user_login(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('ultrasound:dashboard')
    
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.get_full_name()}!')
                return redirect('ultrasound:dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    
    return render(request, 'ultrasound/login.html', {'form': form})
    
@login_required
@user_passes_test(is_admin)
def register_staff(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Staff {user.get_full_name()} registered successfully!')
            return redirect('ultrasound:view_staff')
    else:
        form = UserRegistrationForm()
    return render(request, 'ultrasound/register_staff.html', {'form': form})

def user_register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('ultrasound:dashboard')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['username']  
            user.save()
            
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('ultrasound:login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'ultrasound/register.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.role == 'doctor')
def update_appointment_status(request, pk):
    appointment = get_object_or_404(Appointment, id=pk)
    
    if request.method == "POST":
        new_status = request.POST.get("status")
        if new_status in dict(Appointment.STATUS_CHOICES).keys():
            appointment.status = new_status
            appointment.save()
            messages.success(request, f"Appointment status updated to {appointment.get_status_display()}.")
        return redirect('ultrasound:doctor_dashboard')
    
    return render(request, 'ultrasound/update_appointment_status.html', {'appointment': appointment})

def user_logout(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('ultrasound:home')

# Dashboard Views
@login_required
def dashboard(request):
    """Main dashboard - redirects based on user role"""
    if request.user.role == 'admin':
        return redirect('ultrasound:admin_dashboard')
    elif request.user.role == 'doctor':
        return redirect('ultrasound:doctor_dashboard')
    elif request.user.role == 'receptionist':
        return redirect('ultrasound:receptionist_dashboard')
    else:
        return redirect('ultrasound:patient_dashboard')

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Admin dashboard view"""
    # Get statistics
    total_patients = Patient.objects.count()
    total_reports = UltrasoundReport.objects.count()
    today_reports = UltrasoundReport.objects.filter(scan_date=date.today()).count()
    pending_reports = UltrasoundReport.objects.filter(created_at__date=date.today()).count()
    total_appointments = Appointment.objects.count()
    today_appointments = Appointment.objects.filter(appointment_date=date.today()).count()
    total_doctors = User.objects.filter(role='Doctor').count() 
    total_receptionists = User.objects.filter(role='Receptionist').count() 
    total_staff = User.objects.all().count()

    
    # Recent activities
    recent_reports = UltrasoundReport.objects.select_related('patient', 'doctor').order_by('-created_at')[:5]
    recent_appointments = Appointment.objects.select_related('patient', 'doctor').order_by('-created_at')[:5]
    
    context = {
        'total_patients': total_patients,
        'total_reports': total_reports,
        'today_reports': today_reports,
        'pending_reports': pending_reports,
        'total_appointments': total_appointments,
        'today_appointments': today_appointments,
        'recent_reports': recent_reports,
        'recent_appointments': recent_appointments,
        'total_doctors': total_doctors,
        'total_receptionists': total_receptionists,
        'total_staff':total_staff,
    }
    return render(request, 'ultrasound/admin_dashboard.html', context)


@login_required
@user_passes_test(is_doctor)
def doctor_dashboard(request):
    """Doctor dashboard view"""
    # Get doctor-specific statistics
    today_reports = UltrasoundReport.objects.filter(
        doctor=request.user,
        scan_date=date.today()
    ).count()
    
    total_reports = UltrasoundReport.objects.filter(doctor=request.user).count()
    today_appointments = Appointment.objects.filter(
        doctor=request.user,
        appointment_date=date.today()
    ).count()
    
    # Recent reports by this doctor
    recent_reports = UltrasoundReport.objects.filter(
        doctor=request.user
    ).select_related('patient').order_by('-created_at')[:5]
    
    # Today's appointments
    today_appointments_list = Appointment.objects.filter(
        doctor=request.user,
        appointment_date=date.today()
    ).select_related('patient').order_by('appointment_time')
    
    context = {
        'today_reports': today_reports,
        'total_reports': total_reports,
        'today_appointments': today_appointments,
        'recent_reports': recent_reports,
        'today_appointments_list': today_appointments_list,
    }
    return render(request, 'ultrasound/doctor_dashboard.html', context)


@login_required
@user_passes_test(is_patient)
def patient_dashboard(request):
    """Patient dashboard view"""
    try:
        patient_profile = request.user.patient_profile
        patient_record = patient_profile.patient_record
    except:
        patient_record = None
    
    if patient_record:
        # Get patient-specific data
        upcoming_appointments = Appointment.objects.filter(
            patient=patient_record,
            appointment_date__gte=date.today(),
            status__in=['scheduled', 'confirmed']
        ).order_by('appointment_date', 'appointment_time')[:3]
        
        recent_reports = UltrasoundReport.objects.filter(
            patient=patient_record
        ).order_by('-scan_date')[:3]
        
        next_appointment = upcoming_appointments.first() if upcoming_appointments.exists() else None
        last_report = recent_reports.first() if recent_reports.exists() else None
        
        context = {
            'patient_record': patient_record,
            'upcoming_appointments': upcoming_appointments,
            'recent_reports': recent_reports,
            'next_appointment': next_appointment,
            'last_report': last_report,
        }
    else:
        context = {'patient_record': None}
    
    return render(request, 'ultrasound/patient_dashboard.html', context)


@login_required
@user_passes_test(is_receptionist)
def receptionist_dashboard(request):
    """Receptionist dashboard: register, search, and book appointments"""

    #Patient Registration
    if request.method == 'POST' and 'register_patient' in request.POST:
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Patient registered successfully!')
            return redirect('ultrasound:receptionist_dashboard')

    #GET Request/search
    query = request.GET.get('q', '')
    if query:
        patients = Patient.objects.filter(full_name__icontains=query).order_by('-created_at')
    else:
        patients = Patient.objects.all().order_by('-created_at')

    doctors = DoctorProfile.objects.all()
    patient_form = PatientForm()
    reports = UltrasoundReport.objects.filter(status='ready').order_by('-scan_date')

    notifications = request.user.notifications.all().order_by('-created_at')
    unread_notifications_count = notifications.filter(is_read=False).count()

    context = {
        'patients': patients,
        'doctors': doctors,
        'form': patient_form,
        'query': query,
        'reports': reports,
        'notifications': notifications,
        'unread_notifications_count': unread_notifications_count,
    }
    return render(request, 'ultrasound/receptionist_dashboard.html', context)

@login_required
@user_passes_test(is_receptionist)
def book_appointment(request):
    """Receptionist books appointment for a patient"""
    patient_id = request.GET.get('patient_id')
    patient_record = get_object_or_404(Patient, id=patient_id)
    doctors = DoctorProfile.objects.all()

    if request.method == 'POST':
        doctor_id = request.POST.get('doctor_id')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        reason = request.POST.get('reason')

        doctor_profile = get_object_or_404(DoctorProfile, id=doctor_id)

        Appointment.objects.create(
            patient=patient_record,
            doctor=doctor_profile.user,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            reason=reason
        )

        Notification.objects.create(
            user=doctor_profile.user,
            message=f"New appointment booked for {patient_record.full_name} on {appointment_date} at {appointment_time}"
        )

        messages.success(
            request,
            f"Appointment booked for {patient_record.full_name} with {doctor_profile.user.get_full_name()}!"
        )
        return redirect('ultrasound:receptionist_dashboard')

    context = {
        'patient_record': patient_record,
        'doctors': doctors
    }
    return render(request, 'ultrasound/book_appointment.html', context)


# Patient Management Views
@login_required
@user_passes_test(is_staff_member)
def add_patient(request):
    """Add new patient view"""
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save()
            messages.success(request, f'Patient {patient.full_name} added successfully!')
            return redirect('ultrasound:view_patients')
    else:
        form = PatientForm()
    
    return render(request, 'ultrasound/add_patient.html', {'form': form})


@login_required
@user_passes_test(is_staff_member)
def view_patients(request):
    """View all patients with search and pagination"""
    search_form = SearchForm(request.GET)
    patients = Patient.objects.all().order_by('-created_at')
    
    if search_form.is_valid() and search_form.cleaned_data.get('search_query'):
        query = search_form.cleaned_data['search_query']
        patients = patients.filter(
            Q(full_name__icontains=query) |
            Q(phone__icontains=query) |
            Q(notes__icontains=query)
        )
    
    # Pagination
    paginator = Paginator(patients, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_form': search_form,
        'total_patients': patients.count(),
    }
    return render(request, 'ultrasound/view_patients.html', context)


@login_required
@user_passes_test(is_staff_member)
def edit_patient(request, patient_id):
    """Edit patient view"""
    patient = get_object_or_404(Patient, id=patient_id)
    
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, f'Patient {patient.full_name} updated successfully!')
            return redirect('ultrasound:view_patients')
    else:
        form = PatientForm(instance=patient)
    
    context = {
        'form': form,
        'patient': patient,
    }
    return render(request, 'ultrasound/edit_patient.html', context)


@login_required
@user_passes_test(is_staff_member)
def delete_patient(request, patient_id):
    """Delete patient view"""
    patient = get_object_or_404(Patient, id=patient_id)
    
    if request.method == 'POST':
        patient_name = patient.full_name
        patient.delete()
        messages.success(request, f'Patient {patient_name} deleted successfully!')
        return redirect('ultrasound:view_patients')
    
    context = {'patient': patient}
    return render(request, 'ultrasound/delete_patient.html', context)

@login_required
@user_passes_test(is_staff_member)
def add_report(request):
    """Add a new ultrasound report with previous reports shown (if patient exists)."""

    patient_id = request.GET.get("patient_id")
    patient = None
    previous_reports = None

    if patient_id:
        patient = get_object_or_404(Patient, id=patient_id)
        previous_reports = UltrasoundReport.objects.filter(
            patient=patient
        ).order_by("-scan_date")[:5]

    if request.method == "POST":
        form = UltrasoundReportForm(request.POST)
        if patient:
            form.instance.patient = patient

        if form.is_valid():
            report = form.save(commit=False)
            report.patient = patient
            report.doctor = request.user
            report.signature = (
                f"Signed electronically by {request.user.get_full_name()} "
                f"on {timezone.now().strftime('%d %b %Y, %I:%M %p')}"
            )
            report.save()

            # Update appointment status
            Appointment.objects.filter(
                patient=patient,
                appointment_date=report.scan_date,
                status="scheduled"
            ).update(status="completed")

            # Notify receptionists
            recipients = User.objects.filter(role='receptionist')
            for user in recipients:
                Notification.objects.create(
                    user=user,
                    message=f"New report uploaded for {patient.full_name} by Dr. {request.user.get_full_name()}"
                )

            messages.success(
                request,
                f"Report for {report.patient.full_name} created successfully!"
            )
            return redirect("ultrasound:view_reports")
    else:
        form = UltrasoundReportForm()

    context = {
        "form": form,
        "patient_previous_reports": previous_reports,
        "patient": patient,
    }
    return render(request, "ultrasound/add_report.html", context)


def mark_notification_read(request, pk):
    notif = Notification.objects.get(pk=pk, user=request.user)
    notif.is_read = True
    notif.save()
    return redirect("ultrasound:dashboard")


@login_required
@user_passes_test(is_staff_member)
def view_reports(request):
    """View all ultrasound reports with search and pagination"""
    search_form = SearchForm(request.GET)
    reports = UltrasoundReport.objects.select_related('patient', 'doctor').order_by('-created_at')
    
    if search_form.is_valid() and search_form.cleaned_data.get('search_query'):
        query = search_form.cleaned_data['search_query']
        reports = reports.filter(
            Q(patient__full_name__icontains=query) |
            Q(report_id__icontains=query) |
            Q(doctor__first_name__icontains=query) |
            Q(doctor__last_name__icontains=query)
        )
    
    # Pagination
    paginator = Paginator(reports, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_form': search_form,
        'total_reports': reports.count(),
    }
    return render(request, 'ultrasound/view_reports.html', context)


def can_view_report(user):
    return user.role in ['receptionist', 'doctor']
@login_required
@user_passes_test(can_view_report)
def view_report_detail(request, report_id):
    """View detailed ultrasound report"""
    report = get_object_or_404(UltrasoundReport, report_id=report_id)
    
    context = {
        'report': report,
    }
    return render(request, 'ultrasound/view_report_detail.html', context)


@login_required 
@user_passes_test(is_staff_member)
def edit_report(request, report_id):
    report = get_object_or_404(UltrasoundReport, report_id=report_id)

    if request.method == 'POST':
        report.scan_date = request.POST.get('scan_date')
        report.scan_type = request.POST.get('scan_type')
        report.fetal_position = request.POST.get('fetal_position')
        report.fetal_status = request.POST.get('fetal_status')
        report.bdp = request.POST.get('bdp')
        report.crl = request.POST.get('crl')
        report.fl = request.POST.get('fl')
        report.hc = request.POST.get('hc')
        report.ac = request.POST.get('ac')
        report.suspected_sex = request.POST.get('suspected_sex')
        report.average_fetal_age = request.POST.get('average_fetal_age')
        report.placenta_position = request.POST.get('placenta_position')
        report.placenta_maturity = request.POST.get('placenta_maturity')
        report.remarks = request.POST.get('remarks')
        report.save()

        messages.success(request, f'Report for {report.patient.full_name} updated successfully!')
        return redirect('ultrasound:view_reports')

    context = {'report': report}
    return render(request, 'ultrasound/edit_report.html', context)


@login_required
@user_passes_test(is_staff_member)
def delete_report(request, report_id):
    """Delete ultrasound report view"""
    report = get_object_or_404(UltrasoundReport, report_id=report_id)
    
    if request.method == 'POST':
        patient_name = report.patient.full_name
        report.delete()
        messages.success(request, f'Report for {patient_name} deleted successfully!')
        return redirect('ultrasound:view_reports')
    
    context = {'report': report}
    return render(request, 'ultrasound/delete_report.html', context)


@login_required
def print_report(request, report_id):
    """Print-friendly ultrasound report view"""
    report = get_object_or_404(UltrasoundReport, report_id=report_id)
    
    context = {
        'report': report,
    }
    return render(request, 'ultrasound/print_report.html', context)


# Patient-specific views
@login_required
@user_passes_test(is_patient)
def my_reports(request):
    """Patient's own reports view"""
    try:
        patient_profile = request.user.patient_profile
        patient_record = patient_profile.patient_record
        reports = UltrasoundReport.objects.filter(patient=patient_record).order_by('-scan_date')
    except:
        reports = []
        patient_record = None
    
    context = {
        'reports': reports,
        'patient_record': patient_record,
    }
    return render(request, 'ultrasound/my_reports.html', context)


@login_required
@user_passes_test(is_patient)
def my_appointments(request):
    """Patient's own appointments view"""
    try:
        patient_profile = request.user.patient_profile
        patient_record = patient_profile.patient_record
        appointments = Appointment.objects.filter(patient=patient_record).order_by('-appointment_date')
    except:
        appointments = []
        patient_record = None
    
    context = {
        'appointments': appointments,
        'patient_record': patient_record,
    }
    return render(request, 'ultrasound/my_appointments.html', context)


# Profile Views
@login_required
def profile(request):
    """User profile view"""
    user = request.user
    
    if user.role == 'doctor':
        try:
            profile = user.doctor_profile
            profile_form = DoctorProfileForm(instance=profile)
        except:
            profile = None
            profile_form = DoctorProfileForm()
    elif user.role == 'patient':
        try:
            profile = user.patient_profile
            profile_form = PatientProfileForm(instance=profile)
        except:
            profile = None
            profile_form = PatientProfileForm()
    else:
        profile = None
        profile_form = None
    
    user_form = UserProfileForm(instance=user)
    
    if request.method == 'POST':
        if 'update_user' in request.POST:
            user_form = UserProfileForm(request.POST, instance=user)
            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('ultrasound:profile')
        elif 'update_profile' in request.POST and profile_form:
            profile_form = profile_form.__class__(request.POST, instance=profile)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('ultrasound:profile')
    
    context = {
        'user': user,
        'profile': profile,
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'ultrasound/profile.html', context)


# API Views for AJAX requests
@login_required
def get_patient_data(request):
    """Get patient data for AJAX requests"""
    if request.method == 'GET' and request.is_ajax():
        patient_id = request.GET.get('patient_id')
        try:
            patient = Patient.objects.get(id=patient_id)
            data = {
                'id': patient.id,
                'full_name': patient.full_name,
                'date_of_birth': patient.date_of_birth.strftime('%Y-%m-%d'),
                'gender': patient.gender,
                'phone': patient.phone,
                'age': patient.age,
            }
            return JsonResponse({'success': True, 'data': data})
        except Patient.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Patient not found'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})


@login_required
def get_dashboard_stats(request):
    """Get dashboard statistics for AJAX requests"""
    if request.method == 'GET' and request.is_ajax():
        try:
            if request.user.role == 'admin':
                stats = {
                    'total_patients': Patient.objects.count(),
                    'total_reports': UltrasoundReport.objects.count(),
                    'today_reports': UltrasoundReport.objects.filter(scan_date=date.today()).count(),
                    'pending_reports': UltrasoundReport.objects.filter(created_at__date=date.today()).count(),
                }
            elif request.user.role == 'doctor':
                stats = {
                    'today_reports': UltrasoundReport.objects.filter(
                        doctor=request.user,
                        scan_date=date.today()
                    ).count(),
                    'total_reports': UltrasoundReport.objects.filter(doctor=request.user).count(),
                    'today_appointments': Appointment.objects.filter(
                        doctor=request.user,
                        appointment_date=date.today()
                    ).count(),
                }
            else:
                stats = {}
            
            return JsonResponse({'success': True, 'data': stats})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})


@login_required
@user_passes_test(is_receptionist)
@require_POST
def mark_report_printed(request, report_id):
    report = get_object_or_404(UltrasoundReport, report_id=report_id)
    report.status = 'printed'
    report.save()
    messages.success(request, f'Report {report.report_id} marked as printed.')
    return redirect('ultrasound:receptionist_dashboard')

# Staff Management Views
@login_required
@user_passes_test(is_admin)
def view_staff(request):
    """View all staff members (doctors, receptionists, etc.)"""
    staff_members = User.objects.exclude(role='patient').order_by('role', 'first_name')

    # Optional search
    query = request.GET.get('q', '')
    if query:
        staff_members = staff_members.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(username__icontains=query) |
            Q(role__icontains=query)
        )

    # Pagination
    paginator = Paginator(staff_members, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'total_staff': staff_members.count(),
        'query': query,
    }
    return render(request, 'ultrasound/view_staff.html', context)


@login_required
@user_passes_test(is_admin)
def edit_staff(request, user_id):
    """Edit a staff member's details"""
    staff = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = StaffEditForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            messages.success(request, f'Staff member {staff.get_full_name()} updated successfully!')
            return redirect('ultrasound:view_staff')
    else:
        form = StaffEditForm(instance=staff)

    context = {
        'form': form,
        'staff': staff,
    }
    return render(request, 'ultrasound/edit_staff.html', context)


@login_required
@user_passes_test(is_admin)
def delete_staff(request, user_id):
    """Delete a staff member"""
    staff = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        staff_name = staff.get_full_name()
        staff.delete()
        messages.success(request, f'Staff member {staff_name} deleted successfully!')
        return redirect('ultrasound:view_staff')

    context = {'staff': staff}
    return render(request, 'ultrasound/delete_staff.html', context)




