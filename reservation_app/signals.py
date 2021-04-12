from django.conf import settings
from django.db.models.signals import (
    pre_save, post_save
)
from django.dispatch import receiver
from reservation_app.models import SessionRequest


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def user_post_save(sender, instance, created, *args, **kwargs):
    """
    sample
    """
    pass


@receiver(pre_save, sender=SessionRequest)
def session_request_pre_save(sender, instance, *args, **kwargs):
    """
    This func is for set random 5-digit number before save instance
    """
    if instance.is_accepted:
        from random import randint
        while True:
            random_uid = f'{randint(10000, 99999)}'
            if not SessionRequest.objects.filter(unique_id=random_uid).exists():
                break
        instance.unique_id = random_uid
