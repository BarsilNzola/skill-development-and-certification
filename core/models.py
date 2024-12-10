from django.db import models
from django.conf import settings


# Course Model
class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title


# Module Model
class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='modules/', blank=True, null=True)

    def __str__(self):
        return f"{self.course.title} - {self.title}"


# Lesson Model
class Lesson(models.Model):
    module = models.ForeignKey(Module, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    week = models.IntegerField(default=1)  # Week number
    day = models.IntegerField(default=1)   # Day of the week
    
    def __str__(self):
        return f"{self.module.title} - {self.title}"


class Progress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title} - {'Completed' if self.completed else 'Not Completed'}"

class ModuleProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    completed_lessons = models.IntegerField(default=0)
    total_lessons = models.IntegerField(default=0)  # You can set this when the module is created.
    progress_percentage = models.FloatField(default=0.0)

    def save(self, *args, **kwargs):
        # Dynamically set total_lessons to the number of lessons in the associated module
        if not self.total_lessons:
            self.total_lessons = self.module.lessons.count()  # Assuming `lessons` is a related field on `Module`
        
        # Call the original save method
        super().save(*args, **kwargs)

    def update_progress(self):
        # Update the number of completed lessons
        self.completed_lessons = Progress.objects.filter(
            user=self.user, lesson__module=self.module, completed=True
        ).count()
        print(f"Completed Lessons: {self.completed_lessons}")  # Debugging
        
        # Prevent division by zero
        if self.total_lessons > 0:
            self.progress_percentage = (self.completed_lessons / self.total_lessons) * 100
        else:
            self.progress_percentage = 0.0
        
        # Save the progress
        self.save()

    def __str__(self):
        return f"{self.user.username} - {self.module.title} - {self.progress_percentage:.2f}%"




# Quiz Model
class Quiz(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='quizzes', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.lesson.title} - {self.title}"


# Question Model
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    correct_answer = models.CharField(max_length=200)
    incorrect_answers = models.JSONField()  # A list of incorrect answers

    def __str__(self):
        return f"{self.quiz.title} - {self.text}"


# User Profile Model
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_profile')
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username


# User Course Enrollment Model
class UserCourseEnrollment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"


# Learning Resource Model (for external links)
class LearningResource(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='learning_resources/', blank=True, null=True) 

    def __str__(self):
        return self.title

class Assignment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateTimeField()
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    module = models.ForeignKey('Module', on_delete=models.CASCADE)
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE, null=False)
    
    # Add fields for submission tracking
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)  # Track the user who submitted
    github_link = models.URLField(null=True, blank=True)  # URL for the GitHub repository link
    submitted_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)  # Track the submission date
    
    def __str__(self):
        return self.title
    

class Certificate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey("Course", on_delete=models.CASCADE)
    date_generated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Certificate for {self.user.username} - {self.course.title}"
