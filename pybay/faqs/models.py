from django.db import models

from ordered_model.models import OrderedModel


class CategoryManager(models.Manager):
    def faqs_per_category(self):
        categories = [
            (cat.slug, cat.title, cat.faqs.all())
            for cat in self.order_by('order').prefetch_related('faqs').all()
            if cat.faqs.count()
        ]
        others = Faq.objects.filter(category=None).all()
        if others:
            categories.append(('other', 'Other', others))
        return categories


class Category(OrderedModel):
    class Meta(OrderedModel.Meta):
        verbose_name_plural = "Categories"

    title = models.CharField(max_length=200)
    slug = models.SlugField()

    objects = CategoryManager()

    def __str__(self):
        return self.title


class Faq(OrderedModel):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='faqs')
    title = models.CharField(max_length=200)
    body = models.TextField()
    show_on_registration = models.BooleanField(default=False)
    show_on_sponsors = models.BooleanField(default=False)
    show_on_home = models.BooleanField(default=False)

    def __str__(self):
        return "{}".format(self.title)
