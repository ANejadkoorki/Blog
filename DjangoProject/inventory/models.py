from django.db import models
from django.utils.translation import ugettext as _
from . import enums


# Create your models here.
class Product(models.Model):
    """
    Represents A single Product
    """
    name = models.CharField(
        max_length=200,
        verbose_name='Product`s name',
        db_index=True,
    )
    description = models.TextField(
        verbose_name=_('Description'),
        help_text='Description text to describe the product',
    )
    price = models.PositiveIntegerField(default=0, db_index=True)
    qty_in_stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(
        default=False,
        help_text='Will this product be sold?',
    )
    type = models.CharField(
        max_length=100,
        choices=enums.ProductTypes.choices
    )
