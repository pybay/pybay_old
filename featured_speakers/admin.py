from django.db import models
from django.contrib import admin

from ordered_model.admin import OrderedModelAdmin

from .models import FeaturedSpeaker

class FeaturedSpeakerAdmin(OrderedModelAdmin):
    list_display = ('title', 'speaker', 'move_up_down_links')
    formfield_overrides = {
        models.OneToOneField: {'to_field_name': 'name'},
    }

admin.site.register(FeaturedSpeaker, FeaturedSpeakerAdmin)
