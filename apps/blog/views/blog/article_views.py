# Standard Python Library imports.
from functools import reduce
import operator

# Core Django imports.
from django.contrib import messages
from django.db.models import Q
from django.db.models.query import QuerySet
from django.views.generic import (
    DetailView,
    ListView,
)

# Blog application imports.
from apps.blog.models.article_models import Article
from apps.blog.models.category_models import Category
from apps.blog.forms.blog.comment_forms import CommentForm
from apps.blog.models.article_models import ListAsQuerySet

from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

class ArticleListView(ListView):
    context_object_name = "articles"
    paginate_by = 2
    queryset = Article.objects.filter(status=Article.PUBLISHED, deleted=False)
    template_name = "blog/article/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        articles = Article.objects.filter(status=Article.PUBLISHED, deleted=False)
        page = self.request.GET.get('page', 1)

        paginator = Paginator(articles, 2)
        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)
        all_tags = []
        for article in Article.objects.filter(status=Article.PUBLISHED, deleted=False):
            tags = article.tags.all()
            for tag in tags:
                all_tags.append(tag.name)
                
            
        tags_qs = ListAsQuerySet(all_tags, model=Article)
        print(tags_qs)
        context['categories'] = Category.objects.filter(approved=True)
        context['tags'] = tags_qs
        context['articles'] = articles
        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/article/article_detail.html'

    def get_context_data(self, **kwargs):
        session_key = f"viewed_article {self.object.slug}"
        if not self.request.session.get(session_key, False):
            self.object.views += 1
            self.object.save()
            self.request.session[session_key] = True

        kwargs['related_articles'] = \
            Article.objects.filter(category=self.object.category, status=Article.PUBLISHED).order_by('?')[:3]
        kwargs['article'] = self.object
        kwargs['comment_form'] = CommentForm()
        return super().get_context_data(**kwargs)


class ArticleSearchListView(ListView):
    model = Article
    paginate_by = 12
    context_object_name = 'search_results'
    template_name = "blog/article/article_search_list.html"

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
            query_list = query.split()
            search_results = Article.objects.filter(
                reduce(operator.and_,
                       (Q(title__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(slug__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(body__icontains=q) for q in query_list))
            )

            if not search_results:
                messages.info(self.request, f"No results for '{query}'")
                return search_results.filter(status=Article.PUBLISHED, deleted=False)
            else:
                messages.success(self.request, f"Results for '{query}'")
                return search_results.filter(status=Article.PUBLISHED, deleted=False)
        else:
            messages.error(self.request, f"Sorry you did not enter any keyword")
            return []

    def get_context_data(self, **kwargs):
        """
            Add categories to context data
        """
        context = super(ArticleSearchListView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(approved=True)
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
                                                       status=Article.PUBLISHED,
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
