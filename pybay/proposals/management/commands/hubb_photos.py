import argparse
import json
import logging
from urllib.request import urlretrieve


from django.core.management.base import BaseCommand, CommandError
from django.core.files import File

from django.contrib.auth.models import User
from symposion.speakers.models import Speaker


class AttrDict(dict):
    def __init__(self, dct):
        super(AttrDict, self).__init__(**dct)
        self.__dict__ = self


def update_photo(data, force):
  for record in data['speakers']:
    record = AttrDict(record)
    speaker = Speaker.objects.filter(invite_email=record.speaker_email).first()
    if not speaker:
      print("Speaker not found for user {}".format(record))
      return
    photo_url = record.photo
    update = not speaker.photo or force
    if photo_url and update:
      print("downloading {} for {}".format(photo_url, speaker))
      path, _ = urlretrieve(photo_url)
      with open(path, 'rb') as fp:
        speaker.photo.save(speaker.name_slug + ".jpg", File(fp))
        print("saving {}".format(speaker.photo))


class Command(BaseCommand):
    help = 'import talks/speakers/slots'

    def add_arguments(self, parser):
        parser.add_argument('--data', help="json data file to import", type=argparse.FileType('r'), default=None)
        parser.add_argument('--force', help="Update existing photos", default=False)

    def handle(self, *args, **options):
      data = json.load(options['data'])
      for record in data:
        record = AttrDict(record)
        update_photo(record, options['force'])
