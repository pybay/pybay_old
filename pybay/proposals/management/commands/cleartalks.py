from django.core.management.base import BaseCommand, CommandError

from pybay.proposals.models import TalkProposal
from django.contrib.auth.models import User
from symposion.speakers.models import Speaker
from symposion.schedule.models import Slot


class Command(BaseCommand):
    help = 'import talks/speakers/slots'

    def handle(self, *args, **options):
      speakers = []
      users = []
      speakers = [tp.speaker for tp in TalkProposal.objects.all()]
      users = [speaker.user for speaker in speakers if not speaker.user.is_staff]
      TalkProposal.objects.all().delete()
      map(lambda speaker: speaker.delete, speakers)
      map(lambda user: user.delete, users)
      Slot.objects.all().delete()
