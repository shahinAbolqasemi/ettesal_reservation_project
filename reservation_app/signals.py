from django.conf import settings
from django.db.models.signals import (
    pre_save, post_save
)
from django.dispatch import receiver


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def user_post_save(sender, instance, created, *args, **kwargs):
    """
    """
    pass
