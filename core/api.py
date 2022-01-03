
from rest_framework import routers
from django.urls import path,include
from core.apps.blog.api.views import ArticleApiView

router = routers.DefaultRouter()

router.register(r'articles', ArticleApiView, 'articles')

app_name = 'api'


urlpatterns = [
    
      path('', include(router.urls))
]