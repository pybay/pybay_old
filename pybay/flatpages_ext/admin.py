from django.contrib import admin

from .models import HostedPicture


class HostedPictureAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'html']


admin.site.register(HostedPicture, HostedPictureAdmin)
