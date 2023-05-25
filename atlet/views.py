from django.http import HttpResponse
from django.shortcuts import render

from django.shortcuts import render, redirect
from django.db import connection, InternalError

from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from util.query import *
from atlet.query import *
from Babadu.helper.function import *

# Create your views here.

@csrf_exempt
def atlet_ikut_ujian(request):
    print(request.method)
    if request.method == 'POST':
        tahun = request.POST.get("tahun")
        batch = request.POST.get("batch")
        tempat = request.POST.get("tempat")
        tanggal = request.POST.get("tanggal")

        testIsinya = execute(f"""
            SELECT 
                tahun, 
                batch, 
                tempat, 
                tanggal
            FROM ATLET_NONKUALIFIKASI_UJIAN_KUALIFIKASI
            WHERE id_atlet = '{request.session['id']}'
                AND tahun = '{tahun}'
                AND batch = '{batch}'
                AND tempat = '{tempat}'
                AND tanggal = '{tanggal}'
        """)

        print(testIsinya)

        if testIsinya == [] :

            executeUPDATE(f"""
                INSERT INTO ATLET_NONKUALIFIKASI_UJIAN_KUALIFIKASI (ID_Atlet, Tahun, Batch, Tempat, Tanggal, Hasil_Lulus)
                VALUES ('{request.session['id']}', {tahun}, {batch}, '{tempat}', '{tanggal}', 'false');
                """)
            
            print("INI KALO NONE")
            
            return HttpResponse(status=200)

        return HttpResponse(status=400)


    else :
        return HttpResponse(status=404)

@csrf_exempt
def tes_kualifikasi(request):
    if request.method == 'GET':
        return render(request, "tes_kualifikasi.html")
    elif request.method == 'POST':
        lulus = request.POST.get('lulus')
        if lulus == 'true' :
            executeUPDATE(f"""
                UPDATE ATLET_NONKUALIFIKASI_UJIAN_KUALIFIKASI
                SET Hasil_Lulus = true
                WHERE ID_Atlet = '{request.session['id']}'
                    AND (Tahun, Batch, Tempat, Tanggal) = (
                        SELECT Tahun, Batch, Tempat, Tanggal
                        FROM (
                            SELECT Tahun, Batch, Tempat, Tanggal,
                                ROW_NUMBER() OVER (ORDER BY COUNT(*) DESC) AS row_num
                            FROM ATLET_NONKUALIFIKASI_UJIAN_KUALIFIKASI
                            WHERE ID_Atlet = '{request.session['id']}'
                            GROUP BY Tahun, Batch, Tempat, Tanggal
                        ) AS subquery
                        WHERE row_num = 1
                    );
            """)
            # WHERE id_atlet = '{request.session['id']}';
        
            riwayat_ujian_kualifikasi = execute(f"""
            SELECT 
                tahun, 
                batch, 
                tempat, 
                tanggal, 
                hasil_lulus 
            FROM ATLET_NONKUALIFIKASI_UJIAN_KUALIFIKASI a JOIN MEMBER m ON a.ID_Atlet = m.id 
            WHERE id_atlet = '{request.session['id']}';
            """)

            context = {
                "riwayat_ujian_kualifikasi": riwayat_ujian_kualifikasi,
            }

            return HttpResponse(status=200)

        return render(request, "riwayat_ujian_kualifikasi.html", context)


def sql_get_status_kualifikasi(id):
    return f"""
    SELECT 
        K.World_Rank,
        K.World_Tour_Rank,
        CASE
            WHEN K.ID_Atlet IS NOT NULL THEN 'Qualified'
            ELSE 'Not Qualified'
        END AS status_kualifikasi
    FROM ATLET A
    LEFT JOIN ATLET_KUALIFIKASI K ON K.ID_Atlet = A.ID
    LEFT JOIN ATLET_NON_KUALIFIKASI N ON N.ID_Atlet = A.ID
    WHERE A.ID = '{id}';
    """

# """
#     UPDATE atlet_nonkualifikasi_ujian_kualifikasi
#     SET Hasil_Lulus = true
#     WHERE ID_Atlet = '{id}';
#     """

def daftar_event(request):
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

    query_events = "SELECT Nama_Event, Total_Hadiah, Tgl_Mulai, Kategori_superseries FROM EVENT WHERE Nama_Stadium = '{}' AND Tgl_Mulai < CURRENT_DATE".format(pk)
    events = execute(query_events)
    
    context = {
        'events': events
    }
    return render(request, "pilih_event.html", context)

def pilih_partai(request, pk):
    event = execute(f"""
        SELECT Nama_Event, Total_Hadiah, Tgl_Mulai, Tgl_Selesai, Kategori_superseries, Nama_Stadium, event.Negara, s.kapasitas
        FROM EVENT
        JOIN stadium s ON s.nama = event.nama_stadium
        WHERE Nama_Event = '{pk}';
    """)
    context = {
        'event': event,
    }
    return render(request,"pilih_partai.html", context)

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

def get_riwayat_ujian_kualifikasi(request):
    print(request.session['id'])

    riwayat_ujian_kualifikasi = execute(f"""
    SELECT 
        tahun, 
        batch, 
        tempat, 
        tanggal, 
        hasil_lulus 
    FROM ATLET_NONKUALIFIKASI_UJIAN_KUALIFIKASI a JOIN MEMBER m ON a.ID_Atlet = m.id 
    WHERE id_atlet = '{request.session['id']}';
    """)

    context = {
        "riwayat_ujian_kualifikasi": riwayat_ujian_kualifikasi,
    }

    return render(request, "riwayat_ujian_kualifikasi.html", context)



