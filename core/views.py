from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.http import JsonResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from rest_framework import generics
from .models import UserProfile, Course, Module, Lesson, Progress, ModuleProgress, Certificate, Quiz, Question, Assignment, LearningResource
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
from django.utils import timezone
from .forms import LoginForm, SignUpForm, ProfileEditForm  # Import forms
import os
import json
from django.conf import settings

def login_signup(request):
    # Handle API requests (from your JavaScript)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            data = json.loads(request.body)
            
            # Handle login API
            if request.path.endswith('/api/login/'):
                user = authenticate(
                    request,
                    username=data.get('username'),
                    password=data.get('password')
                )
                if user is not None:
                    login(request, user)
                    return JsonResponse({
                        'success': True,
                        'redirect': '/dashboard/'  # Update with your dashboard URL
                    })
                return JsonResponse({'error': 'Invalid username or password'}, status=400)
            
            # Handle signup API
            elif request.path.endswith('/api/signup/'):
                User = get_user_model()
                
                # Check if username or email exists
                if User.objects.filter(username=data.get('username')).exists():
                    return JsonResponse({'error': 'Username already exists'}, status=400)
                if User.objects.filter(email=data.get('email')).exists():
                    return JsonResponse({'error': 'Email already exists'}, status=400)
                
                # Create user
                user = User.objects.create_user(
                    username=data['username'],
                    email=data['email'],
                    password=data['password1'],
                    first_name=data['first_name'],
                    last_name=data['last_name']
                )
                
                # Auto-login after registration
                auth_user = authenticate(
                    request,
                    username=data['username'],
                    password=data['password1']
                )
                if auth_user:
                    login(request, auth_user)
                
                return JsonResponse({
                    'success': True,
                    'message': 'Registration successful!',
                    'redirect': '/dashboard/'  # Update with your dashboard URL
                })
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    # Handle regular form submissions (fallback)
    login_form = LoginForm(request.POST or None)
    signup_form = SignUpForm(request.POST or None)
    
    # Regular form processing
    if request.method == 'POST':
        if 'login_form' in request.POST and login_form.is_valid():
            user = authenticate(
                request,
                username=login_form.cleaned_data['username'],
                password=login_form.cleaned_data['password']
            )
            if user:
                login(request, user)
                return redirect('home')
        
        elif 'signup_form' in request.POST and signup_form.is_valid():
            User = get_user_model()
            user = User.objects.create_user(
                username=signup_form.cleaned_data['username'],
                email=signup_form.cleaned_data['email'],
                password=signup_form.cleaned_data['password1'],
                first_name=signup_form.cleaned_data['first_name'],
                last_name=signup_form.cleaned_data['last_name']
            )
            # Auto-login
            auth_user = authenticate(
                request,
                username=signup_form.cleaned_data['username'],
                password=signup_form.cleaned_data['password1']
            )
            if auth_user:
                login(request, auth_user)
            return redirect('home')

    return render(request, 'login_signup.html', {
        'login_form': login_form,
        'signup_form': signup_form
    })

@login_required
def dashboard_view(request):
    modules = Module.objects.all()
    learning_resources = LearningResource.objects.all()
    return render(request, 'dashboard.html', {'username': request.user.username, 'modules': modules, 'learning_resources': learning_resources})

@login_required
def update_profile_picture(request):
    form = None
    
    if request.method == 'POST':
        # Check if user has a related UserProfile
        if hasattr(request.user, 'user_profile'):  
            user_profile = request.user.user_profile  # Access the related UserProfile

            # Use the form to handle profile picture update
            form = ProfileEditForm(request.POST, request.FILES, instance=user_profile)

            if form.is_valid():
                form.save()  # Save the form (i.e., update the profile picture)
                messages.success(request, "Profile picture updated successfully!")
                return redirect('dashboard')  # Redirect to the profile page (adjust URL as needed)
            else:
                messages.error(request, "Please upload a valid profile picture.")
        else:
            messages.error(request, "User profile does not exist.")
    else:
        # If it's a GET request, instantiate the form with the user's current profile
        if hasattr(request.user, 'user_profile'):
            form = ProfileEditForm(instance=request.user.user_profile)
        else:
            messages.error(request, "User Profile does not exist.")
        
    return render(request, 'profile_edit.html', {'form': form})

