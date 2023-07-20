from django.urls import path
from .views import (
    clipboardshare_home, 
    clipboardshare_details, 
    clipboardshare_details_pwcheck, 
    clipboardshare_details_fail, 
    clipboardshare_create, 
)



urlpatterns = [
    path('', clipboardshare_home), 
    path('details/', clipboardshare_details), 
    path('details/verify/', clipboardshare_details_pwcheck), 
    path('details/verify/failure/', clipboardshare_details_fail), 
    path('create/', clipboardshare_create), 
    
]
