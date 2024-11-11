from rest_framework import serializers

from engineerThesis.serializers import RegisterSerializer
from tutoring.models import TutorProfile, StudentProfile, ParentProfile, User, Role
from tutoring.serializers.serializers import SubjectSerializer, AvailableHourSerializer, EducationLevelSerializer, \
    WorkingExperienceSerializer


class TutorProfileSerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(many=True)
    average_rating = serializers.ReadOnlyField()
    available_hours = AvailableHourSerializer(many=True)
    working_experience = WorkingExperienceSerializer(many=True)

    class Meta:
        model = TutorProfile
        fields = ['id', 'bio', 'subjects', 'average_rating', 'working_experience']

class StudentProfileSerializer(serializers.ModelSerializer):
    available_hours = AvailableHourSerializer(many=True)
    education_level = EducationLevelSerializer(many=True)
    class Meta:
        model = StudentProfile
        fields = ['id', 'bio', 'goal', 'tasks_description', 'education_level', 'available_hours']

class ParentProfileSerializer(serializers.ModelSerializer):
    children = RegisterSerializer(many=True, read_only=True)

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
        return User.objects.filter(is_active=True)

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
        fields = ['id', 'username','email', 'first_name', 'last_name', 'roles' ,'date_of_birth', 'phone_number', 'tutor_profile', 'student_profile', 'parent_profile']

