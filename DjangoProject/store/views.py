import logging
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from rest_framework.decorators import action
from rest_framework.exceptions import NotAuthenticated

from inventory import models as inventorymodels
from rest_framework import viewsets, permissions, status

from . import models, serializers, permissions as my_permissions

# Create your views here.
logger = logging.getLogger(__name__)


def add_to_cart(request, product_id):
    """
        add a product to cart
    """
    product_instance = get_object_or_404(klass=inventorymodels.Product, pk=product_id)

    # check if product can be sold
    if not product_instance.can_be_sold():
        messages.error(request, 'This Product can`t be sold.')
        return redirect('inventory:list')

    # check if product is in stock
    if not product_instance.is_in_stock(1):
        messages.error(request, 'This Product with this qty  is Not available.')
        return redirect('inventory:list')

    if 'cart' not in request.session.keys():
        request.session['cart'] = {
            # '1': 1
            # product_id = qty
        }
    if str(product_instance.pk) in request.session['cart'].keys():
        request.session['cart'][str(product_instance.pk)] += 1
    else:
        request.session['cart'][str(product_instance.pk)] = 1
    # save the Session
    request.session.modified = True

    messages.success(request, f'The product \"{product_instance.name}\" added to cart .')
    return redirect('inventory:list')


def view_cart(request):
    """
        renders the cart items.
    """
    object_list = []

    for item in request.session.get('cart', []):
        object_list += [
            {
                'product': inventorymodels.Product.objects.get(pk=int(item)),
                'qty': request.session['cart'][item],
            }
        ]

    return render(request, 'store/view_cart.html', context={
        'page_title': 'cart',
        'object_list': object_list
    })


def deletee_row(request, product_id):
    """
        deletes a product row
    """
    request.session['cart'].pop(str(product_id), None)
    request.session.modified = True
    messages.success(request, 'Removed Successfully.')
    return redirect('store:view-cart')


@require_POST
@csrf_exempt
def deduct_from_cart(request):
    """
        deducts one from product qty
    """
    product_id = request.POST.get('product_id', None)
    # what if no product_id provided?
    if not product_id:
        return JsonResponse(
            {
                'success': False,
                'error': 'The Input Data is Invalid.'
            },
            status=400
        )
    # Cast product_id to string
    product_id = str(product_id)
    # try to minus qty
    try:
        request.session['cart'][product_id] -= 1
        request.session.modified = True
        return JsonResponse(
            {
                'success': True,
                'qty': request.session['cart'][product_id]
            },
            status=200
        )
    # what if product is not in cart
    except KeyError:
        return JsonResponse(
            {
                'success': False,
                'error': 'The Input Data is Invalid. Not in the cart'
            },
            status=400
        )


"""
   DRF REST Views
"""


class OrderViewSet(viewsets.ModelViewSet):
    """
        Viewset for store.Order
    """
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSeralizer
    permission_classes = [my_permissions.IsOwnerOrReadOnly]

    # def filter_queryset(self, queryset):
    #     super().filter_queryset(queryset)
    #     return queryset.filter(owner=self.request.user)

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_anonymous:
            raise NotAuthenticated('You need to be Logged In')
        return qs.filter_by_owner(self.request.user)

    @action(detail=True, description='Cancels an order', )
    def cancel_order(self, request, *args, **kwargs):
        """
            cancels an order
        """
        order_instance = self.get_object()
        order_instance.set_as_canceled()
        order_serializer = self.get_serializer(instance=order_instance)
        return JsonResponse(data=order_serializer.data, status=status.HTTP_202_ACCEPTED)


class OrderItemViewSet(viewsets.ModelViewSet):
    """
        Viewset for store.OrderItem
    """
    queryset = models.OrderItem.objects.all()
    serializer_class = serializers.OrderItemSerializer
    permission_classes = [my_permissions.IsOwnerOfParentOrReadOnly]


@login_required
def finalize_order(request):
    """
        finalize order
    """
    cart = request.session.get('cart', None)
    # if cart does not exist
    if not cart:
        messages.error(request, 'Your Cart Is Empty.')
        return redirect('inventory:list')

    order_instance = models.Order.objects.create(owner=request.user)

    for product_id in cart:
        product = inventorymodels.Product.objects.get(pk=product_id)
        qty = cart[product_id]
        if not product.is_in_stock(qty):
            messages.error(request, f'The {product.name} with this qty doesn\'t exist ')
            return redirect('store:view-cart')
        order_item_instance = models.OrderItem.objects.create(
            order=order_instance,
            product=product,
            qty=qty,
            price=product.price,
        )
        # deduct from stock
        product.deduct_from_stock(qty)
    messages.info(request, 'Order Submitted Successfully.')
    logger.info(f'the user {request.user} placed order {order_instance.pk}')
    request.session.pop('cart')
    request.session.modified = True
    return redirect('inventory:list')


class ListOrdersView(LoginRequiredMixin, ListView):
    model = models.Order
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(owner=self.request.user)
        return qs
