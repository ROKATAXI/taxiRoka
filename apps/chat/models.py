from django.db import models
from apps.user.models import CustomUser as User

# ERD CLOUD 링크: https://www.erdcloud.com/d/zB3wiAaQY7PxnzLyY

class Chatting(models.Model):
    # 메시지 보낸 유저, 메시지 내용, 메시지 전달 시각
    msg_sender = models.ForeignKey(User, on_delete=models.CASCADE)
    msg_content = models.TextField()
    sent_time = models.DateTimeField()
