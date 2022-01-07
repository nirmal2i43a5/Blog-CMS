from django.urls import path
from .views import ProjectView

app_name = 'myprojects'

urlpatterns = [
    path(
         route='list/',
        view=ProjectView.as_view(),
        name="projects"
        
        )
]
