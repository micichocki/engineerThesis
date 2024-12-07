from rest_framework import serializers

from tutoring.models import BankAccount, LessonPayment, Lesson
from tutoring.serializers.user_serializers import UserSerializer


class BankAccountSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = BankAccount
        fields = ['id', 'user', 'account_number', 'bank_name']

class LessonPaymentSerializer(serializers.ModelSerializer):
    lesson = serializers.PrimaryKeyRelatedField(queryset=Lesson.objects.all())
    payment_status = serializers.CharField(max_length=100)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = LessonPayment
        fields = ['id', 'lesson', 'payment_status', 'amount', 'created_at']

