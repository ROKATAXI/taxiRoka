from django.shortcuts import render, redirect
from .models import *
from apps.user.models import *
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# Create your views here.

def main(request):
    user_location = request.user.location
    rooms = MatchingRoom.objects.filter(matching__host_yn = True, matching__user_id__location = user_location)

    ctx = {
        'rooms':rooms,
    }

    return render(request, 'matching/matchinglist.html', context=ctx)

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

        return redirect('matching/')
    
    return render(request, "matching/matching_create.html")