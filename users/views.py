from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from .models import CustomUser, UserProgress
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
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
        try:
            # Parse JSON data from request body
            data = json.loads(request.body)
            print("Parsed JSON data:", data)  # Debugging line

            # Pass the parsed JSON data to the form
            signup_form = SignUpForm(data)

            if signup_form.is_valid():
                User = get_user_model()
                User.objects.create_user(
                    username=signup_form.cleaned_data.get('username'),
                    email=signup_form.cleaned_data.get('email'),
                    password=signup_form.cleaned_data.get('password'),
                )
                return JsonResponse({'message': 'Signup successful!'}, status=201)
            
            # If form is invalid, return errors
            print("Form errors:", signup_form.errors)  # Debugging line
            return JsonResponse({'message': 'Invalid data', 'errors': signup_form.errors}, status=400)

        except json.JSONDecodeError as e:
            print("JSON parsing error:", str(e))  # Debugging line
            return JsonResponse({'message': 'Invalid JSON data', 'error': str(e)}, status=400)

    return JsonResponse({'message': 'Invalid request method'}, status=405)


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        import json
        try:
            # Parse JSON body
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            # Authenticate user
            user = authenticate(request, username=username, password=password)

            if user:
                return JsonResponse({'message': 'Login successful!'}, status=200)
            else:
                return JsonResponse({'message': 'Invalid username or password.'}, status=401)
        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}'}, status=500)

    # Return a 405 Method Not Allowed for non-POST requests
    return JsonResponse({'message': 'Method not allowed'}, status=405)

@login_required
def get_user_progress(request):
    user = request.user
    try:
        progress = UserProgress.objects.get(user=user)
        return JsonResponse({'progress_percentage': progress.progress_percentage}, status=200)
    except UserProgress.DoesNotExist:
        return JsonResponse({'progress_percentage': 0}, status=200)
