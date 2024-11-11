from rest_framework import generics

from tutoring.models import Lesson
from tutoring.serializers.serializers import LessonSerializer


class LessonListView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
