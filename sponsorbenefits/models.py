from django.db import models
from ordered_model.models import OrderedModel


class BenefitLevel(OrderedModel):
    class Meta(OrderedModel.Meta):
        verbose_name_plural = "Benefit Levels"

    text = models.CharField(max_length=200, help_text="EG Gold, Silver, etc")
    def __str__(self):
        return self.text


class Benefit(OrderedModel):
    text = models.CharField(max_length=255, help_text="Display table etc.")
    price = models.IntegerField()
    benefit_level = models.ManyToManyField(BenefitLevel, related_name='levels', blank=True)

    def __str__(self):
        return self.text
