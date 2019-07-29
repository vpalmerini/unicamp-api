from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register('', views.InstituteViewSet, base_name='institutes')

urlpatterns = router.urls
