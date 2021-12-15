# -*- encoding: utf-8 -*-
"""

"""

from django.urls import path, re_path
from .views import (DashboardHomeView,pages)

app_name = 'home'
urlpatterns = [

    # The home page
    path('', DashboardHomeView.as_view(), name='dashboard'),

    # Matches any html file
    re_path(r'^.*\.*', pages, name='pages'),

]
