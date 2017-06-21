from django.db import models

from ordered_model.models import OrderedModel
from symposion.speakers.models import Speaker


class FeaturedSpeaker(OrderedModel):
    title = models.CharField(max_length=50)
    speaker = models.OneToOneField(Speaker, on_delete=models.CASCADE, primary_key=True)

    class Meta(OrderedModel.Meta):
        pass
