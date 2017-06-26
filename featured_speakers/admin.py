from django import forms
from django.contrib import admin
from django.db import models

from ordered_model.admin import OrderedModelAdmin

from .models import FeaturedSpeaker
from symposion.speakers.models import Speaker

class SpeakerChoiceField(forms.ModelChoiceField):
    """Class to overwrite __str__ implementation on speakers and provide text in dropdown."""
    def label_from_instance(self, obj):
        return obj.name

class FeaturedSpeakerForm(forms.ModelForm):
    speaker = SpeakerChoiceField(Speaker.objects.all())

class FeaturedSpeakerAdmin(OrderedModelAdmin):
    list_display = ('title', 'speaker_name', 'move_up_down_links')
    form = FeaturedSpeakerForm
    def speaker_name(self, obj):
        return obj.speaker.name
    speaker_name.admin_order_field = 'speaker'



admin.site.register(FeaturedSpeaker, FeaturedSpeakerAdmin)
