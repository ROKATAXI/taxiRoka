from apps.matching.models import *

def notifications(request):
    if request.user.is_authenticated:
        alarms = Alarm.objects.filter(user_id=request.user)
        return {'alarms': alarms}
    return {}
