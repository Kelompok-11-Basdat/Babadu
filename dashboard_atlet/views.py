from django.shortcuts import render
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render

from django.shortcuts import render, redirect
from django.db import connection, InternalError

from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from util.query import *
from atlet.query import *
from Babadu.helper.function import *
def show_dashboard_atlet(request):
    data = execute(f"""
    SELECT
  M.Nama AS Nama_Lengkap,
  A.Negara_Asal AS Negara,
  M.Email,
  A.Tgl_Lahir AS Tanggal_Lahir,
  CASE WHEN A.Play_Right THEN 'Right Hand' ELSE 'Left Hand' END AS Play,
  A.Height AS Tinggi_Badan,
  CASE WHEN A.Jenis_Kelamin THEN 'Male' ELSE 'Female' END AS Jenis_Kelamin,
  COALESCE(MC.Nama, '-') AS Pelatih,
  CASE
    WHEN AK.ID_Atlet IS NULL THEN 'Not Qualified'
    ELSE COALESCE(CAST(A.World_Rank AS VARCHAR), '-')
  END AS Status,
  COALESCE(CAST(A.World_Rank AS VARCHAR), '-') AS World_Rank,
  SUM(COALESCE(PH.Total_Point, 0)) AS Total_Poin
FROM
  ATLET A
  INNER JOIN MEMBER M ON A.ID = M.ID
  LEFT JOIN ATLET_PELATIH AP ON A.ID = AP.ID_Atlet
  LEFT JOIN MEMBER MC ON AP.ID_Pelatih = MC.ID
  LEFT JOIN ATLET_KUALIFIKASI AK ON A.ID = AK.ID_Atlet
  LEFT JOIN POINT_HISTORY PH ON A.ID = PH.ID_Atlet
WHERE
  M.ID = '1509b2a8-422a-4cde-bf1b-f289c267d494'
GROUP BY
  M.Nama,
  A.Negara_Asal,
  M.Email,
  A.Tgl_Lahir,
  A.Play_Right,
  A.Height,
  A.Jenis_Kelamin,
  A.World_Rank,
  MC.Nama,
  AK.ID_Atlet;

    """)
    print(data)
    context = {
        'data': data,
    }
    return render(request, "dashboard_atlet.html", context)


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