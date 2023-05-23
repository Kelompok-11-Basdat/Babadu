from django.shortcuts import render

from django.shortcuts import render, redirect
from django.db import connection, InternalError

from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from util.query import *
from atlet.query import *
from Babadu.helper.function import *

# Create your views here.
def tes_kualifikasi(request):
    return render(request, "tes_kualifikasi.html")

def daftar_event(request):
    return render(request, "daftar_event.html")

def pilih_event(request, stadium):
    return render(request, "pilih_event.html")

def pilih_kategori(request, stadium, event):
    return render(request, "pilih_kategori.html")

def ujian_kualifikasi(request):
    #GET LIST UJIAN KUALIFIKASI
    ujian_kualifikasi = execute("""
    SELECT
        Tahun,
        Batch,
        Tempat,
        Tanggal
    FROM UJIAN_KUALIFIKASI;
    """)

    context = {
        "ujian_kualifikasi": ujian_kualifikasi,
    }

    return render(request, "ujian_kualifikasi.html", context)

