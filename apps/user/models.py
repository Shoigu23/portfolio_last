from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.utils import timezone


class User(AbstractUser):
    photo = models.ImageField(upload_to='users_image', null=True, blank=True)
    is_confirm_email = models.BooleanField(default=False)


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def str(self) -> str:
        return f'EmailVerification for {self.user.email}'


    def send_verification_email(self):
        link = f'users/verify/{self.user.email}/{self.code}'
        verification_link = f'127.0.0.1:8000/{link}'
        subject = f'Подтверждение учетной записи для {self.user.username}'
        message = f'Для подтверждение учетной записи перейдите по ссылке {verification_link}'
        send_mail(
            subject=subject,
            message=message,
            from_email='toichubaev3930@mail.ru',
            recipient_list=[self.user.email],
            fail_silently=False 
        )

    def is_expired(self):
        return True if timezone.now() >= self.expiration else False


