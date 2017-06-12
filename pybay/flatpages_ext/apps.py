from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class FlatpagesExtConfig(AppConfig):
    name = 'pybay.flatpages_ext'
    verbose_name = _("Flat Pages Extensions")
