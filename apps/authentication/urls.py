# -*- encoding: utf-8 -*-
"""

"""

from django.urls import path
from .views import (
  # login_view, 
  #                   UserRegisterView,
  #                   UserLogoutView,
  #                     ActivateView,
  #               AccountActivationSentView,
                SubscriptionView,
                SubscriptionActivateView,
                SendEmail
                )
# from allauth.account.views import LoginView, SignupView 

app_name = 'authentication'
urlpatterns = [
    # path('login/', login_view, name="login"),
    # path('register/', UserRegisterView.as_view(), name="register"),
    #  path('login/', LoginView.as_view(), name="login"),
      # path('register/', SignupView.as_view(), name="register"),
    #  path("logout/", LogoutView.as_view(), name="logout"),
    
    # path(route='account_activation_sent/',
    #      view=AccountActivationSentView.as_view(),
    #      name='account_activation_sent'
    #      ),

    # path(route='activate/<uidb64>/<token>/',
    #      view=ActivateView.as_view(),
    #      name='activate'
    #      ), 
      path('email_sent/', SendEmail.as_view(), name="email_sent"),
    path('user_subscription/', SubscriptionView.as_view(), name="user_subscription"),
    path('user_subscription/', SubscriptionView.as_view(), name="user_subscription"),
    path(route='subscription_activate/<uidb64>/<token>/',
         view=SubscriptionActivateView.as_view(),
         name='subscription_activate'
         ),

]
