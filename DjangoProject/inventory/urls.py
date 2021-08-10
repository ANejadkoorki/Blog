from django.urls import path
from . import views

app_name = 'inventory'
urlpatterns = [
    path('', views.ListProductView.as_view(), name='list'),
    path('api/v1', views.ProductsList.as_view(), name=''),
    path('list2/', views.product_list, name='list2'),
    path('list3/', views.ProductList2.as_view(), name='list3'),
]
