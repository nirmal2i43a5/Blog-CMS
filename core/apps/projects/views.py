from django.shortcuts import redirect, render

from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

class ProjectView(LoginRequiredMixin,View):
    
    def get(self,request,*args, **kwargs):
        return render(request,'projects/project_list.html')
        