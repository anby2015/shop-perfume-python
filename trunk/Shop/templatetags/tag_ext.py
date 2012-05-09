from django import template
from Shop.menus import get_main_menu, get_menu_path
from Shop.models import Category

register = template.Library()

@register.inclusion_tag('menu.html')
def render_menu(category):
    menus = get_main_menu()
    paths = []

    if isinstance(category, Category):
        paths = get_menu_path(category)

    return { 'menus' : menus, 'paths' : paths }


