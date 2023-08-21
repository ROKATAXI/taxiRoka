from django.shortcuts import render
from apps.matching.models import *
from apps.chat.models import *
from django.utils import timezone

def chat(request, room_uuid):
    msg_history = get_refined_msg_history(request, room_uuid)
    return render(request, "chat/chat.html", {"room_uuid" : room_uuid, 'msg_history' : msg_history})


def get_refined_msg_history(request, room_uuid):

    my_msg_history = get_my_msg_history(request, room_uuid)

    if my_msg_history is None:
        return None

    refined_my_msg_history = [
        {
            "sender": get_anon(request, room_uuid, msg.msg_sender) if msg.msg_sender else None,
            "content": msg.msg_content,
            "me" : get_me_tf(request, msg.msg_sender),
            "sent_time": get_sent_time(sent_time.hour, sent_time.minute)
        }
        for msg in my_msg_history
        for sent_time in [timezone.localtime(msg.sent_time)]
    ]
    return refined_my_msg_history


def get_my_msg_history(request, room_uuid):
    matching_room = MatchingRoom.objects.get(uuid = room_uuid)
    msgs = Message.objects.filter(chatting_room_id = matching_room)

    my_anon_name = get_anon(request, room_uuid, request.user)
    enter_msg = my_anon_name  + ' 님이 입장하였습니다.'
    leave_msg =  my_anon_name + ' 님이 퇴장하였습니다.'

    enter_msg_row = msgs.filter(msg_content = enter_msg).last()
    leave_msg_row = msgs.filter(msg_content = leave_msg).last()

    # 입장 메시지 x: 채팅방에 처음 입장한 유저
    # 퇴장 메시지 o: 채팅방에 재입장한 유저
    if (enter_msg_row is None) or (leave_msg_row and enter_msg_row.id < leave_msg_row.id):
        return None
    
    return msgs.filter(id__gte = enter_msg_row.id)


def get_anon(request, room_uuid, msg_sender):
    anon_name = request.session.get(msg_sender.id, None) # 익명 또는 None

    if anon_name is not None:
        return anon_name
    
    return get_anon_from_db(request, room_uuid, msg_sender)


def get_anon_from_db(request, room_uuid, msg_sender):
    matching_room = MatchingRoom.objects.get(uuid = room_uuid)
    matching = Matching.objects.filter(matching_room_id = matching_room, user_id = msg_sender)

    if matching.exists():
        anon_name = matching[0].anon_name   
    else:
        anon_name = '(알수없음)'

    request.session[msg_sender.id] = anon_name

    return anon_name


def get_me_tf(request, msg_sender):
    return request.user == msg_sender


def get_sent_time(hour, minute):
    am_pm = "오전"
    if hour > 12:
        am_pm = "오후"
        hour -= 12
    return f"{am_pm} {hour}:{minute}"