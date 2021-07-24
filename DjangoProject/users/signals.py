from django.contrib.auth import get_user_model
from django.db.models.signals import post_save

from store.signals import order_placed
from django.dispatch import receiver

from users.models import Profile


@receiver(order_placed)
def send_email_when_order_is_placed(sender, **kwargs):
    """
        a callback for sending email when an order is placed.
    """

    print(f'hello from signals. {kwargs["created"]}')


@receiver(post_save, sender=get_user_model())
def make_profile_when_user_created(sender, **kwargs):
    if kwargs['created']:
        Profile.objects.create(user= kwargs['instance'])

