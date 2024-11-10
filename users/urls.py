from django.urls import path
from .views import UserCreate
from .views import UserProfile
from .views import login_view, signup_view

urlpatterns = [
    path('register/', UserCreate.as_view(), name='user-create'),
    path('profile/', UserProfile.as_view(), name='user-profile'),
    path('api/login/', login_view, name='login'),
    path('api/signup/', signup_view, name='signup'),
]
