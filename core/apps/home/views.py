

from django import template
from django.contrib.auth.decorators import login_required,permission_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from core.apps.blog.models import Article
from core.apps.authentication.models import Subscription


@login_required(login_url="/login/")
def author_dashboard(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/author_dashboard.html')
    return HttpResponse(html_template.render(context, request))

class DashboardHomeView(LoginRequiredMixin,PermissionRequiredMixin,View):
    permission_required = 'blog.view_article'
    context = {}
    template_name = 'home/author_dashboard.html'

 
    def get(self, request, *args, **kwargs):
        """
        Returns the author details
        """

        articles_list = Article.objects.filter(author=request.user)

        total_articles_written = articles_list.count()
        total_articles_published = articles_list.filter(status=Article.PUBLISHED, deleted=False).count()
        total_articles_views = sum(article.views for article in articles_list)
        # total_articles_comments = sum(
        #     article.comments.count() for article in articles_list)

        recent_published_articles_list = articles_list.filter(
            status=Article.PUBLISHED, deleted=False).order_by("-date_published")[:5]

        self.context['total_articles_written'] = total_articles_written
        self.context['total_articles_published'] = total_articles_published
        self.context['total_articles_views'] = total_articles_views
        # self.context['total_articles_comments'] = total_articles_comments
        self.context['recent_published_articles_list'] = recent_published_articles_list

        return render(request, self.template_name, self.context)
    


@csrf_exempt
def check_email_exist(request):
    email = request.POST.get('email')
    subscription_email = Subscription.objects.filter(email = email).exists()
    if subscription_email:
        return HttpResponse(True)
    else:
        return HttpResponse(False)
    
    
@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


def error_404(request, exception):
        data = {}
        return render(request,'home/page-404.html', data)