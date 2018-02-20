from django.contrib import admin
from .models import Category, Faq
from ordered_model.admin import OrderedModelAdmin


class CategoryAdmin(OrderedModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'move_up_down_links')

class FaqAdmin(OrderedModelAdmin):
    list_display = ('category', 'title', 'move_up_down_links')
    list_filter = ('category',)


admin.site.register(Faq, FaqAdmin)
admin.site.register(Category, CategoryAdmin)
