from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken

from .exceptions.exceptions import DuplicateKeyException
from .models import TutorProfile, StudentProfile, ParentProfile, Lesson, BankAccount, Payment, LessonPayment
from .serializers import TutorProfileSerializer, StudentProfileSerializer, ParentProfileSerializer, LessonSerializer, BankAccountSerializer, \
    PaymentSerializer, LessonPaymentSerializer, UserSerializer


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


class LessonListView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class BankAccountListView(generics.ListCreateAPIView):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer


class BankAccountDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer


class PaymentListCreateView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class LessonPaymentListCreateView(generics.ListCreateAPIView):
    queryset = LessonPayment.objects.all()
    serializer_class = LessonPaymentSerializer


class LessonPaymentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LessonPayment.objects.all()
    serializer_class = LessonPaymentSerializer


class TokenVerifyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        token = request.data.get('token')
        try:
            UntypedToken(token)
            return Response({"isValid": True}, status=status.HTTP_200_OK)
        except (InvalidToken, TokenError) as e:
            return Response({"isValid": False,"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
        except DuplicateKeyException as e:
            return Response({"error": e.message}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
