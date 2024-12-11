from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from rest_framework import generics
from .models import CustomUser, UserProgress
from core.models import Module, LearningResource, Course, Lesson, Progress, ModuleProgress, Certificate, Assignment
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.html import mark_safe
from django.utils import timezone
from django.contrib.auth.models import User
from core.forms import LoginForm, SignUpForm, ProfileEditForm
from django.http import HttpResponse
from django.http import HttpResponseNotFound, HttpResponseRedirect
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

    return render(request, 'profile_edit.html', {'form': form}) # Render the correct template

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
    return render(request, 'index.html')  # Redirect to login page

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
        assignment_submitted = Assignment.objects.get(lesson=lesson, user=request.user)
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
def mark_lesson_complete(request, lesson_id):
    if request.method == "POST":
        user = request.user
        lesson = get_object_or_404(Lesson, id=lesson_id)

        # Get or create progress record for the lesson
        progress, created = Progress.objects.get_or_create(user=user, lesson=lesson)
        print(f"Progress created: {created}")
        progress.completed = True
        progress.save()
        
        print(f"Progress created: {created}, Progress status: {progress.completed}")  # Debugging

        # Optionally update module progress
        module_progress, created = ModuleProgress.objects.get_or_create(
            user=user,
            module=lesson.module,
            defaults={'total_lessons': lesson.module.lessons.count()}  # Set total lessons if not already set
        )

        print(f"Before Update: {module_progress.completed_lessons}/{module_progress.total_lessons}")  # Debugging

        # Update the module progress
        module_progress.update_progress()  # This will update completed_lessons and progress_percentage

        print(f"After Update: {module_progress.completed_lessons}/{module_progress.total_lessons}")  # Debugging

        # Return success message to the frontend
        return JsonResponse({"status": "success", "message": "Lesson marked as completed!"})

    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=400)

def generate_certificate(request, course_id, user_id):
    # Fetch the course and user
    course = get_object_or_404(Course, id=course_id)
    user = get_object_or_404(User, id=user_id)

    # Check if all lessons in the course are completed
    total_lessons = Lesson.objects.filter(module__course=course).count()
    completed_lessons = Progress.objects.filter(user=user, lesson__module__course=course, completed=True).count()

    if total_lessons == 0 or completed_lessons < total_lessons:
        return JsonResponse({"status": "error", "message": "You need to complete all lessons to generate the certificate."}, status=400)

    # Check if a certificate already exists
    certificate, created = Certificate.objects.get_or_create(user=user, course=course)

    # Generate the certificate PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="certificate.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    p.setFont("Helvetica-Bold", 24)
    p.drawString(200, 750, "Certificate of Completion")
    p.setFont("Helvetica", 14)
    p.drawString(100, 700, f"This certifies that {user.first_name} {user.last_name}")
    p.drawString(100, 675, f"has successfully completed the course '{course.title}'")
    p.drawString(100, 650, f"on {certificate.date_generated.strftime('%B %d, %Y')}")
    p.showPage()
    p.save()

    return response