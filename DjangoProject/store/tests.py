from django.test import TestCase

# Create your tests here.
from django.urls import reverse


class MyOrdersViewtestCase(TestCase):
    """
        test ListOrders view
    """

    def setUp(self):
        pass

    def test_auth_required(self):
        """
            tests if view redirects anonymous user to log in page
        """
        response = self.client.get(reverse('store:list-orders'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/Login/', response.url)
        response = self.client.get(reverse('store:list-orders'), follow=True)
        self.assertContains(response,'Log in')
