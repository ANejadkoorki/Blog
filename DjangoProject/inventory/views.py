from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from rest_framework import generics
from . import models, serializers


class ListProductView(ListView):
    """
        show`s a list of active products
    """
    queryset = models.Product.objects.filter(
        is_active=True,
    )

    extra_context = {'page_title': 'Products'}


"""
    REST Views
"""


class ProductsList(generics.ListAPIView):
    """
        REST List View for product model
    """
    queryset = models.Product.objects.filter(is_active=True)
    serializer_class = serializers.ProductSerializer
