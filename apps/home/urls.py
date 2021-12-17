

from django.urls import path, re_path
from .views import (DashboardHomeView,pages,check_email_exist)

app_name = 'home'
urlpatterns = [

    # The home page
    path('', DashboardHomeView.as_view(), name='dashboard'),
        path('check_email_exist/', check_email_exist, name='check_email_exist'),

    # Matches any html file
    re_path(r'^.*\.*', pages, name='pages'),

]
