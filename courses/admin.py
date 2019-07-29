from django.contrib import admin
from .models import *


class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'institute', 'shift')
    list_filter = ('institute', )


admin.site.register(Course, CourseAdmin)
