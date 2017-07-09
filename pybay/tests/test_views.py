from django.test import TestCase
from django.core.urlresolvers import reverse
from pybay.proposals.models import TalkProposal
from pybay.utils import get_accepted_speaker_by_slug
from symposion.proposals.models import ProposalKind
from symposion.speakers.models import Speaker
from symposion.proposals.models import AdditionalSpeaker
from model_mommy import mommy
from model_mommy.random_gen import gen_image_field
from symposion.reviews.models import ProposalResult

import itertools


class SpeakersModelTest(TestCase):

    def test_get_slug(self):
        self.speaker = mommy.make(Speaker, name="Lorem Ipsum",
                                  photo=gen_image_field())
        self.assertEquals(self.speaker.name_slug,
                          "lorem-ipsum")

    def test_get_active_speaker_by_slug(self):
        s1 = mommy.make(Speaker, name="Lorem Ipsum 1",
                        photo=gen_image_field())
        s2 = mommy.make(Speaker, name="Lorem Ipsum 2",
                        photo=gen_image_field())
        s3 = mommy.make(Speaker, name="Lorem Ipsum 3",
                        photo=gen_image_field())

        kind = mommy.make(ProposalKind)
        p2 = TalkProposal.objects.create(
            title='test this title', kind=kind,
            speaker=s2, audience_level=1,
        )
        mommy.make(ProposalResult, proposal=p2, status='accepted')
        self.assertEquals(
            get_accepted_speaker_by_slug(s2.name_slug),
            s2,
        )
        with self.assertRaises(Speaker.DoesNotExist):
            get_accepted_speaker_by_slug(s1.name_slug)



class SpeakersViewTest(TestCase):

    def setUp(self):
        kind = mommy.make(ProposalKind)
        self.speaker = mommy.make(Speaker, photo=gen_image_field())
        self.proposal = TalkProposal.objects.create(
            title='test this title', kind=kind,
            speaker=self.speaker,
            audience_level=1,
        )
        proposal_result = mommy.make(ProposalResult,
            proposal=self.proposal,
            status='accepted')

    def test_returns_200(self):
        response = self.client.get(reverse('pybay_speakers_list'))
        self.assertEquals(response.status_code, 200)

    def test_accepted_users(self):
        response = self.client.get(reverse('pybay_speakers_list'))
        self.assertIn('chunks', response.context)
        self.assertEquals(response.context['chunks'], [[self.speaker]])

    def test_additional_speaker(self):
        speaker2 = mommy.make(Speaker, photo=gen_image_field())
        mommy.make(
            AdditionalSpeaker,
            proposalbase=self.proposal,
            speaker=speaker2,
            status=AdditionalSpeaker.SPEAKING_STATUS_ACCEPTED)
        response = self.client.get(reverse('pybay_speakers_list'))
        speakers = list(itertools.chain.from_iterable(response.context['chunks']))
        self.assertCountEqual(speakers, [self.speaker, speaker2])
