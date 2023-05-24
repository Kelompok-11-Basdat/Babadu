from django.shortcuts import render
from django.db import connection

def show_dashboard_atlet(request):
    cursor = connection.cursor()
    cursor.execute("""
        SELECT
            M.Nama AS "Nama lengkap",
            A.Negara_Asal AS "Negara",
            M.Email AS "Email",
            A.Tgl_Lahir AS "Tanggal lahir",
            CASE
                WHEN A.Play_Right THEN 'Right Hand'
                ELSE 'Left Hand'
            END AS "Play",
            A.Height AS "Tinggi badan",
            CASE
                WHEN A.Jenis_Kelamin THEN 'Laki-laki'
                ELSE 'Perempuan'
            END AS "Jenis Kelamin",
            COALESCE(P.Memiliki_Pelatih, '-') AS "Pelatih",
            CASE
                WHEN AK.ID_Atlet IS NOT NULL THEN 'Qualified'
                ELSE 'Not Qualified'
            END AS "Status",
            COALESCE(CAST(A.World_Rank AS VARCHAR), '-') AS "World rank",
            COALESCE(PH.Total_Point, 0) AS "Total poin"
        FROM
            ATLET A
            INNER JOIN MEMBER M ON A.ID = M.ID
            LEFT JOIN ATLET_KUALIFIKASI AK ON A.ID = AK.ID_Atlet
            LEFT JOIN (
                SELECT ID_Pelatih, 'Yes' AS Memiliki_Pelatih
                FROM ATLET_PELATIH
            ) P ON A.ID = P.ID_Pelatih
            LEFT JOIN POINT_HISTORY PH ON A.ID = PH.ID_Atlet
        ORDER BY
            CASE
                WHEN A.World_Rank IS NULL THEN 1
                ELSE 0
            END,
            A.World_Rank,
            M.Nama;
    """)
    data = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    context = {
        'columns': columns,
        'data': data
    }
    return render(request, 'dashboard_atlet.html', context)