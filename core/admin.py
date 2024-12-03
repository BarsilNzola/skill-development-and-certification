from django.contrib import admin
from .models import Course, Module, Lesson, Progress, Quiz, Question, UserProfile, Certificate, UserCourseEnrollment, LearningResource

admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Lesson)
admin.site.register(Progress)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(UserProfile)
admin.site.register(UserCourseEnrollment)
admin.site.register(LearningResource)

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'date_generated')
    list_filter = ('date_generated',)

# Register your models here.
