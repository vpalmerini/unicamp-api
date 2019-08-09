from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register('', views.ProfessorViewSet, base_name='professors')

urlpatterns = router.urls