from rest_framework.routers import DefaultRouter
from .views import InstituteViewSet
from courses.views import CourseViewSet
from subjects.views import SubjectViewSet
from professors.views import ProfessorViewSet
from classes.views import ClassViewSet
from students.views import StudentViewSet
from rest_framework_extensions.routers import NestedRouterMixin


class NestedDefaultRouter(NestedRouterMixin, DefaultRouter):
    pass


router = NestedDefaultRouter()

institutes_router = router.register('', InstituteViewSet)

institutes_router.register(
    'courses',
    CourseViewSet,
    basename='institute-courses',
    parents_query_lookups=['institute']).register(
        'students',
        StudentViewSet,
        basename='institute-course-students',
        parents_query_lookups=['course__institute', 'course'])

institutes_router.register(
    'subjects',
    SubjectViewSet,
    basename='institute-subjects',
    parents_query_lookups=['institute']).register(
        'classes',
        ClassViewSet,
        basename='institute-subject-classes',
        parents_query_lookups=['subject__institute', 'subject'])

institutes_router.register('professors',
                           ProfessorViewSet,
                           basename='institute-professors',
                           parents_query_lookups=['institute'])

urlpatterns = router.urls
