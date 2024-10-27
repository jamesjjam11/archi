from django.db import models
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.contrib.auth.models import User

class SystemEvent(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
def get_users_online():
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    user_ids = []

    for session in sessions:
        data = session.get_decoded()
        if '_auth_user_id' in data:
            user_ids.append(data['_auth_user_id'])

    users_online = User.objects.filter(id__in=user_ids)
    return users_online
