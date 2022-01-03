from core.apps.blog.api.serializers  import ArticleSerializer
from core.apps.blog.models.article_models import Article
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated

class ArticleApiView(ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    # authentication_classes = (TokenAuthentication, SessionAuthentication)
    # permission_classes = (IsAuthenticated, )