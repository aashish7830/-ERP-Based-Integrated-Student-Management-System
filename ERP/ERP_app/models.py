from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# User Profile Extensions
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    enrollment_no = models.CharField(max_length=50, unique=True, null=True, blank=True)
    contact_no = models.CharField(max_length=15, null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    school = models.CharField(max_length=100, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    section = models.CharField(max_length=10, null=True, blank=True)
    role = models.CharField(max_length=50, choices=[
        ('admin', 'Admin'),
        ('dean', 'Dean'),
        ('hod', 'HOD'),
        ('faculty', 'Faculty'),
        ('crc', 'CRC'),
        ('student', 'Student'),
    ], default='student')
    college_name = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"

# Attendance Models
class AttendanceRecord(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendance_records')
    enrollment_no = models.CharField(max_length=50)
    student_name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    school = models.CharField(max_length=100)
    year = models.IntegerField()
    section = models.CharField(max_length=10)
    course = models.CharField(max_length=100)
    faculty = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='faculty_attendance')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
    ], default='absent')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date', 'student_name']
        indexes = [
            models.Index(fields=['enrollment_no', 'date']),
            models.Index(fields=['department', 'date']),
            models.Index(fields=['school', 'date']),
            models.Index(fields=['year', 'section']),
            models.Index(fields=['course', 'date']),
            models.Index(fields=['faculty', 'date']),
        ]
    
    def __str__(self):
        return f"{self.student_name} - {self.date} - {self.status}"

# Placement Models
class PlacementUpdate(models.Model):
    company_name = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    package = models.DecimalField(max_digits=10, decimal_places=2, help_text="CTC in LPA")
    eligibility_cgpa = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True, 
                                          validators=[MinValueValidator(0), MaxValueValidator(10)])
    branches_allowed = models.CharField(max_length=500, help_text="Comma-separated list of branches")
    last_date = models.DateField()
    drive_date = models.DateField()
    job_location = models.CharField(max_length=200)
    mode = models.CharField(max_length=20, choices=[
        ('on-campus', 'On-campus'),
        ('off-campus', 'Off-campus'),
    ], default='on-campus')
    description = models.TextField()
    job_description_file = models.FileField(upload_to='placement_jds/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], default='pending')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='placement_updates_created')
    created_at = models.DateTimeField(auto_now_add=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='placement_updates_approved')
    approved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.company_name} - {self.role}"

class PlacementApplication(models.Model):
    placement = models.ForeignKey(PlacementUpdate, on_delete=models.CASCADE, related_name='applications')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='placement_applications')
    enrollment_no = models.CharField(max_length=50)
    student_name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    cgpa = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    resume = models.FileField(upload_to='placement_resumes/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('applied', 'Applied'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
        ('selected', 'Selected'),
    ], default='applied')
    applied_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(null=True, blank=True)
    
    class Meta:
        ordering = ['-applied_at']
        unique_together = ['placement', 'student']
    
    def __str__(self):
        return f"{self.student_name} - {self.placement.company_name}"

# Student Application Models
class ApplicationRequest(models.Model):
    APPLICATION_TYPES = [
        ('leave', 'Leave Application'),
        ('bonafide', 'Bonafide Certificate Request'),
        ('character', 'HR / Character Certificate Request'),
        ('attendance_report', 'Attendance Report Request'),
        ('marksheet', 'Marksheet / Transcript Request'),
        ('event_permission', 'Event Participation Permission'),
        ('internship_letter', 'Internship Letter Request'),
        ('fee_receipt', 'Fee Receipt/Scholarship Application'),
        ('bus_hostel', 'Bus/Hostel Application'),
        ('id_card', 'IT/ID Card Reissue Request'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='application_requests')
    application_type = models.CharField(max_length=50, choices=APPLICATION_TYPES)
    
    # Auto-filled fields
    student_name = models.CharField(max_length=100)
    enrollment_no = models.CharField(max_length=50)
    department = models.CharField(max_length=100)
    course = models.CharField(max_length=100, null=True, blank=True)
    semester = models.CharField(max_length=20, null=True, blank=True)
    mobile = models.CharField(max_length=15)
    email = models.EmailField()
    
    # Manual fields
    reason = models.CharField(max_length=200)
    custom_reason = models.TextField(null=True, blank=True)  # For custom reason input
    from_date = models.DateField(null=True, blank=True)  # For leave applications
    to_date = models.DateField(null=True, blank=True)  # For leave applications
    extra_note = models.TextField(null=True, blank=True)
    
    # Status tracking
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('in_process', 'In Process'),
    ], default='pending')
    
    # Admin fields
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_applications')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    admin_notes = models.TextField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['student', 'application_type']),
            models.Index(fields=['status', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.get_application_type_display()} - {self.student_name} ({self.enrollment_no})"

# ==================== UNIVERSITY STRUCTURE MODELS ====================

# Governing Bodies
class GoverningBody(models.Model):
    BODY_TYPES = [
        ('chancellor', 'Chancellor'),
        ('vice_chancellor', 'Vice-Chancellor'),
        ('registrar', 'Registrar'),
        ('dean', 'Dean'),
    ]
    
    body_type = models.CharField(max_length=50, choices=BODY_TYPES)
    name = models.CharField(max_length=200)
    designation = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    icon = models.CharField(max_length=50, default='bi-person-badge')
    color = models.CharField(max_length=20, default='primary')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['body_type', 'name']
        verbose_name_plural = 'Governing Bodies'
    
    def __str__(self):
        return f"{self.get_body_type_display()} - {self.name}"

# Schools/Faculties
class School(models.Model):
    name = models.CharField(max_length=200, unique=True)
    short_name = models.CharField(max_length=50, null=True, blank=True)
    icon = models.CharField(max_length=50, default='bi-building')
    color = models.CharField(max_length=20, default='primary')
    description = models.TextField(null=True, blank=True)
    dean = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='schools_as_dean')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_department_count(self):
        return self.departments.count()
    
    def get_program_count(self):
        return Program.objects.filter(department__school=self).count()

