# -*- encoding: utf-8 -*-
"""

"""

from django.contrib import admin
from django.urls import path, include  # add this
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),          # Django admin route
     path('ckeditor/', include('ckeditor_uploader.urls')),
    path("", include("apps.authentication.urls",namespace='authentication')), # Auth routes - login / register
    path("dashboard/", include("apps.home.urls",namespace = 'home')),           # UI Kits Html files
    path("", include("apps.blog.urls",namespace='blog'))             # UI Kits Html files
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)