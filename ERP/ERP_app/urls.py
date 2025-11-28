from django.urls import path
from . import views

urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    
    # Generic page views
    path('account-office-portal/', views.page_view, {'page_name': 'account-office-portal'}, name='account-office-portal'),
    path('admin-dashboard/', views.page_view, {'page_name': 'admin-dashboard'}, name='admin-dashboard'),
    path('admin-student-registration/', views.page_view, {'page_name': 'admin-student-registration'}, name='admin-student-registration'),
    path('alumni-relations/', views.page_view, {'page_name': 'alumni-relations'}, name='alumni-relations'),
    path('anti-ragging/', views.page_view, {'page_name': 'anti-ragging'}, name='anti-ragging'),
    path('assignment/', views.page_view, {'page_name': 'assignment'}, name='assignment'),
    path('attendance/', views.page_view, {'page_name': 'attendance'}, name='attendance'),
    path('calendar/', views.page_view, {'page_name': 'calendar'}, name='calendar'),
    path('chancellor-president-portal/', views.page_view, {'page_name': 'chancellor-president-portal'}, name='chancellor-president-portal'),
    path('class/', views.page_view, {'page_name': 'class'}, name='class'),
    path('college-info/', views.page_view, {'page_name': 'college-info'}, name='college-info'),
    path('crc-portal/', views.crc_dashboard, name='crc-portal'),
    path('cultural-committee/', views.page_view, {'page_name': 'cultural-committee'}, name='cultural-committee'),
    path('dashboard/', views.page_view, {'page_name': 'dashboard'}, name='dashboard'),
    path('dean-academics-portal/', views.page_view, {'page_name': 'dean-academics-portal'}, name='dean-academics-portal'),
    path('disciplinary-committee/', views.page_view, {'page_name': 'disciplinary-committee'}, name='disciplinary-committee'),
    path('environmental-sustainability/', views.page_view, {'page_name': 'environmental-sustainability'}, name='environmental-sustainability'),
    path('events/', views.page_view, {'page_name': 'events'}, name='events'),
    path('exam-form-main/', views.page_view, {'page_name': 'exam-form-main'}, name='exam-form-main'),
    path('exam-form-reappear/', views.page_view, {'page_name': 'exam-form-reappear'}, name='exam-form-reappear'),
    path('examination/', views.page_view, {'page_name': 'examination'}, name='examination'),
    path('external-datesheet/', views.page_view, {'page_name': 'external-datesheet'}, name='external-datesheet'),
    path('faculty-portal/', views.page_view, {'page_name': 'faculty-portal'}, name='faculty-portal'),
    path('fees/', views.page_view, {'page_name': 'fees'}, name='fees'),
    path('finance-portal/', views.page_view, {'page_name': 'finance-portal'}, name='finance-portal'),
    path('hostel/', views.page_view, {'page_name': 'hostel'}, name='hostel'),
    path('hr-department/', views.page_view, {'page_name': 'hr-department'}, name='hr-department'),
    path('innovation-startup/', views.page_view, {'page_name': 'innovation-startup'}, name='innovation-startup'),
    path('internal-datesheet/', views.page_view, {'page_name': 'internal-datesheet'}, name='internal-datesheet'),
    path('international-relations/', views.page_view, {'page_name': 'international-relations'}, name='international-relations'),
    path('iqac/', views.page_view, {'page_name': 'iqac'}, name='iqac'),
    path('it-department/', views.page_view, {'page_name': 'it-department'}, name='it-department'),
    path('legal-cell/', views.page_view, {'page_name': 'legal-cell'}, name='legal-cell'),
    path('library/', views.page_view, {'page_name': 'library'}, name='library'),
    path('maintenance-security/', views.page_view, {'page_name': 'maintenance-security'}, name='maintenance-security'),
    path('medical-center/', views.page_view, {'page_name': 'medical-center'}, name='medical-center'),
    path('nss-ncc/', views.page_view, {'page_name': 'nss-ncc'}, name='nss-ncc'),
    path('online-learning/', views.page_view, {'page_name': 'online-learning'}, name='online-learning'),
    path('placement/', views.student_placement_page, name='placement'),
    path('pr-office/', views.page_view, {'page_name': 'pr-office'}, name='pr-office'),
    path('registrar-office/', views.page_view, {'page_name': 'registrar-office'}, name='registrar-office'),
    path('registrar-portal/', views.page_view, {'page_name': 'registrar-portal'}, name='registrar-portal'),
    path('registration/', views.page_view, {'page_name': 'registration'}, name='registration'),
    path('research-innovation/', views.page_view, {'page_name': 'research-innovation'}, name='research-innovation'),
    path('result/', views.page_view, {'page_name': 'result'}, name='result'),
    path('scholarship-portal/', views.page_view, {'page_name': 'scholarship-portal'}, name='scholarship-portal'),
    path('sports-committee/', views.page_view, {'page_name': 'sports-committee'}, name='sports-committee'),
    path('student-welfare/', views.page_view, {'page_name': 'student-welfare'}, name='student-welfare'),
    path('syllabus/', views.page_view, {'page_name': 'syllabus'}, name='syllabus'),
    path('test-navigation/', views.page_view, {'page_name': 'test-navigation'}, name='test-navigation'),
    path('transport-fee/', views.page_view, {'page_name': 'transport-fee'}, name='transport-fee'),
    path('university-structure/', views.page_view, {'page_name': 'university-structure'}, name='university-structure'),
    path('vice-chancellor-portal/', views.page_view, {'page_name': 'vice-chancellor-portal'}, name='vice-chancellor-portal'),
    path('womens-cell/', views.page_view, {'page_name': 'womens-cell'}, name='womens-cell'),
    
    # Attendance Views
    path('admin-attendance-dashboard/', views.admin_attendance_dashboard, name='admin-attendance-dashboard'),
    path('dean-attendance-dashboard/', views.dean_attendance_dashboard, name='dean-attendance-dashboard'),
    path('hod-attendance-dashboard/', views.hod_attendance_dashboard, name='hod-attendance-dashboard'),
    
    # Admin Search
    path('admin-search/', views.admin_search, name='admin-search'),
    
    # CRC Placement Views
    path('crc/add-company/', views.crc_add_company, name='crc-add-company'),
    path('crc/edit-company/<int:company_id>/', views.crc_edit_company, name='crc-edit-company'),
    path('crc/applications/<int:company_id>/', views.crc_view_applications, name='crc-view-applications'),
    
    # Admin Placement Approval
    path('admin/placement-approval/', views.admin_placement_approval, name='admin-placement-approval'),
    path('admin/approve-placement/<int:company_id>/', views.admin_approve_placement, name='admin-approve-placement'),
    
    # Student Placement Views
    path('student/apply-placement/<int:placement_id>/', views.student_apply_placement, name='student-apply-placement'),
    
    # Student Application Center
    path('application-center/', views.application_center, name='application-center'),
    path('application-form/<str:app_type>/', views.application_form, name='application-form'),
    path('submit-application/', views.submit_application, name='submit-application'),
    path('view-application/<int:app_id>/', views.view_application, name='view-application'),
    path('application-status/', views.application_status, name='application-status'),
    
    # University Structure API
    path('api/university-structure/', views.get_university_structure, name='university-structure-api'),
]
