from django import forms
from django.contrib import admin

from .models import TalkProposal, TutorialProposal

THEME_CHOICES = ["Fundamentals", "Data", "DevOps", "Speed", "Community", "Hardware"]

class ThemeFilter(admin.SimpleListFilter):
    """Provide sane list of themes from ad-hoc data.

    We used multiple strings in a single "theme" field to capture this. Should have been FK to normalize data.

    Since it's not... let's do some data parsing and munging here.
    """
    title = 'Theme'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'themes'

    def lookups(self, request, model_admin):
        return zip(THEME_CHOICES, THEME_CHOICES)

    def queryset(self, request, queryset):
        theme = self.value()
        if theme:
          return queryset.filter(themes__icontains=theme)
        else:
          return queryset


class TalkProposalAdmin(admin.ModelAdmin):
    list_display = ('title', 'themes', 'speaker', 'speaker_email', 'phone', 'status',
                    'audience_level', 'submitted')
    search_fields = ['title', 'speaker', 'description']
    ordering = ['-submitted', 'result__status', 'speaker']
    list_filter = (ThemeFilter,)
    list_per_page = 200

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
