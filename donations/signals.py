from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from .models import Donation


@receiver(pre_save, sender=Donation)
def delete_old_image_on_image_update(sender, instance, **kwargs):
    if not instance.pk:
        return

    old = sender.objects.get(id=instance.pk)
    if old.image and old.image != instance.image:
        old.image.delete(save=False)


@receiver(post_delete, sender=Donation)
def delete_image_on_donation_delete(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)
