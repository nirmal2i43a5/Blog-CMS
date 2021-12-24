from django.contrib import admin
from .models.article_models import Article
from .models.category_models import Category
from .models.author_models import Profile

# Register your models here.

admin.site.register(Article)
admin.site.register(Category)
admin.site.register(Profile)