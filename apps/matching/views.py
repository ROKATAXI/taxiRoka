from django.shortcuts import render, redirect
from .models import *
from apps.user.models import *
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime


# 매칭 방 리스트

def main(request):
    if request.user.is_authenticated:
        user_location = request.user.location
        rooms = MatchingRoom.objects.filter(matching__host_yn = True, matching__user_id__location = user_location)
        rooms = rooms.order_by("departure_date", "departure_time", "create_date")
    else:
        rooms = MatchingRoom.objects.all()

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

        return redirect('/matching/')
    
    return render(request, "matching/createroom.html")

# 매칭 신청하기
@login_required
def matching_apply(request, pk):
    matching_room = MatchingRoom.objects.get(id=pk)
    selected_seats = str(list(Matching.objects.filter(matching_room_id=matching_room).values_list('seat_num', flat=True))) # 이미 선택된 좌석들(더 좋은 방법이 없을까..?)
    user = CustomUser.objects.get(pk=request.user.pk)
    already_apply = Matching.objects.filter(matching_room_id = matching_room, user_id = request.user).exists()
    
    if already_apply or matching_room.current_num == matching_room.max_num:
        return redirect('/matching/')
    

    if request.method == 'POST':
        seat_num = request.POST['seat_num']
        #신청자 Matching객체 생성해주기
        matching = Matching.objects.create(    
            matching_room_id=matching_room,
            user_id=user,
            host_yn=False,
            seat_num=seat_num,
            matching_date=datetime.now()  
        )
        #신청자 수 1증가
        matching_room.current_num += 1

        #현재 인원이 최대 인원 수와 같아진다면 매칭방 종료
        #if matching_room.current_num == matching_room.max_num:
        #    matching_room.end_yn = False

        matching_room.save()
        return redirect('/matching/')
    else:
        ctx = {
            'matching_room': matching_room,
            'selected_seats': selected_seats,
        }
        return render(request, 'matching/matching_apply.html', context=ctx)

# 매칭방 수정하기
@login_required
def matching_update(request, pk):
    user = CustomUser.objects.get(pk=request.user.pk)
    matching_room = MatchingRoom.objects.get(id=pk)
    is_host = Matching.objects.get(matching_room_id = matching_room, host_yn = True)
    is_guest = Matching.objects.filter(matching_room_id = matching_room, host_yn = False).exists()
    selected_seats = str(list(Matching.objects.filter(matching_room_id=matching_room, host_yn = False).values_list('seat_num', flat=True)))
    current_num = matching_room.current_num
    max_num = int(matching_room.max_num)

    # 현재 인원수보다 적게 max_num을 변경할 수는 없음 (추후에 변경해야 될 하드코딩)
    if current_num == 4:
        change_yn = False
    else:
        change_yn = True

    # 이미 매칭 완료된 방은 수정 불가능
    #if current_num == max_num:
    #   return redirect('/matching/')

    if is_host.user_id == user:
        if request.method == 'POST':
            if not is_guest:  # 방장만 존재하는 경우
                matching_room.departure_area = request.POST["departure_area"]
                matching_room.destination_area = request.POST["destination_area"]
                matching_room.departure_date = request.POST["departure_date"]
                matching_room.departure_time = request.POST["departure_time"]
                matching_room.max_num = request.POST["max_num"]
                matching_room.save()

                is_host.seat_num = request.POST['seat_num']
                is_host.save()

                return redirect('/matching/')
            else:     # 방장 외 인원이 존재하는 경우
                matching_room.max_num = request.POST["max_num"]
                matching_room.save()
                
                is_host.seat_num = request.POST['seat_num']
                is_host.save()

                return redirect('/matching/')
        else:
            ctx={
                'matching_room':matching_room,
                'selected_seats':selected_seats,
                'change_yn':change_yn,
                'is_guest':is_guest,
            }
            return render(request, 'matching/matching_update.html', context=ctx)
    else:
        return redirect('/matching/')

# 매칭방 내역
@login_required
def matching_history(request):
    user = CustomUser.objects.get(pk=request.user.pk)
    matching_rooms = Matching.objects.filter(user_id=user, matching_room_id__end_yn = True) # 매칭 예정 방들
    matched_rooms = Matching.objects.filter(user_id=user, matching_room_id__end_yn = False) # 매칭 완료된 방들
    number_all = Matching.objects.filter(user_id=user).count() # 모든 사용 이력 수
    number_matching = Matching.objects.filter(user_id=user, matching_room_id__end_yn = True).count() # 매칭 예정 수
    number_matched = Matching.objects.filter(user_id=user, matching_room_id__end_yn = False).count() # 매칭 완료 수
 
    ctx = {
        'matching_rooms':matching_rooms,
        'matched_rooms':matched_rooms,
        'number_all':number_all,
        'number_matching':number_matching,
        'number_matched':number_matched,
    }

    return render(request, "matching/matching_history.html", context=ctx)


# 매칭방 나오기
@login_required
def matching_delete(request, pk):

    if request.method == 'POST':
        user = CustomUser.objects.get(pk=request.user.pk)
        matching = Matching.objects.get(id=pk)
        matching_room = matching.matching_room_id
        is_host = Matching.objects.filter(matching_room_id = matching_room, host_yn = True, user_id = user).exists()

        if is_host:  # 현재 유저가 방장일 경우
            if matching_room.current_num == 1:
                matching_room.delete()                 # 매칭 방의 인원 수가 0명이면 해당 매칭 방 삭제
            else:
                new_host = Matching.objects.filter(matching_room_id=matching_room, host_yn=False).first()  # 방장 권한 이전
                new_host.host_yn = True
                new_host.save()

                matching.delete()
                matching_room.current_num -= 1         # 해당 유저의 Matching을 삭제하면 MatchingRoom의 현재 인원 수 -1
                matching_room.save()
        else: 
            matching.delete() 
            matching_room.current_num -= 1 
            matching_room.save()
            
            if matching_room.current_num == 0:
                matching_room.delete()


    return redirect('/matching/')

