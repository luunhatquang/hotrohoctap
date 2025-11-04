from django.contrib import admin
from .models import School, Program, Admission, StudentProfile, TrialExam, HsaExam, TsaExam


class AdmissionInline(admin.TabularInline):
    model = Admission
    extra = 1

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'school')
    inlines = [AdmissionInline]

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'region')

@admin.register(Admission)
class AdmissionAdmin(admin.ModelAdmin):
    list_display = ('program', 'year', 'score', 'code')

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)

