import argparse
from datetime import datetime
import json
import logging
import re
import sys

from django.core.management.base import BaseCommand, CommandError
from pybay.proposals.models import Proposal, TalkProposal, TutorialProposal, THEMES
from django.contrib.auth.models import User
from symposion.speakers.models import Speaker
from symposion.proposals.models import AdditionalSpeaker
from symposion.schedule.models import Day, Presentation, Slot, SlotKind, SlotRoom, Room
from symposion.conference.models import Section
from symposion.reviews.models import ProposalResult

proposal_keys = [
    "audience_level",
    "themes",
    "talk_length",
    "what_attendees_will_learn",
    "title",
    "description",
    "abstract",
    "additional_notes",
]

FANCY_COMMA = b'\xe2\x80\x9a'.decode('utf8')

# Create conference and section in the admin and use a hard coded value to import talks
# Create schedule which has a section, dates, and talk kinds and publish/not publish. All this in the admin
# Create rooms which have a room names


class AttrDict(dict):
    def __init__(self, dct):
        super(AttrDict, self).__init__(**dct)
        self.__dict__ = self


def copyattr(frm, to, key):
    try:
        setattr(to, key, getattr(frm, key))
    except AttributeError:
        # print("Couldn't get key %s from data %s" % (key, frm))
        setattr(to, key, "")


COMMA_PAT = re.compile(r",(?=[\w&])")
reverse_themes = {v: k for k, v in THEMES.items()}


def create_speakers(data):
    # Speakers
    speakers = []
    for record in data.speakers:
        record = AttrDict(record)
        user, created = User.objects.get_or_create(username=record.speaker_email)
        if created:
            user.email = record.speaker_email
            user.save()
        speaker, created = Speaker.objects.get_or_create(user=user)
        speaker.name = " ".join([record.first_name, record.last_name])
        speaker.user = user
        speaker.invite_email = record.speaker_email
        speaker.biography = record.speaker_biography or ""
        speaker.twitter_username = record.twitter_username or ""
        speaker.annotation = json.dumps(
            record
        )  # JSON all the speaker data since we don't have fields for it all
        speaker.save()
        speakers.append(speaker)
    return speakers


def fix_themes(themes):
    themes = themes.replace(FANCY_COMMA, ',')
    themes = list(filter(None, COMMA_PAT.split(themes)))
    real_themes = [reverse_themes[desc] for desc in themes if desc in reverse_themes]
    if len(themes) > len(real_themes):
        print("Can't find all themes in %s" % themes)
    return ",".join(real_themes)


def create_proposal(data):
    if "tutorial" in data.type:
        tp = TutorialProposal.with_kind()
        tp.ticket_price = "150.00"
        data.talk_length = 0
    else:
        tp = TalkProposal.with_kind()
        data.talk_length = int(data.talk_length.split()[0])
        data.themes = fix_themes(getattr(data, "theme", ""))

    # Special cases
    data.audience_level = Proposal.audience_text(data.audience_level)
    tp.what_attendees_will_learn = ""

    speakers = create_speakers(data)

    for key in proposal_keys:
        copyattr(data, tp, key)

    first_speaker, *rest = speakers
    tp.speaker = first_speaker
    tp.save()
    for speaker in rest:
        a = AdditionalSpeaker(
            speaker=speaker,
            proposalbase=tp,
            status=AdditionalSpeaker.SPEAKING_STATUS_ACCEPTED,
        )
        a.save()
    return tp


def dt(s):
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%S-07:00")


def create_slot(record, tp):
    if 'tutorial' in record.type:
        slotkind = SlotKind.objects.filter(label="tutorials").first()
    else:
        slotkind = SlotKind.objects.filter(label="talks").first()
    room = Room.objects.filter(name=record.room).first()
    if not room:
        raise Room.DoesNotExist("No room called {}".format(record.room))
    section = Section.objects.filter(slug="talks").first()
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
    p = Presentation(
        slot=s,
        title=tp.title,
        description=tp.description,
        abstract=tp.abstract,
        speaker=list(tp.speakers())[0],
        proposal_base_id=tp.id,
        section=section,
    )
    p.save()
    return p


class Command(BaseCommand):
    help = "import talks/speakers/slots"

    def add_arguments(self, parser):
        parser.add_argument(
            "--data",
            help="json data file to import",
            type=argparse.FileType("r"),
            default=None,
        )
        parser.add_argument(
            "--tutorials", help="Import tutorials?", action="store_true", default=False
        )

    def handle(self, *args, **options):
        if not options["data"]:
            raise SystemExit("Must supply --data option")
        data = json.load(options["data"])
        for record in data:
            try:
                record = AttrDict(record)
                if options["tutorials"] and "tutorial" not in record.type:
                    continue
                elif options["tutorials"] == False and "talk" not in record.type:
                    continue
                tp = create_proposal(record)
                print(self.style.SUCCESS('Successfully created proposal "%s"' % tp))
                p = create_slot(record, tp)
                print(self.style.SUCCESS('Successfully created presentation "%s"' % p))
                # Finally set status to accepted
                ProposalResult(proposal=tp, accepted=True, status="accepted").save()
            except Exception as e:
                print(self.style.ERROR(e))
