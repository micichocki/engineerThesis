from rest_framework import generics

from tutoring.models import BankAccount, LessonPayment
from tutoring.serializers.payment_serializers import BankAccountSerializer, LessonPaymentSerializer
class LessonPaymentListCreateView(generics.ListCreateAPIView):
    queryset = LessonPayment.objects.all()
    serializer_class = LessonPaymentSerializer

class LessonPaymentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LessonPayment.objects.all()
    serializer_class = LessonPaymentSerializer

class BankAccountDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
