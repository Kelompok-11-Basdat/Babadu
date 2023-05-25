from django.urls import path
from dashboard_atlet.views import show_dashboard_atlet

app_name = 'dashboard_atlet'

urlpatterns = [
    path('', show_dashboard_atlet, name='show_dashboard_atlet'),
]