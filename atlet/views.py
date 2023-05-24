from django.shortcuts import render

from django.shortcuts import render, redirect
from django.db import connection, InternalError

from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages


from util.query import *

# Create your views here.
def tes_kualifikasi(request):
    return render(request, "tes_kualifikasi.html")

def daftar_event(request):
    stadium = execute("""
                        SELECT Nama, Alamat, Kapasitas, Negara
                        FROM STADIUM;
                        """)
    context = {
        "stadium": stadium,
    }
    return render(request, "daftar_event.html", context)


def pilih_event(request, stadium):
    return render(request, "pilih_event.html")

def pilih_kategori(request, stadium, event):
    return render(request, "pilih_kategori.html")

def form_kualifikasi(request):
    return render(request, "form_kualifikasi.html")

