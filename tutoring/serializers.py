from rest_framework import serializers
from .models import Tutor, Subject, Student, Parent, Lesson, BankAccount, Payment, LessonPayment


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name']

class TutorSerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(many=True)
    average_rating = serializers.ReadOnlyField()

    class Meta:
        model = Tutor
        fields = ['id', 'username', 'first_name', 'last_name', 'bio', 'subjects', 'average_rating']

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'username', 'first_name', 'last_name', 'bio']

class LessonSerializer(serializers.ModelSerializer):
    tutor = serializers.StringRelatedField()
    student = serializers.StringRelatedField()
    subject = serializers.StringRelatedField()

    class Meta:
        model = Lesson
        fields = [
            'id', 'tutor', 'student', 'subject', 'start_time', 'end_time',
            'created_at', 'google_meet_url', 'rating', 'feedback'
        ]
        read_only_fields = ('created_at',)  # Prevent editing created_at field


class ParentSerializer(serializers.ModelSerializer):
    children = StudentSerializer(many=True, read_only=True)

    class Meta:
        model = Parent
        fields = ['id', 'username', 'first_name', 'last_name', 'children']

class BankAccountSerializer(serializers.ModelSerializer):
    tutor = TutorSerializer()

    class Meta:
        model = BankAccount
        fields = ['id', 'tutor', 'account_number', 'bank_name']


class PaymentSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField()
    tutor = serializers.StringRelatedField()
    lesson = serializers.StringRelatedField()

    class Meta:
        model = Payment
        fields = ['id', 'student', 'tutor', 'amount', 'payment_date', 'status', 'lesson']

class LessonPaymentSerializer(serializers.ModelSerializer):
    lesson = serializers.StringRelatedField()  # Display lesson details (e.g., subject name)
    payment = PaymentSerializer()  # Nest the PaymentSerializer to show payment details

    class Meta:
        model = LessonPayment
        fields = ['id', 'lesson', 'payment', 'payment_status']
