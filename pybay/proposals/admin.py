from django.contrib import admin

from .models import TalkProposal, TutorialProposal


class TalkProposalAdmin(admin.ModelAdmin):
    list_display = ('title', 'speaker', 'speaker_email', 'speaker_phone_number', 'status')
    ordering = ['result__status', 'speaker']

    def speaker_phone_number(self, obj):
        return obj.speaker.phone_number
    speaker_phone_number.admin_order_field  = 'speaker__phone_number'


admin.site.register(TalkProposal, TalkProposalAdmin)
admin.site.register(TutorialProposal)
