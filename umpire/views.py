from django.db import InternalError
from django.shortcuts import redirect, render
from util.query import *
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from umpire.query import *

def show_dashboard_umpire(request):
    nama = execute(f"""SELECT m.nama FROM MEMBER m, UMPIRE u WHERE m.id=u.id AND u.id='{request.session['id']}'""")
    email = execute(f"""SELECT m.email FROM MEMBER m, UMPIRE u WHERE m.id=u.id AND u.id='{request.session['id']}'""")
    negara = execute(f"""SELECT u.negara FROM UMPIRE u WHERE u.id='{request.session['id']}'""")
    
    context = {
        "nama": nama,
        "email": email,
        "negara": negara
    }
    return render(request, "dashboard_umpire.html", context)

def show_daftar_atlet(request):
    atlet_kualifikasi = execute("""
                        SELECT DISTINCT m.nama, a.tgl_lahir, a.negara_asal, a.play_right, a.height, ak.world_rank, ak.world_tour_rank, a.jenis_kelamin, p.total_point
                        FROM ATLET_KUALIFIKASI ak
                        LEFT OUTER JOIN MEMBER m ON m.id = ak.id_atlet
                        LEFT OUTER JOIN ATLET a ON a.id = ak.id_atlet
                        LEFT JOIN POINT_HISTORY p ON ak.id_atlet = p.id_atlet
                        AND p.total_point IN (
                            SELECT total_point FROM POINT_HISTORY p
                            WHERE ak.id_atlet = p.id_atlet
                            ORDER BY (tahun, bulan, minggu_ke) DESC LIMIT 1
                        );
                        """)

    atlet_non_kualifikasi = execute("""
                        SELECT DISTINCT m.nama, a.tgl_lahir, a.negara_asal, a.play_right, a.height, a.jenis_kelamin
                        FROM ATLET_NON_KUALIFIKASI an
                        LEFT OUTER JOIN MEMBER m ON m.id = an.id_atlet
                        LEFT OUTER JOIN ATLET a ON a.id = an.id_atlet
                        """)
    
    atlet_ganda = execute("""
                        SELECT ag.id_atlet_ganda, m1.nama AS nama_1, m2.nama AS nama_2, SUM(p1.total_point + p1.total_point) AS total_point
                        FROM ATLET_GANDA ag
                        LEFT OUTER JOIN MEMBER m1 ON m1.id = ag.id_atlet_kualifikasi
                        LEFT OUTER JOIN MEMBER m2 ON m2.id = ag.id_atlet_kualifikasi_2
                        LEFT OUTER JOIN POINT_HISTORY p1 ON p1.id_atlet = ag.id_atlet_kualifikasi
                        AND p1.total_point IN (
                            SELECT total_point FROM POINT_HISTORY p
                            WHERE ag.id_atlet_kualifikasi = p.id_atlet
                            ORDER BY (tahun, bulan, minggu_ke) DESC LIMIT 1
                        )
                        LEFT OUTER JOIN POINT_HISTORY p2 ON p2.id_atlet = ag.id_atlet_kualifikasi_2
                        AND p2.total_point IN (
                            SELECT total_point FROM POINT_HISTORY p
                            WHERE ag.id_atlet_kualifikasi_2 = p.id_atlet
                            ORDER BY (tahun, bulan, minggu_ke) DESC LIMIT 1
                        )
                        GROUP BY ag.id_atlet_ganda, m1.nama, m2.nama;
                      """)

    context = {
        "atlet_kualifikasi": atlet_kualifikasi,
        "atlet_non_kualifikasi": atlet_non_kualifikasi,
        "atlet_ganda": atlet_ganda,
    }

    return render(request, "daftar_atlet.html", context)

def buat_tes_kualifikasi(tahun, batch, tempat, tanggal):
    try:
        query = execute(f"""
        INSERT INTO 
            UJIAN_KUALIFIKASI(Tahun, Batch, Tempat, Tanggal)
        VALUES
        (
            {tahun},
            {batch},
            {tempat},
            '{tanggal}'
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
        

@csrf_exempt
def form_buat_ujian_kualifikasi(request):
    if request.method == 'POST':
         if 'submitFormUjian' in request.POST:
            tahun = request.POST.get('tahun')
            batch = request.POST.get('batch')
            tempat = request.POST.get('tempat')
            tanggal = request.POST.get('tanggal')
            data = buat_tes_kualifikasi(tahun, batch, tempat, tanggal)
            if data['success']:
                return redirect('umpire:ujian_kualifikasi_umpire')
            else:
                messages.info(request,data['msg'])
    return render(request, "form_kualifikasi.html")

def ujian_kualifikasi_umpire(request):
    # GET UJIAN KUALIFIKASI from database
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

    return render(request, "ujian_kualifikasi_umpire.html", context)

def riwayat_ujian_kualifikasi_umpire(request):
    #GET RIWAYAT UJIAN KUALIFIKASI
    riwayat_ujian_kualifikasi_umpire = execute("""
    SELECT
        nama,
        tahun,
        batch,
        tempat,
        tanggal,
        Hasil_Lulus
    FROM ATLET_NONKUALIFIKASI_UJIAN_KUALIFIKASI a JOIN MEMBER m ON a.ID_Atlet = m.id
    """)

    context = {
        "riwayat_ujian_kualifikasi_umpire": riwayat_ujian_kualifikasi_umpire,
    }

    return render(request, "riwayat_ujian_kualifikasi_umpire.html", context)

def list_event(request):
    events = execute("""
        SELECT e.Nama_event, e.Tahun, e.Nama_stadium, pk.Jenis_partai, e.Kategori_Superseries, e.Tgl_mulai, e.Tgl_selesai, COUNT(PPK.nomor_peserta) AS jumlah_peserta, S.Kapasitas
        FROM EVENT e, STADIUM s, PARTAI_KOMPETISI pk, PARTAI_PESERTA_KOMPETISI ppk
        WHERE e.Nama_event = pk.Nama_event AND e.Nama_stadium = s.Nama AND e.Tahun = pk.Tahun_event
        AND ppk.Nama_event = pk.Nama_event AND ppk.Tahun_event = pk.Tahun_event
        AND ppk.Jenis_partai = pk.Jenis_partai
        GROUP BY e.Nama_event, e.Tahun, e.Nama_stadium, pk.Jenis_partai, e.Kategori_Superseries, e.Tgl_mulai, e.Tgl_selesai, s.Kapasitas;
        """)
    
    context = {
        "events": events
    }

    return render(request, "partai_kompetisi_event.html", context)