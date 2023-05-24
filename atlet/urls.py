from django.urls import path
from atlet.views import *

app_name = 'atlet'


urlpatterns = [
    path('ujian-kualifikasi/', ujian_kualifikasi, name='ujian_kualifikasi' ),
    path('tes-kualifikasi/', tes_kualifikasi, name='tes_kualifikasi' ),
    path('daftar-event/', daftar_event, name='daftar_event' ),
    path('pilih_stadium/<str:pk>/', pilih_stadium, name='pilih_stadium'),
    path('riwayat-ujian-kualifikasi/', get_riwayat_ujian_kualifikasi, name='riwayat_ujian_kualifikasi' ),

    path('atlet-ikut-ujian/', atlet_ikut_ujian, name='atlet_ikut_ujian' ),

]