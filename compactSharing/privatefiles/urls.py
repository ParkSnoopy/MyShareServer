from django.urls import path
from .views import (
    privatefiles, 
)


urlpatterns = [
    path('', privatefiles), 
]
