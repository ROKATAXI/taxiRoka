import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from apps.matching.models import *
from apps.chat.models import *
from apps.user.models import *
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize

class ChatConsumer(WebsocketConsumer):
    
    # 클라이언트로부터 연결 요청이 온 경우
    def connect(self):

        self.accept()
        
        self.room_uuid = self.scope["url_route"]["kwargs"]["room_uuid"]
        self.room_group_name = f"chat_{self.room_uuid}"
        type = self.scope['query_string'].decode('utf-8').split('=')[1]

        # 채팅방에 처음 입장 또는 재입장
        if type == 'initial':
            anon_name = self.get_anon(self.room_uuid, self.scope['user'])
            content = anon_name + " 님이 입장하였습니다."

            self.save_msg(content, None)

            async_to_sync(self.channel_layer.group_send)( 
                self.room_group_name, {"type": "chat.message", "message": content}
            )

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )


    # websocket 서버가 클라이언트로부터 데이터를 전달받은 경우
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        content = text_data_json["message"]
        user = self.scope['user']
        anon_name = self.get_anon(self.get_uuid_from_path(self.scope['path']), user)

        self.save_msg(content, user)

        async_to_sync(self.channel_layer.group_send) ( 
            self.room_group_name, {"type": "chat.message", "message": content, "name": anon_name}
        )


    def chat_message(self, event):
        content = event["message"]
        name = event.get("name", "Anonymous")
        anon_name = self.get_anon(self.get_uuid_from_path(self.scope['path']), self.scope['user'])
        me = anon_name == name

        self.send(text_data=json.dumps({"message": content, "name": name, "me": me}))


    # 클라이언트에서 websocket 연결 종료 요청을 보낸 경우 + URL이 바뀐 경우 등
    def disconnect(self, close_code):

        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

        # 클라이언트가 '방 나가기' 버튼 클릭
        if close_code == None:
            user = self.scope['user']
            anon_name = self.get_anon(self.get_uuid_from_path(self.scope['path']), user)
            content = anon_name + " 님이 퇴장하였습니다."

            self.save_msg(content, user)

            async_to_sync(self.channel_layer.group_send)( 
                self.room_group_name, {"type": "chat.message", "message": content}
            )


    def get_anon(self, room_uuid, user):
        anon_name = self.scope['session'].get(room_uuid, '') # 익명 또는 ''

        if anon_name != '':
            return anon_name
        
        return self.get_anon_from_db(room_uuid, user)


    def get_anon_from_db(self, room_uuid, user):
        matching_room = MatchingRoom.objects.get(uuid = room_uuid)
        matching = Matching.objects.get(matching_room_id = matching_room, user_id = user)
        anon_name = matching.anon_name
        
        self.scope['session'][room_uuid] = anon_name
        self.scope['session'].save()

        return anon_name


    def save_msg(self, content, sender):
        Message.objects.create(
            chatting_room_id = self.get_matching_room(),
            msg_sender = sender,
            msg_content = content
        )


    def get_matching_room(self):
        matching_room = self.scope['session'].get('chatting_room_obj', None) # MatchingRoom 또는 None

        if matching_room != None:
            return matching_room
        
        return self.get_matching_room_from_db()


    def get_matching_room_from_db(self):
        uuid = self.get_uuid_from_path(self.scope['path'])
        matching_room = MatchingRoom.objects.get(uuid = uuid)

        self.scope['session']['matching_room_obj'] = serialize('json', [matching_room], cls=DjangoJSONEncoder)
        self.scope['session'].save()

        return matching_room


    def get_uuid_from_path(self, path):
        uuid = self.scope['session'].get(path, '') # uuid 또는 ''

        if uuid != '':
            return uuid
        
        return self.extract_uuid(path)


    def extract_uuid(self, path):
        start = path.find('/ws/chat/') + len('/ws/chat/')
        end = path.find('/', start)
        uuid = path[start : end]

        self.scope['session'][path] = uuid
        self.scope['session'].save()

        return uuid