from apps.matching.models import *
import json

def notifications(request):
    if request.user.is_authenticated:
        alarms = Alarm.objects.filter(user_id=request.user)
        alarm_num = len(alarms)
        ctx = {
            'alarms':alarms,
            'alarm_num':json.dumps(alarm_num),
        }
        return ctx
    return {}
