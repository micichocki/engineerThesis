from django.contrib import admin
from .models import User, AvailableHour, Subject, Lesson, BankAccount, Payment, LessonPayment, EducationLevel


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'date_of_birth', 'phone_number', 'get_tutor_profile', 'get_student_profile', 'get_parent_profile')
    search_fields = ('username', 'email', 'first_name', 'last_name')

    def get_tutor_profile(self, obj):
        return obj.tutorprofile if hasattr(obj, 'tutorprofile') else None
    get_tutor_profile.short_description = 'Tutor Profile'

    def get_student_profile(self, obj):
        return obj.studentprofile if hasattr(obj, 'studentprofile') else None
    get_student_profile.short_description = 'Student Profile'

    def get_parent_profile(self, obj):
        return obj.parentprofile if hasattr(obj, 'parentprofile') else None
    get_parent_profile.short_description = 'Parent Profile'


@admin.register(AvailableHour)
class AvailableHourAdmin(admin.ModelAdmin):
    list_display = ('day_of_week', 'start_time', 'end_time')
    list_filter = ('day_of_week',)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(EducationLevel)
class EducationalLevelAdmin(admin.ModelAdmin):
    list_display = ('level',)
    search_fields = ('level',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('tutor', 'student', 'subject', 'start_time', 'end_time', 'rating')
    list_filter = ('tutor', 'student', 'subject')
    search_fields = ('tutor__username', 'student__username', 'subject__name')


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'account_number', 'bank_name')
    search_fields = ('user__username', 'account_number')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'tutor', 'amount', 'payment_date', 'status', 'lesson')
    list_filter = ('status', 'tutor', 'student')
    search_fields = ('student__username', 'tutor__username', 'lesson__subject__name')


@admin.register(LessonPayment)
class LessonPaymentAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'payment', 'payment_status')
    search_fields = ('lesson__id', 'payment__status')

