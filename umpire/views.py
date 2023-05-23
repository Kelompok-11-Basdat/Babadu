from django.shortcuts import render
from util.query import *

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


