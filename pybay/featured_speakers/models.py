from django.db import models

from ordered_model.models import OrderedModel
from symposion.speakers.models import Speaker


class FeaturedSpeaker(OrderedModel):
    speaker = models.OneToOneField(Speaker, on_delete=models.CASCADE, primary_key=True)
    description = models.TextField()

    class Meta(OrderedModel.Meta):
        pass
