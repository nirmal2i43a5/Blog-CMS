
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from django.views.generic import (
    DetailView,
    ListView,
)
# Blog application imports.
from core.apps.blog.models.article_models import Article
from core.apps.blog.models.category_models import Category
# from core.apps.blog.forms.blog.comment_forms import CommentForm
from core.apps.blog.models.article_models import ListAsQuerySet

from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger


# @method_decorator(cache_page(60*15),name = 'dispatch')
class ArticleListView(ListView):
    paginate_by = 12
    context_object_name = "articles"
    # queryset = Article.objects.filter( deleted=False)
    template_name = "blog/article/article_home.html"

    def get_queryset(self):
        # return Article.objects.filter(deleted=False)
   
        return Article.objects.filter(draft = False, deleted=False).prefetch_related('tags')
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        articles = self.object_list#return get_queryset
        page = self.request.GET.get('page', 1)
        paginator = Paginator(articles, 12)
        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)
            
        all_tags = []
        # categoriy_articles_count = []
        
        # for category in Category.objects.values_list('pk', flat=True):#instead of all use this
        #     category_instance = Category.objects.get(pk = category)
        #     articles_count = category_instance.articles.filter(
        #                                                        status = Article.PUBLISHED,
        #                                                        deleted=False
        #                                                        ).count()
        #     categoriy_articles_count.append(articles_count)
            
  
        for article in articles:
            
            '''For categories article count'''
            # category_instance = get_object_or_404(Category, pk = article.category.pk)
            # articles_count = category_instance.articles.all().count()
            # categoriy_articles_count.append(articles_count)
     
            
            '''For accessing tags list of all articles'''
            tags = article.tags.all()#values_list('name',flat = True)
            for tag in tags:
                all_tags.append(tag.name)
                
        tags_qs = ListAsQuerySet(all_tags, model=Article)
        # context['categories'] = zip(
        #                             Category.objects.filter(approved=True),#.values_list('name','slug','image'),
        #                             categoriy_articles_count
        #                             )
        context['tags'] = set(tags_qs)#creating unique tag
        context['articles'] = articles
        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/article/article_detail.html'
    # queryset = Article.objects.all()
    # def get_object(self, queryset=None):
    #     return Article.objects.get(slug=self.kwargs.get('slug'))
    
    def get_context_data(self, **kwargs):
        session_key = f"viewed_article {self.object.slug}"
        if not self.request.session.get(session_key, False):
            self.object.views += 1
            self.object.save()
            self.request.session[session_key] = True

        kwargs['related_articles'] = \
            Article.objects.filter(category=self.object.category)
            
        kwargs['article'] = self.object
        kwargs['tags'] = self.object.tags.all()
        # kwargs['comment_form'] = CommentForm()
        return super().get_context_data(**kwargs)


class ArticleSearchListView(ListView):
    model = Article
    paginate_by = 12
    context_object_name = 'search_articles'
    template_name = "blog/article/article_home.html"
    
    
    def get_queryset(self):
        """
        Search for a user input in the search bar.

        It pass in the query value to the search view using the 'q' parameter.
        Then in the view, It searches the 'title', 'slug', 'body' and fields.

        To make the search a little smarter, say someone searches for
        'container docker ansible' and It want to search the records where all
        3 words appear in the article content in any order, It split the query
        into separate words and chain them.
        """

        query = self.request.GET.get('q')
        if query:
            search_articles = Article.objects.filter(
                Q(title__icontains = query)
                |Q(tags__name__icontains = query)
                |Q(slug__icontains = query)
                # |Q(body__icontains = query)
            )

            if not search_articles:
                messages.info(self.request, f"Search Results for : {query}")
                return search_articles.filter( draft = False, deleted=False)
            else:
                messages.success(self.request, f"Search Results for : {query}")
                return search_articles.filter( draft = False, deleted=False)
        else:
            messages.error(self.request, f"Sorry you did not enter any keyword")
            return []


    def get_context_data(self, **kwargs):
        """
            Add categories to context data
        """
        context = super(ArticleSearchListView, self).get_context_data(**kwargs)
        all_tags = []
        search_articles = self.object_list#return object from get_queryset [object_list is default use keyword while getting object]
        for article in search_articles:
            tags = article.tags.all()
            for tag in tags:
                all_tags.append(tag.name)            
        tags_qs = ListAsQuerySet(all_tags, model=Article)
        # context['categories'] = Category.objects.filter(approved=True)
        context['tags'] = set(tags_qs)
        return context


class TagArticlesListView(ListView):
    """
        List articles related to a tag.
    """
    model = Article
    paginate_by = 12
    context_object_name = 'tag_articles_list'
    template_name = 'blog/article/tag_articles_list.html'

    def get_queryset(self):
        """
            Filter Articles by tag_name
        """

        tag_name = self.kwargs.get('tag_name', '')

        if tag_name:
            tag_articles_list = Article.objects.filter(tags__name__in=[tag_name],
                                                       draft=False,
                                                       deleted=False
                                                       )

            if not tag_articles_list:
                messages.info(self.request, f"No Results for '{tag_name}' tag")
                return tag_articles_list
            else:
                messages.success(self.request, f"Results for '{tag_name}' tag")
                return tag_articles_list
        else:
            messages.error(self.request, "Invalid tag")
            return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(approved=True)
        return context
