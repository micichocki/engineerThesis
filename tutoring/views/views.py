from rest_framework import generics

from tutoring.models import Lesson, EducationLevel, Subject
from tutoring.serializers.serializers import LessonSerializer, EducationLevelSerializer, SubjectSerializer


class LessonListView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class EducationLevelListView(generics.ListCreateAPIView):
    queryset = EducationLevel.objects.all()
    serializer_class = EducationLevelSerializer

class EducationLevelDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EducationLevel.objects.all()
    serializer_class = EducationLevelSerializer

class SubjectListView(generics.ListCreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


