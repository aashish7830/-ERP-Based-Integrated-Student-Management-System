"""
Management command to populate university structure from flowchart
Run: python manage.py populate_university_structure
"""
from django.core.management.base import BaseCommand
from ERP_app.models import (
    GoverningBody, School, Department, Program, AcademicSection, SupportCell
)

class Command(BaseCommand):
    help = 'Populate university structure database from flowchart data'

    def handle(self, *args, **options):
        self.stdout.write('Creating University Structure...')
        
        # 1. Create Governing Bodies
        self.stdout.write('Creating Governing Bodies...')
        GoverningBody.objects.get_or_create(
            body_type='chancellor',
            defaults={
                'name': 'Chancellor',
                'designation': 'Ceremonial Head',
                'description': 'Ceremonial head of the university',
                'icon': 'bi-person-badge',
                'color': 'primary'
            }
        )
        GoverningBody.objects.get_or_create(
            body_type='vice_chancellor',
            defaults={
                'name': 'Vice-Chancellor',
                'designation': 'Executive Head',
                'description': 'Executive head of the university',
                'icon': 'bi-person-check',
                'color': 'success'
            }
        )
        GoverningBody.objects.get_or_create(
            body_type='registrar',
            defaults={
                'name': 'Registrar',
                'designation': 'Administrative Head',
                'description': 'Administrative head of the university',
                'icon': 'bi-file-earmark-text',
                'color': 'info'
            }
        )
        GoverningBody.objects.get_or_create(
            body_type='dean',
            defaults={
                'name': 'Deans',
                'designation': 'Faculty Leaders',
                'description': 'Leaders of various schools/faculties',
                'icon': 'bi-mortarboard',
                'color': 'warning'
            }
        )
        
        # 2. Create Schools
        self.stdout.write('Creating Schools...')
        schools_data = [
            {
                'name': 'School of Engineering',
                'short_name': 'Engineering',
                'icon': 'bi-cpu',
                'color': 'primary',
                'departments': [
                    'Computer Science Engineering (CSE)',
                    'Information Technology (IT)',
                    'Electronics & Communication Engineering (ECE)',
                    'Electrical Engineering (EE)',
                    'Mechanical Engineering (ME)',
                    'Civil Engineering (CE)',
                    'AI & Machine Learning (AI/ML)',
                    'Data Science',
                    'Robotics & Automation',
                    'Chemical Engineering'
                ],
                'programs': ['B.Tech', 'M.Tech', 'PhD']
            },
            {
                'name': 'School of Science',
                'short_name': 'Science',
                'icon': 'bi-flask',
                'color': 'info',
                'departments': [
                    'Physics',
                    'Chemistry',
                    'Mathematics',
                    'Zoology',
                    'Botany',
                    'Biotechnology',
                    'Microbiology',
                    'Environmental Science',
                    'Biochemistry',
                    'Geology / Earth Science'
                ],
                'programs': ['B.Sc', 'M.Sc', 'PhD']
            },
            {
                'name': 'School of Arts & Humanities',
                'short_name': 'Arts',
                'icon': 'bi-book',
                'color': 'warning',
                'departments': [
                    'Hindi',
                    'English',
                    'Sanskrit',
                    'Urdu / Persian',
                    'History',
                    'Geography',
                    'Philosophy',
                    'Performing Arts (Music/Dance)',
                    'Fine Arts (Drawing/Painting)'
                ],
                'programs': ['BA', 'MA', 'PhD']
            },
            {
                'name': 'School of Commerce & Management',
                'short_name': 'Commerce',
                'icon': 'bi-briefcase',
                'color': 'success',
                'departments': [
                    'Commerce',
                    'Accounting & Finance',
                    'Marketing',
                    'Human Resource Management',
                    'Business Administration',
                    'Economics'
                ],
                'programs': ['B.Com', 'BBA', 'MBA', 'M.Com', 'PhD']
            },
            {
                'name': 'School of Agriculture',
                'short_name': 'Agriculture',
                'icon': 'bi-tree',
                'color': 'success',
                'departments': [
                    'Agronomy',
                    'Horticulture',
                    'Soil Science',
                    'Agricultural Engineering',
                    'Plant Pathology',
                    'Entomology',
                    'Genetics & Plant Breeding',
                    'Forestry',
                    'Food Technology'
                ],
                'programs': ['B.Sc Agriculture', 'M.Sc Agriculture', 'PhD']
            },
            {
                'name': 'School of Law',
                'short_name': 'Law',
                'icon': 'bi-shield-check',
                'color': 'danger',
                'departments': [
                    'Constitutional Law',
                    'Criminal Law',
                    'Corporate Law',
                    'Civil Law',
                    'Family Law',
                    'Human Rights Law',
                    'Cyber Law',
                    'Intellectual Property Rights (IPR)'
                ],
                'programs': ['BA LLB', 'BBA LLB', 'LLB', 'LLM', 'PhD']
            },
            {
                'name': 'School of Medical Sciences',
                'short_name': 'Medical',
                'icon': 'bi-heart-pulse',
                'color': 'danger',
                'departments': [
                    'Anatomy',
                    'Physiology',
                    'Biochemistry',
                    'Pathology',
                    'Pharmacology',
                    'Microbiology',
                    'Community Medicine',
                    'Surgery',
                    'Medicine',
                    'Orthopedics',
                    'Pediatrics',
                    'Gynecology'
                ],
                'programs': ['MBBS', 'MD/MS', 'BPT, BOT', 'Nursing']
            },
            {
                'name': 'School of Pharmacy',
                'short_name': 'Pharmacy',
                'icon': 'bi-capsule',
                'color': 'primary',
                'departments': [
                    'Pharmaceutics',
                    'Pharmacology',
                    'Pharmaceutical Chemistry',
                    'Pharmacognosy',
                    'Pharmaceutical Biotechnology'
                ],
                'programs': ['D.Pharm', 'B.Pharm', 'M.Pharm', 'PhD']
            },
            {
                'name': 'School of Education',
                'short_name': 'Education',
                'icon': 'bi-mortarboard',
                'color': 'info',
                'departments': [
                    'Teacher Training',
                    'Educational Psychology',
                    'Curriculum Studies',
                    'Special Education',
                    'Educational Technology',
                    'Physical Education'
                ],
                'programs': ['B.Ed', 'M.Ed', 'B.P.Ed', 'PhD']
            },
            {
                'name': 'School of Computer Applications',
                'short_name': 'Computer',
                'icon': 'bi-laptop',
                'color': 'primary',
                'departments': [
                    'Computer Applications',
                    'Software Engineering',
                    'Data Analytics',
                    'Cyber Security',
                    'Cloud Computing',
                    'Networking & Systems Administration'
                ],
                'programs': ['BCA', 'MCA', 'PG Diploma in Computer Applications', 'PhD']
            },
            {
                'name': 'School of Social Sciences',
                'short_name': 'Social',
                'icon': 'bi-people',
                'color': 'warning',
                'departments': [
                    'Sociology',
                    'Psychology',
                    'Social Work',
                    'Anthropology',
                    'Political Science',
                    'Public Administration',
                    'Geography'
                ],
                'programs': ['BA Social Sciences', 'MA', 'MSW (Social Work)', 'PhD']
            },
        ]
        
        for school_data in schools_data:
            school, created = School.objects.get_or_create(
                name=school_data['name'],
                defaults={
                    'short_name': school_data['short_name'],
                    'icon': school_data['icon'],
                    'color': school_data['color']
                }
            )
            
            # Create Departments for this school
            for dept_name in school_data['departments']:
                department, dept_created = Department.objects.get_or_create(
                    school=school,
                    name=dept_name,
                    defaults={'is_active': True}
                )
                
                # Create Programs for this department
                for prog_name in school_data['programs']:
                    Program.objects.get_or_create(
                        department=department,
                        name=prog_name,
                        defaults={
                            'degree_type': self._get_degree_type(prog_name),
                            'is_active': True
                        }
                    )
        
        # 3. Create Academic Sections
        self.stdout.write('Creating Academic Sections...')
        academic_sections = [
            ('examination', 'Examination Cell', 'Handles all examination related activities'),
            ('admission', 'Admission Cell', 'Manages student admissions'),
            ('placement', 'Training & Placement Cell', 'Manages placements and internships'),
            ('library', 'Library', 'Library and resource management'),
            ('research', 'Research & Development Cell', 'Research and development activities'),
            ('sports', 'Sports & Cultural Cell', 'Sports and cultural activities'),
            ('hostel', 'Hostel Management', 'Hostel administration'),
            ('finance', 'Finance & Accounts', 'Financial management'),
            ('hr', 'Human Resource Department (HR)', 'HR management'),
        ]
        
        for section_type, name, description in academic_sections:
            AcademicSection.objects.get_or_create(
                section_type=section_type,
                defaults={
                    'name': name,
                    'description': description,
                    'is_active': True
                }
            )
        
        # 4. Create Support Cells
        self.stdout.write('Creating Support Cells...')
        support_cells = [
            ('alumni', 'Alumni Relations', 'Alumni network management'),
            ('anti_ragging', 'Anti-Ragging', 'Anti-ragging committee'),
            ('cultural', 'Cultural Committee', 'Cultural activities'),
            ('disciplinary', 'Disciplinary Committee', 'Disciplinary matters'),
            ('iqac', 'IQAC', 'Internal Quality Assurance Cell'),
            ('nss_ncc', 'NSS/NCC', 'National Service Scheme / NCC'),
            ('sports', 'Sports Committee', 'Sports activities'),
            ('womens', 'Women\'s Cell', 'Women\'s welfare'),
        ]
        
        for cell_type, name, description in support_cells:
            SupportCell.objects.get_or_create(
                cell_type=cell_type,
                defaults={
                    'name': name,
                    'description': description,
                    'is_active': True
                }
            )
        
        self.stdout.write(self.style.SUCCESS('Successfully populated university structure!'))
        self.stdout.write(f'Created: {School.objects.count()} Schools, {Department.objects.count()} Departments, {Program.objects.count()} Programs')
    
    def _get_degree_type(self, program_name):
        """Determine degree type from program name"""
        if 'B.' in program_name or 'BA' in program_name or 'B.Sc' in program_name or 'B.Com' in program_name or 'BBA' in program_name or 'BCA' in program_name or 'B.Ed' in program_name or 'B.Pharm' in program_name or 'D.Pharm' in program_name or 'LLB' in program_name or 'MBBS' in program_name or 'BPT' in program_name:
            return 'bachelor'
        elif 'M.' in program_name or 'MA' in program_name or 'M.Sc' in program_name or 'M.Com' in program_name or 'MBA' in program_name or 'MCA' in program_name or 'M.Ed' in program_name or 'M.Pharm' in program_name or 'LLM' in program_name or 'MD' in program_name or 'MS' in program_name:
            return 'master'
        elif 'PhD' in program_name or 'Ph.D' in program_name:
            return 'phd'
        elif 'Diploma' in program_name or 'PG Diploma' in program_name:
            return 'diploma'
        else:
            return 'certificate'

