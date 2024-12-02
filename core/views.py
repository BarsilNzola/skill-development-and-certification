from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from rest_framework import generics
from .models import Course, Module, Lesson, Progress, Quiz, Question, Assignment, LearningResource
from .serializers import (
    CourseSerializer, ModuleSerializer, LessonSerializer, ProgressSerializer,
    QuizSerializer, QuestionSerializer, AssignmentSerializer
)
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile picture updated successfully!")
            return redirect('dashboard')  # Redirect to your desired page after success
    else:
        form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'users/profile_edit.html', {'form': form})

@login_required
def module_lessons_view(request, module_id):
    try:
        module = Module.objects.get(id=module_id)
        lessons = module.lessons.all()
        return render(request, 'module_lessons.html', {'module': module, 'lessons': lessons})
    except Module.DoesNotExist:
        return HttpResponseNotFound("Module not found")

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
