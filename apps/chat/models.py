from django.db import models
from apps.user.models import CustomUser as User
from apps.matching.models import MatchingRoom

# ERD CLOUD 링크: https://www.erdcloud.com/d/zB3wiAaQY7PxnzLyY

class Message(models.Model):
    # 채팅방 식별자, 메시지 보낸 유저, 메시지 내용, 메시지 전달 시각
    chatting_room_id = models.ForeignKey(MatchingRoom, on_delete=models.CASCADE)
    msg_sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    msg_content = models.TextField()
    sent_time = models.DateTimeField(auto_now_add=True)
