from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.vending.models import Place


@receiver(post_save, sender=Place)
def create_qr_code(sender, instance, **kwargs):
    if not instance.qr_code:
        instance.generate_qr_code()
        instance.save()
