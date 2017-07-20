from django import template

from symposion.reviews.models import ProposalResult
from pybay.proposals.models import Proposal

register = template.Library()

def _int0(value):
  try:
    return int(value)
  except ValueError:
    return 0

_LEVELS = dict(Proposal.AUDIENCE_LEVELS)


@register.simple_tag
def tutorial_level(tutorial):
  return _LEVELS[tutorial.audience_level]


@register.inclusion_tag('frontend/tutorials.html', takes_context=True)
def tutorials(context):
    results = ProposalResult.objects.filter(status='accepted', proposal__kind__name='tutorial')
    proposals = [r.proposal.tutorialproposal for r in results]
    half_tutorials = [p for p in proposals if _int0(p.ticket_price) < 200]
    full_tutorials = [p for p in proposals if _int0(p.ticket_price) > 200]
    return {
        'half': half_tutorials,
        'full': full_tutorials,
    }
