from django import template

from featured_speakers.models import FeaturedSpeaker

register = template.Library()


@register.inclusion_tag('featured_speakers/list.html', takes_context=True)
def featured_speakers(context):
    context['speakers'] = FeaturedSpeaker.objects.all()
    return context
