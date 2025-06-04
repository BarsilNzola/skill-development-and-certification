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
    mentor = models.ForeignKey(  # Add this field
        'Mentor', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='mentees'
    )
    
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
    # Assignment Status Choices
    STATUS_DRAFT = 'draft'
    STATUS_SUBMITTED = 'submitted'
    STATUS_UNDER_REVIEW = 'under_review'
    STATUS_NEEDS_REVISION = 'needs_revision'
    STATUS_COMPLETED = 'completed'
    
    STATUS_CHOICES = [
        (STATUS_DRAFT, 'Draft (Not Submitted)'),
        (STATUS_SUBMITTED, 'Submitted for Review'),
        (STATUS_UNDER_REVIEW, 'Under Review'),
        (STATUS_NEEDS_REVISION, 'Needs Revision'),
        (STATUS_COMPLETED, 'Completed'),
    ]

    # Assignment Core Fields
    title = models.CharField(max_length=255)
    due_date = models.DateTimeField()
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='assignments')
    module = models.ForeignKey('Module', on_delete=models.CASCADE, related_name='assignments')
    lesson = models.ForeignKey('Lesson', on_delete=models.SET_NULL, null=True, blank=True, related_name='assignments')
    
    # Submission Tracking
    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='submit_assignment'
    )
    submitted_at = models.DateTimeField(null=True, blank=True)
    github_repo = models.URLField(null=True, blank=True)
    live_demo = models.URLField(null=True, blank=True)
    attachment = models.FileField(upload_to='assignments/%Y/%m/%d/', null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_DRAFT
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-submitted_at']
        verbose_name = 'Student Assignment'
        verbose_name_plural = 'Student Assignments'
    
    def __str__(self):
        return f"{self.title} - {self.course.title}"
    
    @property
    def is_submitted(self):
        return self.status != self.STATUS_DRAFT

class Feedback(models.Model):
    # Feedback Rating Choices
    RATING_CHOICES = [
        (1, 'Needs Significant Improvement'),
        (2, 'Needs Some Improvement'),
        (3, 'Meets Expectations'),
        (4, 'Exceeds Expectations'),
        (5, 'Outstanding Work'),
    ]
    
    # Core Feedback Fields
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name='feedbacks'
    )
    mentor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='given_feedbacks',
        limit_choices_to={'groups__name': 'Mentors'}
    )
    comments = models.TextField()
    technical_score = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    creativity_score = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    completeness_score = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    is_published = models.BooleanField(default=False)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Mentor Feedback'
        verbose_name_plural = 'Mentor Feedbacks'
        unique_together = ('assignment', 'mentor')  # One feedback per mentor per assignment
    
    def __str__(self):
        return f"Feedback for {self.assignment.title} by {self.mentor.username}"
    
    @property
    def average_score(self):
        return round((self.technical_score + self.creativity_score + self.completeness_score) / 3, 1)
    
    @property
    def score_breakdown(self):
        return {
            'technical': self.get_technical_score_display(),
            'creativity': self.get_creativity_score_display(),
            'completeness': self.get_completeness_score_display(),
            'average': self.average_score
        }
    
class Mentor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    github_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    whatsapp_number = models.CharField(max_length=20, blank=True)  # format: +1234567890
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Mentor: {self.user.username}"  

class Certificate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey("Course", on_delete=models.CASCADE)
    date_generated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Certificate for {self.user.username} - {self.course.title}"
