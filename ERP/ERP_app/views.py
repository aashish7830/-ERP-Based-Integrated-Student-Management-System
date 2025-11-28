from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, JsonResponse
from django.db.models import Q, Count, Avg, Sum
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from datetime import datetime, timedelta
from functools import partial
import json
from .models import (
    AttendanceRecord, PlacementUpdate, PlacementApplication, UserProfile, ApplicationRequest,
    GoverningBody, School, Department, Program, FacultyMember, AcademicSection, SupportCell
)

# List of all available templates
AVAILABLE_TEMPLATES = [
    'index',
    'account-office-portal',
    'admin-dashboard',
    'admin-student-registration',
    'alumni-relations',
    'anti-ragging',
    'assignment',
    'attendance',
    'calendar',
    'chancellor-president-portal',
    'class',
    'college-info',
    'crc-portal',
    'cultural-committee',
    'dashboard',
    'dean-academics-portal',
    'disciplinary-committee',
    'environmental-sustainability',
    'events',
    'exam-form-main',
    'exam-form-reappear',
    'examination',
    'external-datesheet',
    'faculty-portal',
    'fees',
    'finance-portal',
    'hostel',
    'hr-department',
    'innovation-startup',
    'internal-datesheet',
    'international-relations',
    'iqac',
    'legal-cell',
    'library',
    'maintenance-security',
    'medical-center',
    'nss-ncc',
    'online-learning',
    'placement',
    'pr-office',
    'registrar-office',
    'registrar-portal',
    'registration',
    'research-innovation',
    'result',
    'scholarship-portal',
    'sports-committee',
    'student-welfare',
    'syllabus',
    'test-navigation',
    'transport-fee',
    'university-structure',
    'vice-chancellor-portal',
    'womens-cell',
]


def page_view(request, page_name):
    """Generic view to render any template page"""
    template_name = f'{page_name}.html'
    
    if page_name not in AVAILABLE_TEMPLATES:
        raise Http404("Page not found")
    
    context = {
        'page_name': page_name,
        'current_page': page_name,
    }
    
    try:
        return render(request, template_name, context)
    except Exception as e:
        # If template doesn't exist, return 404
        raise Http404(f"Template not found: {template_name}")


def index(request):
    """Home page view"""
    return render(request, 'index.html', {'current_page': 'index'})


# ==================== UNIVERSITY STRUCTURE VIEWS ====================

def get_university_structure(request):
    """Get complete university structure from database"""
    structure = {
        'governing_bodies': list(GoverningBody.objects.filter(is_active=True).values()),
        'schools': [],
        'academic_sections': list(AcademicSection.objects.filter(is_active=True).values()),
        'support_cells': list(SupportCell.objects.filter(is_active=True).values()),
    }
    
    # Get schools with departments and programs
    schools = School.objects.filter(is_active=True).prefetch_related('departments__programs')
    for school in schools:
        school_data = {
            'id': school.id,
            'name': school.name,
            'short_name': school.short_name,
            'icon': school.icon,
            'color': school.color,
            'departments': []
        }
        
        for dept in school.departments.filter(is_active=True):
            dept_data = {
                'id': dept.id,
                'name': dept.name,
                'short_name': dept.short_name,
                'hod_id': dept.hod_id,
                'programs': list(dept.programs.filter(is_active=True).values('id', 'name', 'degree_type'))
            }
            school_data['departments'].append(dept_data)
        
        structure['schools'].append(school_data)
    
    return JsonResponse(structure)


# ==================== ATTENDANCE VIEWS ====================

