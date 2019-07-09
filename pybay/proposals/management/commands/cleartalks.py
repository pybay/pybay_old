from django.core.management.base import BaseCommand, CommandError

from pybay.proposals.models import TalkProposal, TutorialProposal, Proposal
from django.contrib.auth.models import User
from symposion.speakers.models import Speaker
from symposion.schedule.models import Day, Presentation, Slot, SlotRoom
from symposion.reviews.models import ProposalResult


class Command(BaseCommand):
    help = 'import talks/speakers/slots'

    def handle(self, *args, **options):
      speakers = []
      users = []
      TalkProposal.objects.all().delete()
      TutorialProposal.objects.all().delete()
      Slot.objects.filter(content_override__exact='').delete()
      SlotRoom.objects.filter().delete()
      Presentation.objects.all().delete()
      ProposalResult.objects.all().delete()
