from django.template import Library


register = Library()


@register.simple_tag
def value_from_list_or_default(val, allowed_values, default):
    return val if val in allowed_values else default
