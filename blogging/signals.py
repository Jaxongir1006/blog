from django.dispatch import receiver, Signal 
from django.db.models.signals import pre_save,post_save
from .models import Blog
from django.core.mail import send_mail
from django.conf import settings

new_signal = Signal()

@receiver(new_signal)
def listen_new_signal(sender, **kwargs):
    print(kwargs.get('mydata'), 'is received')


@receiver(pre_save, sender = Blog)
def pre_save_blog(sender, instance, **kwargs):
    instance.status = Blog.StatusEnum.DRAFT
    print(instance, 'is being created')

@receiver(post_save, sender = Blog)
def pre_save_blog(sender, instance, created, **kwargs):
    if created:
        send_mail("Blog saytidan xabar", message="Bizda yangi blog qo'yildi ", recipient_list=['jahongir192006@gmail.com'], from_email=settings.EMAIL_HOST_USER)

