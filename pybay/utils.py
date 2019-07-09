from pybay.proposals.models import Proposal
from symposion.speakers.models import Speaker


def get_accepted_speaker_by_slug(speaker_slug):
    """
    This function is purposely done do avoid touching Symposion
    source code. Given the amount of approved speakers is not
    substantial, it's better to iterate over speakers, slugify name,
    and check equality, than create a new field in Symposion.
    """
    approved_talks = Proposal.objects.filter(
        result__status='accepted'
    ).prefetch_related('speaker')
    for approved_talk in approved_talks:
        speakers = {speaker.name_slug: speaker for speaker in approved_talk.speakers()}
        if speaker_slug in speakers:
            return speakers[speaker_slug]

    raise Speaker.DoesNotExist()