def admin_attendance_dashboard(request):
    """Admin: Complete university attendance dashboard"""
    search_query = request.GET.get('search', '')
    
    # Base queryset (handle if table doesn't exist)
    try:
        attendance_records = AttendanceRecord.objects.all()
    except:
        attendance_records = AttendanceRecord.objects.none()
    
    # Search functionality
    if search_query:
        attendance_records = attendance_records.filter(
            Q(enrollment_no__icontains=search_query) |
            Q(student_name__icontains=search_query) |
            Q(department__icontains=search_query) |
            Q(contact_no__icontains=search_query) |
            Q(school__icontains=search_query)
        )
    
    # School-wise attendance
    school_wise = attendance_records.values('school').annotate(
        total_students=Count('student', distinct=True),
        total_present=Count('id', filter=Q(status='present')),
        total_absent=Count('id', filter=Q(status='absent')),
        attendance_percentage=Avg('id', filter=Q(status='present')) * 100 / Count('id')
    )
    
    # Department-wise attendance
    dept_wise = attendance_records.values('department').annotate(
        total_students=Count('student', distinct=True),
        total_present=Count('id', filter=Q(status='present')),
        total_absent=Count('id', filter=Q(status='absent')),
    )
    
    # Year-wise attendance
    year_wise = attendance_records.values('year').annotate(
        total_students=Count('student', distinct=True),
        total_present=Count('id', filter=Q(status='present')),
        total_absent=Count('id', filter=Q(status='absent')),
    )
    
    # Section-wise attendance
    section_wise = attendance_records.values('year', 'section').annotate(
        total_students=Count('student', distinct=True),
        total_present=Count('id', filter=Q(status='present')),
        total_absent=Count('id', filter=Q(status='absent')),
    )
    
    # Course-wise attendance
    course_wise = attendance_records.values('course').annotate(
        total_students=Count('student', distinct=True),
        total_present=Count('id', filter=Q(status='present')),
        total_absent=Count('id', filter=Q(status='absent')),
    )
    
    # Faculty-wise attendance
    faculty_wise = attendance_records.values('faculty__username', 'faculty__first_name', 'faculty__last_name').annotate(
        total_classes=Count('id'),
        total_present=Count('id', filter=Q(status='present')),
        total_absent=Count('id', filter=Q(status='absent')),
    )
    
    # Overall statistics
    total_records = attendance_records.count()
    total_present = attendance_records.filter(status='present').count()
    total_absent = attendance_records.filter(status='absent').count()
    overall_percentage = (total_present / total_records * 100) if total_records > 0 else 0
    
    context = {
        'school_wise': school_wise,
        'dept_wise': dept_wise,
        'year_wise': year_wise,
        'section_wise': section_wise,
        'course_wise': course_wise,
        'faculty_wise': faculty_wise,
        'total_records': total_records,
        'total_present': total_present,
        'total_absent': total_absent,
        'overall_percentage': overall_percentage,
        'search_query': search_query,
    }
    
    return render(request, 'admin-attendance-dashboard.html', context)


def dean_attendance_dashboard(request):
    """Dean: School-level attendance dashboard"""
    # For demo, use a default school
    school = request.GET.get('school', 'School of Engineering')
    
    attendance_records = AttendanceRecord.objects.filter(school=school)
    
    # All departments in school
    dept_wise = attendance_records.values('department').annotate(
        total_students=Count('student', distinct=True),
        total_present=Count('id', filter=Q(status='present')),
        total_absent=Count('id', filter=Q(status='absent')),
    )
    
    # All semesters
    semester_wise = attendance_records.values('year').annotate(
        total_students=Count('student', distinct=True),
        total_present=Count('id', filter=Q(status='present')),
        total_absent=Count('id', filter=Q(status='absent')),
    )
    
    # Shortage list (below 75%)
    all_students = attendance_records.values('student', 'enrollment_no', 'student_name', 'department').annotate(
        total_classes=Count('id'),
        present_count=Count('id', filter=Q(status='present')),
    )
    
    shortage_list = []
    for student in all_students:
        if student['total_classes'] > 0:
            percentage = (student['present_count'] / student['total_classes']) * 100
            if percentage < 75:
                shortage_list.append({
                    'enrollment_no': student['enrollment_no'],
                    'student_name': student['student_name'],
                    'department': student['department'],
                    'percentage': round(percentage, 2),
                    'present': student['present_count'],
                    'total': student['total_classes'],
                })
    
    context = {
        'school': school,
        'dept_wise': dept_wise,
        'semester_wise': semester_wise,
        'shortage_list': shortage_list,
    }
    
    return render(request, 'dean-attendance-dashboard.html', context)


