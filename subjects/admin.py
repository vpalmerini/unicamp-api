from django.contrib import admin
from .models import *


class SubjectAdmin(admin.ModelAdmin):
    list_display = ('initials', 'name', 'institute', 'workload', 'year')
    list_filter = ('institute', 'year', 'workload')


admin.site.register(Subject, SubjectAdmin)
admin.site.register(PreReq)
admin.site.register(Continence)
admin.site.register(Equivalence)
