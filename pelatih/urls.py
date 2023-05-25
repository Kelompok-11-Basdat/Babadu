from django.urls import path
from pelatih.views import *

app_name = 'pelatih'

urlpatterns = [
    path('', show_dashboard_pelatih, name='show_dashboard_pelatih'),
]