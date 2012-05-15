from django.http import Http404
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
from Shop.forms import ProductDetailForm
from Shop.models import Product, Cart, Item

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

    return redirect(last_url.replace('_','/'))

def cart_config(request, product_id):
    cart = get_shopping_cart(request)
    item = cart.get_item_by_product_id(int(product_id))

    if item is None:
        product = Product.objects.get(id=product_id)
        cart.add_item(product, 1)
        item = cart.get_item_by_product_id(int(product_id))

    if request.method == 'POST':
        form = ProductDetailForm(request.POST)
        if form.is_valid():
            item.quantity = int(form.cleaned_data['quantity'])
            update_shopping_cart(request, cart)
    else:
        form = ProductDetailForm()

    viewmodel = {'current' : item.product, 'form' : form}

    ctx = {'viewmodel': viewmodel}

    return render_to_response('Shop/product_detail.html', ctx, context_instance=RequestContext(request))


