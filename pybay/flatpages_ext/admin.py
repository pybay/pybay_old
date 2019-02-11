from django.contrib import admin
from reversion.admin import VersionAdmin
from django.contrib.flatpages.admin import FlatPage, FlatPageAdmin

from .models import HostedPicture

admin.site.unregister(FlatPage)


@admin.register(FlatPage)
class FlatPageVersionedAdmin(VersionAdmin, FlatPageAdmin):
    pass


@admin.register(HostedPicture)
class HostedPictureAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'html']
