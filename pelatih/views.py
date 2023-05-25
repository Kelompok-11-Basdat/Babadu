from django.shortcuts import render

def show_dashboard_pelatih(request):
    nama = execute(f"""SELECT m.nama FROM MEMBER m, PELATIH p WHERE m.id=p.id AND p.id='{request.session['id']}'""")
    email = execute(f"""SELECT m.email FROM MEMBER m, PELATIH p WHERE m.id=p.id AND p.id='{request.session['id']}'""")
    spesialisasi = execute(f"""SELECT s.spesialisasi FROM SPESIALISASI s, PELATIH_SPESIALISASI ps WHERE s.id=ps.id_spesialisasi AND ps.id_pelatih='{request.session['id']}'""")
    tgl_mulai = execute(f"""SELECT p.tanggal_mulai FROM PELATIH p WHERE p.id='{request.session['id']}'""")
    
    context = {
        "nama": nama,
        "email": email,
        "spesialisasi_kategori": spesialisasi,
        "tgl_mulai": tgl_mulai
    }
    return render(request, "dashboard_pelatih.html", context)

def latih_atlet(request):
  
  return render(request, "form_latih_atlet.html")

def show_atlet(request):
  
  return render(request, "form_latih_atlet.html")