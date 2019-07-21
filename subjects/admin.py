from django.contrib import admin
from .models import *

class InstituteAdmin(admin.ModelAdmin):
    list_display = ('initials', 'name')

class SubjectAdmin(admin.ModelAdmin):
    list_display = ('initials', 'name', 'institute', 'workload', 'year')
    list_filter = ('institute', 'year', 'workload')

class ClassAdmin(admin.ModelAdmin):
    list_display = ('class_id', 'subject', 'positions', 'enrolled')

class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'institute')
    list_filter = ('institute', )

class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('name', 'institute')
    list_filter = ('institute', )

admin.site.register(Institute, InstituteAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Professor, ProfessorAdmin)

admin.site.register(Schedule)
admin.site.register(PreReq)
admin.site.register(Continence)
admin.site.register(Equivalence)
