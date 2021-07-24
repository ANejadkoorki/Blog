import logging
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Sum
from django_jalali.db import models as jmodels
from django.utils.translation import ugettext_lazy as _
from . import enums

# Create your models here.
from .signals import order_placed

logger = logging.getLogger(__name__)


class Order(models.Model):
    """
    Represents an order
    """
    owner = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, verbose_name=_('owner'))
    created_on = jmodels.jDateTimeField(auto_now_add=True, verbose_name=_('Order Date'))
    status = models.CharField(
        verbose_name=_('status'),
        help_text='Product`s status',
        choices=enums.OrderStatuses.choices,
        default=enums.OrderStatuses.CREATED,
        max_length=100,
    )

    def __str__(self):
        return f'Order #{self.pk} for {self.owner.get_full_name()}'

    def set_as_canceled(self):
        self.status = enums.OrderStatuses.CANCELED
        self.save()
        logger.info(f'order #{self.pk} was set as CANCELED')
        return

    def save(self, **kwargs):
        if self.pk is None:
            created = True
        else:
            created = False

        super().save(**kwargs)

        order_placed.send(
            sender=self.__class__,
            instance=self,
            created=created,
        )
        logger.debug(f'order signal was sent for order #{self.pk}')

    def get_total_qty(self):
        """
            Sums total qty of related order items in PYTHON
            (which is inefficient)
        """
        # t = 0
        # for item in self.orderitem_set.all():
        #     t += 1
        # return t
        """
            efficiant way
        """
        t = self.orderitem_set.aggregate(Sum('qty'))
        return t.get('qty__sum', 0)

    def get_grand_total(self):
        t = 0
        for item in self.orderitem_set.all():
            t += item.qty * item.price
        return t








class OrderItem(models.Model):
    """
    a single item in the order
    """
    order = models.ForeignKey('store.Order', on_delete=models.CASCADE)
    product = models.ForeignKey('inventory.Product', on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    discount = models.FloatField(default=0)
    price = models.PositiveIntegerField()
