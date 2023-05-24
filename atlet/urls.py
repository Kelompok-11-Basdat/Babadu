from django.urls import path
from atlet.views import *

app_name = 'atlet'


urlpatterns = [
    path('form-kualifikasi/', form_kualifikasi, name='form_kualifikasi' ),
    path('tes-kualifikasi/', tes_kualifikasi, name='tes_kualifikasi' ),
    path('daftar-event/', daftar_event, name='daftar_event' ),
    path('pilih_stadium/<str:pk>/', pilih_stadium, name='pilih_stadium'),

]