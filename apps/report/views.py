from django.shortcuts import render, redirect
from .models import *

def show_report(request):
    if request.method == "POST":
        receiver = request.POST.get('receiver')
        roomUrl = request.POST.get('room_url')

        return render(request, 'report/report.html', {'receiver': receiver, 'roomUrl': roomUrl})

def make_report(request):
    if request.method == "POST":

        # report 테이블에 row 추가
        # 신고 당한 유저에 대해, user 테이블의 count 필드 값 변경
        # 신고가 완료되었다는 모달 띄우기
        # 채팅방 페이지로 redirect

        maker = request.user
        receiver = request.POST.get('receiver') # 익명 이름 바탕으로 user 찾아야 함
        content = request.POST.get('content')
        roomUrl = request.POST.get('room_url')

        # Report.objects.create(
        #     report_maker = maker,
        #     report_receiver = receiver,
        #     report_content = content
        # )

        # receiver.count += 1
        # receiver.save()

        return redirect(roomUrl)