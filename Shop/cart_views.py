from django.http import Http404
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from Shop.models import Product, Cart

def cart_add(request, slug, product_id):
    obj = lookup_object(Product.objects, product_id, slug, 'slug')
    quantity = request.GET.get('quantity', 1)
    cart = get_shopping_cart(request)
    cart.add_item(obj, quantity)
    update_shopping_cart(request, cart)
    ctx = {'object': obj, 'cart': cart}
    return render_to_response('cart/add_to_cart.html', ctx, context_instance=RequestContext(request))

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

def shopping_cart(request, template_name='orders/shopping_cart.html'):
    cart = get_shopping_cart(request)
    ctx = {'cart': cart}
    return render_to_response(template_name, ctx, context_instance=RequestContext(request))