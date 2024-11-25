from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from .models import CustomUser
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
import json
from django.contrib.auth.decorators import login_required 
from .models import UserProgress

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
    

@csrf_exempt
def signup_view(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if User.objects.filter(username=username).exists():
            return JsonResponse({'message': 'Username already taken'}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({'message': 'Email already registered'}, status=400)

        User.objects.create_user(username=username, email=email, password=password)
        return JsonResponse({'message': 'Signup successful!'}, status=201)
    
    return JsonResponse({'message': 'Invalid request method'}, status=400)

    
@csrf_exempt 
def login_view(request): 
    if request.method == 'POST': 
        data = json.loads(request.body.decode('utf-8')) 
        username = data.get('username') 
        password = data.get('password') 
        
        # Dummy authentication for demonstration 
        if username == 'user' and password == 'password': 
            return JsonResponse({'message': 'Login successful!'}, status=200) 
        else: 
            return JsonResponse({'message': 'Invalid credentials'}, status=401) 
    return JsonResponse({'message': 'Invalid request method'}, status=400)

@login_required 
def get_user_progress(request): 
    user = request.user 
    try: 
        progress = UserProgress.objects.get(user=user) 
        return JsonResponse({'progress_percentage': progress.progress_percentage}, status=200) 
    except UserProgress.DoesNotExist: return JsonResponse({'progress_percentage': 0}, status=200)
# Create your views here.
