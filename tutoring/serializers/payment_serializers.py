from rest_framework import serializers

from engineerThesis.serializers import RegisterSerializer
from tutoring.models import Payment, BankAccount, LessonPayment


class PaymentSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField()
    tutor = serializers.StringRelatedField()
    lesson = serializers.StringRelatedField()

    class Meta:
        model = Payment
        fields = ['id', 'student', 'tutor', 'amount', 'payment_date', 'status', 'lesson']

class BankAccountSerializer(serializers.ModelSerializer):
    tutor = RegisterSerializer()

    class Meta:
        model = BankAccount
        fields = ['id', 'tutor', 'account_number', 'bank_name']

class LessonPaymentSerializer(serializers.ModelSerializer):
    lesson = serializers.StringRelatedField()
    payment = PaymentSerializer()

    class Meta:
        model = LessonPayment
        fields = ['id', 'lesson', 'payment', 'payment_status']
