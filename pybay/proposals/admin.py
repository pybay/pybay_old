from django import forms
from django.contrib import admin

from .models import TalkProposal, TutorialProposal


class TalkProposalAdmin(admin.ModelAdmin):
    list_display = ('title', 'speaker', 'speaker_email', 'speaker_phone_number', 'status')
    ordering = ['result__status', 'speaker']

    def speaker_phone_number(self, obj):
        return obj.speaker.phone_number
    speaker_phone_number.admin_order_field  = 'speaker__phone_number'

class TutorialForm(forms.ModelForm):
    """Custom form just to over-ride UX limit of 400 chars on description."""
    description = forms.CharField(max_length=1200,
                                  widget=forms.Textarea(attrs={'class': 'vLargeTextField'}))

    class Meta:
        model = TutorialProposal
        exclude = ['name']


class TutorialProposalAdmin(admin.ModelAdmin):
    form = TutorialForm

admin.site.register(TalkProposal, TalkProposalAdmin)
admin.site.register(TutorialProposal, TutorialProposalAdmin)
