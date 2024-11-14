from datetime import datetime

from django.db import transaction
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from tutoring.models import StudentProfile, TutorProfile, ParentProfile, User, AvailableHour, EducationLevel
from tutoring.serializers.user_serializers import StudentProfileSerializer, TutorProfileSerializer, \
    ParentProfileSerializer, UserSerializer


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


class TutorProfileListView(generics.ListCreateAPIView):
    queryset = TutorProfile.objects.all()
    serializer_class = TutorProfileSerializer


class TutorProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TutorProfile.objects.all()

    serializer_class = TutorProfileSerializer

    def update(self, request, *args, **kwargs):
        tutor_profile = self.get_object()
        tutor_profile.bio = request.data.get('bio', tutor_profile.bio)
        tutor_profile.save()
        return Response(self.serializer_class(tutor_profile).data)


class StudentProfileListView(generics.ListCreateAPIView):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer


class StudentProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer

    def update(self, request, *args, **kwargs):
        with transaction.atomic():
            student_profile = self.get_object()
            student_profile.bio = request.data.get('bio', student_profile.bio).capitalize()
            student_profile.tasks_description = request.data.get('tasks_description',
                                                                 student_profile.tasks_description).capitalize()
            student_profile.goal = request.data.get('goal', student_profile.goal).capitalize()
            education_level = request.data.get('education_level')
            student_profile.education_level = EducationLevel.objects.filter(level=education_level).first()
            available_hours = request.data.get('available_hours')

            if student_profile.available_hours.exists():
                student_profile.available_hours.all().delete()
                student_profile.available_hours.clear()
                student_profile.save()
            if available_hours:
                for day_hours in available_hours.split(';'):
                    day, hours = day_hours.split(':', 1)
                    start_time, end_time = hours.split('-')
                    try:
                        start_time_obj = datetime.strptime(start_time, '%H:%M:%S')
                        end_time_obj = datetime.strptime(end_time, '%H:%M:%S')
                        if start_time_obj >= end_time_obj:
                            return Response({'error': 'Start time cannot be greater than or equal to end time'},
                                            status=400)
                    except ValueError:
                        return Response({'error': 'Invalid time format. Use HH:MM'}, status=400)
                    available_hour = AvailableHour.objects.create(
                        day_of_week=day,
                        start_time=start_time,
                        end_time=end_time
                    )
                    student_profile.available_hours.add(available_hour)

            student_profile.save()
        return Response(self.serializer_class(student_profile).data)


class ParentProfileListView(generics.ListCreateAPIView):
    queryset = ParentProfile.objects.all()
    serializer_class = ParentProfileSerializer


class ParentProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ParentProfile.objects.all()
    serializer_class = ParentProfileSerializer

    def update(self, request, *args, **kwargs):
        parent_profile = self.get_object()
        children_emails = request.data.get('children', [])
        child = None
        for email in children_emails:
            try:
                child = StudentProfile.objects.get(user__email=email)
                if child != request.user:
                    parent_profile.children.add(child)
            except User.DoesNotExist:
                continue
        if not child:
            return Response({'error': 'Parent profile not found'}, status=404)
        parent_profile.save()
        return Response(self.serializer_class(parent_profile).data)

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


