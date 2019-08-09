from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register('', views.ClassViewSet, base_name='classes')

urlpatterns = router.urls
