from django.urls import path
from .views import (
    lightfileshare_home, 
    lightfileshare_details, 
    lightfileshare_details_pwcheck, 
    lightfileshare_details_fail, 
    lightfileshare_create, 
)



urlpatterns = [
    path('', lightfileshare_home), 
    path('details/', lightfileshare_details), 
    path('details/verify/', lightfileshare_details_pwcheck), 
    path('details/verify/failure/', lightfileshare_details_fail), 
    path('create/', lightfileshare_create), 
    
]
