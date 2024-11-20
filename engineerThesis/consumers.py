import hashlib
import json
from urllib.parse import parse_qs

from channels.generic.websocket import  WebsocketConsumer
from asgiref.sync import async_to_sync

from tutoring.models import Message, User
from tutoring.serializers.chat_serializers import MessageSerializer
from tutoring.serializers.user_serializers import UserSerializer


def generate_hash(sender_email, recipient_email):
    emails = sorted([sender_email, recipient_email])
    return hashlib.sha256(":".join(emails).encode()).hexdigest()

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        query_params = parse_qs(self.scope['query_string'].decode())
        self.sender_email = query_params.get("sender", [None])[0]
        self.recipient_email = query_params.get("recipient", [None])[0]

        if self.sender_email and self.recipient_email:
            email_str = ''.join(sorted([self.sender_email, self.recipient_email]))
            raw_hash = hashlib.sha256(email_str.encode('utf-8')).hexdigest()
            self.room_group_name = raw_hash
        else:
            raise ValueError("Sender and recipient emails must be provided")
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()



    def disconnect(self, close_code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = User.objects.filter(email=self.sender_email).first()
        recipient = User.objects.filter(email=self.recipient_email).first()

        created_message = Message.objects.create(
            sender=sender,
            recipient=recipient,
            content=message
        )
        message_json = MessageSerializer(created_message).data,
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_json,
            }
        )

    def chat_message(self, event):
        message = event['message']
        self.send(json.dumps(message[0]))