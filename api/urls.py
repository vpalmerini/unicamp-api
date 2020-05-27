from django.contrib import admin
from django.urls import path, include

base_api_path = 'api/v1'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('{}/institutes/'.format(base_api_path), include('institutes.urls')),
    path('{}/courses/'.format(base_api_path), include('courses.urls')),
    path('{}/subjects/'.format(base_api_path), include('subjects.urls')),
    path('{}/classes/'.format(base_api_path), include('classes.urls')),
    path('{}/professors/'.format(base_api_path), include('professors.urls')),
    path('{}/students/'.format(base_api_path), include('students.urls')),
]
