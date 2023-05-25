from django.urls import path
from pertandingan.views import pertandingan_perempat, pertandingan_semifinal, pertandingan_juara_tiga, pertandingan_final

app_name = 'pertandingan'

urlpatterns = [
    path('perempat', pertandingan_perempat, name='pertandingan_perempat'),
    path('semifinal', pertandingan_semifinal, name='pertandingan_semifinal'),
    path('juaratiga', pertandingan_juara_tiga, name='pertandingan_juara_tiga'),
    path('final', pertandingan_final, name='pertandingan_final')
]