from django.shortcuts import render, redirect
from .models import *
from apps.user.models import *
from apps.vacation.models import *
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime, timedelta
import json
import uuid
import random

# 매칭 방 리스트
def main(request):

    now = timezone.now()

    if request.user.is_authenticated:
        if not request.user.location:
            return redirect('user:social_login')
        user_location = request.user.location
        rooms = MatchingRoom.objects.filter(matching__user_id__location = user_location, end_yn = True).distinct()

        # 날짜 선택 안 했을 시
        rooms = rooms.order_by("departure_date", "departure_time", "create_date")

        # 현재 유저가 host인 방에 대한 리스트
        is_host = list() 
        for room in rooms:
            matching = Matching.objects.filter(matching_room_id = room, user_id = request.user, host_yn = True).exists()
            if matching:
                is_host.append(room)
            # 현재 시각이 매칭방의 출발시간으로부터 3시간 뒤라면 end_yn = False가 된다.
            departure_datetime = datetime.combine(room.departure_date, room.departure_time)
            departure_datetime = timezone.make_aware(departure_datetime)
            if now >= departure_datetime + timedelta(hours=3):
                room.end_yn = False
                room.save()
        rooms = rooms.filter(end_yn = True) 

        selected_date = request.GET.get("selected_date")

        if selected_date:
            selected_date = timezone.datetime.strptime(selected_date, '%Y-%m-%d').date()
            rooms = rooms.filter(departure_date = selected_date)
        
        # 날짜 정보
        # today = datetime.date.today()

        # 이미 신청했는지 여부 판단
        already_apply_ids = Matching.objects.filter(matching_room_id__in=list(rooms), user_id=request.user, host_yn=False).values_list('matching_room_id', flat=True)

        pagetype = 1
        ctx = {
            'rooms':rooms,
            'pagetype':json.dumps(pagetype),
            'is_host':is_host,
            'already_apply_ids': already_apply_ids,
        }

        return render(request, 'matching/matchinglist.html', context=ctx)

    else:
        rooms = MatchingRoom.objects.filter(end_yn = True)
        rooms = rooms.order_by("departure_date", "departure_time", "create_date")

        selected_date = request.GET.get("selected_date")
        if selected_date:
            selected_date = timezone.datetime.strptime(selected_date, '%Y-%m-%d').date()
            rooms = rooms.filter(departure_date = selected_date)
        
        # end_yn = True 판단
        for room in rooms:
            departure_datetime = datetime.combine(room.departure_date, room.departure_time)
            departure_datetime = timezone.make_aware(departure_datetime)
            if now >= departure_datetime + timedelta(hours=3):
                room.end_yn = False
                room.save()
        rooms = rooms.filter(end_yn=True)

        pagetype = 1
        ctx = {
            'rooms':rooms,
            'pagetype':json.dumps(pagetype),
        }

        return render(request, 'matching/matchinglist.html', context=ctx)
    

# 매칭 방 생성
@login_required
def matching_create(request):
    # 방 생성은 3번까지만 가능
    if Matching.objects.filter(user_id = request.user, matching_room_id__end_yn = True).count()>=3:
        return render(request, "matching/createroom.html", {'create_limit': True})

    if request.method == 'POST':
        # print("create요청성공")

        departure_area = request.POST.get("departure_area")
        destination_area = request.POST.get("destination_area")
        departure_date = request.POST.get("departure_date")
        departure_time = request.POST.get("departure_time")
        seat_num = request.POST.get("seat_num")
        max_num = request.POST.get("max_num")

        # 클라이언트가 넘긴 값에 대한 유효성 검사
        context = validate_matching_info(departure_area, destination_area, departure_date, departure_time, seat_num, max_num)
        if context:
            return render(request, "matching/createroom.html", context = context)

        matching_room = MatchingRoom.objects.create(
            departure_area = departure_area,
            destination_area = destination_area,
            departure_date = departure_date,
            departure_time = departure_time,
            max_num = request.POST["max_num"],
            current_num = 1,
            end_yn =True,
            uuid =uuid.uuid4(),
        )
        # print("방생성 룸아이디:", matching_room.id)

        Matching.objects.create(
            matching_room_id=matching_room,
            user_id=request.user,
            host_yn=True,
            seat_num=seat_num,
            matching_date=timezone.now(),
            anon_name=getAnonName(matching_room.id)
        )

        #alarm
        alarm_type = "matching_create"
        alarm_activate(matching_room, alarm_type)

        return redirect('/matching/history/')
    
    return render(request, "matching/createroom.html")

