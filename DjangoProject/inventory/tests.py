from django.test import TestCase

# Create your tests here.
from inventory import models, enums


class ProductTestCase(TestCase):
    """
        test for Product model
    """
    def setUp(self):
        """
            set up the test requirements
        """
        models.Product.objects.create(
            name= "TEstProd1",
            description="TestProd1Description",
            qty_in_stock=100,
            is_active=True,
            type= enums.ProductTypes.PRINT,
        )

    def test_deduct_from_stock(self):
        obj = models.Product.objects.first()
        qty = obj.deduct_from_stock(10)
        self.assertEqual(qty, 90)
