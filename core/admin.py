from django.contrib import admin
from .models import Course, Module, Lesson, Progress, Quiz, Question, UserProfile, UserCourseEnrollment, LearningResource

admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Lesson)
admin.site.register(Progress)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(UserProfile)
admin.site.register(UserCourseEnrollment)
admin.site.register(LearningResource)

# Register your models here.
