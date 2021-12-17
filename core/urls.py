# -*- encoding: utf-8 -*-
"""

"""

from django.contrib import admin
from django.urls import path, include  # add this
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),          # Django admin route
     path('ckeditor/', include('ckeditor_uploader.urls')),
    path("", include("apps.authentication.urls",namespace='authentication')), # Auth routes - login / register
    path("dashboard/", include("apps.home.urls",namespace = 'home')),           # UI Kits Html files
    path("", include("apps.blog.urls",namespace='blog'))   ,          # UI Kits Html files
    
                  #For resetting password via email follow below four link 
    path('password/reset/',auth_views.PasswordResetView.as_view(template_name = 'passwordreset/password_reset_email.html'), 
		 name = "password_reset"),
	
	path('password/reset/done/',auth_views.PasswordResetDoneView.as_view(template_name = 'passwordreset/password_reset_sent.html'), 
		 name = "password_reset_done"),
	
	path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='passwordreset/password_reset_form.html'),
		 name="password_reset_confirm"),  
	   
	 #<token> check  for valid user or not--><uidb64> user id encoded in base 64--this email is sent to the user
	 #<uidb64> helps to know user who request for password
	path('reset/complete/',auth_views.PasswordResetCompleteView.as_view(template_name='passwordreset/password_reset_complete.html'),
		 name="password_reset_complete"),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)