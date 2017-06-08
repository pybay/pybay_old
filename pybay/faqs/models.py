from django.db import models


class CategoryManager(models.Manager):
    def faqs_per_category(self):
        categories = [
            (cat.slug, cat.title, cat.faqs.all())
            for cat in self.prefetch_related('faqs').all()
            if cat.faqs.count()
        ]
        others = Faq.objects.filter(category=None).all()
        if others:
            categories.append(('other', 'Other', others))
        return categories


class Category(models.Model):
    class Meta:
        ordering = ['ordering']
        verbose_name_plural = "Categories"

    title = models.CharField(max_length=200)
    slug = models.SlugField()
    ordering = models.IntegerField()

    objects = CategoryManager()

    def __str__(self):
        return self.title


class Faq(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='faqs')
    title = models.CharField(max_length=200)
    body = models.TextField()
    ordering = models.IntegerField()
    show_on_registration = models.BooleanField(default=False)
    show_on_sponsors = models.BooleanField(default=False)
    show_on_home = models.BooleanField(default=False)

    def __str__(self):
        return "{}: {}".format(self.title, self.body)

    class Meta:
        ordering = ['ordering']
