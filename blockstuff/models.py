from django.db import models


class Col3(models.Model):
    overall_title = models.CharField(max_length=255, blank=True)

    icon_1 = models.CharField(max_length=50, blank=True,
                              help_text="Choose from " +
                              "http://themes-pixeden.com/font-demos/7-stroke/")
    title_1 = models.CharField(max_length=255, blank=True)
    content_1 = models.TextField(blank=True)

    icon_2 = models.CharField(max_length=50, blank=True)
    title_2 = models.CharField(max_length=255, blank=True)
    content_2 = models.TextField(blank=True)

    icon_3 = models.CharField(max_length=50, blank=True)
    title_3 = models.CharField(max_length=255, blank=True)
    content_3 = models.TextField(blank=True)

    show_title = models.BooleanField(default=True)

    def __unicode__(self):
        return self.overall_title

    def __str__(self):
        return self.overall_title
