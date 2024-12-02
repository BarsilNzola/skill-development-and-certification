from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from .models import CustomUser, UserProgress
from core.models import Module, LearningResource, Lesson
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from core.forms import LoginForm, SignUpForm, ProfileEditForm
from django.http import HttpResponseNotFound
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
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
            data = json.loads(request.body)
            signup_form = SignUpForm(data)

            if signup_form.is_valid():
                User = get_user_model()
                User.objects.create_user(
                    username=signup_form.cleaned_data.get('username'),
                    email=signup_form.cleaned_data.get('email'),
                    password=signup_form.cleaned_data.get('password'),
                )
                return JsonResponse({'message': 'Signup successful!'}, status=201)
            
            return JsonResponse({'message': 'Invalid data', 'errors': signup_form.errors}, status=400)

        except json.JSONDecodeError as e:
            return JsonResponse({'message': 'Invalid JSON data', 'error': str(e)}, status=400)

    return JsonResponse({'message': 'Invalid request method'}, status=405)

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                request.session['user_id'] = user.id
                return JsonResponse({'message': 'Login successful!', 'redirect_url': '/users/dashboard/'}, status=200)
            else:
                return JsonResponse({'message': 'Invalid username or password.'}, status=401)
        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}'}, status=500)

    return JsonResponse({'message': 'Method not allowed'}, status=405)

@login_required
def dashboard_view(request):
    modules = Module.objects.all()  # Fetch all available modules
    learning_resources = LearningResource.objects.all()
    
    return render(request, 'dashboard.html', {
        'username': request.user.username,
        'modules': modules,
        'learning_resources': learning_resources
    })

@login_required
def get_user_progress(request):
    user = request.user
    try:
        progress = UserProgress.objects.get(user=user)
        return JsonResponse({'progress_percentage': progress.progress_percentage}, status=200)
    except UserProgress.DoesNotExist:
        return JsonResponse({'progress_percentage': 0}, status=200)
    
@login_required
def update_profile_picture(request):
    """ View to update the user's profile picture """
    try:
        profile = request.user.userprofile
    except ObjectDoesNotExist:
        profile = UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile picture updated successfully!")
            return redirect('dashboard')  # Redirect to your desired page after success
    else:
        form = ProfileEditForm(instance=profile)

    return render(request, 'profile_edit.html', {'form': form})

@login_required
def module_lessons_view(request, module_id):
    try:
        module = Module.objects.get(id=module_id)
        lessons = module.lessons.all()
        return render(request, 'module_lessons.html', {'module': module, 'lessons': lessons})
    except Module.DoesNotExist:
        return HttpResponseNotFound("Module not found")

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page

def lesson_detail_view(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    # Get the next lesson in the same module (by week/day order)
    next_lesson = Lesson.objects.filter(
        module=lesson.module,
        week=lesson.week,
        day=lesson.day + 1
    ).first()

    # If no lesson for the next day exists, try to get the first day of the next week
    if not next_lesson:
        next_lesson = Lesson.objects.filter(
            module=lesson.module,
            week=lesson.week + 1,
            day=1
        ).first()

    context = {
        'lesson': lesson,
        'next_lesson': next_lesson,
    }
    return render(request, 'lesson_detail.html', {'lesson': lesson})
