from django.shortcuts import render
from util.query import *

def show_dashboard_pelatih(request):
    nama = execute(f"""SELECT m.nama FROM MEMBER m, PELATIH p WHERE m.id=p.id AND p.id='{request.session['id']}'""")
    email = execute(f"""SELECT m.email FROM MEMBER m, PELATIH p WHERE m.id=p.id AND p.id='{request.session['id']}'""")
    spesialisasi = execute(f"""SELECT s.spesialisasi FROM SPESIALISASI s, PELATIH_SPESIALISASI ps WHERE s.id=ps.id_spesialisasi AND ps.id_pelatih='{request.session['id']}'""")
    tgl_mulai = execute(f"""SELECT p.tanggal_mulai FROM PELATIH p WHERE p.id='{request.session['id']}'""")
    
    context = {
        "nama": nama[0]['nama'],
        "email": email[0]['email'],
        "spesialisasi_kategori": spesialisasi[0]['spesialisasi'],
        "tgl_mulai": tgl_mulai[0]['tanggal_mulai']
    }
    return render(request, "dashboard_pelatih.html", context)

def latih_atlet(request):
  
    return render(request, "form_latih_atlet.html")

def show_atlet(request):
    atlet = execute(f"""
            SELECT ma.nama, ma.email, a.world_rank
            FROM MEMBER ma, MEMBER mp, PELATIH p, ATLET a, ATLET_PELATIH ap
            WHERE mp.id = p.id AND ma.id = a.id AND ap.id_pelatih = p.id
            AND a.id = ap.id_atlet AND mp.nama = '';
            """)

    context = {
        "atlet": atlet,
    }

    return render(request, "show_atlet.html", context)