# Departments
class Department(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='departments')
    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    hod = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='departments_as_hod')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['school', 'name']
        unique_together = ['school', 'name']
    
    def __str__(self):
        return f"{self.school.name} - {self.name}"
    
    def get_faculty_count(self):
        return self.faculty_members.count()
    
    def get_student_count(self):
        return UserProfile.objects.filter(department=self.name).count()

# Programs (Degrees/Courses)
class Program(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='programs')
    name = models.CharField(max_length=200)
    degree_type = models.CharField(max_length=50, choices=[
        ('bachelor', 'Bachelor'),
        ('master', 'Master'),
        ('phd', 'PhD'),
        ('diploma', 'Diploma'),
        ('certificate', 'Certificate'),
    ])
    duration_years = models.IntegerField(default=4)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['department', 'degree_type', 'name']
        unique_together = ['department', 'name']
    
    def __str__(self):
        return f"{self.department.name} - {self.name}"

# Faculty Members
class FacultyMember(models.Model):
    FACULTY_RANKS = [
        ('hod', 'HOD (Head of Department)'),
        ('professor', 'Professor'),
        ('associate_professor', 'Associate Professor'),
        ('assistant_professor', 'Assistant Professor'),
        ('lecturer', 'Lecturer'),
        ('lab_incharge', 'Senior Lab Incharge'),
        ('curriculum_incharge', 'Faculty Incharge of Curriculum/Exams'),
        ('teaching_assistant', 'Teaching Assistant/Mentor'),
        ('lab_assistant', 'Lab Assistant/Tech Staff'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='faculty_profile')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='faculty_members')
    rank = models.CharField(max_length=50, choices=FACULTY_RANKS)
    specialization = models.CharField(max_length=200, null=True, blank=True)
    qualification = models.CharField(max_length=200, null=True, blank=True)
    experience_years = models.IntegerField(default=0)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    office_room = models.CharField(max_length=50, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    joined_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['department', 'rank', 'user__last_name']
        unique_together = ['user', 'department']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.department.name} ({self.get_rank_display()})"

# Academic Sections
class AcademicSection(models.Model):
    SECTION_TYPES = [
        ('examination', 'Examination Cell'),
        ('admission', 'Admission Cell'),
        ('placement', 'Training & Placement Cell'),
        ('library', 'Library'),
        ('research', 'Research & Development Cell'),
        ('sports', 'Sports & Cultural Cell'),
        ('hostel', 'Hostel Management'),
        ('finance', 'Finance & Accounts'),
        ('hr', 'Human Resource Department (HR)'),
    ]
    
    section_type = models.CharField(max_length=50, choices=SECTION_TYPES)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    incharge = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sections_as_incharge')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['section_type', 'name']
    
    def __str__(self):
        return f"{self.get_section_type_display()} - {self.name}"

# Support Cells
class SupportCell(models.Model):
    CELL_TYPES = [
        ('alumni', 'Alumni Relations'),
        ('anti_ragging', 'Anti-Ragging'),
        ('cultural', 'Cultural Committee'),
        ('disciplinary', 'Disciplinary Committee'),
        ('iqac', 'IQAC'),
        ('nss_ncc', 'NSS/NCC'),
        ('sports', 'Sports Committee'),
        ('womens', 'Women\'s Cell'),
    ]
    
    cell_type = models.CharField(max_length=50, choices=CELL_TYPES)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    coordinator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='cells_as_coordinator')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['cell_type', 'name']
    
    def __str__(self):
        return f"{self.get_cell_type_display()} - {self.name}"
