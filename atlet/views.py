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

    query_events = "SELECT Nama_Event, Total_Hadiah, Tgl_Mulai, Kategori_superseries FROM EVENT WHERE Nama_Stadium = '{}' AND Tgl_Mulai > CURRENT_DATE".format(pk)
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

def get_enrolled_partai_kompetisi_event(request):
    enrolled_partai_kompetisi_event = execute(f"""
        SELECT e.Nama_Event, Tahun, Nama_Stadium, Jenis_Partai, Kategori_Superseries, Tgl_Mulai, Tgl_Selesai 
        FROM EVENT e, PARTAI_KOMPETISI p 
        WHERE e.Nama_Event = p.Nama_Event AND Tahun = Tahun_Event;
    """)
    context = {
        'enrolled_partai_kompetisi_event': enrolled_partai_kompetisi_event,
    }
    return render(request,"enrolled_partai_kompetisi_event.html", context)

def enrolled_event(request):
    enrolled_event = execute(f"""
        SELECT Nama_Event, Tahun, Nama_Stadium, Kategori_Superseries, Tgl_Mulai, Tgl_Selesai 
        FROM EVENT;
    """)
    context = {
        'enrolled_event': enrolled_event,
    }
    return render(request,"enrolled_event.html", context)

@csrf_exempt
def daftar_sponsor(request):
    if request.method == 'POST':
        if 'submitFormUjian' in request.POST:
            nama = request.POST.get('nama')
            tanggalmulai = request.POST.get('tanggalmulai')
            tanggalselesai = request.POST.get('tanggalselesai')
            data = buat_sponsor(nama, tanggalmulai, tanggalselesai, request)
            if data['success']:
                return redirect('atlet:list_sponsor')
            else:
                messages.info(request,data['msg'])
    return render(request, "daftar_sponsor.html")

def list_sponsor(request):
    print(request.session['id'])

    list_sponsor = execute(f"""
        SELECT Nama_Brand, Tgl_Mulai, Tgl_Selesai 
        FROM SPONSOR, ATLET_SPONSOR 
        WHERE ID = ID_Sponsor AND ID_Atlet = '{request.session['id']}';
    """)
    context = {
        'list_sponsor': list_sponsor,
    }
    return render(request,"list_sponsor.html", context)

def buat_sponsor(nama, tanggalmulai, tanggalselesai, request):
    try:
        executeUPDATE(f"""
        INSERT INTO 
            ATLET_SPONSOR(ID_Atlet, ID_Sponsor, Tgl_Mulai, Tgl_Selesai)
        VALUES
        (
            (SELECT DISCTINCT ID FROM SPONSOR WHERE Nama_Brand = '{nama}'),
            '{request.session['id']}',
            '{tanggalmulai}',
            '{tanggalselesai}'
        );
        """)
    except InternalError as e:
        return {
            'success': False,
            'msg': str(e.args)
        }
    else:
        return {
            'success': True,
        }

def dropdown(request):
    sponsor = execute(f"""
        SELECT DISTINCT s.Nama_Brand
        FROM SPONSOR s
        WHERE s.ID NOT IN (
        SELECT ID_SPONSOR
        FROM ATLET_SPONSOR
        WHERE ID_ATLET = '{request.session['id']}'
        );
    """)
    context = {
        'sponsor': sponsor,
    }
    return render(request,"daftar_sponsor.html", context)