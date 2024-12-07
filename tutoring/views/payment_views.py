from rest_framework import generics

from tutoring.models import BankAccount, LessonPayment
from tutoring.serializers.payment_serializers import BankAccountSerializer, LessonPaymentSerializer


class BankAccountListView(generics.ListCreateAPIView):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer


class BankAccountDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer


class LessonPaymentListCreateView(generics.ListCreateAPIView):
    queryset = LessonPayment.objects.all()
    serializer_class = LessonPaymentSerializer

class LessonPaymentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LessonPayment.objects.all()
    serializer_class = LessonPaymentSerializer
