from django.shortcuts import redirect, render

from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from core.apps.blog.models.category_models import Category
class ProjectView(LoginRequiredMixin,View):
    
    def get(self,request,*args, **kwargs):
        context = {
          'title':'Projects'
        }
        return render(request,'projects/project_list.html',context)
        