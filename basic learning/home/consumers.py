from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import async_to_sync

class TestConsumer(AsyncWebsocketConsumer):
    def connect(self):
        self.room_name = "test_consumer"
        self.room_group_name="test_consume_name"
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, self.room_group_name
        )
        self.accept()
        self.send(text_data=json.dumps({'status': 'connected'}))

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message', '')
