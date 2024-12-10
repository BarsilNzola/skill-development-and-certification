from django.contrib import admin
from .models import Course, Module, Lesson, Progress, ModuleProgress, Quiz, Question, UserProfile, UserCourseEnrollment, LearningResource, Assignment, Certificate


# Course Admin
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')  # Fields to display in the list view
    search_fields = ('title', 'description')  # Allow search by title or description
    ordering = ('title',)  # Ordering by course title


# Module Admin
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('course', 'title', 'description', 'image')
    list_filter = ('course',)  # Filter by course
    search_fields = ('title', 'description')  # Allow searching by title/description


# Lesson Admin
class LessonAdmin(admin.ModelAdmin):
    list_display = ('module', 'title', 'week', 'day', 'content')
    list_filter = ('module', 'week')  # Filter by module or week
    search_fields = ('title', 'content')  # Searching by lesson title or content


# Progress Admin
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'completed', 'timestamp')
    list_filter = ('user', 'lesson')  # Filter by user or lesson
    search_fields = ('user__username', 'lesson__title')  # Search by username or lesson title


# ModuleProgress Admin
class ModuleProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'module', 'completed_lessons', 'total_lessons', 'progress_percentage')
    list_filter = ('user', 'module')  # Filter by user or module
    search_fields = ('user__username', 'module__title')  # Search by user or module title


# Quiz Admin
class QuizAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'title')
    list_filter = ('lesson',)  # Filter by lesson
    search_fields = ('title',)  # Search by title


# Question Admin
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'text', 'correct_answer')
    list_filter = ('quiz',)  # Filter by quiz
    search_fields = ('text', 'correct_answer')  # Search by question text or answer


# UserProfile Admin
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_picture', 'bio')
    search_fields = ('user__username', 'bio')  # Search by username or bio


# UserCourseEnrollment Admin
class UserCourseEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'enrolled_on')
    list_filter = ('user', 'course')  # Filter by user or course
    search_fields = ('user__username', 'course__title')  # Search by user or course title


# LearningResource Admin
class LearningResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'description', 'image')
    search_fields = ('title', 'url', 'description')  # Search by title, URL, or description


# Assignment Admin
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'module', 'lesson', 'due_date', 'submitted_by', 'submitted_at')
    list_filter = ('course', 'module', 'lesson', 'submitted_by')  # Filter by various fields
    search_fields = ('title', 'course__title', 'module__title', 'lesson__title')  # Search by course, module, or lesson title


# Certificate Admin
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'date_generated')
    list_filter = ('user', 'course')  # Filter by user or course
    search_fields = ('user__username', 'course__title')  # Search by user or course title


# Register all models with the admin site
admin.site.register(Course, CourseAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Progress, ProgressAdmin)
admin.site.register(ModuleProgress, ModuleProgressAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserCourseEnrollment, UserCourseEnrollmentAdmin)
admin.site.register(LearningResource, LearningResourceAdmin)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(Certificate, CertificateAdmin)
