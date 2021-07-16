from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from inventory import models as inventorymodels


# Create your views here.


def add_to_cart(request, product_id):
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
    request.session.save()

    messages.success(request, f'The product \"{product_instance.name}\" added to cart .')
    return redirect('inventory:list')


def view_cart(request):
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
