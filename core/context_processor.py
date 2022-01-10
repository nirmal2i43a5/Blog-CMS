
from core.apps.blog.models.category_models import Category
from core.apps.blog.models.article_models import Article

def categories(request):
    categoriy_articles_count = []
    
    for category in Category.objects.values_list('pk', flat=True):#instead of all use this
        category_instance = Category.objects.get(pk = category)
        articles_count = category_instance.articles.filter(
                                                            draft = False,
                                                            deleted=False
                                                            ).count()
        categoriy_articles_count.append(articles_count)
    
    categories = zip(
    Category.objects.filter(approved=True),#.values_list('name','slug','image'),
    categoriy_articles_count
                        )
    return {
        'categories':categories
    }