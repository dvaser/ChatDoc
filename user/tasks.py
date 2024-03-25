# yourapp/tasks.py

from celery import shared_task
from django.utils import timezone
from .models import CustomUser

@shared_task
def check_delete_date():
    today = timezone.now().date()
    CustomUser.objects.filter(deleteDate__date=today, isActive=False).delete()

@shared_task
def delete_user():
    try:
        users = CustomUser.objects.all()
        for user in users:
            if (user.deleteDate and (user.deleteDate.date() == timezone.now().date())):
                user.delete()
    except:
        pass