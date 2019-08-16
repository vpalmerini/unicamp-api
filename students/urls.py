from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register('', views.StudentViewSet, base_name='students')

urlpatterns = router.urls