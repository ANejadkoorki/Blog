import jdatetime
import pytz
from django.conf import settings
from django.core.management import BaseCommand

from store import enums
from store.models import Order


class Command(BaseCommand):

    def handle(self, *args, **options):
        qs = Order.objects.filter(status=enums.OrderStatuses.CREATED, )
        today = jdatetime.datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
        for order in qs:
            order_date = order.created_on
            diff = today  - order_date
            if diff.days > 1:
                order.set_as_canceled()
                print(f'order {order.pk} set as canceled.')
            else:
                print(f'the order {order.pk} is less than one day old.')