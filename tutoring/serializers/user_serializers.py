from rest_framework import serializers

from engineerThesis.serializers import RegisterSerializer
from tutoring.models import TutorProfile, StudentProfile, ParentProfile
from tutoring.serializers.serializers import SubjectSerializer


class TutorProfileSerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(many=True)
    average_rating = serializers.ReadOnlyField()

    class Meta:
        model = TutorProfile
        fields = ['id', 'bio', 'subjects', 'average_rating']

class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ['id',  'bio']

class ParentProfileSerializer(serializers.ModelSerializer):
    children = RegisterSerializer(many=True, read_only=True)

    class Meta:
        model = ParentProfile
        fields = ['id', 'children']
