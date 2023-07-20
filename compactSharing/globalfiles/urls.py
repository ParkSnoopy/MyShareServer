from django.urls import path
from .views import (
    static, 
    media, 
)


urlpatterns = [
    path('static/<str:appname>/<str:filetype>/<str:filename>', static), 
    path('media/<str:appname>/<str:filetype>/<str:filename>', media), 
]
