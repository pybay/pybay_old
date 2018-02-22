from django.contrib import admin
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from ordered_model.admin import OrderedModelAdmin

from .models import Benefit, BenefitLevel

class BenefitForm(forms.ModelForm):
    benefit_level = forms.ModelMultipleChoiceField(BenefitLevel.objects.all(),
                                                   required=False,
                                                   widget=FilteredSelectMultiple("Benefit Levels", False))

    class Media:
        css = {'all':('/media/css/widgets.css',)}
        js = ('/admin/jsi18n/',)

    class Meta:
        exclude = []
        model = Benefit


class BenefitLevelAdmin(OrderedModelAdmin):
    list_display = ('text', 'move_up_down_links')


class BenefitAdmin(OrderedModelAdmin):
    list_display = ('text', 'price', 'move_up_down_links')
    form = BenefitForm


admin.site.register(Benefit, BenefitAdmin)
admin.site.register(BenefitLevel, BenefitLevelAdmin)
