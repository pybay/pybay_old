from django.contrib import admin
from .models import MenuItem, SubMenuItem
from ordered_model.admin import OrderedModelAdmin


class MenuAdmin(OrderedModelAdmin):
    list_display = ('text', 'url', 'move_up_down_links')

class SubMenuAdmin(OrderedModelAdmin):
    list_display = ('parent', 'text', 'url', 'move_up_down_links')
    list_filter = ('parent',)


admin.site.register(MenuItem, MenuAdmin)
admin.site.register(SubMenuItem, SubMenuAdmin)
