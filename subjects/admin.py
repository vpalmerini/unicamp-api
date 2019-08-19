from django.contrib import admin
from .models import *


class SubjectAdmin(admin.ModelAdmin):
    list_display = ('initials', 'name', 'institute', 'workload')
    list_filter = ('institute', 'workload')


admin.site.register(Semester)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(PreReq)
admin.site.register(Continence)
admin.site.register(Equivalence)
