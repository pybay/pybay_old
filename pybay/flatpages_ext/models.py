from django.db import models
from django.utils.html import format_html, escape

class HostedPicture(models.Model):
    title = models.CharField(max_length=255)
    picture = models.ImageField(upload_to="fpimg")

    @property
    def url(self):
        return str(self.picture.url)

    @property
    def html(self):
        return escape(format_html(
            '<img src="{}" alt="{}"/>',
            self.url, self.title))

    def __str__(self):
        return self.title
