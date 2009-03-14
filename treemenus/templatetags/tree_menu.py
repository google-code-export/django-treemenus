from django import template

from django.template.defaulttags import url, URLNode
from django.template import Node

from treemenus.models import Menu, MenuItem
from treemenus.config import APP_LABEL


register = template.Library()

def show_menu(context, menu_name, menu_type=None):
    menu = Menu.objects.get(name=menu_name)
    context['menu'] = menu
    if menu_type:
        context['menu_type'] = menu_type
    return context
register.inclusion_tag('%s/menu.html' % APP_LABEL, takes_context=True)(show_menu)


def show_menu_item(context, menu_item):
    if not isinstance(menu_item, MenuItem):
        raise template.TemplateSyntaxError, 'Given argument must be a MenuItem object.'
    
    context['menu_item'] = menu_item
    return context
register.inclusion_tag('%s/menu_item.html' % APP_LABEL, takes_context=True)(show_menu_item)