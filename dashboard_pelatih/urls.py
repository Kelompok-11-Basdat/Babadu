from django.urls import path
from dashboard_pelatih.views import *

app_name = 'dashboard_pelatih'

urlpatterns = [
    path('', show_dashboard_pelatih, name='show_dashboard_pelatih'),
]