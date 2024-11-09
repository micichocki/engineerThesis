from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Avg


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=100, blank=True, null=True, help_text="First name of the user")
    last_name = models.CharField(max_length=100, blank=True, null=True, help_text="Last name of the user")
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Tutor(CustomUser):
    subjects = models.ManyToManyField("Subject", related_name="tutors", blank=True)

    @property
    def average_rating(self) -> float:
        avg_rating = self.lessons.aggregate(Avg('rating'))['rating__avg']
        return avg_rating if avg_rating is not None else 0.0

    def __str__(self):
        return f"{self.username} - Tutor"


    class Meta:
        verbose_name = 'Tutor'
        verbose_name_plural = 'Tutors'



class Student(CustomUser):
    bio = models.TextField(null=True, blank=True, help_text="A brief description of the student")

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name} - Student"
        return f"{self.username} - Student"

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'


class Parent(CustomUser):
    children = models.ManyToManyField(Student, related_name="parents", blank=True)

    def __str__(self):
        return f"{self.username} - Parent"

    class Meta:
        verbose_name = 'Parent'
        verbose_name_plural = 'Parents'


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

    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, null=True, blank=True,
                              related_name="available_hours_tutor")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True,
                                related_name="available_hours_student")

    day_of_week = models.CharField(max_length=9, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        if self.tutor:
            return f"Tutor {self.tutor.username} - {self.day_of_week}: {self.start_time} to {self.end_time}"
        else:
            return f"Student {self.student.username} - {self.day_of_week}: {self.start_time} to {self.end_time}"

    class Meta:
        unique_together = ('tutor', 'student', 'day_of_week', 'start_time', 'end_time')


class Subject(models.Model):
    name = models.CharField(max_length=255, unique=True, help_text="The name of the subject")

    def __str__(self):
        return self.name


class Lesson(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name="lessons")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="lessons")
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name="lessons")
    start_time = models.DateTimeField(help_text="Start time of the lesson")
    end_time = models.DateTimeField(help_text="End time of the lesson")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp of when the lesson was created")
    google_meet_url = models.URLField(null=True, blank=True, help_text="URL to the Google Meet meeting")

    rating = models.DecimalField(
        max_digits=2, decimal_places=1, null=True, blank=True, help_text="Rating for the lesson (1-5)"
    )
    feedback = models.TextField(null=True, blank=True, help_text="Feedback about the lesson")

    def __str__(self):
        return f"Lesson {self.subject} - {self.student.username} with {self.tutor.username} on {self.start_time}"

    class Meta:
        unique_together = ('tutor', 'student', 'start_time')

class BankAccount(models.Model):
    tutor = models.OneToOneField(Tutor, on_delete=models.CASCADE, related_name="bank_account")
    account_number = models.CharField(max_length=26, help_text="The tutor's bank account number")
    bank_name = models.CharField(max_length=100, help_text="Name of the bank")

    def __str__(self):
        return f"Bank account for {self.tutor.username} ({self.bank_name})"


class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="payments")
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Amount paid for the lesson")
    payment_date = models.DateTimeField(auto_now_add=True, help_text="Timestamp of the payment")
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending',
                              help_text="Payment status")
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, blank=True, related_name="payments")

    def __str__(self):
        return f"Payment of {self.amount} by {self.student.username} to {self.tutor.username} for {self.lesson.subject.name}"

    class Meta:
        unique_together = ('student', 'lesson')


class LessonPayment(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="lesson_payments")
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name="lesson_payments")
    payment_status = models.CharField(max_length=20, choices=Payment.PAYMENT_STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Payment for Lesson {self.lesson.id} - {self.payment.status}"






