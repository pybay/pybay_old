import datetime
from django import template

from menu.models import MenuItem

register = template.Library()

@register.inclusion_tag('menu/menu.html')
def menu():
  top = MenuItem.objects.select_related().all()
  return {'menuitems': top}
