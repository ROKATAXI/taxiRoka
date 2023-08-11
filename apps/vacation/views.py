from django.shortcuts import render, redirect
from .models import *

# Create your views here.
def calendar(request):
    return render(request, 'vacation/calendar.html')

def create_vacation(request):
    if request.method == "POST":
        # 폼에서 정보 받아오기
        vacation = Vacation.objects.create(
            departure_area = request.POST.get("departure_area"),
            destination_area = request.POST.get("destination_area"),
            departure_date = request.POST.get("departure_date"),
            arrival_date = request.POST.get("arrival_date"),
            user_id = request.user
        )
        
        return redirect('/vacation/')
    return render(request, "vacation/create.html")


def vacation_list(request):
    user_id = request.user
    vacations = Vacation.objects.filter(user_id=user_id).order_by('departure_date')

    ctx = {
        'vacations':vacations,
    }
    print(vacations)
    return render(request, 'vacation/calendar.html', ctx)


# def update_vacation(request, pk):
#     user = Cust