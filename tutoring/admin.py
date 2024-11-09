from django.contrib import admin
from .models import CustomUser, Tutor, Student, Parent, AvailableHour, Subject, Lesson, BankAccount, Payment, LessonPayment

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'date_of_birth', 'phone_number')
    search_fields = ('username', 'email', 'first_name', 'last_name')


@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'average_rating')
    search_fields = ('username', 'first_name', 'last_name')
    filter_horizontal = ('subjects',)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'bio')
    search_fields = ('username', 'first_name', 'last_name')


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name')
    search_fields = ('username', 'first_name', 'last_name')


@admin.register(AvailableHour)
class AvailableHourAdmin(admin.ModelAdmin):
    list_display = ('tutor', 'student', 'day_of_week', 'start_time', 'end_time')
    list_filter = ('tutor', 'student', 'day_of_week')


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('tutor', 'student', 'subject', 'start_time', 'end_time', 'rating')
    list_filter = ('tutor', 'student', 'subject')
    search_fields = ('tutor__username', 'student__username', 'subject__name')


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('tutor', 'account_number', 'bank_name')
    search_fields = ('tutor__username', 'account_number')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'tutor', 'amount', 'payment_date', 'status', 'lesson')
    list_filter = ('status', 'tutor', 'student')
    search_fields = ('student__username', 'tutor__username', 'lesson__subject__name')


@admin.register(LessonPayment)
class LessonPaymentAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'payment', 'payment_status')
    search_fields = ('lesson__id', 'payment__status')

