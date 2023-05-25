from django.shortcuts import render
import uuid
from django.shortcuts import render, redirect
from django.db import InternalError
from django.contrib import messages

from django.views.decorators.csrf import csrf_exempt

from util.query import *
from atlet.query import *
from Babadu.helper.function import *

def homepage(request):
    return render(request, "onboarding.html")

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


        # create new MEMBER Table Row
        executeUPDATE(f"""
        INSERT INTO
            UMPIRE (ID, Negara)
        VALUES
            (
                '{id}',
                '{negara}'
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
    
def fetch(cursor):
    columns = [col[0] for col in cursor.description]
    result = []
    for row in cursor.fetchall():
        row_dict = {}
        for i, col in enumerate(columns):
            row_dict[col] = row[i]
        result.append(row_dict)
    return result

def is_logged(request):
    return 'email' in request.session

SESSION_ROLE_KEYS = {
    'atlet': 'is_atlet',
    'pelatih': 'is_pelatih',
    'umpire': 'is_umpire',
}

# login
@csrf_exempt
def login(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        query = f"""
            SELECT
            M.ID,
            M.Nama,
            M.Email,
            COALESCE(U.ID, P.ID, A.ID) AS ID_Member,
            CASE
                WHEN A.ID IS NOT NULL THEN 'atlet'
                WHEN P.ID IS NOT NULL THEN 'pelatih'
                WHEN U.ID IS NOT NULL THEN 'umpire'
                ELSE 'none'
            END AS role,
            P.Tanggal_Mulai,
            A.Tgl_Lahir,
            A.Negara_Asal,
            A.Play_Right,
            A.Height,
            A.World_Rank,
            U.Negara,
            A.Jenis_Kelamin
        FROM
            MEMBER AS M
            LEFT JOIN UMPIRE AS U ON M.ID = U.ID
            LEFT JOIN ATLET AS A ON M.ID = A.ID
            LEFT JOIN PELATIH AS P ON M.ID = P.ID
        WHERE
            M.Nama = '{name}' and M.email = '{email}';
        """

 
        data = execute(query)

        request.session['is_atlet'] = False
        request.session['is_pelatih'] = False
        request.session['is_umpire'] = False
        if len(data) == 1:
            temp = data[0]
            for attr in temp:
                if isinstance(temp[attr], uuid.UUID):
                    request.session[attr] = str(temp[attr])
                elif isinstance(temp[attr], datetime.date):
                    date = datetime.datetime.strptime(str(temp[attr]), '%Y-%m-%d')
                    formatted_date = date.strftime('%d %B %Y')
                    request.session[attr] = formatted_date
                else:
                    request.session[attr] = temp[attr]
            request.session[SESSION_ROLE_KEYS[temp['role']]] = True

            print("after login")
            print(request.session['is_atlet'])
            print(request.session['is_pelatih'])
            print(request.session['is_umpire'])

            return redirect('atlet:riwayat_ujian_kualifikasi') # sementara ini pake ini karena blm ada dashboard
        else:
            messages.info(request,'Nama atau Email salah')

    if request.method == 'GET':
        return render(request, 'login.html')


def logout(request):
    if "id" in request.session:
        print("before logout")
        print(request.session['is_atlet'])
        print(request.session['is_pelatih'])
        print(request.session['is_umpire'])

        request.session.clear()
        request.session['is_atlet'] = False
        request.session['is_pelatih'] = False
        request.session['is_umpire'] = False

        print("after logout")
        print(request.session['is_atlet'])
        print(request.session['is_pelatih'])
        print(request.session['is_umpire'])
        return redirect('authentication:login')
    return redirect('')