from django.shortcuts import redirect, render

from django.views.generic import View

class ProjectView(View):
    
    def get(self,request,*args, **kwargs):
        return render(request,'projects/project_list.html')
        