from django.db import models
from django.conf import settings

class Course(models.Model): 
    title = models.CharField(max_length=200) 
    description = models.TextField()

class Module(models.Model): 
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE) 
    title = models.CharField(max_length=200)
    
class Lesson(models.Model): 
    module = models.ForeignKey(Module, related_name='lessons', on_delete=models.CASCADE) 
    title = models.CharField(max_length=200) 
    content = models.TextField()
    
class Progress(models.Model): 
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE) 
    completed = models.BooleanField(default=False) 
    timestamp = models.DateTimeField(auto_now_add=True)
    
class Quiz(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='quizzes', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    correct_answer = models.CharField(max_length=200)
    incorrect_answers = models.JSONField()  # A list of incorrect answers


# Create your models here.
