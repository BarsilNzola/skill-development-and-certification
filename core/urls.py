from django.urls import path
from .views import home, login_signup, CourseListCreate, CourseDetail, ModuleListCreate, ModuleDetail, LessonListCreate, LessonDetail, ProgressListCreate, ProgressDetail, QuizListCreate, QuizDetail, QuestionListCreate, QuestionDetail, generate_certificate

urlpatterns = [
    path('', home, name='home'),
    path('login_signup/', login_signup, name='login_signup'),
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
