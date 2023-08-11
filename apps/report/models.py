from django.db import models
from apps.user.models import CustomUser as User

class Report(models.Model):
    # 신고한 유저, 신고당한 유저, 신고 사유, 신고시각
    report_maker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='maker')
    report_receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    report_content = models.TextField(max_length=300)
    reported_time = models.DateTimeField(auto_now_add=True)