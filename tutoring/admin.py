from django.contrib import admin
from .models import (
    User,
    Role,
    TutorProfile,
    StudentProfile,
    ParentProfile,
    WorkingExperience,
    EducationLevel,
    AvailableHour,
    Subject,
    Lesson,
    LessonDocument,
    BankAccount,
    LessonPayment,
    TutorSubjectPrice,
    Message,
    GoogleCredentials,
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'date_of_birth', 'phone_number', 'city', 'avatar', 'get_roles')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('roles',)

    def get_roles(self, obj):
        return ", ".join([role.name for role in obj.roles.all()])
    get_roles.short_description = 'Roles'


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(TutorProfile)
class TutorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'is_remote', 'average_rating')
    search_fields = ('user__username', 'bio')
    list_filter = ('is_remote',)
    filter_horizontal = ('available_hours', 'working_experience')


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'education_level', 'goal')
    search_fields = ('user__username', 'goal')
    list_filter = ('education_level',)
    filter_horizontal = ('available_hours',)


@admin.register(ParentProfile)
class ParentProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)
    filter_horizontal = ('children',)


@admin.register(WorkingExperience)
class WorkingExperienceAdmin(admin.ModelAdmin):
    list_display = ('position', 'start_date', 'end_date')
    search_fields = ('position',)
    list_filter = ('start_date', 'end_date')


@admin.register(EducationLevel)
class EducationLevelAdmin(admin.ModelAdmin):
    list_display = ('level',)
    search_fields = ('level',)


@admin.register(AvailableHour)
class AvailableHourAdmin(admin.ModelAdmin):
    list_display = ('day_of_week', 'start_time', 'end_time')
    list_filter = ('day_of_week',)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('tutor', 'student', 'subject', 'start_time', 'end_time', 'rating', 'price_per_hour', 'is_remote', 'is_accepted')
    list_filter = ('tutor', 'student', 'subject', 'is_remote', 'is_accepted')
    search_fields = ('tutor__user__username', 'student__user__username', 'subject__name')
    filter_horizontal = ('documents',)


@admin.register(LessonDocument)
class LessonDocumentAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'document', 'uploaded_at')
    search_fields = ('lesson__id',)


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'account_number', 'bank_name')
    search_fields = ('user__username', 'account_number')


@admin.register(LessonPayment)
class LessonPaymentAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'amount', 'payment_status', 'created_at')
    search_fields = ('lesson__id', 'payment_status')


@admin.register(TutorSubjectPrice)
class TutorSubjectPriceAdmin(admin.ModelAdmin):
    list_display = ('tutor', 'subject', 'price_min', 'price_max')
    search_fields = ('tutor__user__username', 'subject__name')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'content', 'timestamp')
    search_fields = ('sender__username', 'recipient__username', 'content')


@admin.register(GoogleCredentials)
class GoogleCredentialsAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'refresh_token')
    search_fields = ('user__username',)
