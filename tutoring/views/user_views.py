from rest_framework import generics

from tutoring.models import StudentProfile, TutorProfile, ParentProfile
from tutoring.serializers.user_serializers import StudentProfileSerializer, TutorProfileSerializer, \
    ParentProfileSerializer


class TutorProfileListView(generics.ListCreateAPIView):
    queryset = TutorProfile.objects.all()
    serializer_class = TutorProfileSerializer


class TutorProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TutorProfile.objects.all()
    serializer_class = TutorProfileSerializer


class StudentProfileListView(generics.ListCreateAPIView):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer


class StudentProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer


class ParentProfileListView(generics.ListCreateAPIView):
    queryset = ParentProfile.objects.all()
    serializer_class = ParentProfileSerializer


class ParentProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ParentProfile.objects.all()
    serializer_class = ParentProfileSerializer