def hod_attendance_dashboard(request):
    """HOD: Department-level attendance dashboard"""
    # For demo, use a default department
    department = request.GET.get('department', 'Computer Science Engineering')
    
    attendance_records = AttendanceRecord.objects.filter(department=department)
    
    # All batches
    batch_wise = attendance_records.values('year', 'section').annotate(
        total_students=Count('student', distinct=True),
        total_present=Count('id', filter=Q(status='present')),
        total_absent=Count('id', filter=Q(status='absent')),
    )
    
    # All subjects
    subject_wise = attendance_records.values('course').annotate(
        total_students=Count('student', distinct=True),
        total_present=Count('id', filter=Q(status='present')),
        total_absent=Count('id', filter=Q(status='absent')),
    )
    
    # Shortage students
    all_students = attendance_records.values('student', 'enrollment_no', 'student_name', 'year', 'section').annotate(
        total_classes=Count('id'),
        present_count=Count('id', filter=Q(status='present')),
    )
    
    shortage_students = []
    for student in all_students:
        if student['total_classes'] > 0:
            percentage = (student['present_count'] / student['total_classes']) * 100
            if percentage < 75:
                shortage_students.append({
                    'enrollment_no': student['enrollment_no'],
                    'student_name': student['student_name'],
                    'year': student['year'],
                    'section': student['section'],
                    'percentage': round(percentage, 2),
                    'present': student['present_count'],
                    'total': student['total_classes'],
                })
    
    # Daily summary
    today = timezone.now().date()
    daily_summary = attendance_records.filter(date=today).aggregate(
        total=Count('id'),
        present=Count('id', filter=Q(status='present')),
        absent=Count('id', filter=Q(status='absent')),
    )
    
    # Weekly summary
    week_start = today - timedelta(days=today.weekday())
    weekly_summary = attendance_records.filter(date__gte=week_start).aggregate(
        total=Count('id'),
        present=Count('id', filter=Q(status='present')),
        absent=Count('id', filter=Q(status='absent')),
    )
    
    # Monthly summary
    month_start = today.replace(day=1)
    monthly_summary = attendance_records.filter(date__gte=month_start).aggregate(
        total=Count('id'),
        present=Count('id', filter=Q(status='present')),
        absent=Count('id', filter=Q(status='absent')),
    )
    
    context = {
        'department': department,
        'batch_wise': batch_wise,
        'subject_wise': subject_wise,
        'shortage_students': shortage_students,
        'daily_summary': daily_summary,
        'weekly_summary': weekly_summary,
        'monthly_summary': monthly_summary,
    }
    
    return render(request, 'hod-attendance-dashboard.html', context)


# ==================== ADMIN SEARCH ====================

