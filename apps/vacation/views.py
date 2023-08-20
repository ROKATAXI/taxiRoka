from django.shortcuts import render, redirect
from .models import *
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import date
from apps.vacation.models import * 
from django.http import JsonResponse

def calendar(request):
    return render(request, 'vacation/calendar.html')


@csrf_exempt
def create_vacation(request):
    reqObj = json.loads(request.body)

    start_year = reqObj['startYear']
    start_month = reqObj['startMonth']
    start_date = reqObj['startDate']
    end_year = reqObj['endYear']
    end_month = reqObj['endMonth']
    end_date = reqObj['endDate']

    start = date(int(start_year), int(start_month), int(start_date))
    end = date(int(end_year), int(end_month), int(end_date))

    if end < start:
        start, end = end, start

    vacation = Vacation.objects.create(
        departure_date = start,
        arrival_date = end,
        user_id = request.user
    )

    responseData = {
        'start_date': start.strftime('%Y년 %#m월 %#d일'),
        'end_date': end.strftime('%Y년 %#m월 %#d일'),
        'vacation_id': vacation.id
    }
    return JsonResponse(responseData)


def vacation_list(request):
    user_id = request.user
    vacations = Vacation.objects.filter(user_id=user_id).order_by('departure_date')

    ctx = {
        'vacations':vacations,
    }
    return render(request, 'vacation/calendar.html', ctx)


@csrf_exempt
def delete_vacation(request, pk):
    if request.method == 'POST':
        vacation = Vacation.objects.filter(id=pk)
        vacation.delete()
    
        responseData = {
            'vac_id': pk
        }
        return JsonResponse(responseData)
    
    return render(request, 'error.html') # 잘못된 요청