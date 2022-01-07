from rest_framework import serializers
from core.apps.blog.models.article_models import Article

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'