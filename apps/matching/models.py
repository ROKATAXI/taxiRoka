from django.db import models

# ERD CLOUD 링크: https://www.erdcloud.com/d/zB3wiAaQY7PxnzLyY

class MatchingRoom(models.Model):
    # 출발날짜, 출발시간, 출발지, 도착지, 최대인원수, 현재인원수, 매칭방생성일, 배칭방 생성/종료 여부
    departure_date = models.DateField()
    departure_time = models.TimeField()
    departure_area = models.CharField(max_length = 10)
    destination_area = models.CharField(max_length = 10)
    max_num = models.IntegerField()
    current_num = models.IntegerField()
    create_date = models.DateTimeField()
    end_yn = models.BooleanField()

class Mathcing(models.Model):
    # 매칭방식별자, 유저식별자, 방장여부, 좌석번호, 매칭일
    matching_room_id = models.ForeignKey(MatchingRoom, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    host_yn = models.BooleanField()
    seat_num = models.IntegerField()
    matching_date = models.DateTimeField()
