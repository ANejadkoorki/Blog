from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from . import models


class ListProductView(ListView):
    """
        show`s a list of active products
    """
    queryset = models.Product.objects.filter(
        is_active=True,
    )

    extra_context = {'page_title': 'Products'}
