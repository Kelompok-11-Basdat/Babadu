from django.http import HttpResponse
from django.shortcuts import render

from django.shortcuts import render, redirect
# from django.db import connection, InternalError

from django.views.decorators.csrf import csrf_exempt

from util.query import *
# from atlet.query import *
# from Babadu.helper.function import *

@csrf_exempt
def pertandingan_perempat(request):

    if request.method == 'POST':
        nama_event = request.POST.get("nama_event")
        tahun_event = request.POST.get("tahun_event")

        # nama_event = "Net Nuisance"
        # tahun_event = 2020

        query = """
            -- Atlet Ganda
            (SELECT M.Nama
            FROM ATLET_GANDA AS AG, MEMBER AS M
            WHERE (AG.ID_Atlet_Kualifikasi = M.ID OR AG.ID_Atlet_Kualifikasi_2 = M.ID)
            AND AG.ID_Atlet_Ganda IN
                (SELECT PK.ID_Atlet_Ganda
                FROM PESERTA_KOMPETISI AS PK
                WHERE PK.ID_Atlet_Ganda IS NOT NULL
                AND Nomor_Peserta IN
                    (SELECT PPK.Nomor_Peserta
                    FROM PARTAI_PESERTA_KOMPETISI AS PPK
                    WHERE PPK.Nama_Event = '{nama_event}'
                    AND PPK.Tahun_Event = {tahun_event})))
            UNION
            -- Atlet tunggal
            (SELECT M.Nama
            FROM MEMBER AS M
            WHERE 
            AND M.ID IN
                (SELECT PK.ID_Atlet_Kualifikasi
                FROM PESERTA_KOMPETISI AS PK
                WHERE PK.ID_Atlet_Ganda IS NULL
                AND Nomor_Peserta IN
                    (SELECT PPK.Nomor_Peserta
                    FROM PARTAI_PESERTA_KOMPETISI AS PPK
                    WHERE PPK.Nama_Event = '{nama_event}'
                    AND PPK.Tahun_Event = {tahun_event})))
        """

        data = execute(query=query)
        # print(data)

        context = {
            data : data,
        }
        return render(request, 'pertandingan_perempat.html', context)

@csrf_exempt
def pertandingan_semifinal(request):
    if request.method == 'POST':

        context = {

        }
        return render(request, 'pertandingan_semifinal.html', context)

@csrf_exempt
def pertandingan_juara_tiga(request):
    if request.method == 'POST':
        context = {

        }
        return render(request, 'pertandingan_juara_tiga.html', context)

@csrf_exempt
def pertandingan_final(request):
    if request.method == 'POST':
        context = {

        }
        return render(request, 'pertandingan_final.html', context)