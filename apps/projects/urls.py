from django.urls import path
from .views import ProjectView

app_name = 'myprojects'

urlpatterns = [
    path('projects/list/',ProjectView.as_view(),name = 'projects')
]
