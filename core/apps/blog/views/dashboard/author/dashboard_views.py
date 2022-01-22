# Django imports.
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import  permission_required
# Blog app imports.
from core.apps.blog.forms.blog.article_forms import ArticleUpdateForm, ArticleCreateForm
from core.apps.blog.models.article_models import Article

def home(request):
    return render(request, 'blog/blog_home.html')



class ArticleWriteView(LoginRequiredMixin,PermissionRequiredMixin, View):

    template_name = 'blog/author/article_create_form.html'
    context_object = {}
    permission_required = "blog.add_article"
    
    def get(self, request, *args, **kwargs):
        article_create_form = ArticleCreateForm()
        self.context_object["article_create_form"] = article_create_form
        self.context_object["title"] = 'Article'
        return render(request, self.template_name, self.context_object)

    def post(self, request, *args, **kwargs):
        article_create_form = ArticleCreateForm(request.POST, request.FILES)
        if article_create_form.is_valid():
            new_article = article_create_form.save(commit=False)
            new_article.author = request.user
            new_article.save()
            article_create_form.save_m2m()#Save tags for respective posts
            messages.success(self.request, f"Article published successfully.")
            return redirect(to="blog:article_detail", slug=new_article.slug)

    


class ArticleUpdateView(LoginRequiredMixin,PermissionRequiredMixin, View):

    template_name = 'blog/author/article_update_form.html'
    context_object = {}
    permission_required = "blog.change_article"

    def get(self, request, *args, **kwargs):

        old_article = get_object_or_404(Article, slug=self.kwargs.get("slug"))
        article_update_form = ArticleUpdateForm(instance=old_article)

        self.context_object["article_update_form"] = article_update_form
        self.context_object["article"] = old_article
        self.context_object["title"] = 'Update Article'
        return render(request, self.template_name, self.context_object)



    def post(self, request, *args, **kwargs):
            article_instance = get_object_or_404(Article, slug=self.kwargs.get("slug"))
            article_update_form = ArticleCreateForm(request.POST, request.FILES, instance =article_instance )
            if article_update_form.is_valid():
                instance = article_update_form.save(commit=False)
                instance.author = request.user
                instance.save()
                article_update_form.save_m2m()#Save tags for respective posts
            messages.success(self.request, f"Article published successfully.")
            return redirect(to="blog:article_detail", slug=article_instance.slug)
        
class ArticleDeleteView(LoginRequiredMixin,PermissionRequiredMixin, View):
    """
      Deletes article
    """
    permission_required = "blog.delete_article"
    def get(self, *args, **kwargs):
        """
           Checks if user who has requested to delete the article is the
           owner of the article.
           If the user is the owner, it sets the deleted field of the article to true and
           return a successful message.
           If the user is not the owner, it tells user he/she can't delete it
        """
        article = get_object_or_404(Article, slug=self.kwargs.get("slug"))

        if not self.request.user.username == article.author.username:
            messages.error(request=self.request, message="You do not have permission to delete this article.")
            return HttpResponseRedirect(self.request.META.get('HTTP_REFERER', '/'))

        article.deleted = True
        article.save()

        messages.success(request=self.request, message="Article Deleted Successfully")
        return redirect(to='blog:deleted_articles')





class ArticlePublishView(LoginRequiredMixin,PermissionRequiredMixin, View):
    """
       View to publish a drafted article
    """
    permission_required = "blog.view_article"
    def get(self, request, *args, **kwargs):
        """
            Gets article slug from user and gets the article from the
            database.
            It then sets the status to publish and date published to now and
            then save the article and redirects the author to his/her published
            articles.
        """
        article = get_object_or_404(Article, slug=self.kwargs.get('slug'))
        article.draft = True
        article.date_published = timezone.now()
        article.date_updated = timezone.now()
        article.save()

        messages.success(request, f"Article Published successfully.")
        return redirect('blog:article_detail', slug=article.slug)


