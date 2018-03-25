from django.db import models
from ordered_model.models import OrderedModel


class BenefitRow(OrderedModel):

    text = models.CharField(max_length=255, help_text="Display table etc.")
    diamond_text = models.CharField(max_length=255, default="", blank=True)
    gold_text = models.CharField(max_length=255, default="", blank=True)
    silver_text = models.CharField(max_length=255, default="", blank=True)
    bronze_text = models.CharField(max_length=255, default="", blank=True)

    def __str__(self):
        return self.text
