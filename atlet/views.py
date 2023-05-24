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
    # with connection.cursor() as cursor:
    #     cursor.execute("SELECT Nama, Alamat, Kapasitas, Negara FROM STADIUM;")
    #     stadium = cursor.fetchall()
    stadium = execute("""
                        SELECT Nama, Alamat, Kapasitas, Negara
                        FROM STADIUM;
                        """)
    context = {
        "stadiums": stadium,
    }

    return render(request, "daftar_event.html", context)

def pilih_stadium(request, pk):
    # query_stadium = "SELECT Nama, Alamat, Kapasitas, Negara FROM STADIUM WHERE Nama = '{}' LIMIT 1".format(pk)
    # stadium = execute(query_stadium)
    # print(stadium)

    query_events = "SELECT Nama_Event, Total_Hadiah, Tgl_Mulai, Kategori_superseries FROM EVENT WHERE Nama_Stadium = '{}' AND Tgl_Mulai > CURRENT_DATE".format(pk)
    events = execute(query_events)
    print(events)

    context = {
        # 'stadium': stadium,
        'events': events
    }
    return render(request, "pilih_event.html", context)

def pilih_kategori(request, stadium, event):
    return render(request, "pilih_kategori.html")

def form_kualifikasi(request):
    return render(request, "form_kualifikasi.html")

