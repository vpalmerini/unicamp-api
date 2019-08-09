from rest_framework.routers import DefaultRouter
from .views import SubjectViewSet
from classes.views import ClassViewSet
from rest_framework_extensions.routers import NestedRouterMixin


class NestedDefaultRouter(NestedRouterMixin, DefaultRouter):
    pass


router = NestedDefaultRouter()

subjects_router = router.register('', SubjectViewSet)

# subjects_router.register('classes',
#                          ClassViewSet,
#                          basename='subject-classes',
#                          parents_query_lookups=['subject'])

urlpatterns = router.urls