from django.db.models import Q
from rest_framework import generics

from tutoring.models import Lesson, EducationLevel, Subject, Message, User, ParentProfile
from tutoring.serializers.chat_serializers import MessageSerializer
from tutoring.serializers.serializers import EducationLevelSerializer, SubjectSerializer
from tutoring.serializers.user_serializers import LessonSerializer, UserSerializer, LessonUpdateSerializer


class StudentLessonListView(generics.ListAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        return Lesson.objects.filter(student__user=self.request.user)

class ParentLessonListView(generics.ListAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        parent_profile = ParentProfile.objects.get(user=self.request.user)
        children = parent_profile.children.all()
        return Lesson.objects.filter(student__in=children)

class TutorLessonListView(generics.ListAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        return Lesson.objects.filter(tutor__user=self.request.user)

class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return LessonUpdateSerializer
        return LessonSerializer

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

class EducationLevelListView(generics.ListCreateAPIView):
    queryset = EducationLevel.objects.all()
    serializer_class = EducationLevelSerializer

class SubjectListView(generics.ListCreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        sender = User.objects.filter(id=self.request.user.id).first()
        recipient_email = self.request.query_params.get('recipient')
        recipient = User.objects.filter(email=recipient_email).first()
        users = [sender, recipient]
        return Message.objects.filter(
            sender__in=users,
            recipient__in=users,
        ).order_by('timestamp')

class UserWithMessagesListView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        current_user = self.request.user
        messages = Message.objects.filter(
            Q(sender=current_user) | Q(recipient=current_user)
        )
        user_ids = (set(messages.values_list('sender', flat=True)) | set(
            messages.values_list('recipient', flat=True))) - {current_user.id}
        return User.objects.filter(id__in=user_ids).distinct()

