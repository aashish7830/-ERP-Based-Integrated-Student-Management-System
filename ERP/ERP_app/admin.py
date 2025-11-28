from django.contrib import admin
from .models import (
    UserProfile, AttendanceRecord, PlacementUpdate, PlacementApplication,
    ApplicationRequest, GoverningBody, School, Department, Program,
    FacultyMember, AcademicSection, SupportCell
)

# Register all models
admin.site.register(UserProfile)
admin.site.register(AttendanceRecord)
admin.site.register(PlacementUpdate)
admin.site.register(PlacementApplication)
admin.site.register(ApplicationRequest)
admin.site.register(GoverningBody)
admin.site.register(School)
admin.site.register(Department)
admin.site.register(Program)
admin.site.register(FacultyMember)
admin.site.register(AcademicSection)
admin.site.register(SupportCell)

