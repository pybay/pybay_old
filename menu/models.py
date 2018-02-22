from django.db import models

from ordered_model.models import OrderedModel


class MenuItem(OrderedModel):
    class Meta(OrderedModel.Meta):
        verbose_name_plural = "Menu Items"

    text = models.CharField(max_length=200, help_text="Display text for link")
    url = models.CharField(max_length=255,
                           help_text="URL (/relative or http://domain.com)")
    target = models.BooleanField(default=False,
                              help_text="Check to open in new window")
    def __str__(self):
        return self.text


class SubMenuItem(OrderedModel):
    class Meta(OrderedModel.Meta):
        verbose_name_plural = "SubMenu Items"

    parent = models.ForeignKey(MenuItem, related_name='menuitems')
    text = models.CharField(max_length=255, help_text="Display text for link")
    url = models.CharField(max_length=255, help_text="URL (/relative or http://domain.com)")
    target = models.BooleanField(default=False,
                              help_text="Check to open in new window")

    def __str__(self):
        return self.text
