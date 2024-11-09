from django.db import models

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

# Create your models here.
