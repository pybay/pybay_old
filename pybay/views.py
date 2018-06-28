import datetime
import json
import itertools

from django.shortcuts import render
from django.http import (HttpResponse, HttpResponseForbidden,
                         HttpResponseNotFound)
from django.views.generic import TemplateView
from django.db.models import Prefetch
from django.utils import timezone

from .forms import CallForProposalForm
from pybay.faqs.models import Faq, Category
from symposion.sponsorship.models import Sponsor
from pybay.proposals.models import TalkProposal, Proposal
from pybay.countdowns.models import Countdown
from pybay.utils import get_accepted_speaker_by_slug
from symposion.speakers.models import Speaker
from symposion.schedule.models import Schedule

from collections import defaultdict
from django.conf import settings

from logging import getLogger

log = getLogger(__file__)

cfp_close_date = settings.PROJECT_DATA['cfp_close_date']


SOME_TIME_IN_THE_FAR_FUTURE = (datetime.date(3018, 6, 27), datetime.time(23, 59))


def _make_proposal_sort_key(proposal):
    """Returns a key that can be used to sort proposals based on date

    If proposal is not slotted or is a presentation. It will be bumped
    to the end (sorted with lowest propority, at the end of everything else)

    :param propoal: a proposal instance
    :return: a sortable key
    """
    try:
        proposal_slot = proposal.presentation.slot
    except AttributeError:
        return SOME_TIME_IN_THE_FAR_FUTURE

    if not proposal_slot:
        return SOME_TIME_IN_THE_FAR_FUTURE

    return (proposal_slot.day.date, proposal_slot.start)


def pybay_sponsors_list(request):
    active_sponsors = Sponsor.objects.filter(active=True).order_by('name')
    sponsor_map = defaultdict(list)

    for sponsor in active_sponsors:
        sponsor_map[sponsor.level.name].append(sponsor)

    return render(request, 'frontend/sponsors_list.html', {
        "gold_sponsors": sponsor_map['Gold'],
        "silver_sponsors": sponsor_map['Silver'],
        "bronze_sponsors": sponsor_map['Bronze'],
        "diversity_sponsors": sponsor_map['Diversity'],
        "bronze_logo": "",
        "gold_logo": "",
        "silver_logo": "",
        "diversity_logo": "",
    })


def pybay_faq_index(request):
    faqs = Category.objects.faqs_per_category()
    return render(request, 'frontend/faq.html', {'faq_categories': faqs})


class FaqTemplateView(TemplateView):

    faq_filter = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filters = {}
        if self.faq_filter is not None:
            filters[self.faq_filter] = True
        context['faqs'] = Faq.objects.filter(**filters)
        return context


