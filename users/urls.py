from django.urls import path
from .views import (
    UserCreate, 
    UserProfile, 
    login_view, 
    signup_view, 
    dashboard_view, 
    get_user_progress, 
    logout_view,
    update_profile_picture,
    module_lessons_view,
    lesson_detail_view,
    mark_lesson_complete
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'users'

urlpatterns = [
    path('register/', UserCreate.as_view(), name='user-create'),
    path('profile/', UserProfile.as_view(), name='user-profile'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('profile/edit/', update_profile_picture, name='profile_edit'),
    path('update-profile-picture/', update_profile_picture, name='update-profile-picture'),
    path('module/<int:module_id>/lessons/', module_lessons_view, name='module_lessons'),
    path('lesson/<int:lesson_id>/', lesson_detail_view, name='lesson_detail'),
    path('lesson/<int:lesson_id>/complete/', mark_lesson_complete, name='mark_lesson_complete'),    
    path('logout/', logout_view, name='logout'),  # New logout route
    path('api/progress/', get_user_progress, name='get_user_progress'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
