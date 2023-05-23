from django.urls import path
from .views import *

app_name = 'umpire'

urlpatterns = [
    path('form-kualifikasi/', form_buat_ujian_kualifikasi, name='form_kualifikasi' ),
    path('daftar-atlet/', show_daftar_atlet, name='show-daftar-atlet'),
    path('ujian-kualifikasi-umpire/', ujian_kualifikasi_umpire, name='ujian_kualifikasi_umpire' ),
]