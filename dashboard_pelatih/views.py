from django.shortcuts import render

def show_dashboard_pelatih(request):
    nama = request.session["nama"]
    email = request.session["email"]
    id_pelatih = request.session["member_id"]
    spesialisasi = query("""SELECT S.SPESIALISASI
                    FROM SPESIALISASI S, PELATIH_SPESIALISASI PS
                    WHERE S.ID=PS.ID_SPESIALISASI
                    AND ID_PELATIH='{}';
                    """.format(id_pelatih))
    spesialisasi = ', '.join([s["spesialisasi"] for s in spesialisasi])

    tgl_mulai = query(f"SELECT tanggal_mulai FROM PELATIH WHERE ID='{id_pelatih}'")[0]["tanggal_mulai"]
    
    context = {
        "nama": nama,
        "email": email,
        "spesialisasi": spesialisasi,
        "tgl_mulai": tgl_mulai
    }
    
    return render(request, 'dashboard-pelatih.html', context)
