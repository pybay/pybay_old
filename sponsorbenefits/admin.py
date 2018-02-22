from django.contrib import admin
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

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

class BenefitAdmin(admin.ModelAdmin):
    list_display = ('text', 'price')
    form = BenefitForm

admin.site.register(Benefit, BenefitAdmin)
admin.site.register(BenefitLevel)
