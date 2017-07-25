from django.contrib import admin

from . import models


class CountdownAdmin(admin.ModelAdmin):
    list_display = 'title', 'date'


admin.site.register(models.Countdown, CountdownAdmin)
