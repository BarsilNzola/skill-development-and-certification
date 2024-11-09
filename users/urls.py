from django.urls import path
from .views import UserCreate
from .views import UserProfile

urlpatterns = [
    path('register/', UserCreate.as_view(), name='user-create'),
    path('profile/', UserProfile.as_view(), name='user-profile'),
]
