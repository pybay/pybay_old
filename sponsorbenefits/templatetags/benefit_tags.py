import datetime
from django import template
from django.utils.safestring import mark_safe
from django.template.defaultfilters import stringfilter

from sponsorbenefits.models import BenefitRow

register = template.Library()

@register.simple_tag(takes_context=True)
def load_benefits(context):
    context['benefits'] = BenefitRow.objects.all().order_by('order')
    return ''

@register.filter
@stringfilter
def checkmark(text):
    checkmark = '<span class="glyphicon glyphicon-ok"></span>'
    output = checkmark if text.lower() == 'yes' else '<span>{}</span>'.format(text)
    return mark_safe(output)
