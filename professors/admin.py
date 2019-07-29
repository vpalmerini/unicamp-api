from django.contrib import admin
from .models import *


class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('name', 'institute')
    list_filter = ('institute', )


admin.site.register(Professor, ProfessorAdmin)
