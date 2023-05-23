from django.urls import path
from .views import *

app_name = 'umpire'

urlpatterns = [
    path('daftar-atlet/', show_daftar_atlet, name='show-daftar-atlet'),
]