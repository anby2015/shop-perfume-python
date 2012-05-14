from django.http import Http404
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
from Shop.models import Product, Cart

def cart_add(request, slug, product_id):
    obj = lookup_object(Product.objects, product_id, slug, 'slug')
    quantity = request.GET.get('quantity', 1)
    cart = get_shopping_cart(request)
    cart.add_item(obj, quantity)
    update_shopping_cart(request, cart)

    return redirect('cart_shopping_cart')

def lookup_object(queryset, object_id=None, slug=None, slug_field=None):
    if object_id is not None:
        obj = queryset.get(pk=object_id)
    elif slug and slug_field:
        kwargs = {slug_field: slug}
        obj = queryset.get(**kwargs)
    else:
        raise Http404
    return obj

def get_shopping_cart(request, cart_class=Cart):
    return request.session.get('cart', None) or cart_class()

def update_shopping_cart(request, cart):
    request.session['cart'] = cart

def shopping_cart(request):
    cart = get_shopping_cart(request)
    ctx = {'items': cart.items, 'length' : cart.get_length() }
    return render_to_response('cart/shopping_cart.html', ctx, context_instance=RequestContext(request))

def cart_remove(request, itemid, last_url):
    cart = get_shopping_cart(request)
    cart.remove_item(int(itemid))
    update_shopping_cart(request, cart)

    return redirect(last_url)

def cart_config(request, itemid):
    cart = get_shopping_cart(request)
    viewmodel = {'current' : cart.get_item(int(itemid)).product}
    ctx = {'viewmodel': viewmodel}

    return render_to_response('Shop/product_detail.html', ctx, context_instance=RequestContext(request))
