from django.contrib import admin
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from ordered_model.admin import OrderedModelAdmin

from .models import BenefitRow, AlaCarteBenefitRow, AddOnBenefitRow


class BenefitAdmin(OrderedModelAdmin):
    list_display = ('text', 'move_up_down_links')


class TitleAdmin(OrderedModelAdmin):
    list_display = ('title', 'move_up_down_links')


admin.site.register(BenefitRow, BenefitAdmin)
admin.site.register(AlaCarteBenefitRow, TitleAdmin)
admin.site.register(AddOnBenefitRow, TitleAdmin)
