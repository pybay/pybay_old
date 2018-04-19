from django import forms
from django.contrib import admin

from .models import TalkProposal, TutorialProposal


class TalkProposalAdmin(admin.ModelAdmin):
    list_display = ('title', 'themes', 'speaker', 'speaker_email', 'phone', 'status', 'submitted')
    ordering = ['-submitted', 'result__status', 'speaker']
    list_filter = ('themes',)

    def speaker_phone_number(self, obj):
        return obj.speaker.phone

    speaker_phone_number.admin_order_field = 'phone'

    def speaker_status(self, obj):
        return obj.speaker.status

    speaker_status.admin_order_field = 'status'


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
