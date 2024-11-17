import json
from channels.generic.websocket import AsyncWebsocketConsumer

from tutoring.models import User, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message_content = text_data_json['message']
        recipient_username = text_data_json['recipient']
        sender = User.objects.get(username=self.scope['user'].username)
        recipient = User.objects.get(username=recipient_username)

        message = Message.objects.create(sender=sender, recipient=recipient, content=message_content)

        await self.send(text_data=json.dumps({
            'id': message.id,
            'sender': message.sender.username,
            'recipient': message.recipient.username,
            'content': message.content,
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }))