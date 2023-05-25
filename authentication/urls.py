from django.urls import path
from authentication.views import *

app_name = 'authentication'

urlpatterns = [
    path('register/', show_register, name='register' ),
]