class AuthorWrittenArticlesView(LoginRequiredMixin,PermissionRequiredMixin, View):
    """
       Displays all articles written by an author.
    """
    permission_required = "blog.view_article"
    def get(self, request):
        """
           Returns all articles written by an author.
        """
        template_name = 'dashboard/author/author_written_article_list.html'
        context_object = {}

        written_articles = Article.objects.filter( deleted=False).order_by('-date_created')
        total_articles_written = len(written_articles)

        page = request.GET.get('page', 1)

        paginator = Paginator(written_articles, 5)
        try:
            written_articles_list = paginator.page(page)
        except PageNotAnInteger:
            written_articles_list = paginator.page(1)
        except EmptyPage:
            written_articles_list = paginator.page(paginator.num_pages)

        context_object['written_articles_list'] = written_articles_list
        context_object['total_articles_written'] = total_articles_written

        return render(request, template_name, context_object)


class AuthorPublishedArticlesView(LoginRequiredMixin,PermissionRequiredMixin,View):
    """
       Displays published articles by an author.
    """
    permission_required = "blog.view_article"
    
    # @method_decorator(permission_required('blog.view_article',raise_exception=True))
    def get(self, request):
        
        """
           Returns published articles by an author.
        """
        template_name = 'blog/author/author_published_article_list.html'
        context_object = {}

        published_articles = Article.objects.filter(
                                                    draft = False).order_by('-date_published')
        total_articles_published = published_articles.count()

        page = request.GET.get('page', 1)

        paginator = Paginator(published_articles, 10)
        try:
            published_articles_list = paginator.page(page)
        except PageNotAnInteger:
            published_articles_list = paginator.page(1)
        except EmptyPage:
            published_articles_list = paginator.page(paginator.num_pages)

        context_object['published_articles_list'] = published_articles_list
        context_object['total_articles_published'] = total_articles_published
        context_object['title'] = 'Published Articles'

        return render(request, template_name, context_object)


class AuthorDraftedArticlesView(LoginRequiredMixin,PermissionRequiredMixin, View):
    """
       Displays drafted articles by an author.
    """
    
    permission_required = "blog.view_article"
    def get(self, request):
        
        """
           Returns drafted articles by an author.
        """
        
        template_name = 'blog/author/author_drafted_article_list.html'
        context_object = {}

        drafted_articles = Article.objects.filter(
                                                  draft = True, deleted=False).order_by('-date_created')
        total_articles_drafted = len(drafted_articles)

        page = request.GET.get('page', 1)

        paginator = Paginator(drafted_articles, 5)
        try:
            drafted_articles_list = paginator.page(page)
        except PageNotAnInteger:
            drafted_articles_list = paginator.page(1)
        except EmptyPage:
            drafted_articles_list = paginator.page(paginator.num_pages)

        context_object['drafted_articles_list'] = drafted_articles_list
        context_object['total_articles_drafted'] = total_articles_drafted
        context_object['title'] = 'Drafted Articles'

        return render(request, template_name, context_object)


class AuthorDeletedArticlesView(LoginRequiredMixin,PermissionRequiredMixin, View):
    permission_required = "blog.view_article"
    def get(self, request):
        template_name = 'blog/author/author_deleted_article_list.html'
        context_object = {}

        deleted_articles = Article.objects.filter(
                                                  deleted=True).order_by('-date_published')
        total_articles_deleted = len(deleted_articles)

        page = request.GET.get('page', 1)

        paginator = Paginator(deleted_articles, 5)
        try:
            deleted_articles_list = paginator.page(page)
        except PageNotAnInteger:
            deleted_articles_list = paginator.page(1)
        except EmptyPage:
            deleted_articles_list = paginator.page(paginator.num_pages)

        context_object['deleted_articles_list'] = deleted_articles_list
        context_object['total_articles_deleted'] = total_articles_deleted
        context_object['title'] = 'Deleted Articles'

        return render(request, template_name, context_object)
