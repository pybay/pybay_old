import json
import itertools

from django.shortcuts import render
from django.http import (HttpResponse, HttpResponseForbidden,
                         HttpResponseNotFound)
from django.views.generic import TemplateView
from django.db.models import Prefetch

from .forms import CallForProposalForm
from pybay.faqs.models import Faq, Category
from symposion.sponsorship.models import Sponsor
from pybay.proposals.models import TalkProposal, Proposal
from pybay.utils import get_accepted_speaker_by_slug
from symposion.speakers.models import Speaker
from symposion.schedule.models import Schedule

from collections import defaultdict
from django.conf import settings

from logging import getLogger

log = getLogger(__file__)

cfp_close_date = settings.PROJECT_DATA['cfp_close_date']


def pybay_sponsors_list(request):
    active_sponsors = Sponsor.objects.filter(active=True).order_by('name')
    sponsor_map = defaultdict(list)

    for sponsor in active_sponsors:
        sponsor_map[sponsor.level.name].append(sponsor)

    return render(request, 'frontend/sponsors_list.html', {
        "gold_sponsors": sponsor_map['Gold'],
        "silver_sponsors": sponsor_map['Silver'],
        "bronze_sponsors": sponsor_map['Bronze'],
        "bronze_logo": "",
        "gold_logo": "",
        "silver_logo": "",
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
    speaker_approved_talks = TalkProposal.objects.filter(
        speaker=speaker
    ).filter(result__status='accepted')

    return render(request, 'frontend/speakers_detail.html',
                  {'speaker': speaker, 'talks': speaker_approved_talks,
                   'speaker_website': speaker_approved_talks[0].speaker_website})


def pybay_speakers_list(request):
    accepted_proposals = TalkProposal.objects.filter(result__status='accepted')
    speakers = []
    for proposal in accepted_proposals:
        speakers += list(proposal.speakers())

    speakers = list(set(speakers))  # filters duplicate speakers
    speakers = sorted(speakers, key=lambda i: i.name)  # sorts alphabetically

    return render(request, 'frontend/speakers_list.html', {
        'speakers': speakers
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
        "category": proposal.category,
        "what_will_attendees_learn": proposal.what_will_attendees_learn,
        # "title": proposal.talk_links,
        # "title": proposal.meetup_talk,
        "speaker_and_talk_history": proposal.speaker_and_talk_history,
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
        slots = list(grouper)
        kind = slots[0].kind if len(slots) == 1 and slots[0].content_override else ''
        yield time, slots, kind


FILTER_CATEGORIES = [
    "All things Web",
    "DevOps",
]


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

    filters = [
        (name.lower().replace(' ', ''), name)
        for name in FILTER_CATEGORIES
    ]

    ctx = {
        'schedules': schedules,
        'filters' :  filters + [('other', 'Other'), ('level-1', 'Beginner-friendly')],
        'allowed_categories': [slug for slug, _ in filters]
    }

    return render(request, "frontend/schedule.html", ctx)
