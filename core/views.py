from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.http import JsonResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from rest_framework import generics
from .models import UserProfile, Course, Module, Lesson, Progress, ModuleProgress, Quiz, Question, Assignment, LearningResource
from .serializers import (
    CourseSerializer, ModuleSerializer, LessonSerializer, ProgressSerializer,
    QuizSerializer, QuestionSerializer, AssignmentSerializer
)
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.html import mark_safe
from .forms import LoginForm, SignUpForm, ProfileEditForm  # Import forms

def login_signup(request):
    login_form = LoginForm()
    signup_form = SignUpForm()
    
    if request.method == 'POST':
        if 'signup_form' in request.POST:
            signup_form = SignUpForm(request.POST)
            if signup_form.is_valid():
                User = get_user_model()
                User.objects.create_user(
                    username=signup_form.cleaned_data.get('username'),
                    email=signup_form.cleaned_data.get('email'),
                    password=signup_form.cleaned_data.get('password')
                )
                return redirect('home')
        elif 'login_form' in request.POST:
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data.get('username')
                password = login_form.cleaned_data.get('password')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home')
    else:
        signup_form = SignUpForm()
        login_form = LoginForm()

    return render(request, 'login_signup.html', {'signup_form': signup_form, 'login_form': login_form})

def home(request): 
    return render(request, 'index.html')

@login_required
def dashboard_view(request):
    modules = Module.objects.all()
    learning_resources = LearningResource.objects.all()
    return render(request, 'dashboard.html', {'username': request.user.username, 'modules': modules, 'learning_resources': learning_resources})

@login_required
def update_profile_picture(request):
    """ View to update the user's profile picture """
    try:
        profile = request.user.user_profile
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
        
         # Group lessons by week
        lessons_by_week = {}
        for lesson in lessons:
        # Assuming you have a way to associate lessons with weeks
            week = lesson.week 
            day = lesson.day
            
            if week not in lessons_by_week:
                lessons_by_week[week] = {}
                
            # Add lesson to the correct day
            if day not in lessons_by_week[week]:
                lessons_by_week[week][day] = []
                
            lessons_by_week[week][day].append(lesson)
        
        return render(request, 'module_lessons.html', {'module': module, 'lessons_by_week': lessons_by_week})
    except Module.DoesNotExist:
        return HttpResponseNotFound("Module not found")
    
def lesson_detail_view(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    lesson.content = mark_safe(lesson.content)  # Mark content as safe in the view
    
    # Calculate the total number of lessons in the same module
    total_lessons = Lesson.objects.filter(module=lesson.module).count()
    
    # Calculate the number of completed lessons for the current user
    completed_lessons = Progress.objects.filter(user=request.user, lesson__module=lesson.module, completed=True).count()
    
    # Calculate the progress percentage
    if total_lessons > 0:
        progress_percentage = (completed_lessons / total_lessons) * 100
    else:
        progress_percentage = 0
    
    # Check if the current lesson is completed by the user
    lesson_completed = Progress.objects.filter(user=request.user, lesson=lesson, completed=True).exists()

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
        'progress_percentage': progress_percentage,
        'lesson_completed': lesson_completed,  # Pass completion status to the template
    }
    return render(request, 'lesson_detail.html', context)



@login_required
def logout_view(request):
    logout(request)
    return render(request, 'index.html')  # Redirect to home page


def mark_lesson_complete(request, lesson_id):
    if request.method == "POST":
        user = request.user
        lesson = get_object_or_404(Lesson, id=lesson_id)
        
        # Get or create progress record for the lesson
        progress, created = Progress.objects.get_or_create(user=user, lesson=lesson)
        progress.completed = True
        progress.save()
        
        print(f"Progress created: {created}, Progress status: {progress.completed}")  # Debugging

        # Optionally update the module progress
        # Ensure total_lessons is set for the first time when ModuleProgress is created
        module_progress, created = ModuleProgress.objects.get_or_create(
            user=user,
            module=lesson.module,
            defaults={'total_lessons': lesson.module.lessons.count(), 'completed_lessons': 0, 'progress_percentage': 0.0}
        )
        
        print(f"Before Update: {module_progress.completed_lessons}/{module_progress.total_lessons}")  # Debugging

        # Update the module progress
        module_progress.update_progress()  # This will update completed_lessons and progress_percentage
        
        print(f"After Update: {module_progress.completed_lessons}/{module_progress.total_lessons}")  # Debugging
        
        # Optionally, return the updated progress or success message
        return JsonResponse({"status": "success", "message": "Lesson marked as completed!"})

    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=400)



class CourseListCreate(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class CourseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class ModuleListCreate(generics.ListCreateAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer

class ModuleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer

class LessonListCreate(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class LessonDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class ProgressListCreate(generics.ListCreateAPIView):
    queryset = Progress.objects.all()
    serializer_class = ProgressSerializer

class ProgressDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Progress.objects.all()
    serializer_class = ProgressSerializer

class QuizListCreate(generics.ListCreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

class QuizDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

class QuestionListCreate(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

def generate_certificate(request, course_id, user_id):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="certificate.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    p.drawString(100, 750, "Certificate of Completion")
    p.drawString(100, 725, f"Course ID: {course_id}")
    p.drawString(100, 700, f"User ID: {user_id}")
    p.showPage()
    p.save()

    return response

class AssignmentListCreate(generics.ListCreateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

class AssignmentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
