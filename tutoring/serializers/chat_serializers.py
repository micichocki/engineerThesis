from rest_framework import serializers

from tutoring.models import Message
from tutoring.serializers.user_serializers import UserSerializer


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer()
    recipient = UserSerializer()
    class Meta:
        model = Message
        fields = ['sender', 'recipient', 'content', 'timestamp']