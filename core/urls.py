from django.urls import path, include
from django.contrib import admin
from .views import home, login_signup, CourseListCreate, CourseDetail, ModuleListCreate, ModuleDetail, LessonListCreate, LessonDetail, ProgressListCreate, ProgressDetail, QuizListCreate, QuizDetail, QuestionListCreate, QuestionDetail, generate_certificate
from users.views import login_view, signup_view, dashboard_view

app_name = 'core'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls', namespace='users')),  # Include the namespace here
    path('', home, name='home'),
    path('login_signup/', login_signup, name='login_signup'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('courses/', CourseListCreate.as_view(), name='course-list-create'),
    path('courses/<int:pk>/', CourseDetail.as_view(), name='course-detail'),
    path('modules/', ModuleListCreate.as_view(), name='module-list-create'),
    path('modules/<int:pk>/', ModuleDetail.as_view(), name='module-detail'),
    path('lessons/', LessonListCreate.as_view(), name='lesson-list-create'),
    path('lessons/<int:pk>/', LessonDetail.as_view(), name='lesson-detail'),
    path('progress/', ProgressListCreate.as_view(), name='progress-list-create'),
    path('progress/<int:pk>/', ProgressDetail.as_view(), name='progress-detail'),
    path('quizzes/', QuizListCreate.as_view(), name='quiz-list-create'),
    path('quizzes/<int:pk>/', QuizDetail.as_view(), name='quiz-detail'),
    path('questions/', QuestionListCreate.as_view(), name='question-list-create'),
    path('questions/<int:pk>/', QuestionDetail.as_view(), name='question-detail'),
    path('certificates/<int:course_id>/<int:user_id>/', generate_certificate, name='generate-certificate'),
]
