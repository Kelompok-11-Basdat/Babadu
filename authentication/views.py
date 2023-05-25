from django.shortcuts import render
import uuid
from django.shortcuts import render, redirect
from django.db import InternalError
from django.contrib import messages

from django.views.decorators.csrf import csrf_exempt

from util.query import *
from atlet.query import *
from Babadu.helper.function import *


# Create your views here.
@csrf_exempt
def show_register(request):
    if request.method == 'POST':
        if 'submitAtlet' in request.POST:
            nama = request.POST.get('nama')
            email = request.POST.get('email')
            negara_asal = request.POST.get('negara_asal')
            tgl_lahir = request.POST.get('tgl_lahir')
            play_right = request.POST.get('play_right')
            height = request.POST.get('height')
            jenis_kelamin = request.POST.get('jenis_kelamin')
            data = register_atlet(nama, email, negara_asal, tgl_lahir, play_right, height, jenis_kelamin)
            if data['success']:
                return redirect('authentication:login')
            else:
                messages.info(request,data['msg'])
        elif 'submitPelatih' in request.POST:
            nama = request.POST.get('nama')
            email = request.POST.get('email')
            spesialisasi = request.POST.getlist('spesialisasi')
            tanggal_mulai = request.POST.get('tanggal_mulai')
            data = register_pelatih(nama, email, spesialisasi, tanggal_mulai)
            if data['success']:
                return redirect('authentication:login')
            else:
                messages.info(request,data['msg'])
        elif 'submitUmpire' in request.POST:
            nama = request.POST.get('nama')
            email = request.POST.get('email')
            negara = request.POST.get('negara')
            data = register_umpire(nama, email, negara)
            if data['success']:
                return redirect('authentication:login')
            else:
                messages.info(request,data['msg'])
    return render(request, 'register.html')

def register_atlet(nama, email, negara_asal, tgl_lahir, play_right, height, jenis_kelamin):
    try:
        id = uuid.uuid4()

        # create new MEMBER Table Row
        executeUPDATE(f"""
        INSERT INTO
            MEMBER (id, nama, email) 
        VALUES
            (
                '{id}',
                '{nama}',
                '{email}'
            );
        """)

        # create new ATLET Table Row
        executeUPDATE(f"""
        INSERT INTO
            ATLET (
                ID,
                Tgl_Lahir,
                Negara_Asal,
                Play_Right,
                Height,
                World_Rank,
                Jenis_Kelamin
            )
        VALUES
            (
                '{id}',
                '{tgl_lahir}',
                '{negara_asal}',
                {play_right},
                {height},
                0,
                {jenis_kelamin}
            );
        """)

        # query_atlet = sql_insert_atlet(id, tgl_lahir, negara_asal, play_right, height, jenis_kelamin)
        # cursor.execute(query_atlet)
    except InternalError as e:
        return {
            'success': False,
            'msg': str(e.args)
        }
    else:
        return {
            'success': True,
        }
    
def register_pelatih(nama, email, spesialisasi, tanggal_mulai):
    try:
        id = uuid.uuid4()

        # create new MEMBER Table Row
        executeUPDATE(f"""
        INSERT INTO
            MEMBER (id, nama, email) 
        VALUES
            (
                '{id}',
                '{nama}',
                '{email}'
            );
        """)

        # create new PELATIH Table Row
        executeUPDATE(f"""
        INSERT INTO
            PELATIH (ID, Tanggal_Mulai)
        VALUES
            (
                '{id}',
                '{tanggal_mulai}'
            );
        """)

        # create new PELATIH by SPESIALISASI in PELATIH_SPESIALISASI
        for i in spesialisasi:
            executeUPDATE(f"""
                INSERT INTO 
                    PELATIH_SPESIALISASI (ID_Pelatih, ID_Spesialisasi)
                SELECT 
                    '{id}', 
                    ID FROM SPESIALISASI 
                WHERE Spesialisasi = '{i}';
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

def register_umpire(nama, email, negara):
    try:
        id = uuid.uuid4()
        cursor = connection.cursor()
        cursor.execute("SET SEARCH_PATH TO BABADU;")
        query_member = sql_insert_member(id, nama, email)
        cursor.execute(query_member)
        query_umpire = sql_insert_umpire(id, negara)
        cursor.execute(query_umpire)
    except InternalError as e:
        return {
            'success': False,
            'msg': str(e.args)
        }
    else:
        return {
            'success': True,
        }