# 매칭 신청하기
@login_required
def matching_apply(request, pk):
    # 방 신청 제한
    if Matching.objects.filter(user_id = request.user, matching_room_id__end_yn = True).count()>=3:
        return render(request, "matching/matching_apply.html", {'create_limit': True})

    matching_room = MatchingRoom.objects.get(id=pk)
    selected_seats = list(Matching.objects.filter(matching_room_id=matching_room).values_list('seat_num', flat=True)) # 이미 선택된 좌석들(더 좋은 방법이 없을까..?)
    user = request.user
    #이미 신청한 방인지 여부 파악
    already_apply = Matching.objects.filter(matching_room_id = matching_room, user_id = request.user).exists()
    
    if already_apply or matching_room.current_num == matching_room.max_num:
        return redirect('/matching/')
    
    #매칭방 정보를 넘겨주어 그 방에 있는 유저들을 파악하고 알림 테이블에 정보 저장
    

    if request.method == 'POST':
        seat_num = request.POST.get("seat_num")

        # 클라이언트가 넘긴 값에 대한 유효성 검사
        context = validate_matching_seat(seat_num)
        if context:
            context['matching_room'] = matching_room
            context['selected_seats'] = json.dumps(selected_seats)
            return render(request, 'matching/matching_apply.html', context = context)

        alarm_type = "matching_apply"
        alarm_activate(matching_room, alarm_type)

        #신청자 Matching객체 생성해주기
        Matching.objects.create(
            matching_room_id=matching_room,
            user_id=user,
            host_yn=False,
            seat_num=seat_num,
            matching_date=datetime.now(),
            anon_name=getAnonName(matching_room.id)
        )
        
        #신청자 수 1증가
        matching_room.current_num += 1

        #현재 인원이 최대 인원 수와 같아진다면 매칭방 종료
        #if matching_room.current_num == matching_room.max_num:
        #    matching_room.end_yn = False

        matching_room.save()
        # history페이지 or 로 연결되게 바꿀 것(영진)
        return redirect('/matching/')
    else:
        ctx = {
            'matching_room': matching_room,
            'selected_seats': json.dumps(selected_seats), #jsno화
            'already_apply':already_apply
        }
        return render(request, 'matching/matching_apply.html', context=ctx)

