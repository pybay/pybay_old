import argparse
import json
import sys
from django.core.management.base import BaseCommand, CommandError

from pybay.proposals.models import TalkProposal
from django.contrib.auth.models import User
from symposion.speakers.models import Speaker
from symposion.proposals.models import AdditionalSpeaker


proposal_keys = ["audience_level", "theme", "length", "what_attendees_will_learn",
        "title", "description", "abstract", "additional_notes"]

speaker_keys = ['first_name', 'last_name', 'biography']

user_keys = ['email']

# Create conference and section in the admin and use a hard coded value to import talks
# Create schedule which has a section, dates, and talk kinds and publish/not publish. All this in the admin
# Create rooms which have a room names

slots = "name day kind start end".split()
slot_room = ["slot_id", "room_id"]

session = ['day_id', 'slots'] # Maybe I don't need these?


class AttrDict(dict):
    def __init__(self, dct):
        super(AttrDict, self).__init__(**dct)
        self.__dict__ = self
        self.audience_level = 1
        self.theme = 'ai'
        self.length=25
        self.what_attendees_will_learn = "asdf"
        self.abstract = ''

PIPELINE = [{
  "audience_level": 1,
  "theme": 'ai',
  "length": 25,
  "what_attendees_will_learn": "asdf",
  "title": "My talk",
  "description": "It's got some stuff!",
  "abstract": "even more stuff",
  "additional_notes": "lastly",
  "speakers": [{"speaker_email": "jon@aol.com",
                "first_name": "Jon",
                "last_name": "Snow",
                "speaker_biography": "Keeping watch"},
               {"speaker_email": "arya@aol.com",
                "first_name": "Arya",
                "last_name": "Stark",
                "speaker_biography": "Valar Morghulis"}],
  "start_time": "2018-08-17 09:00:00",
  "end_time": "2018-08-17 09:45:00",
  "room": "Robertson",
}]


def copyattr(frm, to, key):
  setattr(to, key, getattr(frm, key))

def create_talk_proposal(data):
  tp = TalkProposal.with_kind()
  data = AttrDict(data)
  speakers = []
  for record in data.speakers:
    record = AttrDict(record)
    user, created = User.objects.get_or_create(username=record.speaker_email)
    if created:
      user.email = record.speaker_email
      user.save()
    speaker, created = Speaker.objects.get_or_create(user=user)
    if created:
      speaker.name = " ".join([record.first_name, record.last_name])
      speaker.user = user
      speaker.save()
    speakers.append(speaker)

  for key in proposal_keys:
    copyattr(data, tp, key)
  first_speaker, *rest = speakers
  tp.speaker = first_speaker
  tp.save()
  for speaker in rest:
    a = AdditionalSpeaker(speaker=speaker,
                          proposalbase=tp,
                          status=AdditionalSpeaker.SPEAKING_STATUS_ACCEPTED)
    a.save()

  return tp

def create_slot(data):
  pass

class Command(BaseCommand):
    help = 'import talks/speakers/slots'

    def add_arguments(self, parser):
        parser.add_argument('--data', help="json data file to import", type=argparse.FileType('r'), default=None)

    def handle(self, *args, **options):
      if options['data']:
        data = json.load(options['data'])
      else:
        data = PIPELINE
      for record in data:
        tp = create_talk_proposal(record)
        self.stdout.write(self.style.SUCCESS('Successfully created proposal "%s"' % tp))