@login_required
def module_lessons_view(request, module_id):
    try:
        module = Module.objects.get(id=module_id)
        lessons = module.lessons.order_by('week', 'day')
        
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
    
    # Certificate eligibility
    certificate_eligible = progress_percentage == 100

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

    # Check if there's an existing assignment submission for the user
    assignment_submitted = None
    try:
        assignment_submitted = Assignment.objects.get(lesson=lesson, submitted_by=request.user)
    except Assignment.DoesNotExist:
        assignment_submitted = None

    # Check if the current lesson is Day 5
    is_day_5 = lesson.day == 5

    context = {
        'lesson': lesson,
        'next_lesson': next_lesson,
        'progress_percentage': progress_percentage,
        'lesson_completed': lesson_completed,
        'certificate_eligible': certificate_eligible,
        'assignment_submitted': assignment_submitted,
        'is_day_5': is_day_5,  # Pass the Day 5 check to the template
    }
    
    return render(request, 'lesson_detail.html', context)

@login_required
def submit_assignment(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)

    # Only allow submission if it's Day 5
    if lesson.day == 5:
        if request.method == 'POST':
            github_link = request.POST['github_link']
            # Ensure the user hasn't already submitted for this lesson
            if Assignment.objects.filter(lesson=lesson, submitted_by=request.user).exists():
                return redirect('core:lesson_detail', lesson_id=lesson.id)  # Redirect if already submitted

            # Create the new assignment submission
            assignment = Assignment.objects.create(
                lesson=lesson,  # Properly set the lesson field
                submitted_by=request.user,
                github_link=github_link,
                submitted_at=timezone.now(),  # Automatically set the submission time
            )
            return redirect('core:lesson_detail', lesson_id=lesson.id)  # Redirect after submission

    # Redirect if it's not Day 5
    return redirect('core:lesson_detail', lesson_id=lesson.id)  # Redirect to lesson detail if not Day 5


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
    course = get_object_or_404(Course, id=course_id)
    user = get_object_or_404(User, id=user_id)

    total_lessons = Lesson.objects.filter(module__course=course).count()
    completed_lessons = Progress.objects.filter(user=user, lesson__module__course=course, completed=True).count()

    if total_lessons == 0 or completed_lessons < total_lessons:
        return JsonResponse({"status": "error", "message": "You need to complete all lessons to generate the certificate."}, status=400)

    certificate, created = Certificate.objects.get_or_create(user=user, course=course)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="certificate.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Load paths
    logo_path = os.path.join(settings.BASE_DIR, 'static', 'core', 'images', 'logo.png')
    bg_path = os.path.join(settings.BASE_DIR, 'static', 'core', 'images', 'certificate_bg.png')

    # Draw background image
    if os.path.exists(bg_path):
        p.drawImage(bg_path, 0, 0, width=width, height=height)

    # Draw logo
    if os.path.exists(logo_path):
        p.drawImage(logo_path, width/2 - 50, 720, width=100, height=50)

    # Title
    p.setFont("Helvetica-Bold", 28)
    p.drawCentredString(width / 2, 650, "Certificate of Completion")

    # Recipient info
    p.setFont("Helvetica", 16)
    p.drawCentredString(width / 2, 600, f"This certifies that {user.username}")
    p.drawCentredString(width / 2, 575, f"has successfully completed the course:")
    p.setFont("Helvetica-Bold", 18)
    p.drawCentredString(width / 2, 550, f"'{course.title}'")
    p.setFont("Helvetica", 14)
    p.drawCentredString(width / 2, 520, f"Date: {certificate.date_generated.strftime('%B %d, %Y')}")

    p.showPage()
    p.save()

    return response

class AssignmentListCreate(generics.ListCreateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

class AssignmentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
