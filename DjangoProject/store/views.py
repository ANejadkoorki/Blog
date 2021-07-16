from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from inventory import models as inventorymodels


# Create your views here.


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

