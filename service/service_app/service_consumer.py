import json, uuid
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

list_user_online = set()

class ServiceConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'server'      
        self.username = self.scope['url_route']['kwargs']['username']
        
        if self.username in list_user_online:
            print("Không được phép !")
        else:
            list_user_online.add(self.username)
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )
            self.accept()
            self.send(json.dumps({
                "status": "ok",
                "name": self.username
            }))     

        print(list_user_online)

    # def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     async_to_sync(self.channel_layer.group_send)(
    #         self.room_group_name,
    #         {
    #             'type': 'handle_send',
    #             'message': text_data_json
    #         }
    #     )
    
    # def handle_send(self, event):
    #     message = event["message"]
    #     self.send(json.dumps({
    #         'type':'join',
    #         'message': message["message"]
    #     }))


    