from celery import shared_task
import datetime
import uuid
from django.utils import timezone
from apps.user.models import User, EmailVerification

@shared_task
def send_verification_email(user_id):
    user = User.objects.get(id=user_id)
    expiration = timezone.now() + datetime.timedelta(hours=48)
    record = EmailVerification.objects.create(code=uuid.uuid4(), user=user, expiration=expiration)
    record.send_verification_email()