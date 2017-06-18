from django.template.defaultfilters import slugify

from pybay.proposals.models import TalkProposal
from symposion.speakers.models import Speaker


def get_slugged_name_from_speaker(speaker):
    return slugify(speaker.name)


def get_accepted_speaker_by_slug(speaker_slug):
    """
    This function is purpously done do avoid touching Symposion
    source code. Given the amount of approved speakers is not
    substantial, it's better to iterate over speakers, slugify name,
    and check equality, than create a new field in Symposion.
    """
    approved_talks = TalkProposal.objects.filter(
        result__status='accepted'
    ).prefetch_related('speaker')
    for approved_talk in approved_talks:
        if get_slugged_name_from_speaker(approved_talk.speaker) == speaker_slug:
            return approved_talk.speaker

    raise Speaker.DoesNotExist()
