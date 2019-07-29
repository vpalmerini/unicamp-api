from django.contrib import admin
from .models import *


class ClassAdmin(admin.ModelAdmin):
    list_display = ('class_id', 'subject', 'positions', 'enrolled')


admin.site.register(Class, ClassAdmin)
admin.site.register(Schedule)
