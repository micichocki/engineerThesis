import json
from channels.generic.websocket import  WebsocketConsumer
from asgiref.sync import async_to_sync

from tutoring.models import Message


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.sender = self.scope['url_route']['kwargs']['sender']
        self.recipient = self.scope['url_route']['kwargs']['recipient']
        sorted_users = sorted([self.sender, self.recipient])
        self.room_group_name = f'chat_{sorted_users[0]}_{sorted_users[1]}'
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

        Message.objects.create(
            sender=self.sender,
            recipient=self.recipient,
            content=message
        )

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps({
            'message': message
        }))