from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from .models import CustomUser, UserProgress
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.decorators import login_required
from core.forms import LoginForm, SignUpForm  # Import forms
import json

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
        signup_form = SignUpForm(request.POST)
        if signup_form.is_valid():
            User = get_user_model()
            User.objects.create_user(
                username=signup_form.cleaned_data.get('username'),
                email=signup_form.cleaned_data.get('email'),
                password=signup_form.cleaned_data.get('password')
            )
            return JsonResponse({'message': 'Signup successful!'}, status=201)
        return JsonResponse({'message': 'Invalid data'}, status=400)
    else:
        signup_form = SignUpForm()
        return render(request, 'login_signup.html', {'signup_form': signup_form})

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'message': 'Login successful!'}, status=200)
            return JsonResponse({'message': 'Invalid credentials'}, status=401)
    else:
        login_form = LoginForm()
        return render(request, 'login_signup.html', {'login_form': login_form})

@login_required
def get_user_progress(request):
    user = request.user
    try:
        progress = UserProgress.objects.get(user=user)
        return JsonResponse({'progress_percentage': progress.progress_percentage}, status=200)
    except UserProgress.DoesNotExist:
        return JsonResponse({'progress_percentage': 0}, status=200)
