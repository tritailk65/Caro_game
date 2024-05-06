import json, uuid
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class ServiceConsumer(WebsocketConsumer):
    def connect(self):
        # Nếu hàng đợi có người chờ, ghép cặp với họ và tạo phòng
        if waiting_queue:
            partner_channel_name = waiting_queue.popleft()  # Lấy người chờ
            self.room_group_name = partner_channel_name[1] # Lấy mã phòng được tạo từ người chơi 1

            self.accept()

            # Thêm hai người vào phòng
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                partner_channel_name[0] # Channel người chơi 1
            )    

            self.send(json.dumps({
                "type": "Matching",
                "symbol": "O",
                "room": self.room_group_name,
                "message": "Success"
            }))              

            # Gửi thông tin về phòng tới cả hai người
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    "type": "start_connection",
                    "room_group_name": self.room_group_name
                }
            )

        else:
            # Nếu không có người chờ, thêm người dùng vào hàng đợi
            self.room_group_name = str(uuid.uuid4())  # Tạo tên phòng duy nhất
            # Thêm người chơi vào hàng đợi
            waiting_queue.append((self.channel_name,self.room_group_name))
            self.accept()
            self.send(json.dumps({
                "type": "Matching",
                "symbol": "X",
                "room": self.room_group_name,
                "message": "Waiting"
            }))

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'handle_send',
                'message': text_data_json
            }
        )
    
    def handle_send(self, event):
        message = event["message"]
        # Gửi dữ liệu chat
        if message["type"] == "chat":
            self.send(json.dumps({
                'type':'chat',
                'message': message["message"]
            }))
        # Gửi dữ liệu trò chơi
        elif message["type"] == "move":
            self.send(json.dumps({
                'type':'move',
                'player' : message["player"],
                'position': {
                    'row': message["position"]["row"],
                    'col': message["position"]["col"]
                }
            }))

    # Xử lý thông báo matching thành công
    def start_connection(self, event):
        room_group_name = event["room_group_name"]
        self.send(json.dumps({
                "type": "start_connection",
                "room_group_name": room_group_name
            }))
        
    def disconnect(self,event):
        # Gửi thông báo tới những người còn lại trong phòng
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'user_disconnected',
                'message': "A user has disconnected. Room will be closed."
            }
        )

        # Nếu không còn người dùng trong phòng, xóa phòng đó
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

        # Nếu đang chờ trong hàng đợi, xóa khỏi hàng đợi
        global waiting_queue
        waiting_queue = deque([item for item in waiting_queue if item[0] != self.channel_name])

    def user_disconnected(self,event):
        message = event["message"]
        self.send(json.dumps({
                "type": "disconnected",
                "message": message
            }))

