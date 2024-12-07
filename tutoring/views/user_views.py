from datetime import datetime

from django.db import transaction
from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from tutoring.models import StudentProfile, TutorProfile, ParentProfile, User, AvailableHour, EducationLevel, \
    WorkingExperience, Subject, TutorSubjectPrice, Lesson
from tutoring.serializers.user_serializers import StudentProfileSerializer, TutorProfileSerializer, \
    ParentProfileSerializer, UserSerializer, LessonCreateSerializer, LessonAcceptSerializer, LessonDocumentSerializer, \
    LessonFeedbackSerializer


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)


class TutorProfileListView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = TutorProfile.objects.all()
    serializer_class = TutorProfileSerializer

class TutorProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = TutorProfile.objects.all()
    serializer_class = TutorProfileSerializer

    def update(self, request, *args, **kwargs):
        with transaction.atomic():
            tutor_profile = TutorProfile.objects.select_related('user').get(user_id=request.user.id)

            tutor_profile.bio = request.data.get('bio', tutor_profile.bio).capitalize()
            working_experience = request.data.get('working_experience')
            if working_experience:
                tutor_profile.working_experience.all().delete()
                tutor_profile.working_experience.clear()
                for experience in working_experience:
                    experience_obj = WorkingExperience.objects.create(
                        position=experience.get('position'),
                        start_date=experience.get('start_date'),
                        end_date=experience.get('end_date') or None,
                        description=experience.get('description'),
                    )
                    tutor_profile.working_experience.add(experience_obj)
            subject_prices = request.data.get('subject_prices', [])
            tutor_profile.subjects.clear()

            for subject_price in subject_prices:
                subject_name = subject_price.get('name', {})
                price_min = subject_price.get('min_price')
                price_max = subject_price.get('max_price')
                subject = Subject.objects.filter(name=subject_name).first()
                if not subject:
                    return Response({'error': 'Invalid subject: {}'.format(subject_name)}, status=400)
                TutorSubjectPrice.objects.create(
                    tutor=tutor_profile,
                    subject=subject,
                    price_min=price_min,
                    price_max=price_max
                )
            available_hours = request.data.get('available_hours')

            if tutor_profile.available_hours.exists():
                tutor_profile.available_hours.all().delete()
                tutor_profile.available_hours.clear()
                tutor_profile.save()
            if available_hours:
                for day_hours in available_hours.split(';'):
                    day, hours = day_hours.split(':', 1)
                    start_time, end_time = hours.split('-')
                    try:
                        start_time_obj = datetime.strptime(start_time, '%H:%M').replace(second=0)
                        end_time_obj = datetime.strptime(end_time, '%H:%M').replace(second=0)
                        if start_time_obj >= end_time_obj:
                            return Response({'error': 'Start time cannot be greater than or equal to end time'},
                                            status=400)
                    except ValueError:
                        return Response({'error': 'Invalid time format. Use HH:MM'}, status=400)

                    available_hour = AvailableHour.objects.create(
                        day_of_week=day,
                        start_time=start_time_obj,
                        end_time=end_time_obj
                    )
                    tutor_profile.available_hours.add(available_hour)
        User.objects.filter(id=tutor_profile.user.id).update(city=request.data.get('city').capitalize())
        tutor_profile.is_remote = request.data.get('is_remote', tutor_profile.is_remote)
        tutor_profile.save()
        return Response(TutorProfileSerializer(tutor_profile).data)


class StudentProfileListView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer


class StudentProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer

    def update(self, request, *args, **kwargs):
        with transaction.atomic():
            student_profile = self.get_object()
            bio = request.data.get('bio', student_profile.bio)
            if bio:
                student_profile.bio = bio.capitalize()
            tasks_description = request.data.get('tasks_description', student_profile.tasks_description)
            if tasks_description:
                student_profile.tasks_description = tasks_description.capitalize()
            goal = request.data.get('goal', student_profile.goal)
            if goal:
                student_profile.goal = goal.capitalize()
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
                        start_time_obj = datetime.strptime(start_time, '%H:%M').replace(second=0)
                        end_time_obj = datetime.strptime(end_time, '%H:%M').replace(second=0)
                        if start_time_obj >= end_time_obj:
                            return Response({'error': 'Start time cannot be greater than or equal to end time'},
                                            status=400)
                    except ValueError:
                        return Response({'error': 'Invalid time format. Use HH:MM'}, status=400)

                    available_hour = AvailableHour.objects.create(
                        day_of_week=day,
                        start_time=start_time_obj,
                        end_time=end_time_obj
                    )
                    student_profile.available_hours.add(available_hour)
            student_profile.save()
        return Response(self.serializer_class(student_profile).data)


