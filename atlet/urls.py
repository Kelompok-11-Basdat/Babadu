from django.urls import path
from atlet.views import *

app_name = 'atlet'


urlpatterns = [
    path('ujian-kualifikasi/', ujian_kualifikasi, name='ujian_kualifikasi' ),
    path('tes-kualifikasi/', tes_kualifikasi, name='tes_kualifikasi' ),
    path('daftar-event/', daftar_event, name='daftar_event' ),
    path('pilih_stadium/<str:pk>/', pilih_stadium, name='pilih_stadium'),
    path('riwayat-ujian-kualifikasi/', get_riwayat_ujian_kualifikasi, name='riwayat_ujian_kualifikasi' ),
    path('pilih_partai/<str:pk>/', pilih_partai, name='pilih_partai'),
    path('atlet-ikut-ujian/', atlet_ikut_ujian, name='atlet_ikut_ujian' ),
    path('enrolled-partai-kompetisi-event/', get_enrolled_partai_kompetisi_event, name='enrolled_partai_kompetisi_event' ),
    path('enrolled-event/', enrolled_event, name='enrolled_event' ),
    path('daftar-sponsor/', daftar_sponsor, name='daftar_sponsor' ),
    path('daftar-sponsor/add', daftar_sponsor, name='daftar_sponsor_add' ),
    path('list-sponsor/', list_sponsor, name='list_sponsor' ),
]