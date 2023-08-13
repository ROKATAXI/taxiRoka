from django.shortcuts import render, redirect
from apps.report.models import * 
from apps.matching.models import *
from apps.user.models import *

def show_report(request):
    if request.method == "POST":
        anon_name = request.POST.get('anon_name')
        room_uuid = request.POST.get('room_uuid')

        return render(request, 'report/report.html', {'anon_name': anon_name, 'room_uuid': room_uuid})

def make_report(request):
    if request.method == "POST":

        room_uuid = request.POST.get('room_uuid')
        maker = request.user
        receiver =  get_receiver_info(room_uuid, request.POST.get('anon_name'))
        content = request.POST.get('content')

        Report.objects.create(
            report_maker = maker,
            report_receiver = receiver,
            report_content = content
        )

        receiver.count += 1
        receiver.save()

        return redirect('/chat/' + room_uuid)
    
# 신고당한 사람 정보 얻기: 매칭방 식별자 + 익명 -> 신고당한 사람
def get_receiver_info(room_uuid, anon_name):
    matching_room = MatchingRoom.objects.get(uuid = room_uuid)
    matching = Matching.objects.get(matching_room_id = matching_room.id, anon_name = anon_name)
    return User.objects.get(id = matching.user_id.id)