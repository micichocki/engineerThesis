from rest_framework import serializers

from .choices import ROLE_CHOICES
from .exceptions.exceptions import DuplicateKeyException
from .models import TutorProfile, StudentProfile, ParentProfile, Subject, Lesson, BankAccount, Payment, LessonPayment, \
    User, Role


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name']

class TutorProfileSerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(many=True)
    average_rating = serializers.ReadOnlyField()

    class Meta:
        model = TutorProfile
        fields = ['id', 'username', 'first_name', 'last_name', 'bio', 'subjects', 'average_rating']

class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
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

class PaymentSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField()
    tutor = serializers.StringRelatedField()
    lesson = serializers.StringRelatedField()

    class Meta:
        model = Payment
        fields = ['id', 'student', 'tutor', 'amount', 'payment_date', 'status', 'lesson']

class LessonPaymentSerializer(serializers.ModelSerializer):
    lesson = serializers.StringRelatedField()
    payment = PaymentSerializer()

    class Meta:
        model = LessonPayment
        fields = ['id', 'lesson', 'payment', 'payment_status']

class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField(write_only=True)
    roles = serializers.ChoiceField(choices=ROLE_CHOICES, write_only=True)

    class Meta:
        fields = ('username', 'first_name', 'last_name', 'password', 'roles')
        write_only_fields = ('password', 'account_type')
        read_only_fields = ('id',)

    def create(self, validated_data):
        if User.objects.filter(username=validated_data['username']).exists():
            raise DuplicateKeyException('A user with this email already exists')
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        role_ids = Role.get_role_ids([validated_data['roles']])

        user.roles.add(role_ids[0])
        user.set_password(validated_data['password'])
        user.save()
        return user

class ParentProfileSerializer(serializers.ModelSerializer):
    children = UserSerializer(many=True, read_only=True)

    class Meta:
        model = ParentProfile
        fields = ['id', 'username', 'first_name', 'last_name', 'children']

class BankAccountSerializer(serializers.ModelSerializer):
    tutor = UserSerializer()

    class Meta:
        model = BankAccount
        fields = ['id', 'tutor', 'account_number', 'bank_name']