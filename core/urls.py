from django.urls import path
from .views import CourseList, ModuleList, LessonList

urlpatterns = [
    path('courses/', CourseList.as_view(), name='course-list'),
    path('modules/', ModuleList.as_view(), name='module-list'),
    path('lessons/', LessonList.as_view(), name='lesson-list'),
]
