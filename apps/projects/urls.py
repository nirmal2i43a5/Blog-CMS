from django.urls import path
from .views import ProjectView

app_name = 'myprojects'

urlpatterns = [
    path('/',ProjectView.as_view,name = 'projects')
]