class ParentProfileListView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ParentProfile.objects.all()
    serializer_class = ParentProfileSerializer


class ParentProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
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
            except StudentProfile.DoesNotExist:
                return Response({'error': 'Student profile not found'}, status=404)
        if not child:
            return Response({'error': 'Parent profile not found'}, status=404)
        parent_profile.save()
        return Response(self.serializer_class(parent_profile).data)


class TutorListView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.filter(tutorprofile__isnull=False)
        city = self.request.query_params.get('city')
        subject = self.request.query_params.get('subject')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        remote_only = self.request.query_params.get('remote_only')

        if city:
            queryset = queryset.filter(tutorprofile__user__city__iexact=city)
        if subject:
            queryset = queryset.filter(tutorprofile__subjects__name__iexact=subject)
        if min_price:
            queryset = queryset.filter(tutorprofile__tutorsubjectprice__price_min__gte=min_price)
        if max_price:
            queryset = queryset.filter(tutorprofile__tutorsubjectprice__price_max__lte=max_price)
        if remote_only and remote_only.lower() == 'true':
            queryset = queryset.filter(tutorprofile__is_remote=True)

        return queryset.distinct()

class LessonCreateView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Lesson.objects.all()
    serializer_class = LessonCreateSerializer

    def create(self, request, *args, **kwargs):
        tutor_id = request.data.get('tutor')
        student_id = request.data.get('student')
        subject_id = request.data.get('subject')
        date = request.data.get('date')
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')

        existing_lesson = Lesson.objects.filter(
            tutor_id=tutor_id,
            student_id=student_id,
            subject_id=subject_id,
            start_time__date=date
        ).exists()

        if existing_lesson:
            return Response(
                {'error': 'A lesson with the same tutor, student, and subject already exists for this date.'},
                status=400)

        start_time_iso = datetime.strptime(f"{date} {start_time}", '%Y-%m-%d %H:%M').isoformat()
        end_time_iso = datetime.strptime(f"{date} {end_time}", '%Y-%m-%d %H:%M').isoformat()

        request.data['start_time'] = start_time_iso
        request.data['end_time'] = end_time_iso

        return super().create(request, *args, **kwargs)

class LessonAcceptView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            lesson = Lesson.objects.get(pk=pk)
        except Lesson.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = LessonAcceptSerializer(lesson, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UploadAvatarView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        user = request.user
        avatar = request.data.get('avatar')

        if not avatar:
            return Response({"error": "No avatar image provided"}, status=status.HTTP_400_BAD_REQUEST)

        if avatar.size > 1 * 1024 * 1024 * 1024:
            return Response({"error": "File size exceeds 1 GB limit"}, status=status.HTTP_400_BAD_REQUEST)

        user.avatar = avatar
        user.save()
        return Response({"success": "Avatar uploaded successfully"}, status=status.HTTP_200_OK)

class LessonDocumentUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, id, *args, **kwargs):
        try:
            lesson = Lesson.objects.get(id=id)
        except Lesson.DoesNotExist:
            return Response({"error": "Lesson not found"}, status=status.HTTP_404_NOT_FOUND)

        file_serializer = LessonDocumentSerializer(data=request.data)
        if file_serializer.is_valid():
            file = request.data['document']
            if not file:
                return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
            if file.size > 1 * 1024 * 1024 * 1024:
                return Response({"error": "File size exceeds 1 GB limit"}, status=status.HTTP_400_BAD_REQUEST)
            if not file.name.endswith('.pdf'):
                return Response({"error": "Only PDF files are allowed"}, status=status.HTTP_400_BAD_REQUEST)

            lesson_document = file_serializer.save(lesson=lesson)
            lesson.documents.add(lesson_document)
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LessonFeedbackView(APIView):
    def post(self, request, id, *args, **kwargs):
        try:
            lesson = Lesson.objects.get(id=id)
        except Lesson.DoesNotExist:
            return Response({"error": "Lesson not found"}, status=status.HTTP_404_NOT_FOUND)

        if lesson.rating or lesson.feedback:
            return Response({"error": "This lesson already has a rating or comment"},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = LessonFeedbackSerializer(lesson, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