# 매칭방 수정하기
@login_required
def matching_update(request, pk):
    user = request.user
    matching_room = MatchingRoom.objects.get(id=pk)
    is_host = Matching.objects.get(matching_room_id = matching_room, host_yn = True)
    is_guest = Matching.objects.filter(matching_room_id = matching_room, host_yn = False).exists()
    selected_seats = list(Matching.objects.filter(matching_room_id=matching_room).values_list('seat_num', flat=True))
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
                
                departure_area = request.POST.get("departure_area")
                destination_area = request.POST.get("destination_area")
                departure_date = request.POST.get("departure_date")
                departure_time = request.POST.get("departure_time")
                seat_num = request.POST.get("seat_num")
                max_num = request.POST.get("max_num")

                # 클라이언트가 넘긴 값에 대한 유효성 검사
                context = validate_matching_info(departure_area, destination_area, departure_date, departure_time, seat_num, max_num)
                if context:
                    context['matching_room'] = matching_room
                    context['selected_seats'] = json.dumps(list(seat_num))
                    context['ret_bec_error'] = True
                    return render(request, "matching/matching_update.html", context = context)

                matching_room.departure_area = departure_area
                matching_room.destination_area = destination_area
                matching_room.departure_date = departure_date
                matching_room.departure_time = departure_time
                matching_room.max_num = max_num
                matching_room.save()

                is_host.seat_num = seat_num
                is_host.save()

                return redirect('/matching/')
            else:     # 방장 외 인원이 존재하는 경우
                matching_room.max_num = request.POST["max_num"]
                matching_room.save()
                
                is_host.seat_num = request.POST['seat_num']
                is_host.save()
                alarm_type = "matching_update"
                alarm_activate(matching_room, alarm_type)

                return redirect('/matching/')
        else:
            ctx={
                'matching_room':matching_room,
                'selected_seats':json.dumps(selected_seats),
                'change_yn':change_yn,
                'is_guest':is_guest,
                'max_num': max_num,
            }
            return render(request, 'matching/matching_update.html', context=ctx)
    else:
        return redirect('/matching/') # 이 경우 어떻게 처리할지(핵)

# 매칭방 내역
@login_required
def matching_history(request):
    user = request.user
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
        user = request.user
        # 히스토리 페이지에서 Matching 객체들을 받았기 때문에 Matching의 pk가 적용된다.
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

                alarm_type = "matching_delete"
                alarm_activate(matching_room, alarm_type)
                alarm_type = "new_host"
                alarm_activate(matching_room, alarm_type, new_host) # 불필요한 연산 줄이기 위해

                matching_room.current_num -= 1         # 해당 유저의 Matching을 삭제하면 MatchingRoom의 현재 인원 수 -1
                matching_room.save()
        else: 
            matching.delete() 
            alarm_type = "matching_delete"
            alarm_activate(matching_room, alarm_type)
            matching_room.current_num -= 1 
            matching_room.save()



    return redirect('/matching/')

def getAnonName(matching_room_id):
    animal_names = [
        "강아지", "고양이", "코끼리", "사자", "기린", "원숭이", "팬더", "캥거루", "토끼", "다람쥐",
        "파랑새", "돼지", "말", "앵무새", "호랑이", "펭귄", "북극곰", "침팬지", "수달", "뱀",
        "물고기", "악어", "맷돼지", "비둘기", "거북이", "늑대", "두더지", "햄스터", "하마", "너구리",
        "기니피그", "친칠라", "백조", "고래", "가젤", "캐멀", "물소"
    ]
    matchings = Matching.objects.filter(matching_room_id = matching_room_id)
    
    while True:
        flag = True
        animal = random.choice(animal_names)

        for matching in matchings:
            if animal == matching:
                flag = False
                break
                
        if flag:
            break

    return animal

