from django.urls import path
# from django.conf import settings
# from django.conf.urls.static import static

from .views import (
    static, media, 
)

urlpatterns = [
    path('static/<str:appname>/<str:filetype>/<str:filename>', static), 
    path('media/<str:appname>/<str:filetype>/<str:filename>', media), 
]

# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
