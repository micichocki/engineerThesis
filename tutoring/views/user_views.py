from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from tutoring.models import StudentProfile, TutorProfile, ParentProfile, User
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

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


