import datetime
from django import template

register = template.Library()

@register.filter
def three_col_class(object):
    if object.title_3:
        return "col-md-4 col-sm-6"
    elif object.title_2:
        return "col-md-6 col-sm-12"
    else:
        return "col-md-12 col-sm-12"
