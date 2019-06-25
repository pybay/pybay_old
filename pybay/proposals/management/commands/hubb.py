import argparse
from datetime import datetime
import json
import logging
import re
import sys

from django.core.management.base import BaseCommand, CommandError
from pybay.proposals.models import TalkProposal, THEMES
from django.contrib.auth.models import User
from symposion.speakers.models import Speaker
from symposion.proposals.models import AdditionalSpeaker
from symposion.schedule.models import Day, Presentation, Slot, SlotKind, SlotRoom, Room
from symposion.conference.models import Section
from symposion.reviews.models import ProposalResult

proposal_keys = ["audience_level", "themes", "talk_length", "what_attendees_will_learn",
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


PIPELINE = [{
  "audience_level": "Advanced",
  "themes": 'ai',
  "talk_length": "25 mins",
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
  try:
    setattr(to, key, getattr(frm, key))
  except AttributeError:
    #print("Couldn't get key %s from data %s" % (key, frm))
    setattr(to, key, "")

COMMA_PAT = re.compile(r",(?=[\w&])")
reverse_themes = {v: k for k,v in THEMES.items()}


def create_talk_proposal(data):
  tp = TalkProposal.with_kind()
  # Special cases
  data.audience_level = TalkProposal.audience_text(data.audience_level)
  data.talk_length = int(data.talk_length.split()[0])
  themes = COMMA_PAT.split(getattr(data, 'theme', ""))
  real_themes = [reverse_themes[desc] for desc in themes if desc in reverse_themes]
  if len(themes) > len(real_themes):
    print("Can't find all themes in %s" % themes)
  data.themes = ",".join(real_themes)

  # Speakers
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
      speaker.invite_email = record.speaker_email
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

def dt(s):
  return datetime.strptime(s, "%Y-%m-%dT%H:%M:%S-07:00")


def create_slot(record, tp, slotkind):
  room = Room.objects.filter(name=record.room).first()
  section = Section.objects.filter(slug='talks').first()
  start = dt(record.start_time)
  end = dt(record.end_time)
  day = Day.objects.filter(date=start.date()).first()
  # Make the slot
  s = Slot(name=record.slot[:100], day=day, kind=slotkind, start=start, end=end)
  s.save()
  # Assign room to slot
  sr = SlotRoom(slot=s, room=room)
  sr.save()
  # Create presentation
  p = Presentation(slot=s,
                   title=tp.title,
                   description=tp.description,
                   abstract=tp.abstract,
                   speaker=list(tp.speakers())[0],
                   proposal_base_id=tp.id,
                   section=section)
  p.save()
  return p


class Command(BaseCommand):
    help = 'import talks/speakers/slots'

    def add_arguments(self, parser):
        parser.add_argument('--data', help="json data file to import", type=argparse.FileType('r'), default=None)

    def handle(self, *args, **options):
      if options['data']:
        data = json.load(options['data'])
      else:
        data = PIPELINE
      slotkind = SlotKind.objects.filter(label='talks').first()
      for record in data:
        record = AttrDict(record)
        tp = create_talk_proposal(record)
        self.stdout.write(self.style.SUCCESS('Successfully created proposal "%s"' % tp))
        p = create_slot(record, tp, slotkind)
        self.stdout.write(self.style.SUCCESS('Successfully created presentation "%s"' % p))
        # Finally set status to accepted
        ProposalResult(proposal=tp, accepted=True, status="accepted").save()
