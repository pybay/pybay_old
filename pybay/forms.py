import random
import string

from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from symposion.speakers.models import Speaker
from symposion.proposals.models import ProposalKind
from pybay.proposals.models import TalkProposal

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.bootstrap import PrependedText

class CallForProposalForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=100)
    last_name = forms.CharField(label='Last Name', max_length=100)
    email = forms.EmailField(label='Email')
    website = forms.URLField(label='Website', required=False)
    phone = forms.CharField(label='Phone', max_length=20)
    category = forms.ChoiceField(choices=TalkProposal.CATEGORY_CHOICES)
    audience_level = forms.ChoiceField(choices=TalkProposal.AUDIENCE_LEVELS)
    speaker_bio = forms.CharField(widget=forms.Textarea)
    meetup_talk = forms.ChoiceField(widget=forms.RadioSelect,label="Deliver talk @ future SF Python Meetups if we cannot fit you in the PyBay program?", choices=TalkProposal.MEETUP_CHOICES)
    talk_title = forms.CharField(label='Talk Title', max_length=100)
    description = forms.CharField(label="Brief Description", widget=forms.Textarea)
    abstract = forms.CharField(widget=forms.Textarea)
    what_will_attendees_learn = forms.CharField(widget=forms.Textarea)
    speaker_and_talk_history = forms.CharField(widget=forms.Textarea)
    links_to_past_talks = forms.CharField(widget=forms.Textarea, label="Links to slide deck/talk video", max_length=100, required=False)

    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-md-4'
    helper.field_class = 'col-lg-8'
    helper.layout = Layout(
        PrependedText('first_name', '<i class="glyphicon glyphicon-user"></i>', placeholder='First Name'),
        PrependedText('last_name', '<i class="glyphicon glyphicon-user"></i>',placeholder='Last Name'),
        PrependedText('email', '<i class="glyphicon glyphicon-envelope"></i>',placeholder='   Email'),
        PrependedText('website', '<i class="glyphicon glyphicon-globe"></i>',placeholder='  Home Page'),
        PrependedText('phone', '<i class="glyphicon glyphicon-earphone"></i>',placeholder='415-555-1234'),
        'category',
        'audience_level',
        PrependedText('speaker_bio', '<i class="glyphicon glyphicon-pencil"></i>',placeholder='Speaker Bio'),
        PrependedText('talk_title', '<i class="glyphicon glyphicon-pencil"></i>',placeholder='Talk Title'),
        PrependedText('description', '<i class="glyphicon glyphicon-pencil"></i>',placeholder='A brief description of your presentation to be displayed in the conference schedule.\nPlease limit the descrtiption to 400 characters\n'),
        PrependedText('abstract', '<i class="glyphicon glyphicon-pencil"></i>', placeholder='A more detailed description that sells your talk to attendees and reviewers'),
        PrependedText('what_will_attendees_learn', '<i class="glyphicon glyphicon-pencil"></i>', placeholder='This is for the reviewers, the info here will not be published'),
        PrependedText('speaker_and_talk_history', '<i class="glyphicon glyphicon-pencil"></i>', placeholder='Anything else we should know about you and your speaking experience. Will you have a co-presenter?'),
        PrependedText('links_to_past_talks', '<i class="glyphicon glyphicon-pencil"></i>', placeholder='If you already have your slide deck for this talk, or if you have slide deck or video to past talks, please add the URLs here'),
        'meetup_talk'
    )

    def clean_talk_title(self):
        value = self.cleaned_data["talk_title"]
        if len(value) > 90:
            raise forms.ValidationError(
                u"The talk title must be less than 90 characters"
            )
        return value

    def clean_description(self):
        value = self.cleaned_data["description"]
        if len(value) > 400:
            raise forms.ValidationError(
                u"The description must be less than 400 characters"
            )
        return value

    def save_to_models(self):
        if not self.is_valid():
            raise ValidationError("Trying to save a form that is not valid")
        data = self.cleaned_data

        # Fetch the speaker
        full_name = "{} {}".format(data['first_name'], data['last_name'])
        try:
            user = User.objects.get(username=data['email'])
            speaker = user.speaker_profile
        except User.DoesNotExist:

            # Create a new user
            password = ''.join(random.choice([string.ascii_uppercase + string.digits for i in range(10)]))
            user = User.objects.create_user(
                username=data['email'],
                email=data['email'],
                password=password,
            )

            # Create an associated speaker
            speaker = Speaker.objects.create(
                user=user,
                name=full_name,
                biography=data['speaker_bio'],
            )

        # Create a new talk
        proposal = TalkProposal.objects.create(
            kind=ProposalKind.objects.get(name='talk'),
            title=data['talk_title'],
            description=data['description'],
            abstract=data['abstract'],
            audience_level=data['audience_level'],
            speaker=speaker,
            category=data['category'],
            what_will_attendees_learn=data['what_will_attendees_learn'],
            meetup_talk=data['meetup_talk'],
            speaker_and_talk_history=data['speaker_and_talk_history'],
            talk_links=data['links_to_past_talks'],
        )
        return speaker, proposal