class FrontpageView(FaqTemplateView):
    @classmethod
    def as_view(cls, **kwargs):
        return super().as_view(template_name="frontend/index.html", **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        countdown = Countdown.objects.filter(date__gt=timezone.now()).first()
        if countdown:
            context['countdown'] = countdown.context_for_template()
        return context


def pybay_cfp_create(request):
    if request.method == 'POST':
        form = CallForProposalForm(request.POST)

        # Validate form
        if not form.is_valid():
            return render(request, 'frontend/cfp.html', {'form': form})

        # Create speaker and associated talk
        speaker, proposal = form.save_to_models()
        return render(request, 'frontend/cfp_submitted.html', {
            'speaker': speaker,
            'proposal': proposal,
        })

    else:
        form = CallForProposalForm()
        return render(request, 'frontend/cfp.html',
            {'form': form, 'cfp_close_date': cfp_close_date})


def pybay_speakers_detail(request, speaker_slug):

    # Fetch speaker
    try:
        speaker = get_accepted_speaker_by_slug(speaker_slug)
    except Speaker.DoesNotExist:
        log.error("Speaker %s does not have any approved talks or does not exist", speaker_slug)
        return HttpResponseNotFound()

    # NOTE: Cannot perform reverse lookup (speaker.talk_proposals) for some reason.
    speaker_approved_talks = [
        prop.talkproposal if hasattr(prop, 'talkproposal') else prop.tutorialproposal
        for prop in Proposal.objects.filter(speaker=speaker)
        .filter(result__status='accepted')
        .prefetch_related('talkproposal', 'tutorialproposal')
    ]

    # Sort talks by date first, and then by time
    speaker_approved_talks.sort(key=_make_proposal_sort_key)

    return render(request, 'frontend/speakers_detail.html',
                  {'speaker': speaker, 'talks': speaker_approved_talks,
                   'speaker_website': speaker_approved_talks[0].speaker_website})


def pybay_speakers_list(request):
    accepted_proposals = Proposal.objects.filter(result__status='accepted')
    speakers = []
    for proposal in accepted_proposals:
        speakers += list(proposal.speakers())

    speakers = list(set(speakers))  # filters duplicate speakers
    speakers = sorted(speakers, key=lambda i: i.name)  # sorts alphabetically

    # Make them chunks of 2
    chunks = []
    for chunk_idx in range(0, len(speakers), 2):
        chunks.append(speakers[chunk_idx:chunk_idx + 2])

    return render(request, 'frontend/speakers_list.html', {
        'chunks': chunks
    })


def undecided_proposals(request):
    api_token = request.GET.get('token')
    if api_token != settings.PYBAY_API_TOKEN:
        return HttpResponseForbidden()

    undecided_proposals = Proposal.objects.all()
    result = []
    for proposal in undecided_proposals:
        if proposal.status.lower() == "undecided":
            result.append({'id': proposal.id})

    return HttpResponse(json.dumps({'data': result}), content_type="application/json")


def proposal_detail(request, proposal_id):

    api_token = request.GET.get('token')
    if api_token != settings.PYBAY_API_TOKEN:
        return HttpResponseForbidden()

    proposal = TalkProposal.objects.get(id=proposal_id)
    speakers_list = []
    for speaker in proposal.speakers():
        speakers_list.append({"email": speaker.email, "name": speaker.name, })

    details = {
        "id": proposal.id,
        "description": proposal.description,
        "abstract": proposal.abstract,
        "additional_notes": proposal.additional_notes,
        "title": proposal.title,
        "audience_level": TalkProposal.AUDIENCE_LEVELS[proposal.audience_level-1][1],
        "category": proposal.themes,
        "what_attendees_will_learn": proposal.what_attendees_will_learn,
        # "title": proposal.talk_links,
        # "title": proposal.meetup_talk,
        "speaker_and_talk_history": proposal.speaker_and_talk_history,
        "talk_length": proposal.talk_length,
    }

    result = {
        "speakers": speakers_list,
        "details": details,
    }

    return HttpResponse(
        json.dumps({'data': result}), content_type="application/json"
    )


def _day_slots(day):
    groupby = itertools.groupby(day.slot_set.all(), lambda slot: slot.start)
    for time, grouper in groupby:
        slots = sorted(grouper, key=lambda slot: slot.rooms[0].order if slot.rooms else 0)
        kind = slots[0].kind if len(slots) == 1 and slots[0].content_override else ''
        yield time, slots, kind


FILTER_CATEGORIES = [
    (description, [slug])
    for slug, description in Proposal.THEME_CHOICES]

FILTER_CATEGORIES.append(('Beginner-friendly', ['level-1']))


def pybay_schedule(request):
    if request.user.is_staff:
        schedules = Schedule.objects.filter(hidden=False)
    else:
        schedules = Schedule.objects.filter(published=True, hidden=False)

    schedules.prefetch_related(
        Prefetch('day_set__slot_set__presentation_set__proposal_base'),
    )

    schedules = [
        [(day, _day_slots(day)) for day in schedule.day_set.all()]
        for schedule in schedules
    ]

    ctx = {
        'schedules': schedules,
        'filters' :  FILTER_CATEGORIES,
    }

    return render(request, "frontend/schedule.html", ctx)
