from rest_framework import serializers

from tutoring.models import TutorProfile, StudentProfile, ParentProfile, User, Role, Lesson, Subject
from tutoring.serializers.serializers import SubjectSerializer, AvailableHourSerializer, EducationLevelSerializer, \
    WorkingExperienceSerializer, TutorSubjectPriceSerializer


class TutorProfileSerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(many=True, required=False)
    average_rating = serializers.ReadOnlyField()
    available_hours = AvailableHourSerializer(many=True, required=False)
    working_experience = WorkingExperienceSerializer(many=True, required=False, default=[])
    user_full_name = serializers.SerializerMethodField()
    subject_prices = TutorSubjectPriceSerializer(many=True, required=False)

    def get_user_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    class Meta:
        model = TutorProfile
        fields = ['id', 'bio', 'subjects', 'average_rating', 'working_experience', 'available_hours', 'user_full_name', 'subject_prices', 'is_remote']

class StudentProfileSerializer(serializers.ModelSerializer):
    available_hours = AvailableHourSerializer(many=True,required=False)
    education_level = EducationLevelSerializer(required=False)
    user_full_name = serializers.SerializerMethodField()

    def get_user_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    class Meta:
        model = StudentProfile
        fields = ['id', 'bio', 'tasks_description', 'goal', 'tasks_description', 'education_level', 'available_hours', 'user_full_name']

class ParentProfileSerializer(serializers.ModelSerializer):
    children = StudentProfileSerializer(many=True, read_only=True)

    class Meta:
        model = ParentProfile
        fields = ['id', 'children']


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Role
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    tutor_profile = TutorProfileSerializer(required=False)
    student_profile = StudentProfileSerializer(required=False)
    parent_profile = ParentProfileSerializer(required=False)
    roles = RoleSerializer(many=True)

    def get_queryset(self):
        return User.objects.filter(is_active=True, id=self.context['request'].user.id)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if hasattr(instance, 'tutorprofile'):
            representation['tutor_profile'] = TutorProfileSerializer(instance.tutorprofile).data
        if hasattr(instance, 'studentprofile'):
            representation['student_profile'] = StudentProfileSerializer(instance.studentprofile).data
        if hasattr(instance, 'parentprofile'):
            representation['parent_profile'] = ParentProfileSerializer(instance.parentprofile).data

        return representation

    class Meta:
        model = User
        fields = ['id', 'username','email', 'first_name', 'last_name', 'roles' ,'date_of_birth', 'phone_number', 'tutor_profile', 'student_profile', 'parent_profile', 'city', 'avatar']


class LessonSerializer(serializers.ModelSerializer):
    tutor = TutorProfileSerializer()
    student = StudentProfileSerializer()
    subject = SubjectSerializer()

    class Meta:
        model = Lesson
        fields = [
            'id', 'tutor', 'student', 'subject', 'start_time', 'end_time',
            'created_at', 'google_meet_url', 'rating', 'feedback','price_per_hour', 'is_remote', 'accepted_by','is_accepted','description'
        ]
        read_only_fields = ('id', 'created_at',)

class LessonCreateSerializer(serializers.ModelSerializer):
    tutor = serializers.PrimaryKeyRelatedField(queryset=TutorProfile.objects.all())
    student = serializers.PrimaryKeyRelatedField(queryset=StudentProfile.objects.all())
    subject = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all())

    class Meta:
        model = Lesson
        fields = [
            'id', 'tutor', 'student', 'subject', 'start_time', 'end_time',
            'price_per_hour', 'is_remote','accepted_by','description'
        ]


class LessonAcceptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['is_accepted']
        read_only_fields = ['is_accepted']

    def update(self, instance, validated_data):
        instance.is_accepted = True
        instance.save()
        return instance
