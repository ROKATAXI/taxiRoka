from django.shortcuts import render, redirect
from .models import *
from apps.user.models import *
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import datetime

# 매칭 방 리스트
@login_required
def main(request):
    user_location = request.user.location
    rooms = MatchingRoom.objects.filter(matching__host_yn = True, matching__user_id__location = user_location)

    ctx = {
        'rooms':rooms,
    }

    return render(request, 'matching/matchinglist.html', context=ctx)

# 매칭 방 생성
@login_required
def matching_create(request):
    if request.method == 'POST':
        matching_room = MatchingRoom.objects.create(
            departure_area = request.POST["departure_area"],
            destination_area = request.POST["destination_area"],
            departure_date = request.POST["departure_date"],
            departure_time = request.POST["departure_time"],
            max_num = request.POST["max_num"],
            current_num = 1,
            end_yn =True,
        )
        user = CustomUser.objects.get(pk=request.user.pk)

        matching = Matching.objects.create(
            matching_room_id=matching_room,
            user_id=request.user,
            host_yn=True,
            seat_num=request.POST["seat_num"],
            matching_date=timezone.now()
        )

        return redirect('/')
    
    return render(request, "matching/matching_create.html")

# 매칭 신청하기
@login_required
def matching_apply(request, pk):
    matching_room = MatchingRoom.objects.get(id=pk)
    selected_seats = matching_room.matching.values_list('seat_num', flat = True) #이미 선택된 좌석들

    if request.method == 'POST':
        user = CustomUser.objects.get(pk=request.user.pk)

        seat_num = request.POST['seat_num']
        if seat_num in selected_seats:
            return redirect(f'matching/apply/{matching_room.id}')

        #신청자 Matching객체 생성해주기
        matching = Matching.objects.create(    
            matching_room=matching_room,
            user_id=user,
            host_yn=False,
            seat_num=seat_num,
            matching_date=datetime.now()  
        )

        #신청자 수 1증가
        matching_room.current_num += 1
        matching_room.save()

        return redirect('matching_room_list')

    else:
        ctx = {
            'matching_room': matching_room,
            'selected_seats': selected_seats,
        }
        return render(request, 'matching_apply.html', context=ctx)