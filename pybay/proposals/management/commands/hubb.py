import sys
from django.core.management.base import BaseCommand, CommandError

from pybay.proposals.models import TalkProposal
from django.contrib.auth.models import User
from symposion.speakers.models import Speaker


proposal_keys = ["audience_level", "theme", "length", "what_attendees_will_learn",
        "title", "description", "abstract", "additional_notes"]

speaker_keys = ['first_name', 'last_name', 'biography']

user_keys = ['email']



class AttrDict(dict):
    def __init__(self, kwargs):
        super(AttrDict, self).__init__(**kwargs)
        self.__dict__ = self


pipeline = [AttrDict({
  "audience_level": 1,
  "theme": 'ai',
  "length": 25,
  "what_attendees_will_learn": "asdf",
  "title": "My talk",
  "description": "It's got some stuff!",
  "abstract": "even more stuff",
  "additional_notes": "lastly",
  "speaker_email": "jon@aol.com",
  "first_name": "Jon",
  "last_name": "Snow",
  "speaker_biography": "Blah blah Throne of swords"
})]


def copyattr(frm, to, key):
  setattr(to, key, getattr(frm, key))

def create_talk_proposal(data):
  tp = TalkProposal.with_kind()
  user, created = User.objects.get_or_create(username=data.speaker_email)
  if created:
    user.email = data.speaker_email
    user.save()

  speaker, created = Speaker.objects.get_or_create(user=user)
  if created:
    speaker.name = " ".join([data.first_name, data.last_name])
    speaker.user = user
    speaker.save()

  for key in proposal_keys:
    copyattr(data, tp, key)

  tp.speaker = speaker
  tp.save()
  return tp

class Command(BaseCommand):
    help = 'import talks/speakers/slots'

    def handle(self, *args, **options):
      #raise CommandError('Poll "%s" does not exist' % poll_id)
      for data in pipeline:
        tp = create_talk_proposal(data)
        self.stdout.write(self.style.SUCCESS('Successfully created proposal "%s"' % tp))
