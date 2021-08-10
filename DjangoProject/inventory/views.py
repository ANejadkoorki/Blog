from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from rest_framework import generics, status
from rest_framework.response import Response as drf_response
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

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


@api_view(['GET', 'POST'])
def product_list(request):
    """
        list products
    """
    if request.method == 'GET':
        qs = models.Product.objects.all()
        serializer = serializers.ProductSerializer(data=qs, many=True)
        serializer.is_valid()
        return JsonResponse(serializer.data, safe=False)

    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = serializers.ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(data=serializer.data, status=201)
        return JsonResponse(data=serializer.errors, status=400)


class ProductList2(APIView):
    """
        List all products, or create a new product.
    """

    def get(self, request, format=None):
        snippets = models.Product.objects.all()
        serializer = serializers.ProductSerializer(snippets, many=True)
        return drf_response(serializer.data)

    def post(self, request, format=None):
        serializer = serializers.ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return drf_response(serializer.data, status=status.HTTP_201_CREATED)
        return drf_response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
