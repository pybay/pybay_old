from django.db import models

from symposion.proposals.models import ProposalBase, ProposalKind


THEMES = {
  'devops': 'DevOps‚ Testing‚ & Automation',
  'python': 'Python & Libraries',
  'speed': 'Scale & Performance',
  'web': 'Web‚ IoT‚ & Hardware',
  'ai': 'ML‚ AI‚ & Data',
  'community': 'People & Project Management'
}


class Proposal(ProposalBase):

    AUDIENCE_LEVEL_NOVICE = 1
    AUDIENCE_LEVEL_INTERMEDIATE = 2
    AUDIENCE_LEVEL_EXPERIENCED = 3


    AUDIENCE_LEVELS = [
        (AUDIENCE_LEVEL_NOVICE, "Beginner"),
        (AUDIENCE_LEVEL_INTERMEDIATE, "Intermediate"),
        (AUDIENCE_LEVEL_EXPERIENCED, "Advanced"),
    ]

    @classmethod
    def audience_text(klass, text):
        lookup = {val[:3]: key for key, val in dict(klass.AUDIENCE_LEVELS).items()}
        return lookup[text[:3]]

    MEETUP_CHOICE_YES =  "Yes"
    MEETUP_CHOICE_MAYBE = "Maybe"
    MEETUP_CHOICE_NO =  "No"

    MEETUP_CHOICES = [
         (MEETUP_CHOICE_YES, "Yes"),
         (MEETUP_CHOICE_MAYBE, "Maybe"),
         (MEETUP_CHOICE_NO, "No")
    ]

    THEME_CHOICES = list(THEMES.items())

    TALK_SHORT = 25
    TALK_LONG = 40

    TALK_LENGTHS = [
        (TALK_SHORT, "25 minutes"),
        (TALK_LONG, "40 minutes")
    ]
    audience_level = models.IntegerField(choices=AUDIENCE_LEVELS)

    recording_release = models.BooleanField(
        default=True,
        help_text="By submitting your proposal, you agree to give permission to the conference organizers to record, edit, and release audio and/or video of your presentation. If you do not agree to this, please uncheck this box."
    )
    themes = models.CharField(max_length=250)
    talk_length = models.IntegerField(choices=TALK_LENGTHS, default=25)
    talk_links = models.CharField(max_length=200)
    what_attendees_will_learn = models.TextField()
    meetup_talk = models.CharField(choices=MEETUP_CHOICES, max_length=100, default="No")
    speaker_and_talk_history = models.TextField()
    speaker_website = models.TextField(null=True, blank=True)
    location_override = models.CharField(max_length=200, blank=True)
    phone = models.CharField(blank=False,max_length=15, null=True)

    class Meta:
        abstract = True

    @property
    def theme_slugs(self):
        return self.themes.split(',')

    @property
    def theme_descriptions(self):
        for theme in self.theme_slugs:
            desc = THEMES.get(theme)
            if desc:
                yield THEMES[theme]



class TalkProposal(Proposal):
    class Meta:
        verbose_name = "talk proposal"

    @classmethod
    def with_kind(cls):
      talk_kind = ProposalKind.objects.get(name="talk")
      return cls(kind=talk_kind)

class TutorialProposal(Proposal):
    class Meta:
        verbose_name = "tutorial proposal"

    ticket_price = models.CharField(max_length=50, blank=True)
    sold_out = models.BooleanField(default=False)
