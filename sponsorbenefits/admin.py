from django.contrib import admin
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from ordered_model.admin import OrderedModelAdmin

from .models import BenefitRow


class BenefitAdmin(OrderedModelAdmin):
    list_display = ('text', 'move_up_down_links')

admin.site.register(BenefitRow, BenefitAdmin)
