from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics

from tutoring.models import Lesson, EducationLevel, Subject, Message, User
from tutoring.serializers.serializers import  EducationLevelSerializer, SubjectSerializer
from tutoring.serializers.user_serializers import LessonSerializer


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

@csrf_exempt
def get_message(request, message_id):
    try:
        message = Message.objects.get(id=message_id)
        return JsonResponse({
            'id': message.id,
            'user': message.user.username,
            'content': message.content,
            'timestamp': message.timestamp
        })
    except Message.DoesNotExist:
        return JsonResponse({'error': 'Message not found'}, status=404)

def list_messages(request):
    user = request.user
    other_user_id = request.GET.get('other_user_id')
    other_user = User.objects.get(id=other_user_id)
    messages = Message.objects.filter(
        (Q(sender=user) & Q(recipient=other_user)) | (Q(sender=other_user) & Q(recipient=user))
    ).order_by('timestamp')
    messages_data = [
        {
            'id': message.id,
            'sender': message.sender.username,
            'recipient': message.recipient.username,
            'content': message.content,
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }
        for message in messages
    ]
    return JsonResponse(messages_data, safe=False)


