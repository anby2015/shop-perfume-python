from django import template
from django.core.urlresolvers import resolve
from Shop.menus import get_main_menu, get_menu_path
from Shop.models import Category, Product

register = template.Library()

@register.inclusion_tag('menu.html')
def render_menu(current, is_display_banner=False):

    menus = get_main_menu()
    paths = []

    if isinstance(current, Category):
        paths = get_menu_path(current)

    if current is not None and isinstance(current, Product):
        paths = get_menu_path(current.category)

    return { 'menus' : menus, 'paths' : paths, 'is_display_banner' : is_display_banner }

@register.inclusion_tag('Shop/render_product_list.html')
def render_product_list(product_list, mode):
    return { 'product_list' : product_list, 'mode' : mode }

def get_request_from_context(context):
    messages = [dict.get('messages') for dict in context.dicts if dict.has_key('messages')]
    if not len(messages):
        return None

    return messages[0].request

@register.simple_tag(name='generate_url', takes_context=True)
def generate_url(context, property_name, property_value):
    dict_properties = {'pIndex' : 2, 'pSize' : 3, 'orderBy' : 4, 'sortOrder' : 5, 'mode' : 6}

    if not dict_properties.has_key(property_name):
        return None

    viewmodel = [vm.get('viewmodel') for vm in context.dicts if vm.has_key('viewmodel')]
    if not len(viewmodel):
       return None

    display_info = viewmodel[0].get('display_info', None)
    if display_info is None:
       return None

    request = get_request_from_context(context)

    url_params = [param for param in request.get_full_path().split('/') if len(param) > 0][:2]
    url_params.append(display_info['pIndex'])
    url_params.append(display_info['pSize'])
    url_params.append(display_info['orderBy'])
    url_params.append(display_info['sortOrder'])
    url_params.append(display_info['mode'])

    url_params[dict_properties.get(property_name)] = property_value

    url = '/%s/' % ('/'.join(str(param) for param in url_params))

    if param is not None:
        url += param

    return url

def get_cart_from_context(context):
    request = get_request_from_context(context)
    session = request.session
    return session.get('cart', None)

@register.inclusion_tag('cart/render_cart_block.html', takes_context=True)
def render_cart_block(context):
    request = get_request_from_context(context)
    cart = get_cart_from_context(context)

    if cart is None:
        return {'length' : 0}

    url = request.get_full_path().replace('/', '_')

    return {'total_amount' : cart.get_total_amount(), 'length' : cart.get_length(), 'items' : cart.items, 'url' : url}

def get_url_name_from_request(request):
    return resolve(request.get_full_path()).url_name

@register.simple_tag(name='get_current_url', takes_context=True)
def get_current_url(context):
    request = get_request_from_context(context)

    if request is None:
        return ''

    return request.get_full_path().replace('/', '_')

@register.simple_tag(name='get_quantity', takes_context=True)
def get_quantity(context, product_id):
    cart = get_cart_from_context(context)
    item = cart.get_item_by_product_id(product_id)
    if item is None:
        return 0
    return item.quantity




