from django.test import TestCase
from pybay.forms import CallForProposalForm


class CfpFormTestCase(TestCase):
    fixtures = [
        "conference",
        "proposal_base",
    ]

    def _get_data(self):
        return {
            'first_name': "Daniel",
            'last_name': "Pyrathon",
            'email': "pirosb3@gmail.com",
            'website': "woo.com",
            'phone': "+14155289519",
            'category': "fundamentals",
            'audience_level': 1,
            'speaker_bio': 'wooo',
            'talk_title': 'wooo',
            'description': 'wooo',
            'abstract': 'wooo',
            'what_will_attendees_learn': 'wooo',
            'speaker_and_talk_history': 'wooo2',
            'meetup_talk': '1',
            'links_to_past_talks': 'http://google.com',
        }

    def test_cfp_form_works(self):
        form = CallForProposalForm(self._get_data())
        self.assertTrue(form.is_valid())
        self.assertEqual(
            len(form.cleaned_data), 15
        )

    def test_cannot_ommit_fields(self):
        all_fields = set(self._get_data().keys())
        all_fields.remove('website')
        all_fields.remove('links_to_past_talks')

        for field_name in all_fields:
            data = self._get_data()
            del data[field_name]

            form = CallForProposalForm(data)
            self.assertFalse(form.is_valid())
            self.assertIn(field_name, form.errors)

    def test_form_save_models(self):
        form = CallForProposalForm(self._get_data())
        self.assertTrue(form.is_valid())

        speaker, proposal = form.save_to_models()
        self.assertEqual(speaker.name, "Daniel Pyrathon")
        self.assertEqual(proposal.speaker, speaker)
        self.assertEqual(proposal.speaker_and_talk_history, 'wooo2')
        self.assertEqual(proposal.talk_links, 'http://google.com')
        self.assertEqual(speaker.user.username, "pirosb3@gmail.com")

    def test_form_duplicate_profile(self):
        form1 = CallForProposalForm(self._get_data())
        speaker1, proposal1 = form1.save_to_models()

        data = self._get_data()
        data['talk_title'] = 'woo 2!'
        form2 = CallForProposalForm(data)
        speaker2, proposal2 = form2.save_to_models()

        self.assertEqual(speaker1, speaker2)
