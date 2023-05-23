def sql_get_pelatih_atlet(id):
    return f""" 
    SELECT M.nama
    FROM ATLET_PELATIH AP
        JOIN PELATIH P ON P.ID = AP.ID_Pelatih
        JOIN ATLET A ON A.ID = AP.ID_ATLET
        JOIN MEMBER M ON P.ID = M.ID
    WHERE A.ID = '{id}';
    """



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

def sql_get_total_point(id):
    return f"""
    SELECT 
        SUM(total_point) as total_point
    FROM ATLET A
    JOIN POINT_HISTORY PH ON PH.ID_Atlet = A.ID
    WHERE A.ID = '{id}';
    """

def sql_get_daftar_event():
    return f"""
    SELECT
        Nama,
        Negara,
        Kapasitas
    FROM STADIUM
    """

def sql_get_detail_stadium(nama_stadium):
    return f"""
    SELECT
        Nama_Event,
        Total_Hadiah,
        Tgl_Mulai,
        Kategori_Superseries
    FROM EVENT
    WHERE Nama_Stadium = '{nama_stadium}' AND Tgl_Mulai > NOW();
    """

def sql_get_detail_event(nama_event):
    return f"""
    SELECT
        E.Nama_Event,
        E.Total_Hadiah,
        E.Tgl_Mulai,
        E.Tgl_Selesai,
        E.Kategori_Superseries,
        S.Kapasitas,
        S.Nama as nama_stadium,
        S.Negara
    FROM EVENT E JOIN STADIUM S ON E.Nama_Stadium = S.Nama
    WHERE E.Nama_Event = '{nama_event}';
    """

def sql_get_partai_kompetisi(nama_event, tahun):
    return f"""
    SELECT 
        CASE
            WHEN PK.Jenis_Partai = 'MS' THEN 'Tunggal Putra'
            WHEN PK.Jenis_Partai = 'WS' THEN 'Tunggal Putri'
            WHEN PK.Jenis_Partai = 'MD' THEN 'Ganda Putra'
            WHEN PK.Jenis_Partai = 'WD' THEN 'Ganda Putri'
            WHEN PK.Jenis_Partai = 'XD' THEN 'Ganda Campuran'
        END AS jenis_partai
    FROM PARTAI_KOMPETISI PK
    WHERE Nama_Event = '{nama_event}' AND tahun_event = '{tahun}';
    """

def sql_get_partner(jenis_kelamin):
    return f"""
    SELECT
        M.Nama
        FROM
            ATLET_KUALIFIKASI AK
            JOIN MEMBER M ON AK.ID_Atlet = M.ID
            JOIN ATLET A ON A.ID = AK.ID_Atlet
        WHERE
            A.Jenis_kelamin = {jenis_kelamin};
    """

def sql_get_list_ujian_kualifikasi():
    return f"""
    SELECT
        Tahun,
        Batch,
        Tempat,
        Tanggal
    FROM UJIAN_KUALIFIKASI
    """

def sql_get_riwayat_ujian_kualifikasi(id):
    return f"""
    SELECT tahun, batch, tempat, tanggal, hasil_lulus FROM ATLET_NONKUALIFIKASI_UJIAN_KUALIFIKASI a JOIN MEMBER m ON a.ID_Atlet = m.id 
    WHERE id_atlet = '{id}';
    """