from django.shortcuts import render, get_object_or_404

from .models import TalkProposal


def index(request):
    return render(request, 'proposals/index.html', {'proposals': TalkProposal.objects.all()})
