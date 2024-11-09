from django.shortcuts import render
from rest_framework import generics
from .models import Course, Module, Lesson
from .serializers import CourseSerializer, ModuleSerializer, LessonSerializer

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


# Create your views here.
