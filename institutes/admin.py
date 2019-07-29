from django.contrib import admin
from .models import *


class InstituteAdmin(admin.ModelAdmin):
    list_display = ('initials', 'name')


admin.site.register(Institute, InstituteAdmin)
