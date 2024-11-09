from django.shortcuts import render
from rest_framework import generics
from .models import CustomUser
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated

class UserCreate(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
class UserProfile(generics.RetrieveUpdateAPIView): 
    queryset = CustomUser.objects.all() 
    serializer_class = UserSerializer 
    permission_classes = [IsAuthenticated] 
    
    def get_object(self): 
        return self.request.user


# Create your views here.
