from django.contrib import admin
from django.urls import path, include

base_api_path = 'api/v1'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('{}/institutes/'.format(base_api_path), include('institutes.urls')),
]
