from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import AddressModel, CurrentAddressModel


@receiver(post_save, sender=AddressModel)
def create_or_update_current_address(sender, instance, created, **kwargs):
    if created:
        # Check if a current address already exists for the user
        CurrentAddressModel.objects.update_or_create(user=instance.user, defaults={'address': instance})
