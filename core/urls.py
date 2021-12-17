

from django.contrib import admin
from django.urls import path, include  
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

handler404 = 'apps.home.views.error_404'

urlpatterns = [

    path('admin/', admin.site.urls),         
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path("", include("apps.authentication.urls",namespace='authentication')), 
    path("dashboard/", include("apps.home.urls",namespace = 'home')),           
    path("", include("apps.blog.urls",namespace='blog')) ,      
    path('password/reset/',auth_views.PasswordResetView.as_view(template_name = 'passwordreset/password_reset_email.html'), name = "password_reset"),
	path('password/reset/done/',auth_views.PasswordResetDoneView.as_view(template_name = 'passwordreset/password_reset_sent.html'), name = "password_reset_done"),
	path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='passwordreset/password_reset_form.html'),name="password_reset_confirm"),  
	path('reset/complete/',auth_views.PasswordResetCompleteView.as_view(template_name='passwordreset/password_reset_complete.html'),name="password_reset_complete"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)