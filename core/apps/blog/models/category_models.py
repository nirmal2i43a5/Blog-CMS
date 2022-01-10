# Core Django imports.
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):

    name = models.CharField(max_length=100)
    slug = models.SlugField()
    image = models.ImageField(default='category-default.jpg',
                              upload_to='category_images',null = True, blank = True)
    approved = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        # unique_together = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ('date_created',)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:category_articles',
                       kwargs={'slug': self.slug})
