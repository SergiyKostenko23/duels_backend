import json, datetime
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .serializers import MessageSerializer
from .models import User

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = text_data_json['user']
        photo = text_data_json['photo']
        data = {'message': message, 'user': user, 'photo': photo}
        serializer = MessageSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': user,
                'photo': photo,
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        user = event['user']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'time': str(datetime.datetime.now()),
            'user': User.objects.filter(id=user)[0].nome,
            'user_id': User.objects.filter(id=user)[0].id,
            'photo': 'http://127.0.0.1:8000' + User.objects.filter(id=user)[0].photo.url
        }))