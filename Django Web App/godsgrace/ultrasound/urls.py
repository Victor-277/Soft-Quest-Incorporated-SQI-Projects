from django.urls import path
from . import views

app_name = 'ultrasound'

urlpatterns = [
    # Authentication URLs
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('staff/register/', views.register_staff, name='register_staff'),

    
    # Dashboard URLs
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('doctor-dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('patient-dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('receptionist-dashboard/', views.receptionist_dashboard, name='receptionist_dashboard'),
    
    # Patient Management URLs
    path('add-patient/', views.add_patient, name='add_patient'),
    path('view-patients/', views.view_patients, name='view_patients'),
    path('edit-patient/<int:patient_id>/', views.edit_patient, name='edit_patient'),
    path('delete-patient/<int:patient_id>/', views.delete_patient, name='delete_patient'),
    
    # Staff Management URLs
    path('view-staff/', views.view_staff, name='view_staff'),
    path('edit-staff/<int:user_id>/', views.edit_staff, name='edit_staff'),
    path('delete-staff/<int:user_id>/', views.delete_staff, name='delete_staff'),


    # Ultrasound Report URLs
    path('add-report/', views.add_report, name='add_report'),
    path('view-reports/', views.view_reports, name='view_reports'),
    path('report/<uuid:report_id>/', views.view_report_detail, name='view_report_detail'),
    path('edit-report/<uuid:report_id>/', views.edit_report, name='edit_report'),
    path('delete-report/<uuid:report_id>/', views.delete_report, name='delete_report'),
    path('print-report/<uuid:report_id>/', views.print_report, name='print_report'),
    path('report/<uuid:report_id>/printed/', views.mark_report_printed, name='mark_report_printed'),
    path("notification/<int:pk>/read/", views.mark_notification_read, name="mark_notification_read"),

    
    # Patient-specific URLs
    path('my-reports/', views.my_reports, name='my_reports'),
    path('my-appointments/', views.my_appointments, name='my_appointments'),
    path('book-appointment/', views.book_appointment, name='book_appointment'),
    
    # Profile URLs
    path('profile/', views.profile, name='profile'),
    
    # API URLs for AJAX
    path('api/patient-data/', views.get_patient_data, name='get_patient_data'),
    path('api/dashboard-stats/', views.get_dashboard_stats, name='get_dashboard_stats'),
]

