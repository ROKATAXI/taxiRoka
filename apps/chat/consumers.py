import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from apps.matching.models import Matching, MatchingRoom

class ChatConsumer(WebsocketConsumer):
    
    # 클라이언트로부터 연결 요청이 온 경우
    def connect(self):

        # websocket 서버는 클라이언트와의 연결 수락
        self.accept()

        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        anon_name = self.getAnonName(self.room_name, self.scope['user'].id)
        async_to_sync(self.channel_layer.group_send)( 
            self.room_group_name, {"type": "chat.message", "message": "----- " + anon_name + " 님이 입장하였습니다. -----"}
        )

        # Join group (group에 클라이언트 개별 채널 추가)
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
    
    # websocket 서버가 클라이언트로부터 데이터를 전달받은 경우
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # group_send(): 특정 그룹 내의 모든 채널에게 메시지를 보내는 코드
        anon_name = self.getAnonName(self.room_name, self.scope['user'].id)
        async_to_sync(self.channel_layer.group_send) ( 
            self.room_group_name, {"type": "chat.message", "message": message, "name": anon_name}
        )

    def chat_message(self, event):
        message = event["message"]
        name = event.get("name", "Anonymous")

        anon_name = self.getAnonName(self.room_name, self.scope['user'].id)
        me = anon_name == name # 채팅 메시지를 보낸 사람이 나인지 여부

        self.send(text_data=json.dumps({"message": message, "name": name, "me": me}))

    # 클라이언트에서 websocket 연결 종료 요청을 보낸 경우
    def disconnect(self, close_code):
        # Leave group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

        anon_name = self.getAnonName(self.room_name, self.scope['user'].id)
        async_to_sync(self.channel_layer.group_send)( 
            self.room_group_name, {"type": "chat.message", "message": "----- " + anon_name + " 님이 퇴장하셨습니다. -----"}
        )
    
    # 익명 가져오기: 매칭방 id, 유저 id -> 익명
    def getAnonName(self, room_name, user_id):
        matching_room = MatchingRoom.objects.get(uuid = room_name)
        matching = Matching.objects.get(matching_room_id = matching_room.id, user_id = user_id)
        return matching.anon_name