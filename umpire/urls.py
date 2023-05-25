from django.urls import path
from .views import *

app_name = 'umpire'

urlpatterns = [
    path('', show_dashboard_umpire, name='show_dashboard_umpire' ),
    path('form-kualifikasi/', form_buat_ujian_kualifikasi, name='form_kualifikasi' ),
    path('daftar-atlet/', show_daftar_atlet, name='show_daftar_atlet'),
    path('ujian-kualifikasi-umpire/', ujian_kualifikasi_umpire, name='ujian_kualifikasi_umpire' ),
    path('riwayat-ujian-kualifikasi-umpire/', riwayat_ujian_kualifikasi_umpire, name='riwayat_ujian_kualifikasi_umpire' ),
]