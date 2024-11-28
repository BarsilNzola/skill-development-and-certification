from django.urls import path
from .views import UserCreate, UserProfile, login_view, signup_view, get_user_progress
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'users'

urlpatterns = [
    path('register/', UserCreate.as_view(), name='user-create'),
    path('profile/', UserProfile.as_view(), name='user-profile'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('api/progress/', get_user_progress, name='get_user_progress'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
