from rest_framework import serializers

from tutoring.models import TutorProfile, StudentProfile, ParentProfile, User, Role
from tutoring.serializers.serializers import SubjectSerializer, AvailableHourSerializer, EducationLevelSerializer, \
    WorkingExperienceSerializer


class TutorProfileSerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(many=True,required=False)
    average_rating = serializers.ReadOnlyField()
    available_hours = AvailableHourSerializer(many=True,required=False)
    working_experience = WorkingExperienceSerializer(many=True, required=False, default=[])
    class Meta:
        model = TutorProfile
        fields = ['id', 'bio', 'subjects', 'average_rating', 'working_experience', 'available_hours']

class StudentProfileSerializer(serializers.ModelSerializer):
    available_hours = AvailableHourSerializer(many=True,required=False)
    education_level = EducationLevelSerializer(required=False)
    class Meta:
        model = StudentProfile
        fields = ['id', 'bio', 'tasks_description', 'goal', 'tasks_description', 'education_level', 'available_hours']

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
        fields = ['id', 'username','email', 'first_name', 'last_name', 'roles' ,'date_of_birth', 'phone_number', 'tutor_profile', 'student_profile', 'parent_profile']

