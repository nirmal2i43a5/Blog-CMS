# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from .views import (login_view, 
                    UserRegisterView,
                    UserLogoutView,
                      ActivateView,
                AccountActivationSentView,)

app_name = 'authentication'
urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', UserRegisterView.as_view(), name="register"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
       path(route='account_activation_sent/',
         view=AccountActivationSentView.as_view(),
         name='account_activation_sent'
         ),

    path(route='activate/<uidb64>/<token>/',
         view=ActivateView.as_view(),
         name='activate'
         ),

]
