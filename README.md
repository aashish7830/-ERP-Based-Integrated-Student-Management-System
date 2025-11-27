# ERP Django Project

Django-based ERP system with all HTML templates integrated.

## Setup Instructions

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Migrations

```bash
python manage.py migrate
```

### 3. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 4. Run Development Server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Project Structure

```
ERP/
├── ERP_project/          # Main Django project settings
│   ├── settings.py       # Django settings
│   ├── urls.py          # Main URL configuration
│   └── wsgi.py          # WSGI configuration
├── ERP_app/             # Main Django application
│   ├── views.py         # View functions for all pages
│   ├── urls.py          # URL routing for all pages
│   └── models.py        # Database models
├── templates/           # All HTML templates (55 files)
├── static/              # Static files (CSS, JS)
│   ├── styles.css
│   └── navigation.js
└── manage.py            # Django management script
```

## Available Pages

All HTML templates have been converted to Django templates with:
- Django static file tags for CSS and JS
- Django URL tags for page navigation
- Dynamic routing through Django views

### Student Pages
- Dashboard, Attendance, Fees, Assignment, Calendar, Class, Events
- Examination, Exam Forms, Date Sheets, Hostel, Library
- Placement, Registration, Result, Syllabus, Transport Fee

### Administration Pages
- Admin Dashboard, Student Registration, HR, IT, Maintenance
- Registrar Office, Research & Innovation, Student Welfare

### Board of Trustees
- Chancellor-President Portal, Dean of Academics, Finance Portal
- Registrar Portal, Vice-Chancellor Portal

### Specialized Departments
- Environmental Sustainability, Innovation & Startup
- International Relations, Legal Cell, Medical Center
- Online Learning, PR Office

### Support Cells
- Alumni Relations, Anti-Ragging, Cultural Committee
- Disciplinary Committee, IQAC, NSS-NCC
- Sports Committee, Women's Cell

### Other Portals
- Account Office, CRC Portal, Faculty Portal, Scholarship Portal

## Features

- ✅ All 55 HTML pages integrated with Django
- ✅ Static files properly configured
- ✅ Dynamic URL routing
- ✅ Template inheritance ready
- ✅ Ready for database integration

## Next Steps

1. Add authentication system
2. Create database models for students, faculty, etc.
3. Implement form handling
4. Add API endpoints if needed
5. Deploy to production server

