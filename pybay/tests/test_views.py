from django.test import TestCase
from django.core.urlresolvers import reverse
from pybay.proposals.models import Proposal
from symposion.proposals.models import ProposalKind
from symposion.speakers.models import Speaker
from symposion.proposals.models import AdditionalSpeaker
from model_mommy import mommy
from model_mommy.random_gen import gen_image_field
from symposion.reviews.models import ProposalResult

class SpeakersViewTest(TestCase):

    def setUp(self):
        kind = mommy.make(ProposalKind)
        self.speaker = mommy.make(Speaker, photo=gen_image_field())
        self.proposal = Proposal.objects.create(
            title='test this title', kind=kind, speaker=self.speaker)
        proposal_result = mommy.make(ProposalResult,
            proposal=self.proposal,
            status='accepted')

    def test_returns_200(self):
        response = self.client.get(reverse('pybay_speakers_list'))
        self.assertEquals(response.status_code, 200)

    def test_accepted_users(self):
        response = self.client.get(reverse('pybay_speakers_list'))
        self.assertIn('speakers', response.context)
        self.assertEquals(response.context['speakers'], [self.speaker])

    def test_photo_required(self):
        self.speaker.photo = None
        self.speaker.save()
        response = self.client.get(reverse('pybay_speakers_list'))
        self.assertEquals(response.context['speakers'], [])

    def test_additional_speaker(self):
        speaker2 = mommy.make(Speaker, photo=gen_image_field())
        mommy.make(
            AdditionalSpeaker,
            proposalbase=self.proposal,
            speaker=speaker2,
            status=AdditionalSpeaker.SPEAKING_STATUS_ACCEPTED)
        response = self.client.get(reverse('pybay_speakers_list'))
        self.assertCountEqual(response.context['speakers'], [self.speaker, speaker2])
