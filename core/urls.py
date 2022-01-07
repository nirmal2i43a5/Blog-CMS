

from django.contrib import admin
from django.apps import apps
from django.urls import path, include  
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from core.apps.authentication.views import ( 
                    UserLogoutView,
                # login_view,
                # UserRegisterView,
                AccountActivationSentView,
                ActivateView
                )
from allauth.account.views import (LoginView, 
                                   SignupView ,
                                  #  EmailVerificationSentView,
                                   EmailView)



urlpatterns = [

    path('nirmalad3i2/', admin.site.urls),  
    # path('login/', login_view, name="login"),
      path('login/', LoginView.as_view(), name="login"),
    
    path('register/', SignupView.as_view(), name="register"),    
    path("logout/", UserLogoutView.as_view(), name="logout"),
    
    #   path(route='account_activation_sent/',
    #      view=AccountActivationSentView.as_view(),
    #      name='account_activation_sent'
    #      ),

    path(route='activate/<uidb64>/<token>/',
         view=ActivateView.as_view(),
         name='activate'
         ), 
    
      path("email/", EmailView.as_view(), name="account_email"),#for resending verification link 
    # account_activation_sent
       path(
        "confirm-email/",
       AccountActivationSentView.as_view(),
        name="account_email_verification_sent",
    ),#for default verification link
    
    path("", include("core.apps.authentication.urls",namespace='authentication')), 
    path("dashboard/", include("core.apps.home.urls",namespace = 'home')),           
    path("", include("core.apps.blog.urls",namespace='blog')) , 
     path("", include("core.apps.projects.urls",namespace='myprojects')) , 
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('allauth.urls')), # new
    path('password/reset/',auth_views.PasswordResetView.as_view(template_name = 'passwordreset/password_reset_email.html'), name = "password_reset"),
    path('password/reset/done/',auth_views.PasswordResetDoneView.as_view(template_name = 'passwordreset/password_reset_sent.html'), name = "password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='passwordreset/password_reset_form.html'),name="password_reset_confirm"),  
    path('reset/complete/',auth_views.PasswordResetCompleteView.as_view(template_name='passwordreset/password_reset_complete.html'),name="password_reset_complete"),
        
    
]

# handler404 = 'core.apps.home.views.error_404'
# handler500 = 'core.apps.home.views.error_500'

                
if settings.DEBUG:
    # import debug_toolbar
    urlpatterns += static(settings.STATIC_URL,
                      document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
    urlpatterns = [path('__debug__/', include('debug_toolbar.urls'))] + urlpatterns
    # if apps.is_installed("silk"):
    urlpatterns = [path("silk/", include("silk.urls",namespace='silk'))] + urlpatterns

  