def admin_search(request):
    """Admin search functionality"""
    query = request.GET.get('q', '')
    results = {
        'students': [],
        'departments': [],
        'hods': [],
        'colleges': [],
    }
    
    if query:
        # Search students
        students = UserProfile.objects.filter(
            Q(enrollment_no__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(contact_no__icontains=query)
        ).filter(role='student')[:10]
        
        results['students'] = [{
            'enrollment_no': s.enrollment_no,
            'name': f"{s.user.first_name} {s.user.last_name}",
            'contact': s.contact_no,
            'department': s.department,
        } for s in students]
        
        # Search departments
        departments = UserProfile.objects.filter(
            Q(department__icontains=query)
        ).values('department', 'school').distinct()[:10]
        
        results['departments'] = list(departments)
        
        # Search HODs
        hods = UserProfile.objects.filter(
            Q(role='hod') &
            (Q(user__first_name__icontains=query) |
             Q(user__last_name__icontains=query) |
             Q(department__icontains=query))
        )[:10]
        
        results['hods'] = [{
            'name': f"{h.user.first_name} {h.user.last_name}",
            'department': h.department,
            'contact': h.contact_no,
        } for h in hods]
        
        # Search colleges
        colleges = UserProfile.objects.filter(
            Q(college_name__icontains=query)
        ).values('college_name').distinct()[:10]
        
        results['colleges'] = list(colleges)
    
    return JsonResponse(results)


# ==================== CRC PLACEMENT VIEWS ====================

def crc_dashboard(request):
    """CRC Dashboard"""
    # Since app uses client-side auth, we'll show the page without user check
    # Client-side JavaScript will handle authentication
    
    # Get all companies (for demo, show all pending/approved)
    try:
        companies = PlacementUpdate.objects.all().order_by('-created_at')
        # Statistics
        total_companies = companies.count()
        pending = companies.filter(status='pending').count()
        approved = companies.filter(status='approved').count()
        rejected = companies.filter(status='rejected').count()
        # Get all applications (for demo)
        all_applications = PlacementApplication.objects.all().order_by('-applied_at')[:20]
    except Exception:
        # If database tables don't exist yet, use empty data
        companies = []
        total_companies = 0
        pending = 0
        approved = 0
        rejected = 0
        all_applications = []
    
    context = {
        'companies': companies,
        'total_companies': total_companies,
        'pending': pending,
        'approved': approved,
        'rejected': rejected,
        'applications': all_applications,
    }
    
    return render(request, 'crc-portal.html', context)


def crc_add_company(request):
    """CRC: Add new company"""
    if request.method == 'POST':
        # Get or create a default user for demo purposes
        from django.contrib.auth.models import User
        default_user, _ = User.objects.get_or_create(username='crc_user', defaults={'email': 'crc@university.edu'})
        
        company = PlacementUpdate.objects.create(
            company_name=request.POST.get('company_name'),
            role=request.POST.get('role'),
            package=request.POST.get('package'),
            eligibility_cgpa=request.POST.get('eligibility_cgpa') or None,
            branches_allowed=request.POST.get('branches_allowed'),
            last_date=request.POST.get('last_date'),
            drive_date=request.POST.get('drive_date'),
            job_location=request.POST.get('job_location'),
            mode=request.POST.get('mode'),
            description=request.POST.get('description'),
            created_by=default_user,
            status='pending',
        )
        
        if 'job_description_file' in request.FILES:
            company.job_description_file = request.FILES['job_description_file']
            company.save()
        
        return JsonResponse({'success': True, 'message': 'Company added successfully! Waiting for admin approval.'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})


def crc_edit_company(request, company_id):
    """CRC: Edit company details"""
    company = get_object_or_404(PlacementUpdate, id=company_id)
    
    if request.method == 'POST':
        company.company_name = request.POST.get('company_name')
        company.role = request.POST.get('role')
        company.package = request.POST.get('package')
        company.eligibility_cgpa = request.POST.get('eligibility_cgpa') or None
        company.branches_allowed = request.POST.get('branches_allowed')
        company.last_date = request.POST.get('last_date')
        company.drive_date = request.POST.get('drive_date')
        company.job_location = request.POST.get('job_location')
        company.mode = request.POST.get('mode')
        company.description = request.POST.get('description')
        
        if 'job_description_file' in request.FILES:
            company.job_description_file = request.FILES['job_description_file']
        
        company.save()
        
        return JsonResponse({'success': True, 'message': 'Company updated successfully!'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})


# ==================== ADMIN PLACEMENT APPROVAL ====================

def admin_placement_approval(request):
    """Admin: View and approve/reject placements"""
    try:
        pending_companies = PlacementUpdate.objects.filter(status='pending').order_by('-created_at')
    except:
        pending_companies = []
    
    context = {
        'pending_companies': pending_companies,
    }
    
    return render(request, 'admin-placement-approval.html', context)


def admin_approve_placement(request, company_id):
    """Admin: Approve placement"""
    company = get_object_or_404(PlacementUpdate, id=company_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        # Get or create default admin user
        from django.contrib.auth.models import User
        admin_user, _ = User.objects.get_or_create(username='admin_user', defaults={'email': 'admin@university.edu'})
        
        if action == 'approve':
            company.status = 'approved'
            company.approved_by = admin_user
            company.approved_at = timezone.now()
            company.save()
            return JsonResponse({'success': True, 'message': 'Company approved successfully!'})
        elif action == 'reject':
            company.status = 'rejected'
            company.approved_by = admin_user
            company.approved_at = timezone.now()
            company.save()
            return JsonResponse({'success': True, 'message': 'Company rejected.'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})


# ==================== STUDENT PLACEMENT VIEWS ====================

def student_placement_page(request):
    """Student: View approved placements"""
    # Get only approved placements (or all if none approved yet)
    try:
        approved_placements = PlacementUpdate.objects.filter(status='approved').order_by('-approved_at')
        if not approved_placements.exists():
            approved_placements = PlacementUpdate.objects.all().order_by('-created_at')[:10]
    except:
        approved_placements = []
    
    # Get student's applications
    try:
        from django.contrib.auth.models import User
        default_user, _ = User.objects.get_or_create(username='student_user', defaults={'email': 'student@university.edu'})
        student_applications = PlacementApplication.objects.filter(student=default_user).values_list('placement_id', flat=True)
    except:
        student_applications = []
    
    context = {
        'placements': approved_placements,
        'applied_placements': list(student_applications),
    }
    
    return render(request, 'placement.html', context)


def student_apply_placement(request, placement_id):
    """Student: Apply for placement"""
    placement = get_object_or_404(PlacementUpdate, id=placement_id, status='approved')
    
    if request.method == 'POST':
        # Get or create default user
        from django.contrib.auth.models import User
        default_user, _ = User.objects.get_or_create(username='student_user', defaults={'email': 'student@university.edu'})
        
        # Check if already applied
        if PlacementApplication.objects.filter(placement=placement, student=default_user).exists():
            return JsonResponse({'success': False, 'message': 'You have already applied for this position.'})
        
        try:
            profile, _ = UserProfile.objects.get_or_create(
                user=default_user,
                defaults={
                    'enrollment_no': 'STU001',
                    'department': 'Computer Science',
                    'role': 'student'
                }
            )
            
            application = PlacementApplication.objects.create(
                placement=placement,
                student=default_user,
                enrollment_no=profile.enrollment_no if profile else 'STU001',
                student_name=f"{default_user.first_name or 'Student'} {default_user.last_name or 'User'}",
                department=profile.department if profile else 'Computer Science',
                cgpa=request.POST.get('cgpa') or None,
                status='applied',
            )
            
            if 'resume' in request.FILES:
                application.resume = request.FILES['resume']
                application.save()
            
            return JsonResponse({'success': True, 'message': 'Application submitted successfully!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})


# ==================== CRC APPLICATION VIEWER ====================

def crc_view_applications(request, company_id):
    """CRC: View applications for a specific company"""
    company = get_object_or_404(PlacementUpdate, id=company_id)
    
    applications = PlacementApplication.objects.filter(placement=company).order_by('-applied_at')
    
    context = {
        'company': company,
        'applications': applications,
    }
    
    return render(request, 'crc-applications.html', context)


# ==================== STUDENT APPLICATION CENTER ====================

def application_center(request):
    """Student Application Center - Main page"""
    # For demo, get or create a default user profile
    from django.contrib.auth.models import User
    default_user, _ = User.objects.get_or_create(username='student_user', defaults={'email': 'student@university.edu'})
    
    try:
        profile, _ = UserProfile.objects.get_or_create(
            user=default_user,
            defaults={
                'enrollment_no': 'STU001',
                'department': 'Computer Science',
                'role': 'student'
            }
        )
    except:
        profile = None
    
    # Get student's applications
    applications = ApplicationRequest.objects.filter(student=default_user).order_by('-created_at')
    
    context = {
        'applications': applications,
        'profile': profile or {'user': {'first_name': 'Student', 'last_name': 'User'}, 'enrollment_no': 'STU001', 'department': 'Computer Science'},
    }
    
    return render(request, 'application-center.html', context)


def application_form(request, app_type):
    """Student Application Form - Dynamic form based on application type"""
    # For demo, get or create a default user profile
    from django.contrib.auth.models import User
    default_user, _ = User.objects.get_or_create(username='student_user', defaults={'email': 'student@university.edu'})
    
    try:
        profile, _ = UserProfile.objects.get_or_create(
            user=default_user,
            defaults={
                'enrollment_no': 'STU001',
                'department': 'Computer Science',
                'role': 'student',
                'contact_no': '1234567890'
            }
        )
    except:
        profile = type('obj', (object,), {
            'user': type('obj', (object,), {'first_name': 'Student', 'last_name': 'User', 'email': 'student@university.edu'})(),
            'enrollment_no': 'STU001',
            'department': 'Computer Science',
            'contact_no': '1234567890'
        })()
    
    # Valid application types
    valid_types = [choice[0] for choice in ApplicationRequest.APPLICATION_TYPES]
    if app_type not in valid_types:
        return redirect('application-center')
    
    # Reason options based on application type
    reason_options = get_reason_options(app_type)
    
    context = {
        'app_type': app_type,
        'app_type_display': dict(ApplicationRequest.APPLICATION_TYPES)[app_type],
        'profile': profile,
        'reason_options': reason_options,
    }
    
    return render(request, 'application-form.html', context)


def submit_application(request):
    """Submit student application"""
    if request.method == 'POST':
        # Get or create default user
        from django.contrib.auth.models import User
        default_user, _ = User.objects.get_or_create(username='student_user', defaults={'email': 'student@university.edu'})
        
        try:
            profile, _ = UserProfile.objects.get_or_create(
                user=default_user,
                defaults={
                    'enrollment_no': 'STU001',
                    'department': 'Computer Science',
                    'role': 'student'
                }
            )
        except:
            profile = None
        
        try:
            application = ApplicationRequest.objects.create(
                student=default_user,
                application_type=request.POST.get('application_type'),
                student_name=f"{default_user.first_name or 'Student'} {default_user.last_name or 'User'}",
                enrollment_no=profile.enrollment_no if profile else 'STU001',
                department=profile.department if profile else 'Computer Science',
                course=request.POST.get('course', ''),
                semester=request.POST.get('semester', ''),
                mobile=profile.contact_no if profile else '1234567890',
                email=default_user.email or 'student@university.edu',
                reason=request.POST.get('reason'),
                custom_reason=request.POST.get('custom_reason', ''),
                from_date=request.POST.get('from_date') or None,
                to_date=request.POST.get('to_date') or None,
                extra_note=request.POST.get('extra_note', ''),
                status='pending',
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Application submitted successfully!',
                'application_id': application.id
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})


def view_application(request, app_id):
    """View application details and generate PDF"""
    # For demo, allow viewing any application
    application = get_object_or_404(ApplicationRequest, id=app_id)
    
    context = {
        'application': application,
    }
    
    return render(request, 'application-view.html', context)


def get_reason_options(app_type):
    """Get reason options based on application type"""
    reasons = {
        'leave': [
            'Fever / Illness',
            'Family Emergency',
            'Out of Station',
            'Medical Checkup',
            'Injury',
            'Festival Leave',
            'Personal Work',
            'Hostel Related Work',
            'Exam Preparation',
            'Travel Issue',
        ],
        'bonafide': [
            'Passport',
            'Bank Account',
            'Scholarship',
            'Hostel Admission',
            'Visa',
            'Loan & Documents',
            'Government Certificate',
            'Internship',
        ],
        'character': [
            'Job Application',
            'Internship',
            'Higher Studies',
            'Verification Purpose',
            'Government Form',
            'Police Verification',
        ],
        'marksheet': [
            'Lost Marksheet',
            'Higher Education',
            'Job Interview',
            'University Transfer',
        ],
        'attendance_report': [
            'Attendance Correction',
            'Attendance Report for Parents',
            'Medical Leave Proof',
            'Low Attendance Appeal',
        ],
        'event_permission': [
            'Technical Event',
            'Sports Event',
            'Hackathon',
            'Cultural Fest',
            'External Competition',
        ],
        'internship_letter': [
            'Internship Application',
            'NOC Letter',
            'Internship Verification',
        ],
        'fee_receipt': [
            'Fee Receipt',
            'Scholarship Application',
            'Fee Concession',
        ],
        'bus_hostel': [
            'Bus Pass Application',
            'Hostel Application',
            'Bus Pass Renewal',
            'Hostel Room Change',
        ],
        'id_card': [
            'ID Card Lost',
            'ID Card Damaged',
            'ID Card Reissue',
            'IT Card Request',
        ],
    }
    
    return reasons.get(app_type, ['Other'])


def application_status(request):
    """View all applications status"""
    # For demo, get or create default user
    from django.contrib.auth.models import User
    default_user, _ = User.objects.get_or_create(username='student_user', defaults={'email': 'student@university.edu'})
    
    applications = ApplicationRequest.objects.filter(student=default_user).order_by('-created_at')
    
    context = {
        'applications': applications,
    }
    
    return render(request, 'application-status.html', context)
