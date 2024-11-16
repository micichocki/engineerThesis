from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Avg
from engineerThesis import settings
from tutoring.choices import ROLE_CHOICES

class User(AbstractUser):
    first_name = models.CharField(max_length=100, help_text="First name of the user")
    last_name = models.CharField(max_length=100, help_text="Last name of the user")
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    roles = models.ManyToManyField("Role", related_name="users")
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Role(models.Model):
    name = models.CharField(max_length=20, choices=ROLE_CHOICES, unique=True)

    def __str__(self):
        return self.name

    @classmethod
    def get_role_ids(cls, role_names: list[str]) -> list[int]:
        return [cls.objects.get(name=role_name).id for role_name in role_names]


class TutorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subjects = models.ManyToManyField("Subject", related_name="tutors", blank=True)
    bio = models.TextField(null=True, blank=True)
    available_hours = models.ManyToManyField("AvailableHour", related_name="tutors", blank=True)
    working_experience = models.ManyToManyField("WorkingExperience", related_name="tutors", blank=True)

    @property
    def average_rating(self) -> float:
        lessons = Lesson.objects.filter(tutor=self)
        avg_rating = lessons.aggregate(Avg('rating'))['rating__avg']
        return avg_rating if avg_rating is not None else 0.0

class StudentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    education_level = models.ForeignKey("EducationLevel", on_delete=models.SET_NULL, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    goal = models.TextField(null=True, blank=True, help_text="What student wants to achieve")
    tasks_description = models.TextField(null=True, blank=True, help_text="Description of tasks that student needs help with")
    available_hours = models.ManyToManyField("AvailableHour", related_name="students", blank=True)

class ParentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    children = models.ManyToManyField("StudentProfile", related_name="parents", blank=True)

class WorkingExperience(models.Model):
    position = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

class EducationLevel(models.Model):
    LEVEL_CHOICES = [
        ('primary', 'Primary School'),
        ('secondary', 'Secondary School'),
        ('university', 'University'),
    ]

    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)

    def __str__(self):
        return self.get_level_display()

class AvailableHour(models.Model):
    DAYS_OF_WEEK = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]

    day_of_week = models.CharField(max_length=9, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()


    class Meta:
        unique_together = ('day_of_week', 'start_time', 'end_time')


class Subject(models.Model):
    name = models.CharField(max_length=100)


class Lesson(models.Model):
    tutor = models.ForeignKey(TutorProfile, related_name='lessons_as_tutor', on_delete=models.CASCADE)
    student = models.ForeignKey(StudentProfile, related_name='lessons_as_student', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    rating = models.IntegerField()
    google_meet_url = models.URLField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    feedback = models.TextField(blank=True, null=True)

class BankAccount(models.Model):
    user = models.ForeignKey(User, related_name='bank_accounts', on_delete=models.CASCADE)
    account_number = models.CharField(max_length=100)
    bank_name = models.CharField(max_length=100)

class Payment(models.Model):
    student = models.ForeignKey(User, related_name='payments_as_student', on_delete=models.CASCADE)
    tutor = models.ForeignKey(User, related_name='payments_as_tutor', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField()
    status = models.CharField(max_length=100)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

class LessonPayment(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    payment_status = models.CharField(max_length=100)



