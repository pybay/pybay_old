from django.db import models
from django.utils import timezone


class Countdown(models.Model):
    title = models.TextField(help_text="Text above the countdown")
    date = models.DateTimeField(help_text="The date the countdown counts to")
    cta = models.TextField(help_text="Text on the button below the countdown", verbose_name='Call to action')
    link = models.TextField(help_text="Target of the button below the countdown")

    def context_for_template(self):
        ret = dict(self.__dict__, reference=timezone.now().timestamp())
        ret['date'] = ret['date'].timestamp()
        return ret