## 매칭 시 사이트 내에 알림 표시
from django.views.decorators.csrf import csrf_exempt
#이거 써도 보안상 문제 없는지 확인 필요(영진)
def alarm_activate(matching_room, alarm_type, *args):
    # 어떤 사람이 매칭방을 만들었을 때! -> 이날 휴가출발일을 등록해놓은 유저들에게
    if alarm_type == "matching_create":
        content = "나의 휴가 날짜에 새로운 방이 생성되었어요!"
        vacation_users = (Vacation.objects.filter(departure_date=matching_room.departure_date) | Vacation.objects.filter(arrival_date=matching_room.departure_date))
        for vacation_user in vacation_users:
            Alarm.objects.create(
                user_id = vacation_user.user_id,
                matching_room_id = matching_room,
                content = content,
            )

    # 어떤 사람이 매칭방에 참여했을 때!
    elif alarm_type == "matching_apply":
        content = "새로운 분과 매칭이 이루어졌어요!"
        matchings = Matching.objects.filter(matching_room_id=matching_room)
        # 반복문 최대 3번밖에 안 돌아서 이렇게 처리했어요(영진)
        for matching in matchings:
            Alarm.objects.create(
                user_id = matching.user_id,
                matching_room_id = matching.matching_room_id,
                content = content,
            )

    
    # 그럼 신청한 신청방 정보를 받아와서 매칭 테이블에서 필터링으로 속해있는 유저들이 누군지 확인해볼까?
    
    # 어떤 사람이 매칭방에서 나갔을 때! (참여 부분이랑 겹치는 것 나중에 처리하기)
    elif alarm_type == "matching_delete":
        content = "내 채팅방에서 누군가 나갔습니다."
        matchings = Matching.objects.filter(matching_room_id=matching_room)
        for matching in matchings:
            # print("delete matchings:", matchings)
            Alarm.objects.create(
                user_id = matching.user_id,
                matching_room_id = matching.matching_room_id,
                content = content,
            )

    # 내가 방장이 되었을 때!
    elif alarm_type == "new_host":
        content = "방장이 되었습니다."
        Alarm.objects.create(
                user_id = args[0].user_id,
                matching_room_id = args[0].matching_room_id,
                content = content,
            )

    # 내가 속한 방이 수정되었을 때! ()
    elif alarm_type == "matching_update":
        content = "방 정보가 수정되었습니다. 확인하세요!"
        matchings = Matching.objects.filter(matching_room_id=matching_room)
        for matching in matchings:
            # print("delete matchings:", matchings)
            Alarm.objects.create(
                user_id = matching.user_id,
                matching_room_id = matching.matching_room_id,
                content = content,
            )
        
    
    
    
def alarm_delete(request, alarm_id):
    Alarm.objects.filter(id=alarm_id).delete()
    return redirect(request.META['HTTP_REFERER'])

def questions(request):
    return render(request, 'matching/questions.html')

#매칭방 정보
@login_required
def matching_detail(request, pk):

    matching_room = MatchingRoom.objects.get(id=pk)
    matching = Matching.objects.get(matching_room_id = matching_room, user_id = request.user)
    selected_seats = list(Matching.objects.filter(matching_room_id=matching_room).values_list('seat_num', flat=True))
    user_seat = str(matching.seat_num)
    max_num = int(matching_room.max_num)
    
    ctx={
        'matching_room':matching_room,
        'selected_seats':json.dumps(selected_seats),
        'user_seat':user_seat,
        'max_num':max_num,
    }
    return render(request, "matching/matching_detail.html", context=ctx)
# 매칭 관련 페이지(생성, 수정, 지원)에서 클라이언트가 넘긴 값에 대한 유효성 검사
def validate_matching_info(departure_area, destination_area, departure_date, departure_time, seat_num, max_num):

    context = {}

    if departure_area == "" or destination_area == "" or departure_date == "" or departure_time == "" or seat_num is None or max_num is None:
        context = {
            "departure_area": departure_area,
            "destination_area": destination_area,
            "departure_date": departure_date,
            "departure_time": departure_time,
            "seat_num": seat_num,
            "max_num": max_num
        }

        if departure_area == "" or destination_area == "":
            context["error_msg_area"] = "출발 지점과 도착 지점을 모두 입력해주세요."

        if departure_date == "":
            context["error_msg_date_date"] = "출발 날짜를 입력해주세요."

        if departure_time == "":
            context["error_msg_date_time"] = "출발 시각을 입력해주세요."

        if seat_num is None:
            context["error_msg_seat"] = "좌석을 선택해주세요."

        if max_num is None:
            context["error_msg_max_num"] = "최대 인원 수를 선택해주세요."

    return context


def validate_matching_seat(seat_num):

    context = {}

    if seat_num == None:
        context = { 
            "seat_num": seat_num,
            "error_msg_seat": "좌석을 선택해주세요."
        }

    return context

def questions(request):
    return render(request, 'matching/questions.html')
