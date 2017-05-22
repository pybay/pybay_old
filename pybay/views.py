from django.shortcuts import render

from .forms import CallForProposalForm
from pybay.faqs.models import Faq
from symposion.sponsorship.models import Sponsor
from pybay.proposals.models import Proposal

from collections import defaultdict


def pybay_sponsors_list(request):
    active_sponsors = Sponsor.objects.filter(active=True).order_by('name')
    sponsor_map = defaultdict(list)

    for sponsor in active_sponsors:
        sponsor_map[sponsor.level.name].append(sponsor)

    return render(request, 'frontend/sponsors_list.html', {
        "bronze_sponsors": sponsor_map['Bronze'],
        "gold_sponsors": sponsor_map['Gold'],
        "silver_sponsors": sponsor_map['Silver'],
    })


def pybay_faq_index(request):
    faqs = Faq.objects.order_by('ordering').all()
    return render(request, 'frontend/faq.html', {'faqs': faqs})


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
        return render(request, 'frontend/cfp.html', {'form': form})


def pybay_speakers_list(request):
    accepted_proposals = Proposal.objects.filter(
        result__status='accepted')
    speakers = []
    for proposal in accepted_proposals:
        speakers += list(proposal.speakers())

    speakers = list(set(speakers))  # filters duplicate speakers
    speakers = filter(lambda s: s.photo, speakers)  # filters speakers without photo
    speakers = sorted(speakers, key=lambda i: i.name)  # sorts alphabetically

    return render(request, 'frontend/speakers_list.html', {
        'speakers': speakers
    })
