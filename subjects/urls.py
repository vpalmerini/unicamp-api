from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register('', views.SubjectViewSet, base_name='subjects')

urlpatterns = router.urls