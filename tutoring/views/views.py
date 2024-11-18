from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics

from tutoring.models import Lesson, EducationLevel, Subject, Message, User
from tutoring.serializers.serializers import EducationLevelSerializer, SubjectSerializer, MessageSerializer
from tutoring.serializers.user_serializers import LessonSerializer, UserSerializer


class StudentLessonListView(generics.ListAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        return Lesson.objects.filter(student__user=self.request.user)

class ParentLessonListView(generics.ListAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        return Lesson.objects.filter(student__parent__user=self.request.user)

class TutorLessonListView(generics.ListAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        return Lesson.objects.filter(tutor__user=self.request.user)

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

class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        sender =User.objects.filter(id=self.request.user.id).first()
        recipient = self.request.query_params.get('recipient')
        sorted_users = sorted([sender, recipient])
        return Message.objects.filter(
            sender__in=sorted_users,
            recipient__in=sorted_users
        ).order_by('timestamp')

class UserWithMessagesListView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        current_user = self.request.user
        messages = Message.objects.filter(
            Q(sender=current_user) | Q(recipient=current_user)
        )
        user_ids = set(messages.values_list('sender', flat=True)) | set(messages.values_list('recipient', flat=True))
        return User.objects.filter(id__in=user_ids).distinct()

