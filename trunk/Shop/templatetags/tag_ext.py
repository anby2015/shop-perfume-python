from django import template
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
def render_product_list(product_list):
    return { 'product_list' : product_list }


