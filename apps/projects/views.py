from django.shortcuts import redirect, render

from django.views.generic import View

class ProjectView(View):
    def get(self,request,*args, **kwargs):
        return redirect(request,'projects/project_list.html')
        