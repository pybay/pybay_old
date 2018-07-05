from django import template

from symposion.sponsorship.models import Sponsor

register = template.Library()


@register.inclusion_tag('frontend/sponsors_footer.html', takes_context=True)
def sponsors_footer(context):
    sponsors = Sponsor.objects.filter(active=True)
    return {
        'sponsors': sponsors,
    }


@register.filter
def get_logo(sponsor):
    """Copied and modified from symposion.sponsorship.models.Sponsor - set object.sponsor_logo if not set."""
    if sponsor.sponsor_logo is None:
        benefits = sponsor.sponsor_benefits.filter(benefit__type__in=["weblogo", "simple"], upload__isnull=False)
        for benefit in benefits:
            if benefit.upload:
                sponsor.sponsor_logo = benefit
                sponsor.save()
                break  # Only do this for the first upload on a benefit
    # Never crash due to missing logo!
    if getattr(sponsor.sponsor_logo, 'upload', None):
        return sponsor.sponsor_logo.upload.url
    else:
      return ""
