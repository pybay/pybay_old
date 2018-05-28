import datetime
from django import template
from django.utils.safestring import mark_safe
from django.template.defaultfilters import stringfilter

from sponsorbenefits.models import AddOnBenefitRow, AlaCarteBenefitRow, BenefitRow

register = template.Library()

@register.simple_tag(takes_context=True)
def load_benefits(context):
    context['benefits'] = BenefitRow.objects.all().order_by('order')
    return ''

@register.simple_tag(takes_context=True)
def load_alacarte_benefits(context):
    context['benefits'] = AlaCarteBenefitRow.objects.all().order_by('order')
    return ''

@register.simple_tag(takes_context=True)
def load_addon_benefits(context):
    context['benefits'] = AddOnBenefitRow.objects.all().order_by('order')
    return ''

@register.filter
@stringfilter
def checkmark(text):
    checkmark = '<span class="glyphicon glyphicon-ok"></span>'
    output = checkmark if text.lower() == 'yes' else '<span>{}</span>'.format(text)
    return mark_safe(output)

@register.filter
@stringfilter
def comma2br(text):
    output = "<br>".join(text.split(","))
    return mark_safe(output)

@register.filter
@stringfilter
def count_content_lines(text):
    output = [line for line in text.strip().split("\n")[:-1] if line.strip()]
    return len(output)
