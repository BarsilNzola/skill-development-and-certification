from django.shortcuts import render
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from rest_framework import generics
from .models import Course, Module, Lesson, Progress, Quiz, Question
from .serializers import CourseSerializer, ModuleSerializer, LessonSerializer, ProgressSerializer, QuizSerializer, QuestionSerializer

def home(request): 
    return render(request, 'index.html')

def login_signup(request):
    return render(request, 'login_signup.html')

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



# Create your views here.
