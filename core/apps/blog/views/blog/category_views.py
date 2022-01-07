# Core Django imports.
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (
    CreateView,
    ListView,
    UpdateView
)
from core.apps.blog.models.article_models import Article, Category
from core.apps.blog.models.article_models import ListAsQuerySet

class CategoryArticlesListView(ListView):
    model = Article
    paginate_by = 10
    context_object_name = 'articles'
    template_name = 'blog/category/category_articles.html'

    def get_queryset(self):
        category = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        return Article.objects.filter(category=category, status=Article.PUBLISHED, deleted=False)


    def get_context_data(self, **kwargs):
        context = super(CategoryArticlesListView, self).get_context_data(**kwargs)
        category = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        articles = category.articles.filter(category=category, status=Article.PUBLISHED, deleted=False)
        
        all_tags = []#tags for articles of respective category
        for article in articles:
            tags = article.tags.all()
            for tag in tags:
                all_tags.append(tag.name)
        
        tags_qs = ListAsQuerySet(all_tags, model=Article)        
        context['category'] = category
        context['tags'] = tags_qs
        return context


# class CategoriesListView(ListView):
#     model = Category
#     paginate_by = 12
#     context_object_name = 'categories'
#     template_name = 'blog/category/categories_list.html'
#     permission_required='blog.add_category' 

#     def get_queryset(self):
#         return Category.objects.order_by('-date_created')


class CategoryCreateView(LoginRequiredMixin, SuccessMessageMixin, PermissionRequiredMixin,CreateView):
    model = Category
    fields = ["name", "image"]
    template_name = 'blog/category/category_form.html'
    success_url = reverse_lazy('blog:categories_list')  
    permission_required='blog.add_category'  


    # def form_valid(self, form):
    #     form.instance.save()
    #     messages.success(self.request, f"'{form.instance.name}' "
    #                                    f"submitted successfully. You will be "
    #                                    f"notified when it is approved."
    #                                    f"Thank you !!!")
    #     return redirect('/')
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Category'
        return context
    

class CategoryUpdateCreateView(LoginRequiredMixin, SuccessMessageMixin,
                               UpdateView):
    model = Category
    fields = ["name", "image"]
    template_name = 'blog/category/category_form.html'
    success_url = reverse_lazy("blog:categories_list")
    success_message = "Category Updated Successfully"
    permission_required='blog.change_category'
    
