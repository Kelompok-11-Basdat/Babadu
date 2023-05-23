from django.urls import path
from atlet.views import *

app_name = 'atlet'


urlpatterns = [
    path('ujian-kualifikasi/', ujian_kualifikasi, name='ujian_kualifikasi' ),
    path('tes-kualifikasi/', tes_kualifikasi, name='tes_kualifikasi' ),
    path('daftar-event/', daftar_event, name='daftar_event' ),
    path('daftar-event/<slug:stadium>/', pilih_event, name='pilih_event' ),
    path('daftar-event/<slug:stadium>/<slug:event>/', pilih_kategori, name='pilih_kategori' ),
    

]