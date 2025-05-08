import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import openpyxl
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
from datetime import date
from scipy.interpolate import interp1d
from streamlit_gsheets import GSheetsConnection

# Sidebar dengan navbar hijau
with st.sidebar:
    selected = option_menu(
        menu_title=None,  # Judul menu di navbar
        options=['Home', 'Pemeriksaan Anak', 'Pemeriksaan Dewasa', 'Pemeriksaan Lansia'],
        default_index=0,
        styles={
            "container": {
                "padding": "0!important",
                "background-color": "#2C3E50",  # Navy gelap
                "box-shadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
            },
            "nav-link": {
                "font-size": "16px",
                "font-weight": "600",
                "color": "#ecf0f1",
                "padding": "12px 20px",
                "transition": "0.3s",
                "border-radius": "5px",
                "margin": "4px",
            },
            "nav-link-selected": {
                "background-color": "#1ABC9C",  # Warna hijau toska modern
                "color": "white",
                "font-weight": "bold",
            },
            "icon": {
                "color": "white",
            },
        }
    )

# Menampilkan halaman sesuai pilihan menu
if selected == 'Home':
    st.markdown(
        """
        <style>
        .stApp {
            # background-color: #EDE0D4;
            background-color: #FFCBA4;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("<h1 style='text-align: center; margin-bottom: 30px;'>SELAMAT DATANG DI WEBSITE PEMERIKSAAN KESEHATAN UPTD PUSKESMAS MANGGAR BARU</h1>", unsafe_allow_html=True)

    st.markdown("<h3 style='text-align: center;'>To Cure Sometimes,</h3>", unsafe_allow_html=True)
   

    st.markdown("<h3 style='text-align: center;'>To Relive Often,</h3>", unsafe_allow_html=True)
    

    st.markdown("<h3 style='text-align: center;'>To Comfort Always.</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>(Quote by: Hippocrates)</p>", unsafe_allow_html=True)
    
elif selected == 'Pemeriksaan Anak':
    st.title('FORMULIR PEMERIKSAAN ANAK USIA 1-6 TAHUN')

    st.markdown(
        """
        <style>
        .stApp {
            # background-color: #EDE0D4;
            background-color: #FFCBA4;
        }
        </style>
        """,
        unsafe_allow_html=True
    )



    # Inisialisasi koneksi ke Google Sheets
    conn = st.connection("gsheets", type=GSheetsConnection)

    @st.cache_data
    # Cache untuk mengambil data dari Google Sheets dan menghindari pemrosesan ulang
    def load_data_from_gsheet():
        df = conn.read(worksheet="pkg_balita", usecols=list(range(94)), ttl=5)
        df = df.dropna(how='all')
        return df

    # Load the data from Google Sheets
    df = load_data_from_gsheet()

    nik = st.text_input('NIK', key='input_nik')

    # Menggunakan session_state untuk menyimpan data yang di-load
    if 'input_nik_loaded' not in st.session_state:
        st.session_state.input_nik_loaded = False
    if 'input_data' not in st.session_state:
        st.session_state.input_data = {}
        
    # Fungsi untuk mengisi form berdasarkan nik
    def load_data_by_nik():
        nik_input = st.session_state.input_nik.strip()
        if nik_input:
            # Convert the 'NIK' column to string before using str.contains
            df['NIK'] = df['NIK'].astype(str)
            
            # Search for NIK in the dataframe
            data = df[df['NIK'].str.contains(nik_input, case=False, na=False)]
            
            if not data.empty:
                # If found, store the data in session_state
                st.session_state.input_data = data.iloc[0].to_dict()
                st.session_state.input_nik_loaded = True
                st.success("Data berhasil dimuat.")
            else:
                st.warning("NIK tidak ditemukan.")
        else:
            st.warning("NIK tidak boleh kosong.")


    st.markdown("""
        <style>
        .stButton>button {
            # background-color: #D2B48C; /* Warna coklat kalem */
            background-color: #FFA07A; /* Warna coklat kalem */
            color: white; /* Warna teks putih */
            border: none;
            border-radius: 12px; /* Membuat sudut melengkung */
            padding: 10px 24px; /* Ukuran padding */
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            transition-duration: 0.4s;
            cursor: pointer;
        }

        .stButton>button:hover {
            background-color: #C19A6B; /* Warna coklat lebih gelap saat hover */
        }

        .stButton>button:active {
            background-color: #8B4513; /* Warna coklat lebih gelap saat tombol ditekan */
        }
        </style>
    """, unsafe_allow_html=True)


    # Button to load data based on NIK
    btn_load = st.button('Load', key='btn_load')

    if btn_load:
        load_data_by_nik()

    # Tombol untuk menambahkan data baru
    btn_add = st.button('Tambah Data Baru', key='btn_add')

    if btn_add:
        # Set session state untuk memastikan inputan muncul
        st.session_state.add_new_data = True  # Menandakan kita menambah data baru

    # Formulir inputan untuk data baru hanya tampil jika btn_add ditekan
    if 'add_new_data' in st.session_state and st.session_state.add_new_data:
        # Menampilkan form inputan untuk data baru
        with st.expander('**IDENTITAS PASIEN**'):
            left, right = st.columns(2)
            sekarang = datetime.today().date()
            tgl_pem = left.date_input('Tanggal Pemeriksaan', format='DD/MM/YYYY', value=sekarang, key='tgl_pem', disabled=True)
            nama = left.text_input('Nama Lengkap', value=None, key='nama')
            nik = left.text_input('NIK', value=None, key='nik')
            nik = f"'{nik}"
            jk = left.selectbox('Jenis Kelamin', ['Perempuan', 'Laki-laki'], index=None, key='jk')
            alamat = left.text_input('Alamat', value=None, key='alamat')
            hp = left.text_input('Nomor HP', value=None, key='hp')
            tgl_lhr = right.date_input("Tanggal Lahir", format='DD/MM/YYYY', min_value=datetime(2018, 1, 1), key='tgl_lhr')    
            umur = sekarang - tgl_lhr
            usia_thn = umur.days//365
            usia_bln = umur.days//30
            ut = right.number_input('Usia (dalam tahun)', value=usia_thn, disabled=True, key='ut')
            ub = right.number_input('Usia (dalam bulan)', value=usia_bln, disabled=True, key='ub')
            wali = right.text_input('Nama Wali', value=None, key='wali')
            nik_wali = right.text_input('NIK Wali', value=None, key='nik_wali')
            disabilitas = right.radio('Apakah anak mengalami disabilitas?', ['Tidak', 'Ya'], index=None, key='disabilitas', horizontal=True)

        with st.expander('**SKRINING PERTUMBUHAN**'):
            left, right = st.columns(2)
            bb = left.number_input('Berat Badan (dalam kg)', value=0.0, step=0.1, key='bb')
            posisi = left.radio('Posisi Pengukuran', ['Berdiri', 'Terlentang'], index=0, horizontal=True, key='posisi')
            tb = left.number_input('Tinggi Badan (dalam cm)', value=0.0, step=0.1, key='tb')
            
            lk = left.number_input('Lingkar Kepala (dalam cm)', value=0.0, step=0.1, key='lk')
            
            if 6 <= usia_bln < 60:
                lla = left.number_input('Lingkar Lengan Atas(dalam cm)', value=0.0, step=0.1, key='lla')
            else:
                lla = left.number_input('Lingkar Lengan Atas(dalam cm)', value=0.0, step=0.1, key='lla', disabled=True)
            
            
            if  lla >= 12.5:
                stat_lla = left.text_input('Status LiLA', value='Normal', disabled=True)
            elif 11.5 <= lla <= 12.4:
                stat_lla = left.text_input('Status LiLA', value='Gizi Kurang', disabled=True)
            elif 0 < lla < 11.5:
                stat_lla = left.text_input('Status LiLA', value='Gizi Buruk', disabled=True)
            else:
                stat_lla = left.text_input('Status LiLA', value=None, disabled=True)
                
    
            
            def hitung_bmi(tb, bb):
                try:
                    a = tb * tb / 10000  # konversi tinggi badan ke meter kuadrat
                    imt = bb / a
                    return imt
                except ZeroDivisionError:
                    return 0  # jika tinggi badan 0
                except Exception as e:
                    st.error(f"Terjadi kesalahan saat menghitung BMI: {e}")
                    return 0

            if st.session_state.bb and st.session_state.tb is not None:
                imt=hitung_bmi(tb, bb)
                bmi=right.number_input('Indeks Massa Tubuh', value=imt, disabled=True, key='bmi')
            else:
                bmi=right.number_input('Indeks Massa Tubuh', value=0, disabled=True, key='bmi')
        

            
            if st.session_state.jk == 'Laki-laki': 
            
                if 0 <= usia_bln <= 60:  
                    #untuk BB/U
                    lakibbu = pd.read_excel('gizi.xlsx', sheet_name='Lakibbu')

                    data_lakibbu = lakibbu[lakibbu['Usia'] == int(usia_bln)].index
                    

                    x = lakibbu.iloc[data_lakibbu]
                    
                    minus_tiga_lbbu = x['SD-3'].values[0]
                    minus_dua_lbbu = x['SD-2'].values[0]
                    plus_satu_lbbu = x['SD+1'].values[0]
                    
                    if float(bb) < minus_tiga_lbbu:
                        stat_bbu= right.text_input('BB/U', value='Berat Badan Sangat Kurang', disabled=True, key='stat_bbu')
                    elif minus_tiga_lbbu <= float(bb) < minus_dua_lbbu:
                        stat_bbu= right.text_input('BB/U', value='Berat Badan Kurang', disabled=True, key='stat_bbu')
                    elif minus_dua_lbbu <= float(bb) <= plus_satu_lbbu:
                        stat_bbu= right.text_input('BB/U', value='Berat Badan Normal', disabled=True, key='stat_bbu')
                    else:
                        stat_bbu= right.text_input('BB/U', value='Berat Badan Lebih', disabled=True, key='stat_bbu')

                    #untuk TB/U
                    lakitbu = pd.read_excel('gizi.xlsx', sheet_name='Lakitbu')

                    data_lakitbu = lakitbu[lakitbu['Usia'] == int(usia_bln)].index

                    y = lakitbu.iloc[data_lakitbu]
                    minus_tiga_ltbu = y['SD-3'].values[0]
                    minus_dua_ltbu = y['SD-2'].values[0]
                    plus_satu_ltbu = y['SD+1'].values[0]
                    

                    if float(tb) < minus_tiga_ltbu :
                        stat_tbu= right.text_input('TB/U', value='Sangat Pendek', disabled=True, key='stat_tbu')
                    elif minus_tiga_ltbu <= float(tb) < minus_dua_ltbu:
                        stat_tbu= right.text_input('TB/U', value='Pendek', disabled=True, key='stat_tbu')
                    elif minus_dua_ltbu <= float(tb) <= plus_satu_ltbu:
                        stat_tbu= right.text_input('TB/U', value='Tinggi Badan Normal', disabled=True, key='stat_tbu')
                    else:
                        stat_tbu= right.text_input('TB/U', value='Tinggi', disabled=True, key='stat_tbu')

                    if st.session_state.posisi == 'Berdiri':
                        #untuk BB/TB
                        lakibbtb = pd.read_excel('gizi.xlsx', sheet_name='Lakibbtb')

                        # Mendapatkan list tinggi badan yang tersedia
                        tinggi_badan_teravailable = lakibbtb['Tinggi Badan'].unique()

                        # Fungsi untuk melakukan interpolasi
                        def interpolasi_sd_values(tinggi_input):
                            # Urutkan tinggi badan yang tersedia
                            tinggi_badan_teravailable.sort()
                            
                            # Buat interpolator untuk masing-masing kolom SD-3, SD-2, SD+1, SD+2, SD+3
                            interpolator_sd_minus_3 = interp1d(tinggi_badan_teravailable, lakibbtb['SD-3'], kind='linear', fill_value='extrapolate')
                            interpolator_sd_minus_2 = interp1d(tinggi_badan_teravailable, lakibbtb['SD-2'], kind='linear', fill_value='extrapolate')
                            interpolator_sd_plus_1 = interp1d(tinggi_badan_teravailable, lakibbtb['SD+1'], kind='linear', fill_value='extrapolate')
                            interpolator_sd_plus_2 = interp1d(tinggi_badan_teravailable, lakibbtb['SD+2'], kind='linear', fill_value='extrapolate')
                            interpolator_sd_plus_3 = interp1d(tinggi_badan_teravailable, lakibbtb['SD+3'], kind='linear', fill_value='extrapolate')

                            # Menghitung nilai interpolasi berdasarkan tinggi badan input
                            minus_tiga_lbbtb = interpolator_sd_minus_3(tinggi_input)
                            minus_dua_lbbtb = interpolator_sd_minus_2(tinggi_input)
                            plus_satu_lbbtb = interpolator_sd_plus_1(tinggi_input)
                            plus_dua_lbbtb = interpolator_sd_plus_2(tinggi_input)
                            plus_tiga_lbbtb = interpolator_sd_plus_3(tinggi_input)

                            return minus_tiga_lbbtb, minus_dua_lbbtb, plus_satu_lbbtb, plus_dua_lbbtb, plus_tiga_lbbtb
                            
                                # Cek apakah input tinggi badan valid
                        try:
                            tb = float(tb)
                            bb = float(bb)

                            # Melakukan interpolasi dan mendapatkan nilai SD untuk tinggi badan yang tidak ada di tabel
                            minus_tiga_lbbtb, minus_dua_lbbtb, plus_satu_lbbtb, plus_dua_lbbtb, plus_tiga_lbbtb = interpolasi_sd_values(tb)

                            # Menentukan status BB/TB berdasarkan berat badan yang diinputkan
                            if bb < minus_tiga_lbbtb:
                                stat_bbtb = right.text_input('BB/TB', value='Gizi Buruk', disabled=True, key='stat_bbtb')
                            elif minus_tiga_lbbtb <= bb < minus_dua_lbbtb:
                                stat_bbtb = right.text_input('BB/TB', value='Gizi Kurang', disabled=True, key='stat_bbtb')
                            elif minus_dua_lbbtb <= bb <= plus_satu_lbbtb:
                                stat_bbtb = right.text_input('BB/TB', value='Normal', disabled=True, key='stat_bbtb')
                            elif plus_satu_lbbtb < bb <= plus_dua_lbbtb:
                                stat_bbtb = right.text_input('BB/TB', value='Berisiko Gizi Lebih', disabled=True, key='stat_bbtb')
                            elif plus_dua_lbbtb < bb <= plus_tiga_lbbtb:
                                stat_bbtb = right.text_input('BB/TB', value='Gizi Lebih', disabled=True, key='stat_bbtb')
                            elif bb > plus_tiga_lbbtb:
                                stat_bbtb = right.text_input('BB/TB', value='Obesitas', disabled=True, key='stat_bbtb')
                            else:
                                stat_bbtb = right.text_input('BB/TB', value=None, disabled=True, key='stat_bbtb')
                        except ValueError:
                            st.error("Input tinggi badan dan berat badan harus berupa angka.")
                            stat_bbtb = right.text_input('BB/TB', value=None, disabled=True, key='stat_bbtb')
                    
                    elif st.session_state.posisi == 'Terlentang':
                        #untuk BB/PB
                        lakibbpb = pd.read_excel('gizi.xlsx', sheet_name='Lakibbpb')

                        # Mendapatkan list panjang badan yang tersedia
                        panjang_badan_teravailable = lakibbpb['Panjang Badan'].unique()

                        # Fungsi untuk melakukan interpolasi
                        def interpolasi_sd_values(panjang_input):
                            # Urutkan tinggi badan yang tersedia
                            panjang_badan_teravailable.sort()
                            
                            # Buat interpolator untuk masing-masing kolom SD-3, SD-2, SD+1, SD+2, SD+3
                            interpolator_sd_minus_3 = interp1d(panjang_badan_teravailable, lakibbpb['SD-3'], kind='linear', fill_value='extrapolate')
                            interpolator_sd_minus_2 = interp1d(panjang_badan_teravailable, lakibbpb['SD-2'], kind='linear', fill_value='extrapolate')
                            interpolator_sd_plus_1 = interp1d(panjang_badan_teravailable, lakibbpb['SD+1'], kind='linear', fill_value='extrapolate')
                            interpolator_sd_plus_2 = interp1d(panjang_badan_teravailable, lakibbpb['SD+2'], kind='linear', fill_value='extrapolate')
                            interpolator_sd_plus_3 = interp1d(panjang_badan_teravailable, lakibbpb['SD+3'], kind='linear', fill_value='extrapolate')

                            # Menghitung nilai interpolasi berdasarkan tinggi badan input
                            minus_tiga_lbbpb = interpolator_sd_minus_3(panjang_input)
                            minus_dua_lbbpb = interpolator_sd_minus_2(panjang_input)
                            plus_satu_lbbpb = interpolator_sd_plus_1(panjang_input)
                            plus_dua_lbbpb = interpolator_sd_plus_2(panjang_input)
                            plus_tiga_lbbpb = interpolator_sd_plus_3(panjang_input)

                            return minus_tiga_lbbpb, minus_dua_lbbpb, plus_satu_lbbpb, plus_dua_lbbpb, plus_tiga_lbbpb
        
                                # Cek apakah input tinggi badan valid
                        try:
                            tb = float(tb)
                            bb = float(bb)

                            # Melakukan interpolasi dan mendapatkan nilai SD untuk tinggi badan yang tidak ada di tabel
                            minus_tiga_lbbpb, minus_dua_lbbpb, plus_satu_lbbpb, plus_dua_lbbpb, plus_tiga_lbbpb = interpolasi_sd_values(tb)

                            # Menentukan status BB/PB berdasarkan berat badan yang diinputkan
                            if bb < minus_tiga_lbbpb:
                                stat_bbtb = right.text_input('BB/TB', value='Gizi Buruk', disabled=True, key='stat_bbtb')
                            elif minus_tiga_lbbpb <= bb < minus_dua_lbbpb:
                                stat_bbtb = right.text_input('BB/TB', value='Gizi Kurang', disabled=True, key='stat_bbtb')
                            elif minus_dua_lbbpb <= bb <= plus_satu_lbbpb:
                                stat_bbtb = right.text_input('BB/TB', value='Normal', disabled=True, key='stat_bbtb')
                            elif plus_satu_lbbpb < bb <= plus_dua_lbbpb:
                                stat_bbtb = right.text_input('BB/TB', value='Berisiko Gizi Lebih', disabled=True, key='stat_bbtb')
                            elif plus_dua_lbbpb < bb <= plus_tiga_lbbpb:
                                stat_bbtb = right.text_input('BB/TB', value='Gizi Lebih', disabled=True, key='stat_bbtb')
                            elif bb > plus_tiga_lbbpb:
                                stat_bbtb = right.text_input('BB/TB', value='Obesitas', disabled=True, key='stat_bbtb')
                            else:
                                stat_bbtb = right.text_input('BB/TB', value=None, disabled=True, key='stat_bbtb')
                        except ValueError:
                            st.error("Input tinggi badan dan berat badan harus berupa angka.")
                            stat_bbtb = right.text_input('BB/TB', value=None, disabled=True, key='stat_bbtb')
                        
    
                    #untuk IMT/U
                    lakiimtu = pd.read_excel('gizi.xlsx', sheet_name='Lakiimtu')

                    data_lakiimtu = lakiimtu[lakiimtu['Usia'] == int(usia_bln)].index

                    if len(data_lakiimtu) > 0:
                        r = lakiimtu.iloc[data_lakiimtu]
                        try:
                            minus_tiga_limtu = r['SD-3'].values[0]
                            minus_dua_limtu = r['SD-2'].values[0]
                            plus_satu_limtu = r['SD+1'].values[0]
                            plus_dua_limtu = r['SD+2'].values[0]
                            plus_tiga_limtu = r['SD+3'].values[0]

                            if float(bmi) < minus_tiga_limtu:
                                stat_imtu = right.text_input('IMT/U', value='Gizi Buruk', disabled=True, key='stat_imtu')
                            elif minus_tiga_limtu <= float(bmi) < minus_dua_limtu:
                                stat_imtu = right.text_input('IMT/U', value='Gizi Kurang', disabled=True, key='stat_imtu')
                            elif minus_dua_limtu <= float(bmi) <= plus_satu_limtu:
                                stat_imtu = right.text_input('IMT/U', value='Normal', disabled=True, key='stat_imtu')
                            elif plus_satu_limtu < float(bmi) <= plus_dua_limtu:
                                stat_imtu = right.text_input('IMT/U', value='Berisiko Gizi Lebih', disabled=True, key='stat_imtu')
                            elif plus_dua_limtu < float(bmi) <= plus_tiga_limtu:
                                stat_imtu = right.text_input('IMT/U', value='Gizi Lebih', disabled=True, key='stat_imtu')
                            else:
                                stat_imtu = right.text_input('IMT/U', value='Obesitas', disabled=True, key='stat_imtu')

                        except IndexError:
                            stat_imtu = right.text_input('IMT/U', value=None, disabled=True, key='stat_imtu')
                    else:
                        stat_imtu = right.text_input('IMT/U', value=None, disabled=True, key='stat_imtu')
                        
                        
                    #untuk LK/U
                    lakilku = pd.read_excel('gizi.xlsx', sheet_name='Lakilku')

                    data_lakilku = lakilku[lakilku['Usia'] == int(usia_bln)].index

                    if len(data_lakilku) > 0:
                        s = lakilku.iloc[data_lakilku]
                        try:
                            minus_dua_llku = s['SD-2'].values[0]
                            plus_dua_llku = s['SD+2'].values[0]

                            if float(lk) < minus_dua_llku:
                                stat_lku = right.text_input('LK/U', value='Mikrosefali', disabled=True, key='stat_lku')
                            elif minus_dua_llku <= float(lk) <= plus_dua_llku:
                                stat_lku = right.text_input('LK/U', value='Normosefali', disabled=True, key='stat_lku')
                            else:
                                stat_lku = right.text_input('LK/U', value='Makrosefali', disabled=True, key='stat_lku')

                        except IndexError:
                            stat_lku = right.text_input('LK/U', value=None, disabled=True, key='stat_lku')
                    else:
                        stat_lku = right.text_input('LK/U', value=None, disabled=True, key='stat_lku')
                        
                elif 60 < usia_bln <= 72:
                    stat_bbu = right.text_input('BB/U', value=None, disabled=True)
                    stat_tbu = right.text_input('TB/U', value=None, disabled=True)
                    stat_bbtb = right.text_input('BB/TB', value=None, disabled=True)
                    
                    lakiimtu = pd.read_excel('gizi.xlsx', sheet_name='Lakiimtu')

                    data_lakiimtu = lakiimtu[lakiimtu['Usia'] == int(usia_bln)].index

                    if len(data_lakiimtu) > 0:
                        r = lakiimtu.iloc[data_lakiimtu]
                        try:
                            minus_tiga_limtu = r['SD-3'].values[0]
                            minus_dua_limtu = r['SD-2'].values[0]
                            plus_satu_limtu = r['SD+1'].values[0]
                            plus_dua_limtu = r['SD+2'].values[0]
                            plus_tiga_limtu = r['SD+3'].values[0]

                            if float(bmi) < minus_tiga_limtu:
                                stat_imtu = right.text_input('IMT/U', value='Gizi Buruk', disabled=True, key='stat_imtu')
                            elif minus_tiga_limtu <= float(bmi) < minus_dua_limtu:
                                stat_imtu = right.text_input('IMT/U', value='Gizi Kurang', disabled=True, key='stat_imtu')
                            elif minus_dua_limtu <= float(bmi) <= plus_satu_limtu:
                                stat_imtu = right.text_input('IMT/U', value='Normal', disabled=True, key='stat_imtu')
                            elif plus_satu_limtu < float(bmi) <= plus_dua_limtu:
                                stat_imtu = right.text_input('IMT/U', value='Berisiko Gizi Lebih', disabled=True, key='stat_imtu')
                            elif plus_dua_limtu < float(bmi) <= plus_tiga_limtu:
                                stat_imtu = right.text_input('IMT/U', value='Gizi Lebih', disabled=True, key='stat_imtu')
                            else:
                                stat_imtu = right.text_input('IMT/U', value='Obesitas', disabled=True, key='stat_imtu')

                        except IndexError:
                            stat_imtu = right.text_input('IMT/U', value=None, disabled=True, key='stat_imtu')
                    else:
                        stat_imtu = right.text_input('IMT/U', value=None, disabled=True, key='stat_imtu')
                
                    stat_lku = right.text_input('LK/U', value=None, disabled=True, key='stat_lku')
                    
                else:
                    stat_bbu=right.text_input('BB/U', value=None, disabled=True, key='stat_bbu')
                    stat_tbu=right.text_input('TB/U', value=None, disabled=True, key='stat_tbu')
                    stat_bbtb = right.text_input('BB/TB', value=None, disabled=True, key='stat_bbtb')
                    stat_imtu = right.text_input('IMT/U', value=None, disabled=True, key='stat_imtu')
                    stat_lku = right.text_input('LK/U', value=None, disabled=True, key='stat_lku')
            
            
                    
                    
            elif st.session_state.jk == 'Perempuan':

                if 0 <= usia_bln <= 60:
                    #untuk BB/U
                    prbbu = pd.read_excel('gizi.xlsx', sheet_name='Prbbu')

                    data_prbbu = prbbu[prbbu['Usia'] == int(usia_bln)].index
                    

                    x = prbbu.iloc[data_prbbu]
                    
                    minus_tiga_pbbu = x['SD-3'].values[0]
                    minus_dua_pbbu = x['SD-2'].values[0]
                    plus_satu_pbbu = x['SD+1'].values[0]
                    
                    if float(bb) < minus_tiga_pbbu:
                        stat_bbu= right.text_input('BB/U', value='Berat Badan Sangat Kurang', disabled=True, key='stat_bbu')
                    elif minus_tiga_pbbu <= float(bb) < minus_dua_pbbu:
                        stat_bbu= right.text_input('BB/U', value='Berat Badan Kurang', disabled=True, key='stat_bbu')
                    elif minus_dua_pbbu <= float(bb) <= plus_satu_pbbu:
                        stat_bbu= right.text_input('BB/U', value='Berat Badan Normal', disabled=True, key='stat_bbu')
                    else:
                        stat_bbu= right.text_input('BB/U', value='Berat Badan Lebih', disabled=True, key='stat_bbu')

                    #untuk TB/U
                    prtbu = pd.read_excel('gizi.xlsx', sheet_name='Prtbu')

                    data_prtbu = prtbu[prtbu['Usia'] == int(usia_bln)].index

                    y = prtbu.iloc[data_prtbu]
                    minus_tiga_ptbu = y['SD-3'].values[0]
                    minus_dua_ptbu = y['SD-2'].values[0]
                    plus_satu_ptbu = y['SD+1'].values[0]
                    

                    if float(tb) < minus_tiga_ptbu :
                        stat_tbu= right.text_input('TB/U', value='Sangat Pendek', disabled=True, key='stat_tbu')
                    elif minus_tiga_ptbu <= float(tb) < minus_dua_ptbu:
                        stat_tbu= right.text_input('TB/U', value='Pendek', disabled=True, key='stat_tbu')
                    elif minus_dua_ptbu <= float(tb) <= plus_satu_ptbu:
                        stat_tbu= right.text_input('TB/U', value='Tinggi Badan Normal', disabled=True, key='stat_tbu')
                    else:
                        stat_tbu= right.text_input('TB/U', value='Tinggi', disabled=True, key='stat_tbu')



                    if st.session_state.posisi == 'Berdiri':
                        #untuk BB/TB
                        prbbtb = pd.read_excel('gizi.xlsx', sheet_name='Prbbtb')

                        # Mendapatkan list tinggi badan yang tersedia
                        tinggi_badan_teravailable = prbbtb['Tinggi Badan'].unique()

                        # Fungsi untuk melakukan interpolasi
                        def interpolasi_sd_values(tinggi_input):
                            # Urutkan tinggi badan yang tersedia
                            tinggi_badan_teravailable.sort()
                            
                            # Buat interpolator untuk masing-masing kolom SD-3, SD-2, SD+1, SD+2, SD+3
                            interpolator_sd_minus_3 = interp1d(tinggi_badan_teravailable, prbbtb['SD-3'], kind='linear', fill_value='extrapolate')
                            interpolator_sd_minus_2 = interp1d(tinggi_badan_teravailable, prbbtb['SD-2'], kind='linear', fill_value='extrapolate')
                            interpolator_sd_plus_1 = interp1d(tinggi_badan_teravailable, prbbtb['SD+1'], kind='linear', fill_value='extrapolate')
                            interpolator_sd_plus_2 = interp1d(tinggi_badan_teravailable, prbbtb['SD+2'], kind='linear', fill_value='extrapolate')
                            interpolator_sd_plus_3 = interp1d(tinggi_badan_teravailable, prbbtb['SD+3'], kind='linear', fill_value='extrapolate')

                            # Menghitung nilai interpolasi berdasarkan tinggi badan input
                            minus_tiga_pbbtb = interpolator_sd_minus_3(tinggi_input)
                            minus_dua_pbbtb = interpolator_sd_minus_2(tinggi_input)
                            plus_satu_pbbtb = interpolator_sd_plus_1(tinggi_input)
                            plus_dua_pbbtb = interpolator_sd_plus_2(tinggi_input)
                            plus_tiga_pbbtb = interpolator_sd_plus_3(tinggi_input)

                            return minus_tiga_pbbtb, minus_dua_pbbtb, plus_satu_pbbtb, plus_dua_pbbtb, plus_tiga_pbbtb
                                # Cek apakah input tinggi badan valid
                        try:
                            tb = float(tb)
                            bb = float(bb)

                            # Melakukan interpolasi dan mendapatkan nilai SD untuk tinggi badan yang tidak ada di tabel
                            minus_tiga_pbbtb, minus_dua_pbbtb, plus_satu_pbbtb, plus_dua_pbbtb, plus_tiga_pbbtb = interpolasi_sd_values(tb)

                            # Menentukan status BB/TB berdasarkan berat badan yang diinputkan
                            if bb < minus_tiga_pbbtb:
                                stat_bbtb = right.text_input('BB/TB', value='Gizi Buruk', disabled=True, key='stat_bbtb')
                            elif minus_tiga_pbbtb <= bb < minus_dua_pbbtb:
                                stat_bbtb = right.text_input('BB/TB', value='Gizi Kurang', disabled=True, key='stat_bbtb')
                            elif minus_dua_pbbtb <= bb <= plus_satu_pbbtb:
                                stat_bbtb = right.text_input('BB/TB', value='Normal', disabled=True, key='stat_bbtb')
                            elif plus_satu_pbbtb < bb <= plus_dua_pbbtb:
                                stat_bbtb = right.text_input('BB/TB', value='Berisiko Gizi Lebih', disabled=True, key='stat_bbtb')
                            elif plus_dua_pbbtb < bb <= plus_tiga_pbbtb:
                                stat_bbtb = right.text_input('BB/TB', value='Gizi Lebih', disabled=True, key='stat_bbtb')
                            elif bb > plus_tiga_pbbtb:
                                stat_bbtb = right.text_input('BB/TB', value='Obesitas', disabled=True, key='stat_bbtb')
                            else:
                                stat_bbtb = right.text_input('BB/TB', value=None, disabled=True, key='stat_bbtb')
                        except ValueError:
                            st.error("Input tinggi badan dan berat badan harus berupa angka.")
                            
                    elif st.session_state.posisi == 'Terlentang':
                        #untuk BB/PB
                        prbbpb = pd.read_excel('gizi.xlsx', sheet_name='Prbbpb')

                        # Mendapatkan list panjang badan yang tersedia
                        panjang_badan_teravailable = prbbpb['Panjang Badan'].unique()

                        # Fungsi untuk melakukan interpolasi
                        def interpolasi_sd_values(panjang_input):
                            # Urutkan tinggi badan yang tersedia
                            panjang_badan_teravailable.sort()
                            
                            # Buat interpolator untuk masing-masing kolom SD-3, SD-2, SD+1, SD+2, SD+3
                            interpolator_sd_minus_3 = interp1d(panjang_badan_teravailable, prbbpb['SD-3'], kind='linear', fill_value='extrapolate')
                            interpolator_sd_minus_2 = interp1d(panjang_badan_teravailable, prbbpb['SD-2'], kind='linear', fill_value='extrapolate')
                            interpolator_sd_plus_1 = interp1d(panjang_badan_teravailable, prbbpb['SD+1'], kind='linear', fill_value='extrapolate')
                            interpolator_sd_plus_2 = interp1d(panjang_badan_teravailable, prbbpb['SD+2'], kind='linear', fill_value='extrapolate')
                            interpolator_sd_plus_3 = interp1d(panjang_badan_teravailable, prbbpb['SD+3'], kind='linear', fill_value='extrapolate')

                            # Menghitung nilai interpolasi berdasarkan tinggi badan input
                            minus_tiga_pbbpb = interpolator_sd_minus_3(panjang_input)
                            minus_dua_pbbpb = interpolator_sd_minus_2(panjang_input)
                            plus_satu_pbbpb = interpolator_sd_plus_1(panjang_input)
                            plus_dua_pbbpb = interpolator_sd_plus_2(panjang_input)
                            plus_tiga_pbbpb = interpolator_sd_plus_3(panjang_input)

                            return minus_tiga_pbbpb, minus_dua_pbbpb, plus_satu_pbbpb, plus_dua_pbbpb, plus_tiga_pbbpb
                                # Cek apakah input tinggi badan valid
                        try:
                            tb = float(tb)
                            bb = float(bb)

                            # Melakukan interpolasi dan mendapatkan nilai SD untuk tinggi badan yang tidak ada di tabel
                            minus_tiga_pbbpb, minus_dua_pbbpb, plus_satu_pbbpb, plus_dua_pbbpb, plus_tiga_pbbpb = interpolasi_sd_values(tb)

                            # Menentukan status BB/PB berdasarkan berat badan yang diinputkan
                            if bb < minus_tiga_pbbpb:
                                stat_bbtb = right.text_input('BB/TB', value='Gizi Buruk', disabled=True, key='stat_bbtb')
                            elif minus_tiga_pbbpb <= bb < minus_dua_pbbpb:
                                stat_bbtb = right.text_input('BB/TB', value='Gizi Kurang', disabled=True, key='stat_bbtb')
                            elif minus_dua_pbbpb <= bb <= plus_satu_pbbpb:
                                stat_bbtb = right.text_input('BB/TB', value='Normal', disabled=True, key='stat_bbtb')
                            elif plus_satu_pbbpb < bb <= plus_dua_pbbpb:
                                stat_bbtb = right.text_input('BB/TB', value='Berisiko Gizi Lebih', disabled=True, key='stat_bbtb')
                            elif plus_dua_pbbpb < bb <= plus_tiga_pbbpb:
                                stat_bbtb = right.text_input('BB/TB', value='Gizi Lebih', disabled=True, key='stat_bbtb')
                            elif bb > plus_tiga_pbbpb:
                                stat_bbtb = right.text_input('BB/TB', value='Obesitas', disabled=True, key='stat_bbtb')
                            else:
                                stat_bbtb = right.text_input('BB/TB', value=None, disabled=True, key='stat_bbtb')
                        except ValueError:
                            st.error("Input tinggi badan dan berat badan harus berupa angka.")


                    #untuk IMT/U
                    primtu = pd.read_excel('gizi.xlsx', sheet_name='Primtu')

                    data_primtu = primtu[primtu['Usia'] == int(usia_bln)].index

                    if len(data_primtu) > 0:
                        r = primtu.iloc[data_primtu]
                        try:
                            minus_tiga_pimtu = r['SD-3'].values[0]
                            minus_dua_pimtu = r['SD-2'].values[0]
                            plus_satu_pimtu = r['SD+1'].values[0]
                            plus_dua_pimtu = r['SD+2'].values[0]
                            plus_tiga_pimtu = r['SD+3'].values[0]

                            if float(bmi) < minus_tiga_pimtu:
                                stat_imtu = right.text_input('IMT/U', value='Gizi Buruk', disabled=True, key='stat_imtu')
                            elif minus_tiga_pimtu <= float(bmi) < minus_dua_pimtu:
                                stat_imtu = right.text_input('IMT/U', value='Gizi Kurang', disabled=True, key='stat_imtu')
                            elif minus_dua_pimtu <= float(bmi) <= plus_satu_pimtu:
                                stat_imtu = right.text_input('IMT/U', value='Normal', disabled=True, key='stat_imtu')
                            elif plus_satu_pimtu < float(bmi) <= plus_dua_pimtu:
                                stat_imtu = right.text_input('IMT/U', value='Berisiko Gizi Lebih', disabled=True, key='stat_imtu')
                            elif plus_dua_pimtu < float(bmi) <= plus_tiga_pimtu:
                                stat_imtu = right.text_input('IMT/U', value='Gizi Lebih', disabled=True, key='stat_imtu')
                            else:
                                stat_imtu = right.text_input('IMT/U', value='Obesitas', disabled=True, key='stat_imtu')

                        except IndexError:
                            stat_imtu = right.text_input('IMT/U', value=None, disabled=True, key='stat_imtu')
                    else:
                        stat_imtu = right.text_input('IMT/U', value=None, disabled=True, key='stat_imtu')
                    
                    
                    #untuk LK/U
                    prlku = pd.read_excel('gizi.xlsx', sheet_name='Prlku')

                    data_prlku = prlku[prlku['Usia'] == int(usia_bln)].index

                    if len(data_prlku) > 0:
                        s = prlku.iloc[data_prlku]
                        try:
                            minus_dua_plku = s['SD-2'].values[0]
                            plus_dua_plku = s['SD+2'].values[0]

                            if float(lk) < minus_dua_plku:
                                stat_lku = right.text_input('LK/U', value='Mikrosefali', disabled=True, key='stat_lku')
                            elif minus_dua_plku <= float(lk) <= plus_dua_plku:
                                stat_lku = right.text_input('LK/U', value='Normosefali', disabled=True, key='stat_lku')
                            else:
                                stat_lku = right.text_input('LK/U', value='Makrosefali', disabled=True, key='stat_lku')

                        except IndexError:
                            stat_lku = right.text_input('LK/U', value=None, disabled=True, key='stat_lku')
                    else:
                        stat_lku = right.text_input('LK/U', value=None, disabled=True, key='stat_lku')
            
                elif 60 < usia_bln <= 72:
                    stat_bbu=right.text_input('BB/U', value=None, disabled=True)
                    stat_tbu=right.text_input('TB/U', value=None, disabled=True)
                    stat_bbtb = right.text_input('BB/TB', value=None, disabled=True)
                    primtu = pd.read_excel('gizi.xlsx', sheet_name='Primtu')

                    data_primtu = primtu[primtu['Usia'] == int(usia_bln)].index

                    if len(data_primtu) > 0:
                        r = primtu.iloc[data_primtu]
                        try:
                            minus_tiga_pimtu = r['SD-3'].values[0]
                            minus_dua_pimtu = r['SD-2'].values[0]
                            plus_satu_pimtu = r['SD+1'].values[0]
                            plus_dua_pimtu = r['SD+2'].values[0]
                            plus_tiga_pimtu = r['SD+3'].values[0]

                            if float(bmi) < minus_tiga_pimtu:
                                stat_imtu = right.text_input('IMT/U', value='Gizi Buruk', disabled=True, key='stat_imtu')
                            elif minus_tiga_pimtu <= float(bmi) < minus_dua_pimtu:
                                stat_imtu = right.text_input('IMT/U', value='Gizi Kurang', disabled=True, key='stat_imtu')
                            elif minus_dua_pimtu <= float(bmi) <= plus_satu_pimtu:
                                stat_imtu = right.text_input('IMT/U', value='Normal', disabled=True, key='stat_imtu')
                            elif plus_satu_pimtu < float(bmi) <= plus_dua_pimtu:
                                stat_imtu = right.text_input('IMT/U', value='Berisiko Gizi Lebih', disabled=True, key='stat_imtu')
                            elif plus_dua_pimtu < float(bmi) <= plus_tiga_pimtu:
                                stat_imtu = right.text_input('IMT/U', value='Gizi Lebih', disabled=True, key='stat_imtu')
                            else:
                                stat_imtu = right.text_input('IMT/U', value='Obesitas', disabled=True, key='stat_imtu')

                        except IndexError:
                            stat_imtu = right.text_input('IMT/U', value=None, disabled=True, key='stat_imtu')
                    else:
                        stat_imtu = right.text_input('IMT/U', value=None, disabled=True, key='stat_imtu')
                    
                    stat_lku = right.text_input('LK/U', value=None, disabled=True)
                    
                else:
                    stat_bbu=right.text_input('BB/U', value=None, disabled=True, key='stat_bbu')
                    stat_tbu=right.text_input('TB/U', value=None, disabled=True, key='stat_tbu')
                    stat_bbtb = right.text_input('BB/TB', value=None, disabled=True, key='stat_bbtb')
                    stat_imtu = right.text_input('IMT/U', value=None, disabled=True, key='stat_imtu')
                    stat_lku = right.text_input('LK/U', value=None, disabled=True, key='stat_lku')
                    
        with st.expander('**SKRINING PERKEMBANGAN**'):
            if 3 <= usia_bln < 6: 
                st.write('### KPSP Umur 3 bulan')

                # Membuat kolom untuk menempatkan caption di kiri dan opsi di kanan
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Menentukan lebar kolom (3 bagian untuk caption, 1 bagian untuk opsi)

                with col1:
                    st.image('.img/3_1.png')
                with col2:
                    st.empty()
                    kpsp1 = st.radio('kpsp1', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp1', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/3_2.png')
                with col2:
                    st.empty()
                    kpsp2 = st.radio('kpsp2', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp2', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/3_3.png')
                with col2:
                    st.empty()
                    kpsp3 = st.radio('kpsp3', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp3', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/3_4.png')
                with col2:
                    st.empty()
                    kpsp4 = st.radio('kpsp4', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp4', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/3_5.png')
                with col2:
                    st.empty()
                    kpsp5 = st.radio('kpsp5', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp5', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/3_6.png')
                with col2:
                    st.empty()
                    kpsp6 = st.radio('kpsp6', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp6', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/3_7.png')
                with col2:
                    st.empty()
                    kpsp7 = st.radio('kpsp7', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp7', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/3_8.png')
                with col2:
                    st.empty()
                    kpsp8 = st.radio('kpsp8', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp8', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/3_9.png')
                with col2:
                    st.empty()
                    kpsp9 = st.radio('kpsp9', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp9', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/3_10.png')
                with col2:
                    st.empty()
                    kpsp10 = st.radio('kpsp10', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp10', label_visibility='collapsed')

            elif 6 <= usia_bln < 9:

                st.write('### KPSP Umur 6 bulan')

                # Membuat kolom untuk menempatkan caption di kiri dan opsi di kanan
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Menentukan lebar kolom (3 bagian untuk caption, 1 bagian untuk opsi)

                with col1:
                    st.image('.img/6_1.png')
                with col2:
                    st.empty()
                    kpsp1 = st.radio('kpsp1', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp1', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/6_2.png')
                with col2:
                    st.empty()
                    kpsp2 = st.radio('kpsp2', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp2', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/6_3.png')
                with col2:
                    st.empty()
                    kpsp3 = st.radio('kpsp3', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp3', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/6_4.png')
                with col2:
                    st.empty()
                    kpsp4 = st.radio('kpsp4', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp4', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/6_5.png')
                with col2:
                    st.empty()
                    kpsp5 = st.radio('kpsp5', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp5', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/6_6.png')
                with col2:
                    st.empty()
                    kpsp6 = st.radio('kpsp6', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp6', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/6_7.png')
                with col2:
                    st.empty()
                    kpsp7 = st.radio('kpsp7', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp7', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/6_8.png')
                with col2:
                    st.empty()
                    kpsp8 = st.radio('kpsp8', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp8', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/6_9.png')
                with col2:
                    st.empty()
                    kpsp9 = st.radio('kpsp9', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp9', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/6_10.png')
                with col2:
                    st.empty()
                    kpsp10 = st.radio('kpsp10', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp10', label_visibility='collapsed')
                            
            elif 9 <= usia_bln < 12:

                st.write('### KPSP Umur 9 bulan')

                # Membuat kolom untuk menempatkan caption di kiri dan opsi di kanan
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Menentukan lebar kolom (3 bagian untuk caption, 1 bagian untuk opsi)

                with col1:
                    st.image('.img/9_1.png')
                with col2:
                    st.empty()
                    kpsp1 = st.radio('kpsp1', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp1', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/9_2.png')
                with col2:
                    st.empty()
                    kpsp2 = st.radio('kpsp2', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp2', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/9_3.png')
                with col2:
                    st.empty()
                    kpsp3 = st.radio('kpsp3', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp3', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/9_4.png')
                with col2:
                    st.empty()
                    kpsp4 = st.radio('kpsp4', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp4', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/9_5.png')
                with col2:
                    st.empty()
                    kpsp5 = st.radio('kpsp5', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp5', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/9_6.png')
                with col2:
                    st.empty()
                    kpsp6 = st.radio('kpsp6', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp6', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/9_7.png')
                with col2:
                    st.empty()
                    kpsp7 = st.radio('kpsp7', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp7', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/9_8.png')
                with col2:
                    st.empty()
                    kpsp8 = st.radio('kpsp8', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp8', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/9_9.png')
                with col2:
                    st.empty()
                    kpsp9 = st.radio('kpsp9', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp9', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/9_10.png')
                with col2:
                    st.empty()
                    kpsp10 = st.radio('kpsp10', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp10', label_visibility='collapsed')
                    
            elif 12 <= usia_bln < 15:

                st.write('### KPSP Umur 12 bulan')

                # Membuat kolom untuk menempatkan caption di kiri dan opsi di kanan
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Menentukan lebar kolom (3 bagian untuk caption, 1 bagian untuk opsi)

                with col1:
                    st.image('.img/12_1.png')
                with col2:
                    st.empty()
                    kpsp1 = st.radio('kpsp1', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp1', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/12_2.png')
                with col2:
                    st.empty()
                    kpsp2 = st.radio('kpsp2', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp2', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/12_3.png')
                with col2:
                    st.empty()
                    kpsp3 = st.radio('kpsp3', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp3', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/12_4.png')
                with col2:
                    st.empty()
                    kpsp4 = st.radio('kpsp4', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp4', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/12_5.png')
                with col2:
                    st.empty()
                    kpsp5 = st.radio('kpsp5', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp5', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/12_6.png')
                with col2:
                    st.empty()
                    kpsp6 = st.radio('kpsp6', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp6', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/12_7.png')
                with col2:
                    st.empty()
                    kpsp7 = st.radio('kpsp7', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp7', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/12_8.png')
                with col2:
                    st.empty()
                    kpsp8 = st.radio('kpsp8', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp8', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/12_9.png')
                with col2:
                    st.empty()
                    kpsp9 = st.radio('kpsp9', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp9', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/12_10.png')
                with col2:
                    st.empty()
                    kpsp10 = st.radio('kpsp10', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp10', label_visibility='collapsed')
            
            elif 15 <= usia_bln < 18:

                st.write('### KPSP Umur 15 bulan')

                # Membuat kolom untuk menempatkan caption di kiri dan opsi di kanan
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Menentukan lebar kolom (3 bagian untuk caption, 1 bagian untuk opsi)

                with col1:
                    st.image('.img/15_1.png')
                with col2:
                    st.empty()
                    kpsp1 = st.radio('kpsp1', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp1', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/15_2.png')
                with col2:
                    st.empty()
                    kpsp2 = st.radio('kpsp2', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp2', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/15_3.png')
                with col2:
                    st.empty()
                    kpsp3 = st.radio('kpsp3', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp3', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/15_4.png')
                with col2:
                    st.empty()
                    kpsp4 = st.radio('kpsp4', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp4', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/15_5.png')
                with col2:
                    st.empty()
                    kpsp5 = st.radio('kpsp5', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp5', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/15_6.png')
                with col2:
                    st.empty()
                    kpsp6 = st.radio('kpsp6', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp6', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/15_7.png')
                with col2:
                    st.empty()
                    kpsp7 = st.radio('kpsp7', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp7', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/15_8.png')
                with col2:
                    st.empty()
                    kpsp8 = st.radio('kpsp8', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp8', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/15_9.png')
                with col2:
                    st.empty()
                    kpsp9 = st.radio('kpsp9', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp9', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/15_10.png')
                with col2:
                    st.empty()
                    kpsp10 = st.radio('kpsp10', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp10', label_visibility='collapsed')
                    
            elif 18 <= usia_bln < 21:

                st.write('### KPSP Umur 18 bulan')

                # Membuat kolom untuk menempatkan caption di kiri dan opsi di kanan
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Menentukan lebar kolom (3 bagian untuk caption, 1 bagian untuk opsi)

                with col1:
                    st.image('.img/18_1.png')
                with col2:
                    st.empty()
                    kpsp1 = st.radio('kpsp1', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp1', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/18_2.png')
                with col2:
                    st.empty()
                    kpsp2 = st.radio('kpsp2', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp2', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/18_3.png')
                with col2:
                    st.empty()
                    kpsp3 = st.radio('kpsp3', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp3', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/18_4.png')
                with col2:
                    st.empty()
                    kpsp4 = st.radio('kpsp4', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp4', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/18_5.png')
                with col2:
                    st.empty()
                    kpsp5 = st.radio('kpsp5', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp5', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/18_6.png')
                with col2:
                    st.empty()
                    kpsp6 = st.radio('kpsp6', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp6', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/18_7.png')
                with col2:
                    st.empty()
                    kpsp7 = st.radio('kpsp7', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp7', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/18_8.png')
                with col2:
                    st.empty()
                    kpsp8 = st.radio('kpsp8', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp8', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/18_9.png')
                with col2:
                    st.empty()
                    kpsp9 = st.radio('kpsp9', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp9', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/18_10.png')
                with col2:
                    st.empty()
                    kpsp10 = st.radio('kpsp10', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp10', label_visibility='collapsed')
                    
            elif 21 <= usia_bln < 24:

                st.write('### KPSP Umur 21 bulan')

                # Membuat kolom untuk menempatkan caption di kiri dan opsi di kanan
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Menentukan lebar kolom (3 bagian untuk caption, 1 bagian untuk opsi)

                with col1:
                    st.image('.img/21_1.png')
                with col2:
                    st.empty()
                    kpsp1 = st.radio('kpsp1', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp1', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/21_2.png')
                with col2:
                    st.empty()
                    kpsp2 = st.radio('kpsp2', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp2', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/21_3.png')
                with col2:
                    st.empty()
                    kpsp3 = st.radio('kpsp3', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp3', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/21_4.png')
                with col2:
                    st.empty()
                    kpsp4 = st.radio('kpsp4', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp4', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/21_5.png')
                with col2:
                    st.empty()
                    kpsp5 = st.radio('kpsp5', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp5', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/21_6.png')
                with col2:
                    st.empty()
                    kpsp6 = st.radio('kpsp6', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp6', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/21_7.png')
                with col2:
                    st.empty()
                    kpsp7 = st.radio('kpsp7', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp7', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/21_8.png')
                with col2:
                    st.empty()
                    kpsp8 = st.radio('kpsp8', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp8', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/21_9.png')
                with col2:
                    st.empty()
                    kpsp9 = st.radio('kpsp9', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp9', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/21_10.png')
                with col2:
                    st.empty()
                    kpsp10 = st.radio('kpsp10', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp10', label_visibility='collapsed')
                    
            elif 24 <= usia_bln < 30:

                st.write('### KPSP Umur 24 bulan')

                # Membuat kolom untuk menempatkan caption di kiri dan opsi di kanan
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Menentukan lebar kolom (3 bagian untuk caption, 1 bagian untuk opsi)

                with col1:
                    st.image('.img/24_1.png')
                with col2:
                    st.empty()
                    kpsp1 = st.radio('kpsp1', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp1', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/24_2.png')
                with col2:
                    st.empty()
                    kpsp2 = st.radio('kpsp2', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp2', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/24_3.png')
                with col2:
                    st.empty()
                    kpsp3 = st.radio('kpsp3', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp3', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/24_4.png')
                with col2:
                    st.empty()
                    kpsp4 = st.radio('kpsp4', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp4', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/24_5.png')
                with col2:
                    st.empty()
                    kpsp5 = st.radio('kpsp5', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp5', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/24_6.png')
                with col2:
                    st.empty()
                    kpsp6 = st.radio('kpsp6', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp6', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/24_7.png')
                with col2:
                    st.empty()
                    kpsp7 = st.radio('kpsp7', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp7', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/24_8.png')
                with col2:
                    st.empty()
                    kpsp8 = st.radio('kpsp8', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp8', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/24_9.png')
                with col2:
                    st.empty()
                    kpsp9 = st.radio('kpsp9', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp9', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/24_10.png')
                with col2:
                    st.empty()
                    kpsp10 = st.radio('kpsp10', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp10', label_visibility='collapsed')
                    
            elif 30 <= usia_bln < 36:

                st.write('### KPSP Umur 30 bulan')

                # Membuat kolom untuk menempatkan caption di kiri dan opsi di kanan
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Menentukan lebar kolom (3 bagian untuk caption, 1 bagian untuk opsi)

                with col1:
                    st.image('.img/30_1.png')
                with col2:
                    st.empty()
                    kpsp1 = st.radio('kpsp1', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp1', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/30_2.png')
                with col2:
                    st.empty()
                    kpsp2 = st.radio('kpsp2', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp2', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/30_3.png')
                with col2:
                    st.empty()
                    kpsp3 = st.radio('kpsp3', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp3', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/30_4.png')
                with col2:
                    st.empty()
                    kpsp4 = st.radio('kpsp4', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp4', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/30_5.png')
                with col2:
                    st.empty()
                    kpsp5 = st.radio('kpsp5', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp5', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/30_6.png')
                with col2:
                    st.empty()
                    kpsp6 = st.radio('kpsp6', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp6', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/30_7.png')
                with col2:
                    st.empty()
                    kpsp7 = st.radio('kpsp7', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp7', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/30_8.png')
                with col2:
                    st.empty()
                    kpsp8 = st.radio('kpsp8', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp8', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/30_9.png')
                with col2:
                    st.empty()
                    kpsp9 = st.radio('kpsp9', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp9', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/30_10.png')
                with col2:
                    st.empty()
                    kpsp10 = st.radio('kpsp10', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp10', label_visibility='collapsed')
                    
            elif 36 <= usia_bln < 42:

                st.write('### KPSP Umur 36 bulan')

                # Membuat kolom untuk menempatkan caption di kiri dan opsi di kanan
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Menentukan lebar kolom (3 bagian untuk caption, 1 bagian untuk opsi)

                with col1:
                    st.image('.img/36_1.png')
                with col2:
                    st.empty()
                    kpsp1 = st.radio('kpsp1', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp1', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/36_2.png')
                with col2:
                    st.empty()
                    kpsp2 = st.radio('kpsp2', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp2', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/36_3.png')
                with col2:
                    st.empty()
                    kpsp3 = st.radio('kpsp3', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp3', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/36_4.png')
                with col2:
                    st.empty()
                    kpsp4 = st.radio('kpsp4', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp4', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/36_5.png')
                with col2:
                    st.empty()
                    kpsp5 = st.radio('kpsp5', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp5', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/36_6.png')
                with col2:
                    st.empty()
                    kpsp6 = st.radio('kpsp6', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp6', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/36_7.png')
                with col2:
                    st.empty()
                    kpsp7 = st.radio('kpsp7', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp7', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/36_8.png')
                with col2:
                    st.empty()
                    kpsp8 = st.radio('kpsp8', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp8', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/36_9.png')
                with col2:
                    st.empty()
                    kpsp9 = st.radio('kpsp9', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp9', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/36_10.png')
                with col2:
                    st.empty()
                    kpsp10 = st.radio('kpsp10', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp10', label_visibility='collapsed')
                    
            elif 42 <= usia_bln < 48:

                st.write('### KPSP Umur 42 bulan')

                # Membuat kolom untuk menempatkan caption di kiri dan opsi di kanan
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Menentukan lebar kolom (3 bagian untuk caption, 1 bagian untuk opsi)

                with col1:
                    st.image('.img/42_1.png')
                with col2:
                    st.empty()
                    kpsp1 = st.radio('kpsp1', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp1', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/42_2.png')
                with col2:
                    st.empty()
                    kpsp2 = st.radio('kpsp2', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp2', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/42_3.png')
                with col2:
                    st.empty()
                    kpsp3 = st.radio('kpsp3', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp3', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/42_4.png')
                with col2:
                    st.empty()
                    kpsp4 = st.radio('kpsp4', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp4', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/42_5.png')
                with col2:
                    st.empty()
                    kpsp5 = st.radio('kpsp5', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp5', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/42_6.png')
                with col2:
                    st.empty()
                    kpsp6 = st.radio('kpsp6', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp6', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/42_7.png')
                with col2:
                    st.empty()
                    kpsp7 = st.radio('kpsp7', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp7', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/42_8.png')
                with col2:
                    st.empty()
                    kpsp8 = st.radio('kpsp8', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp8', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/42_9.png')
                with col2:
                    st.empty()
                    kpsp9 = st.radio('kpsp9', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp9', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/42_10.png')
                with col2:
                    st.empty()
                    kpsp10 = st.radio('kpsp10', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp10', label_visibility='collapsed')
                    
            elif 48 <= usia_bln < 54:

                st.write('### KPSP Umur 48 bulan')

                # Membuat kolom untuk menempatkan caption di kiri dan opsi di kanan
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Menentukan lebar kolom (3 bagian untuk caption, 1 bagian untuk opsi)

                with col1:
                    st.image('.img/48_1.png')
                with col2:
                    st.empty()
                    kpsp1 = st.radio('kpsp1', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp1', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/48_2.png')
                with col2:
                    st.empty()
                    kpsp2 = st.radio('kpsp2', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp2', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/48_3.png')
                with col2:
                    st.empty()
                    kpsp3 = st.radio('kpsp3', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp3', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/48_4.png')
                with col2:
                    st.empty()
                    kpsp4 = st.radio('kpsp4', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp4', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/48_5.png')
                with col2:
                    st.empty()
                    kpsp5 = st.radio('kpsp5', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp5', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/48_6.png')
                with col2:
                    st.empty()
                    kpsp6 = st.radio('kpsp6', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp6', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/48_7.png')
                with col2:
                    st.empty()
                    kpsp7 = st.radio('kpsp7', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp7', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/48_8.png')
                with col2:
                    st.empty()
                    kpsp8 = st.radio('kpsp8', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp8', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/48_9.png')
                with col2:
                    st.empty()
                    kpsp9 = st.radio('kpsp9', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp9', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/48_10.png')
                with col2:
                    st.empty()
                    kpsp10 = st.radio('kpsp10', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp10', label_visibility='collapsed')
                    
            elif 54 <= usia_bln < 60:

                st.write('### KPSP Umur 54 bulan')

                # Membuat kolom untuk menempatkan caption di kiri dan opsi di kanan
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Menentukan lebar kolom (3 bagian untuk caption, 1 bagian untuk opsi)

                with col1:
                    st.image('.img/54_1.png')
                with col2:
                    st.empty()
                    kpsp1 = st.radio('kpsp1', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp1', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/54_2.png')
                with col2:
                    st.empty()
                    kpsp2 = st.radio('kpsp2', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp2', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/54_3.png')
                with col2:
                    st.empty()
                    kpsp3 = st.radio('kpsp3', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp3', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/54_4.png')
                with col2:
                    st.empty()
                    kpsp4 = st.radio('kpsp4', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp4', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/54_5.png')
                with col2:
                    st.empty()
                    kpsp5 = st.radio('kpsp5', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp5', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/54_6.png')
                with col2:
                    st.empty()
                    kpsp6 = st.radio('kpsp6', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp6', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/54_7.png')
                with col2:
                    st.empty()
                    kpsp7 = st.radio('kpsp7', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp7', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/54_8.png')
                with col2:
                    st.empty()
                    kpsp8 = st.radio('kpsp8', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp8', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/54_9.png')
                with col2:
                    st.empty()
                    kpsp9 = st.radio('kpsp9', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp9', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/54_10.png')
                with col2:
                    st.empty()
                    kpsp10 = st.radio('kpsp10', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp10', label_visibility='collapsed')
                    
            elif 60 <= usia_bln < 66:

                st.write('### KPSP Umur 60 bulan')

                # Membuat kolom untuk menempatkan caption di kiri dan opsi di kanan
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Menentukan lebar kolom (3 bagian untuk caption, 1 bagian untuk opsi)

                with col1:
                    st.image('.img/60_1.png')
                with col2:
                    st.empty()
                    kpsp1 = st.radio('kpsp1', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp1', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/60_2.png')
                with col2:
                    st.empty()
                    kpsp2 = st.radio('kpsp2', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp2', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/60_3.png')
                with col2:
                    st.empty()
                    kpsp3 = st.radio('kpsp3', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp3', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/60_4.png')
                with col2:
                    st.empty()
                    kpsp4 = st.radio('kpsp4', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp4', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/60_5.png')
                with col2:
                    st.empty()
                    kpsp5 = st.radio('kpsp5', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp5', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/60_6.png')
                with col2:
                    st.empty()
                    kpsp6 = st.radio('kpsp6', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp6', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/60_7.png')
                with col2:
                    st.empty()
                    kpsp7 = st.radio('kpsp7', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp7', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/60_8.png')
                with col2:
                    st.empty()
                    kpsp8 = st.radio('kpsp8', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp8', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/60_9.png')
                with col2:
                    st.empty()
                    kpsp9 = st.radio('kpsp9', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp9', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/60_10.png')
                with col2:
                    st.empty()
                    kpsp10 = st.radio('kpsp10', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp10', label_visibility='collapsed')
                    
            elif 66 <= usia_bln < 72:

                st.write('### KPSP Umur 66 bulan')

                # Membuat kolom untuk menempatkan caption di kiri dan opsi di kanan
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Menentukan lebar kolom (3 bagian untuk caption, 1 bagian untuk opsi)

                with col1:
                    st.image('.img/66_1.png')
                with col2:
                    st.empty()
                    kpsp1 = st.radio('kpsp1', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp1', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/66_2.png')
                with col2:
                    st.empty()
                    kpsp2 = st.radio('kpsp2', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp2', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/66_3.png')
                with col2:
                    st.empty()
                    kpsp3 = st.radio('kpsp3', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp3', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/66_4.png')
                with col2:
                    st.empty()
                    kpsp4 = st.radio('kpsp4', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp4', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/66_5.png')
                with col2:
                    st.empty()
                    kpsp5 = st.radio('kpsp5', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp5', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/66_6.png')
                with col2:
                    st.empty()
                    kpsp6 = st.radio('kpsp6', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp6', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/66_7.png')
                with col2:
                    st.empty()
                    kpsp7 = st.radio('kpsp7', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp7', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/66_8.png')
                with col2:
                    st.empty()
                    kpsp8 = st.radio('kpsp8', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp8', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/66_9.png')
                with col2:
                    st.empty()
                    kpsp9 = st.radio('kpsp9', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp9', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/66_10.png')
                with col2:
                    st.empty()
                    kpsp10 = st.radio('kpsp10', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp10', label_visibility='collapsed')
                    
            elif usia_bln >= 72:

                st.write('### KPSP Umur 72 bulan')

                # Membuat kolom untuk menempatkan caption di kiri dan opsi di kanan
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Menentukan lebar kolom (3 bagian untuk caption, 1 bagian untuk opsi)

                with col1:
                    st.image('.img/72_1.png')
                with col2:
                    st.empty()
                    kpsp1 = st.radio('kpsp1', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp1', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/72_2.png')
                with col2:
                    st.empty()
                    kpsp2 = st.radio('kpsp2', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp2', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/72_3.png')
                with col2:
                    st.empty()
                    kpsp3 = st.radio('kpsp3', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp3', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/72_4.png')
                with col2:
                    st.empty()
                    kpsp4 = st.radio('kpsp4', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp4', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/72_5.png')
                with col2:
                    st.empty()
                    kpsp5 = st.radio('kpsp5', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp5', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/72_6.png')
                with col2:
                    st.empty()
                    kpsp6 = st.radio('kpsp6', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp6', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/72_7.png')
                with col2:
                    st.empty()
                    kpsp7 = st.radio('kpsp7', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp7', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/72_8.png')
                with col2:
                    st.empty()
                    kpsp8 = st.radio('kpsp8', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp8', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/72_9.png')
                with col2:
                    st.empty()
                    kpsp9 = st.radio('kpsp9', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp9', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/72_10.png')
                with col2:
                    st.empty()
                    kpsp10 = st.radio('kpsp10', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp10', label_visibility='collapsed')
            
            else:
                # st.warning('Bukan Termasuk Kriteria Umur Untuk Pemeriksaan KPSP')
                st.write('### KPSP Umur 3 bulan')

                # Membuat kolom untuk menempatkan caption di kiri dan opsi di kanan
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Menentukan lebar kolom (3 bagian untuk caption, 1 bagian untuk opsi)

                with col1:
                    st.image('.img/3_1.png')
                with col2:
                    st.empty()
                    kpsp1 = st.radio('kpsp1', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp1', label_visibility='collapsed', disabled=True)

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/3_2.png')
                with col2:
                    st.empty()
                    kpsp2 = st.radio('kpsp2', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp2', label_visibility='collapsed', disabled=True)
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/3_3.png')
                with col2:
                    st.empty()
                    kpsp3 = st.radio('kpsp3', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp3', label_visibility='collapsed', disabled=True)
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/3_4.png')
                with col2:
                    st.empty()
                    kpsp4 = st.radio('kpsp4', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp4', label_visibility='collapsed', disabled=True)

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/3_5.png')
                with col2:
                    st.empty()
                    kpsp5 = st.radio('kpsp5', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp5', label_visibility='collapsed', disabled=True)
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/3_6.png')
                with col2:
                    st.empty()
                    kpsp6 = st.radio('kpsp6', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp6', label_visibility='collapsed', disabled=True)

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/3_7.png')
                with col2:
                    st.empty()
                    kpsp7 = st.radio('kpsp7', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp7', label_visibility='collapsed', disabled=True)
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/3_8.png')
                with col2:
                    st.empty()
                    kpsp8 = st.radio('kpsp8', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp8', label_visibility='collapsed', disabled=True)
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/3_9.png')
                with col2:
                    st.empty()
                    kpsp9 = st.radio('kpsp9', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp9', label_visibility='collapsed', disabled=True)
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/3_10.png')
                with col2:
                    st.empty()
                    kpsp10 = st.radio('kpsp10', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp10', label_visibility='collapsed', disabled=True)
                
            
            def calculate_score(kpsp1, kpsp2, kpsp3, kpsp4, kpsp5, kpsp6, kpsp7, kpsp8, kpsp9, kpsp10):
                score = 0
                # Penentuan skor
                if kpsp1 == 'Ya':
                    score += 1
                elif kpsp1 == 'Tidak':
                    score += 0

                if kpsp2 == 'Ya':
                    score += 1
                elif kpsp2 == 'Tidak':
                    score += 0
                    
                if kpsp3 == 'Ya':
                    score += 1
                elif kpsp3 == 'Tidak':
                    score += 0
                    
                if kpsp4 == 'Ya':
                    score += 1
                elif kpsp4 == 'Tidak':
                    score += 0
                    
                if kpsp5 == 'Ya':
                    score += 1
                elif kpsp5 == 'Tidak':
                    score += 0
                    
                if kpsp6 == 'Ya':
                    score += 1
                elif kpsp6 == 'Tidak':
                    score += 0
                    
                if kpsp7 == 'Ya':
                    score += 1
                elif kpsp7 == 'Tidak':
                    score += 0
                    
                if kpsp8 == 'Ya':
                    score += 1
                elif kpsp8 == 'Tidak':
                    score += 0
                    
                if kpsp9 == 'Ya':
                    score += 1
                elif kpsp9 == 'Tidak':
                    score += 0
                    
                if kpsp10 == 'Ya':
                    score += 1
                elif kpsp10 == 'Tidak':
                    score += 0

                return score
                
            # Hitung total skor
            total_score = calculate_score(kpsp1, kpsp2, kpsp3, kpsp4, kpsp5, kpsp6, kpsp7, kpsp8, kpsp9, kpsp10)

            if 9 <= total_score <= 10:
                kesimpulan_kpsp = st.text_input('Kesimpulan KPSP', value='Sesuai Umur', disabled=True, key='kesimpulan_kpsp')
            elif 7 <= total_score <= 8:
                kesimpulan_kpsp = st.text_input('Kesimpulan KPSP', value='Meragukan', disabled=True, key='kesimpulan_kpsp')
            elif 0 <= total_score <= 6:
                kesimpulan_kpsp = st.text_input('Kesimpulan KPSP', value='Ada Kemungkinan Penyimpangan', disabled=True, key='kesimpulan_kpsp')
            else:
                kesimpulan_kpsp = st.text_input('Kesimpulan KPSP', value=None, disabled=True, key='kesimpulan_kpsp')
                    
        with st.expander('**SKRINING DIABETES**'):
            left, right = st.columns(2)
            dm1 = left.radio('Apakah anak anda sering lapar atau banyak makan dalam 1 bulan terakhir?', ['Ya', 'Tidak'], index=None, horizontal=True, key='dm1')
            dm2 = left.radio('Apakah anak anda sering haus atau banyak minum dalam 1 bulan terakhir?', ['Ya', 'Tidak'], index=None, horizontal=True, key='dm2')
            dm3 = left.radio('Apakah anak anda sering BAK dalam 1 bulan terakhir?', ['Ya', 'Tidak'], index=None, horizontal=True, key='dm3')
            dm4 = right.radio('Apakah anak anda sering mengompol dalam 1 bulan terakhir', ['Ya', 'Tidak'], index=None, horizontal=True, key='dm4')
            dm5 = right.radio('Apakah berat badan anak anda turun secara drastis?', ['Ya', 'Tidak'], index=None, horizontal=True, key='dm5')
            dm6 = right.radio('Apakah orangtua memiliki riwayat penyakit diabetes?', ['Ya', 'Tidak'], index=None, horizontal=True, key='dm6')

        with st.expander('**SKRINING TALASEMIA**'):
            talasemia1 = st.radio('Apakah ada anggota keluarga kandung  Anda dinyatakan menderita Talasemia,  atau kelainan darah atau pernah menjalani transfusi darah secara rutin?', ['Ya', 'Tidak'], index=None, horizontal=True, key='talasemia1')
            talasemia2 = st.radio('Apakah ada anggota keluarga  kandung Anda dinyatakan sebagai pembawa sifat talasemia (mereka yang memiliki genetik yang tidak normal sehingga berpotensi menurunkan penyakit Talasemia)?', ['Ya', 'Tidak'], index=None, horizontal=True, key='talasemia2')

        with st.expander('**SKRINING TB**'):
            tb1 = st.radio('Apakah anak Anda pernah atau sedang mengalami batuk yang tidak sembuh-sembuh selama lebih dari 2 minggu?', ['Ya', 'Tidak'], index=None, horizontal=True, key='tb1')
            tb2 = st.radio('Apakah berat badan anak Anda turun tanpa alasan yang jelas?', ['Ya', 'Tidak'], index=None, horizontal=True, key='tb2')
            tb3 = st.radio('Apakah berat badan anak Anda tidak naik dalam dua bulan terakhir?', ['Ya', 'Tidak'], index=None, horizontal=True, key='tb3')
            tb4 = st.radio('Apakah anak Anda tidak atau berkurang nafsu makan?', ['Ya', 'Tidak'], index=None, horizontal=True, key='tb4')
            tb5 = st.radio ('Apakah Anda tinggal serumah atau sering bertemu dengan orang yang menderita Tuberkulosis (TBC) atau batuk berkepanjangan?', ['Ya', 'Tidak'], index=None, horizontal=True, key='tb5')
        
        with st.expander('**SKRINING MATA DAN TELINGA**'):
            left, right = st.columns(2)
            visusod = left.text_input('Visus OD', value=None, key='visusod')
            visusos = right.text_input('Visus OS', value=None, key='visusos')
            pupil_putih_od = left.radio('Pemeriksaan Pupil Putih OD', ['Negatif', 'Positif'], index=None, horizontal=True, key='pupil_putih_od')
            pupil_putih_os = right.radio('Pemeriksaan Pupil Putih OS', ['Negatif', 'Positif'], index=None, horizontal=True, key='pupil_putih_os')
            
            if usia_bln <=3:
                st.write('***Tes Daya Dengar umur <= 3 bulan***')
                tdd1 = st.radio('''Apakah bayi dapat mengatakan "Aaaaa", "Oooo"?
                        \nApakah bayi menatap wajah dan tampak mendenagrkan Anda, lalu berbicara saat anda diam?
                        \nApakah anda sesolah-olah berbicara dengan bayi anda?''', ['Ya', 'Tidak'], index=None, horizontal=True, key='tdd1')
                tdd2 = st.radio('''Apakah bayi kaget bila mendengar suara (mengejapkan mata, napas lebih cepat)?
                                \nApakah bayi kelihatan menoleh bila anda berbicara di sebelahnya?''', ['Ya', 'Tidak'], index=None, horizontal=True, key='tdd2')
                tdd3 = st.radio('''Apakah bayi anda dapat tersenyum?
                                \nApakah bayi anda kenal dengan anda, seperti senyum lebih cepat pada anda dibandingkan orang lain?''', ['Ya', 'Tidak'], index=None, horizontal=True, key='tdd3')

            elif 3 < usia_bln <= 6:
                st.write('***Tes Daya Dengar umur 3-6 bulan***')
                tdd1 = st.radio('''Apakah bayi anda dapat tertawa keras?
                                \nApakah bayi dapat bermain menggelembungkan mulut seperti meniup balon?''', ['Ya', 'Tidak'], index=None, horizontal=True, key='tdd1')
                tdd2 = st.radio('''Apakah bayi memberi respons tertentu, seperti menjadi lebih riang bila Anda datang? 
                                \nPemeriksa duduk menghadap bayi yang dipangku orang tuanya, bunyikan bel disamping tanpa terlihat bayi, apakah bayi itu menoleh ke samping?''', ['Ya', 'Tidak'], index=None, horizontal=True, key='tdd2')
                tdd3 = st.radio('''Pemeriksa menatap mata bayi sekitar 45 cm, lalu gunakan mainan untuk menarik pandangan bayi ke kiri, kanan, atas, dan bawah. Apakah bayi dapat mengikutinya?
                                \nApakah bayi berkedip bila pemeriksa melakukan gerakan menusuk mata, lalu berhenti sekitar 3 cm tanpa menyentuh mata? ''', ['Ya', 'Tidak'], index=None, horizontal=True, key='tdd3')

            elif 6 < usia_bln <= 12:
                st.write('***Tes Daya Dengar 6-12 bulan***')
                tdd1 = st.radio('''Apakah bayi dapat membuat suara berulang seperti ‘mamamama’, ‘babababa’? 
                                \nApakah bayi dapat memanggil mama atau papa, walaupun tidak untuk memanggil orang tuanya?''', ['Ya', 'Tidak'], index=None, horizontal=True, key='tdd1')
                tdd2 = st.radio('''Pemeriksa duduk mengahadap bayi yang dipangku orang tuanya, bunyikan bel di samping bawah tanpa terlihat bayi, apakah bayi langsung menoleh ke samping bawah?
                                \nApakah bayi mengikuti perintah tanpa dibantu gerakan badan, seperti “Stop, berikan mainanmu”?''', ['Ya', 'Tidak'], index=None, horizontal=True, key='tdd2')
                tdd3 = st.radio('''Apakah bayi mengikuti perintah dengan dibantu gerakan badan, seperti “Stop, berikan mainanmu”?
                                \nApakah bayi secara spontan memulai permainan dengan gerakan tubuh, seperti ‘Pok Ame-Ame’ atau ‘Cilukba’? ''', ['Ya', 'Tidak'], index=None, horizontal=True, key='tdd3')

            elif 12 < usia_bln <=18:
                st.write('***Tes Daya Dengar 12-18 bulan***')
                tdd1 = st.radio('''Apakah anak dapat memanggil ‘mama’ atau ‘papa’, hanya untuk memanggil orang tuanya?
                                \nApakah anak memulai menggunakan kata-kata lain, selain kata ‘mama’, ‘papa’, anggota keluarga lain, dan hewan peliharaan?''', ['Ya', 'Tidak'], index=None, horizontal=True, key='tdd1')
                tdd2 = st.radio('''Pemeriksa duduk menghadap bayi yang dipangku orang tuanya, bunyikan bel di samping bawah tanpa terlihat bayi, apakah bayi langsung menoleh ke samping bawah?
                                \nApakah anak mengikuti perintah tanpa dibantu gerakan badan, seperti “Stop, berikan mainanmu”?''', ['Ya', 'Tidak'], index=None, horizontal=True, key='tdd2')
                tdd3 = st.radio('''Apakah anak secara spontan memulai permainan dengan gerakan tubuh, seperti ‘Pok Ame-Ame’ atau ‘Cilukba’?
                                \nApakah anak Anda menunjuk dengan jari telunjuk bila ingin sesuatu, bukan dengan cara memegang dengan semua jari?''', ['Ya', 'Tidak'], index=None, horizontal=True, key='tdd3')

            elif 18 < usia_bln <= 24:
                st.write('***Tes Daya Dengar 18-24 bulan***')
                tdd1 = st.radio('''Apakah anak dapat mengucapkan 2 atau lebih kata yang menunjukkan keinginan, seperti “Susu”, “Minum”, “Lagi”? 
                                \nApakah anak secara spontan mengatakan 2 kombinasi kata, seperti “Mau bobo”, “Lihat Papa”?''', ['Ya', 'Tidak'], index=None, horizontal=True, key='tdd1')
                tdd2 = st.radio('''Apakah anak dapat menunjukkan paling sedikit 1 anggota badan, misal “Mana hidungmu?”, “Mana matamu?” tanpa diberi contoh?
                                \nApakah anak dapat mengerjakan 2 macam perintah dalam satu kalimat, seperti “Ambil sepatumu dan taruh disini” tanpa diberi contoh?''', ['Ya', 'Tidak'], index=None, horizontal=True, key='tdd2')
                tdd3 = st.radio('''Apakah anak secara spontan memulai permainan dengan gerakan tubuh, seperti ‘Pok Ame-Ame’ atau ‘Cilukba’?
                                \nApakah anak Anda menunjuk dengan jari telunjuk bila ingin sesuatu, bukan dengan cara memegang dengan semua jari?''', ['Ya', 'Tidak'], index=None, horizontal=True, key='tdd3')

            elif 24 < usia_bln <= 30:
                st.write('***Tes Daya Dengar 24-30 bulan***')
                tdd1 = st.radio('''Apakah anak mulai menggunakan kata-kata lain, selain kata ‘mama’, ‘papa’, anggota keluarga lain, dan hewan peliharaan?
                                \nApakah anak mulai mengungkapkan kata yang berarti ‘milik’ misal “Susu kamu”, “Bonekaku”? ''', ['Ya', 'Tidak'], index=None, horizontal=True, key='tdd1')
                tdd2 = st.radio('''Apakah anak dapat mengerjakan 2 macam perintah dalam satu kalimat, seperti “Ambil sepatu dan taruh disini” tanpa diberi contoh?
                                \nApakah anak dapat menunjuk minimal 2 nama benda di depannya (cangkir, bola, sendok)?''', ['Ya', 'Tidak'], index=None, horizontal=True, key='tdd2')
                tdd3 = st.radio('''Apakah anak secara spontan memulai permainan dengan gerakan tubuh, seperti ‘Pok Ame-Ame’ atau ‘Cilukba’?
                                \nApakah anak Anda menunjuk dengan jari telunjuk bila ingin sesuatu, bukan dengan cara memegang dengan semua jari?''', ['Ya', 'Tidak'], index=None, horizontal=True, key='tdd3')

            elif 30 < usia_bln <= 36:
                st.write('***Tes Daya Dengar 30-36 bulan***')
                tdd1 = st.radio('''Apakah anak dapat menyebutkan nama benda dan kegunaannya, seperi cangkir untuk minum, bola untuk dilempar, pensil warna untuk menggambar, sendok untuk makan?
                                \nApakah lebih dari tiga perempat orang mengerti apa yang dibicarakan anak Anda?''', ['Ya', 'Tidak'], index=None, horizontal=True, key='tdd1')
                tdd2 = st.radio('''Apakah anak dapat menunjukkan minimal 2 nama benda di depannya sesuai fungsinya (misal untuk minum: cangkir, untuk dilempar: bola, untuk makan: sendok, untuk menggambar: pensil warna)?
                                \nApakah anak dapat mengerjakan perintah yang disertai kata depan? (misal: “Sekarang kubus itu di bawah meja, tolong taruh di atas meja”)?''', ['Ya', 'Tidak'], index=None, horizontal=True, key='tdd2')
                tdd3 = st.radio('''Apakah anak secara spontan memulai permainan dengan gerakan tubuh? Seperti ‘Pok Ame−Ame’ atau ‘Cilukba’?
                                \nApakah anak Anda menunjuk dengan jari telunjuk bila ingin sesuatu, bukan dengan cara memegang dengan semua jari?''', ['Ya', 'Tidak'], index=None, horizontal=True, key='tdd3')

            elif usia_bln >36:
                st.write('***Tes Daya Dengar >36 bulan***')
                tdd1 = st.radio('''Apakah anak dapat menyebutkan nama benda dan kegunaannya, seperti cangkir untuk minum, bola untuk dilempar, pensil warna untuk menggambar, sendok untuk makan?
                                \nApakah lebih dari tiga perempat orang mengerti apa yang dibicarakan anak Anda?''', ['Ya', 'Tidak'], index=None, horizontal=True, key='tdd1')
                tdd2 = st.radio('Apakah anak Anda dapat menunjukkan minimal 2 nama benda di depannya sesuai fungsi (misal untuk minum: cangkir, untuk dilempar: bola, untuk makan: sendok, untuk menggambar: pensil warna?)', ['Ya', 'Tidak'], index=None, horizontal=True, key='tdd2')
                tdd3 = st.radio('''Apakah anak secara spontan memulai permainan dengan gerakan tubuh, seperti ‘Pok Ame-Ame’ atau ‘Cilukba’?
                                \nApakah anak Anda menunjuk dengan jari telunjuk bila ingin sesuatu, bukan dengan cara memegang dengan semua jari?''', ['Ya', 'Tidak'], index=None, horizontal=True, key='tdd3')
                
            else:
                tdd1 = st.radio('''Apakah bayi dapat mengatakan "Aaaaa", "Oooo"?
                        \nApakah bayi menatap wajah dan tampak mendenagrkan Anda, lalu berbicara saat anda diam?
                        \nApakah anda sesolah-olah berbicara dengan bayi anda?''', ['Ya', 'Tidak'], index=None, horizontal=True, key='tdd1', disabled=True)
                tdd2 = st.radio('''Apakah bayi kaget bila mendengar suara (mengejapkan mata, napas lebih cepat)?
                                \nApakah bayi kelihatan menoleh bila anda berbicara di sebelahnya?''', ['Ya', 'Tidak'], index=None, horizontal=True, key='tdd2', disabled=True)
                tdd3 = st.radio('''Apakah bayi anda dapat tersenyum?
                                \nApakah bayi anda kenal dengan anda, seperti senyum lebih cepat pada anda dibandingkan orang lain?''', ['Ya', 'Tidak'], index=None, horizontal=True, key='tdd3', disabled=True)

            def calculate_score(tdd1, tdd2, tdd3):
                score = 0
                # Penentuan skor berdasarkan kelompok usia
                if tdd1 == 'Ya':
                    score += 0
                elif tdd1 == 'Tidak':
                    score += 1

                if tdd2 == 'Ya':
                    score += 0
                elif tdd2 == 'Tidak':
                    score += 1
                
                if tdd3 == 'Ya':
                    score += 0
                elif tdd3 == 'Tidak':
                    score += 1

                return score
            
            # Hitung total skor
            total_score = calculate_score(tdd1, tdd2, tdd3)

            if total_score >= 1:
                kesimpulan_tdd = st.text_input('Kesimpulan Tes Daya Dengar', value='Ada Kemungkinan Penyimpangan', disabled=True, key='kesimpulan_tdd')
            else:
                kesimpulan_tdd = st.text_input('Kesimpulan Tes Daya Dengar', value='Sesuai Umur', disabled=True, key='kesimpulan_tdd')
    
        with st.expander('**SKRINING GPPH**'):
            gpph1 = st.radio('Tidak kenal lelah atau aktivitas yang berlebihan', ['Tidak', 'Kadang-kadang', 'Sering', 'Selalu'], index=None, horizontal=True, key='gpph1')
            gpph2 = st.radio('Mudah menjadi gembira, impulsif', ['Tidak', 'Kadang-kadang', 'Sering', 'Selalu'], index=None, horizontal=True, key='gpph2')
            gpph3 = st.radio('Mengganggu anak-anak lain', ['Tidak', 'Kadang-kadang', 'Sering', 'Selalu'], index=None, horizontal=True, key='gpph3')
            gpph4 = st.radio('Gagal menyelesaikan kegiatan yang telah dimulai; rentang perhayian pendek', ['Tidak', 'Kadang-kadang', 'Sering', 'Selalu'], index=None, horizontal=True, key='gpph4')
            gpph5 = st.radio('Menggerak-gerakkan anggota badan atau kepala secara terus menerus', ['Tidak', 'Kadang-kadang', 'Sering', 'Selalu'], index=None, horizontal=True, key='gpph5')
            gpph6 = st.radio('Kurang memperhatikan, mudah teralihkan', ['Tidak', 'Kadang-kadang', 'Sering', 'Selalu'], index=None, horizontal=True, key='gpph6')
            gpph7 = st.radio('Permintaannya harus segera dipenuhi; mudah menjadi frustasi', ['Tidak', 'Kadang-kadang', 'Sering', 'Selalu'], index=None, horizontal=True, key='gpph7')
            gpph8 = st.radio('Sering dan mudah menangis', ['Tidak', 'Kadang-kadang', 'Sering', 'Selalu'], index=None, horizontal=True, key='gpph8')
            gpph9 = st.radio('Suasana hatinya mudah berubah dengan cepat dan drastis', ['Tidak', 'Kadang-kadang', 'Sering', 'Selalu'], index=None, horizontal=True, key='gpph9')
            gpph10 = st.radio('Ledakan kekesalan, tingkah laku ekspolsif dan tak terduga', ['Tidak', 'Kadang-kadang', 'Sering', 'Selalu'], index=None, horizontal=True, key='gpph10')
            # Fungsi untuk menghitung skor
            def calculate_score(gpph1, gpph2, gpph3, gpph4, gpph5, gpph6, gpph7, gpph8, gpph9, gpph10):
                score = 0
                if gpph1 == 'Kadang-kadang':
                    score += 1
                elif gpph1 == 'Sering':
                    score += 2
                elif gpph1 == 'Selalu':
                    score += 3
                else:
                    score += 0

                if gpph2 == 'Kadang-kadang':
                    score += 1
                elif gpph2 == 'Sering':
                    score += 2
                elif gpph2 == 'Selalu':
                    score += 3
                else:
                    score += 0
                
                if gpph3 == 'Kadang-kadang':
                    score += 1
                elif gpph3 == 'Sering':
                    score += 2
                elif gpph3 == 'Selalu':
                    score += 3
                else:
                    score += 0
                
                if gpph4 == 'Kadang-kadang':
                    score += 1
                elif gpph4 == 'Sering':
                    score += 2
                elif gpph4 == 'Selalu':
                    score += 3
                else:
                    score += 0
                    
                if gpph5 == 'Kadang-kadang':
                    score += 1
                elif gpph5 == 'Sering':
                    score += 2
                elif gpph5 == 'Selalu':
                    score += 3
                else:
                    score += 0
                    
                if gpph6 == 'Kadang-kadang':
                    score += 1
                elif gpph6 == 'Sering':
                    score += 2
                elif gpph6 == 'Selalu':
                    score += 3
                else:
                    score += 0
                    
                if gpph7 == 'Kadang-kadang':
                    score += 1
                elif gpph7 == 'Sering':
                    score += 2
                elif gpph7 == 'Selalu':
                    score += 3
                else:
                    score += 0
                    
                if gpph8 == 'Kadang-kadang':
                    score += 1
                elif gpph8 == 'Sering':
                    score += 2
                elif gpph8 == 'Selalu':
                    score += 3
                else:
                    score += 0
                    
                if gpph9 == 'Kadang-kadang':
                    score += 1
                elif gpph9 == 'Sering':
                    score += 2
                elif gpph9 == 'Selalu':
                    score += 3
                else:
                    score += 0
                    
                if gpph10 == 'Kadang-kadang':
                    score += 1
                elif gpph10 == 'Sering':
                    score += 2
                elif gpph10 == 'Selalu':
                    score += 3
                else:
                    score += 0

                return score
            
            # Hitung total skor
            total_score = calculate_score(gpph1, gpph2, gpph3, gpph4, gpph5, gpph6, gpph7, gpph8, gpph9, gpph10)

            # Kesimpulan
            if total_score < 13:
                kesimpulan_gpph = st.text_input('Kesimpulan', value='Normal', disabled=True, key='kesimpulan_gpph')
            else:
                kesimpulan_gpph = st.text_input('Kesimpulan', value='Kemungkinan GPPH', disabled=True, key='kesimpulan_gpph')

            # tidak=0
            # kadang2=1
            # sering=2
            # selalu=3
            
            #<13 = normal
            #>= 13 = kemungkinan gpph
            
        with st.expander('**SKRINING MASALAH PERILAKU EMOSIONAL**'):
            emosi1 = st.radio('Apakah anak Anda sering bereaksi negatif, marah atau tegang tanpa sebab yang jelas? (Bereaksi negatif contohnya rewel, tidak sabaran, banyak menangis, mudah tersinggung atau bereaksi berlebihan bila merasa situasi tidak seperti yang diharapkannya atau kemauannya tidak terpenuhi)', ['Ya', 'Tidak'], index=None, horizontal=True, key='emosi1')
            emosi2 = st.radio('Apakah anak Anda tampak lebih memilih untuk menyendiri, bermain sendiri, atau menghindar dari anak seumurnya atau orang dewasa? (Ingin sendirian, menyendiri dengan ekspresi murung, tidak bersemangat, sedih, atau kehilangan minat terhadap hal-hal yang biasa sangat dinikmati)', ['Ya', 'Tidak'], index=None, horizontal=True, key='emosi2')
            emosi3 = st.radio('Apakah anak Anda cenderung bersikap menentang? (Membantah, melawan, tidak mau menurut atau melakukan hal yang sebaliknya dari apa yang diminta, serta tampak tidak peduli ketika diberitahu atau ditegur)', ['Ya', 'Tidak'], index=None, horizontal=True, key='emosi3')
            emosi4 = st.radio('Apakah anak Anda mudah takut atau cemas berlebihan tanpa sebab yang jelas?(Misalnya takut pada binatang atau benda yang tidak berbahaya, terlihat cemas ketika tidak melihat ibu atau pengasuh)', ['Ya', 'Tidak'], index=None, horizontal=True, key='emosi4')
            emosi5 = st.radio('Apakah anak Anda sering sulit konsentrasi, perhatiannya mudah teralihkan atau banyak bergerak atau tidak bisa diam? (Misalnya anak tidak bisa bertahan lama untuk bermain dengan satu permainan, mudah mengalihkan perhatian bila ada hal lain yang lebih menarik perhatian seperti bunyi atau gerakan, tidak bisa duduk dengan tenang, banyak bergerak atau cenderung berjalan atau berlari mondar-mandir)', ['Ya', 'Tidak'], index=None, horizontal=True, key='emosi5')
            emosi6 = st.radio('Apakah anak Anda lebih banyak menempel atau selalu minta ditemani, mudah cemas, dan tidak percaya diri? (Seakan minta perlindungan atau minta ditemanipada berbagai situasi, terutama ketika berada dalam situasi baru atau ada orang yang baru dikenalnya; mengekspresikan kecemasan serta terlihat tidak percaya diri)', ['Ya', 'Tidak'], index=None, horizontal=True, key='emosi6')
            emosi7 = st.radio('Apakah anak Anda menunjukkan adanya perubahan pola tidur? (Misalnya sulit tidur, terjaga sepanjang hari, sering terbangun di waktu tidur malam oleh karena mimpi buruk, mengigau, menangis di dalam tidurnya)', ['Ya', 'Tidak'], index=None, horizontal=True, key='emosi7')
            emosi8 = st.radio('Apakah anak Anda mengalami perubahan pola makan dari yang biasanya?(Kehilangan nafsu makan, tidak mau makan sama sekali, atau sebaliknya makan berlebihan, sangat memilih jenis makanan, atau membiarkan makanan lama dimulut tanpa dikunyah atau diemut)', ['Ya', 'Tidak'], index=None, horizontal=True, key='emosi8')
            emosi9 = st.radio('Apakah anak Anda seringkali mengeluh sakit kepala, sakit perut, atau keluhan fisik lainnya pada waktu-waktu tertentu?', ['Ya', 'Tidak'], index=None, horizontal=True, key='emosi9')
            emosi10 = st.radio('Apakah anak Anda mudah putus asa atau frustrasi dan sering menunjukkan emosi yang negatif? (Misalnya sedih atau kecewa yang berkepanjangan, mudah mengeluh, marah, atau protes. Misal ketika anak merasa kesulitan dalam menggambar, lalu berteriak minta tolong, marah, atau kertasnya disobek)', ['Ya', 'Tidak'], index=None, horizontal=True, key='emosi10')
            emosi11 = st.radio('Apakah anak Anda menunjukkan kemunduran pola perilaku dari kemampuan yang sudah dimilikinya? (Misalnya mengompol kembali, menghisap jempol, atau tidak mau berpisah dengan orangtua atau pengasuhnya)', ['Ya', 'Tidak'], index=None, horizontal=True, key='emosi11')
            emosi12 = st.radio('Apakah anak Anda sering berkelahi, bertengkar, atau menyerang anak lain baik secara verbal maupun non verbal? (Misalnya mengejek, meneriaki, merebut permainan, atau memukul temannya)', ['Ya', 'Tidak'], index=None, horizontal=True, key='emosi12')
            emosi13 = st.radio('Apakah anak Anda sering diperlakukan tidak menyenangkan oleh anak lain atauorang dewasa? (Misalnya ditinggal bermain, dihindari, diejek, dikata-katai, direbut mainannya, atau disakiti secara fisik)', ['Ya', 'Tidak'], index=None, horizontal=True, key='emosi13')
            emosi14 = st.radio('Apakah anak Anda cenderung berperilaku merusak atau cenderung selalu ingin menang atau menguasai? (Misalnya merusak benda, menyakiti dirinya atau binatang)', ['Ya', 'Tidak'], index=None, horizontal=True, key='emosi14')
            
            
            
            # Fungsi untuk menghitung skor
            def calculate_score(emosi1, emosi2, emosi3, emosi4, emosi5, emosi6, emosi7, emosi8, emosi9, emosi10, emosi11, emosi12, emosi13, emosi14):
                score = 0
                if emosi1 == 'Ya':
                    score += 1
                elif emosi1 == 'Tidak':
                    score += 0
                
                if emosi2 == 'Ya':
                    score += 1
                elif emosi2 == 'Tidak':
                    score += 0
                    
                if emosi3 == 'Ya':
                    score += 1
                elif emosi3 == 'Tidak':
                    score += 0
                    
                if emosi4 == 'Ya':
                    score += 1
                elif emosi4 == 'Tidak':
                    score += 0
                
                if emosi5 == 'Ya':
                    score += 1
                elif emosi5 == 'Tidak':
                    score += 0
                    
                if emosi6 == 'Ya':
                    score += 1
                elif emosi6 == 'Tidak':
                    score += 0
                    
                if emosi7 == 'Ya':
                    score += 1
                elif emosi7 == 'Tidak':
                    score += 0
                
                if emosi8 == 'Ya':
                    score += 1
                elif emosi8 == 'Tidak':
                    score += 0
                    
                if emosi9 == 'Ya':
                    score += 1
                elif emosi9 == 'Tidak':
                    score += 0
                    
                if emosi10 == 'Ya':
                    score += 1
                elif emosi10 == 'Tidak':
                    score += 0
                
                if emosi11 == 'Ya':
                    score += 1
                elif emosi11 == 'Tidak':
                    score += 0
                    
                if emosi12 == 'Ya':
                    score += 1
                elif emosi12 == 'Tidak':
                    score += 0
                    
                if emosi13 == 'Ya':
                    score += 1
                elif emosi13 == 'Tidak':
                    score += 0
                
                if emosi14 == 'Ya':
                    score += 1
                elif emosi14 == 'Tidak':
                    score += 0
                    
                return score
            
            # Hitung total skor
            total_score = calculate_score(emosi1, emosi2, emosi3, emosi4, emosi5, emosi6, emosi7, emosi8, emosi9, emosi10, emosi11, emosi12, emosi13, emosi14)

            # Kesimpulan
            if 0 < total_score <= 1:
                kesimpulan_emosi = st.text_input('Kesimpulan', value='Meragukan', disabled=True, key='kesimpulan_emosi')
            elif total_score >= 2:
                kesimpulan_emosi = st.text_input('Kesimpulan', value='Kemungkinan Anak Mengalami Masalah Perilaku Emosional', disabled=True, key='kesimpulan_emosi')
            else:
                kesimpulan_emosi = st.text_input('Kesimpulan', value='Normal', disabled=True, key='kesimpulan_emosi')

            
            #tidak ada jawaban ya= normal
            #1 jawaban ya = meragukan
            #>=2 jawaban ya = kemungkinan anak mengalami masalah perilaku emosional
            
        with st.expander('**SKRINING GIGI**'):
            gigi = st.text_input('Karies Dentis', value=None, key='gigi')

        with st.expander('**PEMERIKSAAN LABORATORIUM**'):
            left, right = st.columns(2)
            hb = left.number_input('HB', value=None, key='hb')
            eritrosit = left.number_input('Eritrosit(X10*6)', value=None, key='eritrosit')
            htc = left.number_input('Hematokrit', value=None, key='htc')
            leukosit = left.number_input('Leukosit', value=None, key='leukosit')
            trombosit = left.number_input('Trombosit', value=None, key='trombosit')
            mcv = left.number_input('MCV', value=None, key='mcv')
            mch = right.number_input('MCH', value=None, key='mch')
            mchc = right.number_input('MCHC', value=None, key='mchc')
            rdw = right.number_input('RDW', value=None, key='rdw')
            gds = right.number_input('GDS', value=None, key='gds')
            if mcv is not None and eritrosit is not None:
                mi = mcv/eritrosit
                mentzer = right.number_input('Index Mentzer', value=mi, key='mentzer', disabled=True)
            else:
                mentzer = right.number_input('Index Mentzer', value=0, key='mentzer', disabled=True)
        
            
        # Tombol untuk menyimpan data baru
        btn_save_add = st.button('Simpan Data Baru', key='btn_save_add')
        
        if btn_save_add:
            # Menyimpan data baru ke dalam Google Sheets
            new_data = pd.DataFrame(
                [
                    {
                        "Tanggal Pemeriksaan": tgl_pem,
                        "Nama": nama,
                        "NIK": nik.strip(),
                        "Jenis Kelamin": jk,
                        "Tanggal Lahir": tgl_lhr,
                        "Usia_Tahun": ut,
                        "Usia_Bulan": ub,
                        "Alamat": alamat,
                        "Nomor HP": hp,
                        "Nama Wali": wali,
                        "NIK Wali": nik_wali,
                        "Disabilitas": disabilitas,
                        "BB": bb,
                        "TB/PB": tb,
                        "Posisi": posisi,
                        "IMT": bmi,
                        "Lingkar Kepala": lk,
                        "BB/U": stat_bbu, 
                        "TB/U": stat_tbu,
                        "BB/TB": stat_bbtb,
                        "IMT/U": stat_imtu,
                        "LK/U": stat_lku,
                        "LLA": lla,
                        "Status LLA": stat_lla,
                        "KPSP1": kpsp1,
                        "KPSP2": kpsp2,
                        "KPSP3": kpsp3,
                        "KPSP4": kpsp4,
                        "KPSP5": kpsp5,
                        "KPSP6": kpsp6,
                        "KPSP7": kpsp7,
                        "KPSP8": kpsp8,
                        "KPSP9": kpsp9,
                        "KPSP10": kpsp10,
                        "Kesimpulan KPSP": kesimpulan_kpsp,
                        "DM1": dm1,
                        "DM2": dm2,
                        "DM3": dm3,
                        "DM4": dm4,
                        "DM5": dm5,
                        "DM6": dm6,
                        "Talasemia1": talasemia1,
                        "Talasemia2": talasemia2,
                        "TB1": tb1,
                        "TB2": tb2,
                        "TB3": tb3,
                        "TB4": tb4,
                        "TB5": tb5,
                        "Visus OD": visusod,
                        "Visus OS": visusos,
                        "Pupil Putih OD": pupil_putih_od,
                        "Pupil Putih OS": pupil_putih_os,
                        "TDD1": tdd1,
                        "TDD2": tdd2,
                        "TDD3": tdd3,
                        "Kesimpulan TDD": kesimpulan_tdd,
                        "GPPH1": gpph1,
                        "GPPH2": gpph2,
                        "GPPH3": gpph3,
                        "GPPH4": gpph4,
                        "GPPH5": gpph5,
                        "GPPH6": gpph6,
                        "GPPH7": gpph7,
                        "GPPH8": gpph8,
                        "GPPH9": gpph9,
                        "GPPH10": gpph10,
                        "Kesimpulan GPPH": kesimpulan_gpph,
                        "Emosi1": emosi1,
                        "Emosi2": emosi2,
                        "Emosi3": emosi3,
                        "Emosi4": emosi4,
                        "Emosi5": emosi5,
                        "Emosi6": emosi6,
                        "Emosi7": emosi7,
                        "Emosi8": emosi8,
                        "Emosi9": emosi9,
                        "Emosi10": emosi10,
                        "Emosi11": emosi11,
                        "Emosi12": emosi12,
                        "Emosi13": emosi13,
                        "Emosi14": emosi14,
                        "Kesimpulan Emosi": kesimpulan_emosi,
                        "Karies Dentis": gigi,
                        "HB": hb,
                        "Eritrosit": eritrosit,
                        "Hematokrit": htc,
                        "Leukosit": leukosit,
                        "Trombosit": trombosit,
                        "MCV": mcv,
                        "MCH": mch,
                        "MCHC": mchc,
                        "RDW": rdw,
                        "GDS": gds,
                        "Index Mentzer": mentzer
                    }
                ]
            )
            
            # Menambahkan data baru ke DataFrame yang ada
            df = pd.concat([df, new_data], ignore_index=True)

            # Update data ke Google Sheets
            conn.update(worksheet='pkg_balita', data=df)
            st.success("Data baru berhasil disimpan.")
            
            st.cache_data.clear()
            
    # Formulir input dengan pre-filled data jika ada
    if st.session_state.input_nik_loaded:
        with st.expander('**IDENTITAS PASIEN**', expanded=True):
            left, right = st.columns(2)
            sekarang = datetime.today().date()
            tgl_pem_x = left.date_input('Tanggal Pemeriksaan', format='DD/MM/YYYY', value = st.session_state.input_data.get('Tanggal Pemeriksaan', None), key='tgl_pem_x', disabled=True)
            
            nama_x = left.text_input('Nama Lengkap', value=st.session_state.input_data.get('Nama',''), key='nama_x')
            
            nik_x = left.text_input('NIK', value=st.session_state.input_data.get('NIK',''), key='nik_x')
            
            jenis_kelamin_value = st.session_state.input_data.get('Jenis Kelamin', None)
            if pd.isna(jenis_kelamin_value):
                jk_x = left.selectbox('Jenis Kelamin', ['Perempuan', 'Laki-laki'], index=None, key='jk_x')
            else:
                jk_x = left.selectbox('Jenis Kelamin', ['Perempuan', 'Laki-laki'], index= ['Perempuan', 'Laki-laki'].index(jenis_kelamin_value), key='jk_x')
            
            alamat_value = st.session_state.input_data.get('Alamat', '')
            if pd.isna(alamat_value):
                alamat_x = left.text_input('Alamat', value=None, key='alamat_x')
            else:
                alamat_x = left.text_input('Alamat', value=alamat_value, key='alamat_x')
                
            hp_value = st.session_state.input_data.get('Nomor HP', '')
            if pd.isna(hp_value):
                hp_x = left.text_input('Nomor HP', value=None, key='hp_x')
            else:
                hp_x = left.text_input('Nomor HP', value=hp_value, key='hp_x')
                
            tgl_lhr_value = st.session_state.input_data.get('Tanggal Lahir', None)
            if pd.isna(tgl_lhr_value):
                tgl_lhr_x = right.date_input("Tanggal Lahir", format='DD/MM/YYYY', min_value=datetime(2018, 1, 1), value=None, key='tgl_lhr_x')
            else:
                tgl_lhr_x = right.date_input("Tanggal Lahir", format='DD/MM/YYYY', min_value=datetime(2018, 1, 1), value=tgl_lhr_value, key='tgl_lhr_x')    
            
            umur = sekarang - tgl_lhr_x
            usia_thn = umur.days//365
            usia_bln = umur.days//30
            if tgl_lhr_x:
                ut_x = right.number_input('Usia (dalam tahun)', value=usia_thn, disabled=True, key='ut_x')
                ub_x = right.number_input('Usia (dalam bulan)', value=usia_bln, disabled=True, key='ub_x')
            else:
                ut_x = right.number_input('Usia (dalam tahun)', value=0, disabled=True, key='ut_x')
                ub_x = right.number_input('Usia (dalam bulan)', value=0, disabled=True, key='ub_x')
            
            wali_value = st.session_state.input_data.get('Nama Wali', '')
            if pd.isna(wali_value):
                wali_x = right.text_input('Nama Wali', value=None, key='wali_x')
            else:
                wali_x = right.text_input('Nama Wali', value=wali_value, key='wali_x')
                
            nik_wali_value = st.session_state.input_data.get('NIK Wali', '')
            if pd.isna(nik_wali_value):
                nik_wali_x = right.text_input('NIK Wali', value=None, key='nik_wali_x')
            else:
                nik_wali_x = right.text_input('NIK Wali', value=nik_wali_value, key='nik_wali_x')
            
            disabilitas_value = st.session_state.input_data.get('Disabilitas', None)
            if pd.isna(disabilitas_value):
                disabilitas_x = right.radio('Apakah anak mengalami disabilitas?', ['Tidak', 'Ya'], index=None, key='disabilitas_x', horizontal=True)
            else:
                disabilitas_x = right.radio('Apakah anak mengalami disabilitas?', ['Tidak', 'Ya'], index=['Tidak', 'Ya'].index(disabilitas_value), key='disabilitas_x', horizontal=True)
                
        with st.expander('**SKRINING PERTUMBUHAN**'):
            left, right = st.columns(2)
            bb_value = st.session_state.input_data.get('BB', 0.0)
            if pd.isna(bb_value):
                bb_x = left.number_input('Berat Badan (dalam kg)', value=0.0, step=0.1, key='bb_x')
            else:
                bb_x = left.number_input('Berat Badan (dalam kg)', value=bb_value, step=0.1, key='bb_x')
            
            posisi_value = st.session_state.input_data.get('Posisi', None)
            if pd.isna(posisi_value):
                posisi_x = left.radio('Posisi Pengukuran', ['Berdiri', 'Terlentang'], index=0, horizontal=True, key='posisi_x')
            else:
                posisi_x = left.radio('Posisi Pengukuran', ['Berdiri', 'Terlentang'], index=['Berdiri', 'Terlentang'].index(posisi_value), horizontal=True, key='posisi_x')
            
            tb_value = st.session_state.input_data.get('TB/PB', 0.0)
            if pd.isna(tb_value):
                tb_x = left.number_input('Tinggi Badan (dalam cm)', value=0.0, step=0.1, key='tb_x')
            else:
                tb_x = left.number_input('Tinggi Badan (dalam cm)', value=tb_value, step=0.1, key='tb_x')
            
            lk_value = st.session_state.input_data.get('Lingkar Kepala', 0.0)
            if pd.isna(lk_value):
                lk_x = left.number_input('Lingkar Kepala (dalam cm)', value=0.0, step=0.1, key='lk_x')
            else:
                lk_x = left.number_input('Lingkar Kepala (dalam cm)', value=lk_value, step=0.1, key='lk_x')
            
            if 6 <= usia_bln < 60:
                lla_value = st.session_state.input_data.get('LLA', 0.0)
                if pd.isna(lla_value):
                    lla_x = left.number_input('Lingkar Lengan Atas(dalam cm)', value=0.0, step=0.1, key='lla_x')
                else:
                    lla_x = left.number_input('Lingkar Lengan Atas(dalam cm)', value=lla_value, step=0.1, key='lla_x')
                    
                    
            else:
                lla_x = left.number_input('Lingkar Lengan Atas(dalam cm)', value=0, key='lla_x', disabled=True)
            
                    
                
            if  lla_x >= 12.5:
                stat_lla_x = left.text_input('Status LiLA', value='Normal', disabled=True, key= 'stat_lla_x')
            elif 11.5 <= lla_x <= 12.4:
                stat_lla_x = left.text_input('Status LiLA', value='Gizi Kurang', disabled=True, key='stat_lla_x')
            elif 0 < lla_x < 11.5:
                stat_lla_x = left.text_input('Status LiLA', value='Gizi Buruk', disabled=True, key='stat_lla_x')
            else:
                stat_lla_x = left.text_input('Status LiLA', value='', disabled=True, key='stat_lla_x')
                
            
            
            def hitung_bmi(tb, bb):
                try:
                    a = tb * tb / 10000  # konversi tinggi badan ke meter kuadrat
                    imt = bb / a
                    return imt
                except ZeroDivisionError:
                    return 0  # jika tinggi badan 0
                except Exception as e:
                    st.error(f"Terjadi kesalahan saat menghitung BMI: {e}")
                    return 0

            if st.session_state.bb_x and st.session_state.tb_x is not None:
                imt=hitung_bmi(tb_x, bb_x)
                bmi_x=right.number_input('Indeks Massa Tubuh', value=imt, disabled=True, key='bmi_x')
            else:
                bmi_x=right.number_input('Indeks Massa Tubuh', value=0, disabled=True, key='bmi_x')
            
            
            if st.session_state.jk_x == 'Laki-laki':
        
                if 0 <= usia_bln <= 60:
                    #untuk BB/U
                    lakibbu = pd.read_excel('gizi.xlsx', sheet_name='Lakibbu')

                    data_lakibbu = lakibbu[lakibbu['Usia'] == int(usia_bln)].index
                    

                    x = lakibbu.iloc[data_lakibbu]
                    
                    minus_tiga_lbbu = x['SD-3'].values[0]
                    minus_dua_lbbu = x['SD-2'].values[0]
                    plus_satu_lbbu = x['SD+1'].values[0]
                    
                    if float(bb_x) < minus_tiga_lbbu:
                        stat_bbu_x= right.text_input('BB/U', value='Berat Badan Sangat Kurang', disabled=True, key='stat_bbu_x')
                    elif minus_tiga_lbbu <= float(bb_x) < minus_dua_lbbu:
                        stat_bbu_x= right.text_input('BB/U', value='Berat Badan Kurang', disabled=True, key='stat_bbu_x')
                    elif minus_dua_lbbu <= float(bb_x) <= plus_satu_lbbu:
                        stat_bbu_x= right.text_input('BB/U', value='Berat Badan Normal', disabled=True, key='stat_bbu_x')
                    else:
                        stat_bbu_x= right.text_input('BB/U', value='Berat Badan Lebih', disabled=True, key='stat_bbu_x')

                    #untuk TB/U
                    lakitbu = pd.read_excel('gizi.xlsx', sheet_name='Lakitbu')

                    data_lakitbu = lakitbu[lakitbu['Usia'] == int(usia_bln)].index

                    y = lakitbu.iloc[data_lakitbu]
                    minus_tiga_ltbu = y['SD-3'].values[0]
                    minus_dua_ltbu = y['SD-2'].values[0]
                    plus_satu_ltbu = y['SD+1'].values[0]
                    

                    if float(tb_x) < minus_tiga_ltbu :
                        stat_tbu_x = right.text_input('TB/U', value='Sangat Pendek', disabled=True, key='stat_tbu_x')
                    elif minus_tiga_ltbu <= float(tb_x) < minus_dua_ltbu:
                        stat_tbu_x = right.text_input('TB/U', value='Pendek', disabled=True, key='stat_tbu_x')
                    elif minus_dua_ltbu <= float(tb_x) <= plus_satu_ltbu:
                        stat_tbu_x = right.text_input('TB/U', value='Tinggi Badan Normal', disabled=True, key='stat_tbu_x')
                    else:
                        stat_tbu_x = right.text_input('TB/U', value='Tinggi', disabled=True, key='stat_tbu_x')

                    
                    if st.session_state.posisi_x == 'Berdiri':
                        #untuk BB/TB
                        lakibbtb = pd.read_excel('gizi.xlsx', sheet_name='Lakibbtb')

                        # Mendapatkan list tinggi badan yang tersedia
                        tinggi_badan_teravailable = lakibbtb['Tinggi Badan'].unique()

                        # Fungsi untuk melakukan interpolasi
                        def interpolasi_sd_values(tinggi_input):
                            # Urutkan tinggi badan yang tersedia
                            tinggi_badan_teravailable.sort()
                            
                            # Buat interpolator untuk masing-masing kolom SD-3, SD-2, SD+1, SD+2, SD+3
                            interpolator_sd_minus_3 = interp1d(tinggi_badan_teravailable, lakibbtb['SD-3'], kind='linear', fill_value='extrapolate')
                            interpolator_sd_minus_2 = interp1d(tinggi_badan_teravailable, lakibbtb['SD-2'], kind='linear', fill_value='extrapolate')
                            interpolator_sd_plus_1 = interp1d(tinggi_badan_teravailable, lakibbtb['SD+1'], kind='linear', fill_value='extrapolate')
                            interpolator_sd_plus_2 = interp1d(tinggi_badan_teravailable, lakibbtb['SD+2'], kind='linear', fill_value='extrapolate')
                            interpolator_sd_plus_3 = interp1d(tinggi_badan_teravailable, lakibbtb['SD+3'], kind='linear', fill_value='extrapolate')

                            # Menghitung nilai interpolasi berdasarkan tinggi badan input
                            minus_tiga_lbbtb = interpolator_sd_minus_3(tinggi_input)
                            minus_dua_lbbtb = interpolator_sd_minus_2(tinggi_input)
                            plus_satu_lbbtb = interpolator_sd_plus_1(tinggi_input)
                            plus_dua_lbbtb = interpolator_sd_plus_2(tinggi_input)
                            plus_tiga_lbbtb = interpolator_sd_plus_3(tinggi_input)

                            return minus_tiga_lbbtb, minus_dua_lbbtb, plus_satu_lbbtb, plus_dua_lbbtb, plus_tiga_lbbtb
                                # Cek apakah input tinggi badan valid
                        try:
                            tb_x = float(tb_x)
                            bb_x = float(bb_x)

                            # Melakukan interpolasi dan mendapatkan nilai SD untuk tinggi badan yang tidak ada di tabel
                            minus_tiga_lbbtb, minus_dua_lbbtb, plus_satu_lbbtb, plus_dua_lbbtb, plus_tiga_lbbtb = interpolasi_sd_values(tb_x)

                            # Menentukan status BB/TB berdasarkan berat badan yang diinputkan
                            if bb_x < minus_tiga_lbbtb:
                                stat_bbtb_x = right.text_input('BB/TB', value='Gizi Buruk', disabled=True, key='stat_bbtb_x')
                            elif minus_tiga_lbbtb <= bb_x < minus_dua_lbbtb:
                                stat_bbtb_x = right.text_input('BB/TB', value='Gizi Kurang', disabled=True, key='stat_bbtb_x')
                            elif minus_dua_lbbtb <= bb_x <= plus_satu_lbbtb:
                                stat_bbtb_x = right.text_input('BB/TB', value='Normal', disabled=True, key='stat_bbtb_x')
                            elif plus_satu_lbbtb < bb_x <= plus_dua_lbbtb:
                                stat_bbtb_x = right.text_input('BB/TB', value='Berisiko Gizi Lebih', disabled=True, key='stat_bbtb_x')
                            elif plus_dua_lbbtb < bb_x <= plus_tiga_lbbtb:
                                stat_bbtb_x = right.text_input('BB/TB', value='Gizi Lebih', disabled=True, key='stat_bbtb_x')
                            elif bb_x > plus_tiga_lbbtb:
                                stat_bbtb_x = right.text_input('BB/TB', value='Obesitas', disabled=True, key='stat_bbtb_x')
                            else:
                                stat_bbtb_x = right.text_input('BB/TB', value=None, disabled=True, key='stat_bbtb_x')
                        except ValueError:
                            st.error("Input tinggi badan dan berat badan harus berupa angka.")
                            
                    elif st.session_state.posisi_x == 'Terlentang':
                        #untuk BB/PB
                        lakibbpb = pd.read_excel('gizi.xlsx', sheet_name='Lakibbpb')

                        # Mendapatkan list panjang badan yang tersedia
                        panjang_badan_teravailable = lakibbpb['Panjang Badan'].unique()

                        # Fungsi untuk melakukan interpolasi
                        def interpolasi_sd_values(panjang_input):
                            # Urutkan tinggi badan yang tersedia
                            panjang_badan_teravailable.sort()
                            
                            # Buat interpolator untuk masing-masing kolom SD-3, SD-2, SD+1, SD+2, SD+3
                            interpolator_sd_minus_3 = interp1d(panjang_badan_teravailable, lakibbpb['SD-3'], kind='linear', fill_value='extrapolate')
                            interpolator_sd_minus_2 = interp1d(panjang_badan_teravailable, lakibbpb['SD-2'], kind='linear', fill_value='extrapolate')
                            interpolator_sd_plus_1 = interp1d(panjang_badan_teravailable, lakibbpb['SD+1'], kind='linear', fill_value='extrapolate')
                            interpolator_sd_plus_2 = interp1d(panjang_badan_teravailable, lakibbpb['SD+2'], kind='linear', fill_value='extrapolate')
                            interpolator_sd_plus_3 = interp1d(panjang_badan_teravailable, lakibbpb['SD+3'], kind='linear', fill_value='extrapolate')

                            # Menghitung nilai interpolasi berdasarkan tinggi badan input
                            minus_tiga_lbbpb = interpolator_sd_minus_3(panjang_input)
                            minus_dua_lbbpb = interpolator_sd_minus_2(panjang_input)
                            plus_satu_lbbpb = interpolator_sd_plus_1(panjang_input)
                            plus_dua_lbbpb = interpolator_sd_plus_2(panjang_input)
                            plus_tiga_lbbpb = interpolator_sd_plus_3(panjang_input)

                            return minus_tiga_lbbpb, minus_dua_lbbpb, plus_satu_lbbpb, plus_dua_lbbpb, plus_tiga_lbbpb
                                # Cek apakah input tinggi badan valid
                        try:
                            tb_x = float(tb_x)
                            bb_x = float(bb_x)

                            # Melakukan interpolasi dan mendapatkan nilai SD untuk tinggi badan yang tidak ada di tabel
                            minus_tiga_lbbpb, minus_dua_lbbpb, plus_satu_lbbpb, plus_dua_lbbpb, plus_tiga_lbbpb = interpolasi_sd_values(tb_x)

                            # Menentukan status BB/PB berdasarkan berat badan yang diinputkan
                            if bb_x < minus_tiga_lbbpb:
                                stat_bbtb_x = right.text_input('BB/TB', value='Gizi Buruk', disabled=True, key='stat_bbtb_x')
                            elif minus_tiga_lbbpb <= bb_x < minus_dua_lbbpb:
                                stat_bbtb_x = right.text_input('BB/TB', value='Gizi Kurang', disabled=True, key='stat_bbtb_x')
                            elif minus_dua_lbbpb <= bb_x <= plus_satu_lbbpb:
                                stat_bbtb_x = right.text_input('BB/TB', value='Normal', disabled=True, key='stat_bbtb_x')
                            elif plus_satu_lbbpb < bb_x <= plus_dua_lbbpb:
                                stat_bbtb_x = right.text_input('BB/TB', value='Berisiko Gizi Lebih', disabled=True, key='stat_bbtb_x')
                            elif plus_dua_lbbpb < bb_x <= plus_tiga_lbbpb:
                                stat_bbtb_x = right.text_input('BB/TB', value='Gizi Lebih', disabled=True, key='stat_bbtb_x')
                            elif bb_x > plus_tiga_lbbpb:
                                stat_bbtb_x = right.text_input('BB/TB', value='Obesitas', disabled=True, key='stat_bbtb_x')
                            else:
                                stat_bbtb_x = right.text_input('BB/TB', value=None, disabled=True, key='stat_bbtb_x')
                        except ValueError:
                            st.error("Input tinggi badan dan berat badan harus berupa angka.")
                    
                    #untuk IMT/U
                    lakiimtu = pd.read_excel('gizi.xlsx', sheet_name='Lakiimtu')

                    data_lakiimtu = lakiimtu[lakiimtu['Usia'] == int(usia_bln)].index

                    if len(data_lakiimtu) > 0:
                        r = lakiimtu.iloc[data_lakiimtu]
                        try:
                            minus_tiga_limtu = r['SD-3'].values[0]
                            minus_dua_limtu = r['SD-2'].values[0]
                            plus_satu_limtu = r['SD+1'].values[0]
                            plus_dua_limtu = r['SD+2'].values[0]
                            plus_tiga_limtu = r['SD+3'].values[0]

                            if float(bmi_x) < minus_tiga_limtu:
                                stat_imtu_x = right.text_input('IMT/U', value='Gizi Buruk', disabled=True, key='stat_imtu_x')
                            elif minus_tiga_limtu <= float(bmi_x) < minus_dua_limtu:
                                stat_imtu_x = right.text_input('IMT/U', value='Gizi Kurang', disabled=True, key='stat_imtu_x')
                            elif minus_dua_limtu <= float(bmi_x) <= plus_satu_limtu:
                                stat_imtu_x = right.text_input('IMT/U', value='Normal', disabled=True, key='stat_imtu_x')
                            elif plus_satu_limtu < float(bmi_x) <= plus_dua_limtu:
                                stat_imtu_x = right.text_input('IMT/U', value='Berisiko Gizi Lebih', disabled=True, key='stat_imtu_x')
                            elif plus_dua_limtu < float(bmi_x) <= plus_tiga_limtu:
                                stat_imtu_x = right.text_input('IMT/U', value='Gizi Lebih', disabled=True, key='stat_imtu_x')
                            else:
                                stat_imtu_x = right.text_input('IMT/U', value='Obesitas', disabled=True, key='stat_imtu_x')

                        except IndexError:
                            stat_imtu_x = right.text_input('IMT/U', value=None, disabled=True, key='stat_imtu_x')
                    else:
                        stat_imtu_x = st.text_input('IMT/U', value=None, disabled=True, key='stat_imtu_x')
                        
                        
                    #untuk LK/U
                    lakilku = pd.read_excel('gizi.xlsx', sheet_name='Lakilku')

                    data_lakilku = lakilku[lakilku['Usia'] == int(usia_bln)].index

                    if len(data_lakilku) > 0:
                        s = lakilku.iloc[data_lakilku]
                        try:
                            minus_dua_llku = s['SD-2'].values[0]
                            plus_dua_llku = s['SD+2'].values[0]

                            if float(lk_x) < minus_dua_llku:
                                stat_lku_x = right.text_input('LK/U', value='Mikrosefali', disabled=True, key='stat_lku_x')
                            elif minus_dua_llku <= float(lk_x) <= plus_dua_llku:
                                stat_lku_x = right.text_input('LK/U', value='Normosefali', disabled=True, key='stat_lku_x')
                            else:
                                stat_lku_x = right.text_input('LK/U', value='Makrosefali', disabled=True, key='stat_lku_x')

                        except IndexError:
                            stat_lku_x = right.text_input('LK/U', value=None, disabled=True, key='stat_lku_x')
                    else:
                        stat_lku_x = right.text_input('LK/U', value=None, disabled=True, key='stat_lku_x')
                    
                elif 60 < usia_bln <= 72:
                    stat_bbu_x = right.text_input('BB/U', value=None, disabled=True, key='stat_bbu_x')
                    stat_tbu_x = right.text_input('TB/U', value=None, disabled=True, key='stat_tbu_x')
                    stat_bbtb_x = right.text_input('BB/TB', value=None, disabled=True, key='stat_bbtb_x')
                    
                    lakiimtu = pd.read_excel('gizi.xlsx', sheet_name='Lakiimtu')

                    data_lakiimtu = lakiimtu[lakiimtu['Usia'] == int(usia_bln)].index

                    if len(data_lakiimtu) > 0:
                        r = lakiimtu.iloc[data_lakiimtu]
                        try:
                            minus_tiga_limtu = r['SD-3'].values[0]
                            minus_dua_limtu = r['SD-2'].values[0]
                            plus_satu_limtu = r['SD+1'].values[0]
                            plus_dua_limtu = r['SD+2'].values[0]
                            plus_tiga_limtu = r['SD+3'].values[0]

                            if float(bmi_x) < minus_tiga_limtu:
                                stat_imtu_x = right.text_input('IMT/U', value='Gizi Buruk', disabled=True, key='stat_imtu_x')
                            elif minus_tiga_limtu <= float(bmi_x) < minus_dua_limtu:
                                stat_imtu_x = right.text_input('IMT/U', value='Gizi Kurang', disabled=True, key='stat_imtu_x')
                            elif minus_dua_limtu <= float(bmi_x) <= plus_satu_limtu:
                                stat_imtu_x = right.text_input('IMT/U', value='Normal', disabled=True, key='stat_imtu_x')
                            elif plus_satu_limtu < float(bmi_x) <= plus_dua_limtu:
                                stat_imtu_x = right.text_input('IMT/U', value='Berisiko Gizi Lebih', disabled=True, key='stat_imtu_x')
                            elif plus_dua_limtu < float(bmi_x) <= plus_tiga_limtu:
                                stat_imtu_x = right.text_input('IMT/U', value='Gizi Lebih', disabled=True, key='stat_imtu_x')
                            else:
                                stat_imtu_x = right.text_input('IMT/U', value='Obesitas', disabled=True, key='stat_imtu_x')

                        except IndexError:
                            stat_imtu_x = right.text_input('IMT/U', value=None, disabled=True, key='stat_imtu_x')
                    else:
                        stat_imtu_x = right.text_input('IMT/U', value=None, disabled=True, key='stat_imtu_x')
                
                    stat_lku_x = right.text_input('LK/U', value=None, disabled=True, key='stat_lku_x')
                    
                else:
                    stat_bbu_x = right.text_input('BB/U', value=None, disabled=True, key='stat_bbu_x')
                    stat_tbu_x = right.text_input('TB/U', value=None, disabled=True, key='stat_tbu_x')
                    stat_bbtb_x = right.text_input('BB/TB', value=None, disabled=True, key='stat_bbtb_x')
                    stat_imtu_x = right.text_input('IMT/U', value=None, disabled=True, key='stat_imtu_x')
                    stat_lku_x = right.text_input('LK/U', value=None, disabled=True, key='stat_lku_x')

                
                    
            elif st.session_state.jk_x == 'Perempuan':
            
                if 0 <= usia_bln <= 60:
                    #untuk BB/U
                    prbbu = pd.read_excel('gizi.xlsx', sheet_name='Prbbu')

                    data_prbbu = prbbu[prbbu['Usia'] == int(usia_bln)].index
                    

                    x = prbbu.iloc[data_prbbu]
                    
                    minus_tiga_pbbu = x['SD-3'].values[0]
                    minus_dua_pbbu = x['SD-2'].values[0]
                    plus_satu_pbbu = x['SD+1'].values[0]
                    
                    if float(bb_x) < minus_tiga_pbbu:
                        stat_bbu_x= right.text_input('BB/U', value='Berat Badan Sangat Kurang', disabled=True, key='stat_bbu_x')
                    elif minus_tiga_pbbu <= float(bb_x) < minus_dua_pbbu:
                        stat_bbu_x= right.text_input('BB/U', value='Berat Badan Kurang', disabled=True, key='stat_bbu_x')
                    elif minus_dua_pbbu <= float(bb_x) <= plus_satu_pbbu:
                        stat_bbu_x= right.text_input('BB/U', value='Berat Badan Normal', disabled=True, key='stat_bbu_x')
                    else:
                        stat_bbu_x= right.text_input('BB/U', value='Berat Badan Lebih', disabled=True, key='stat_bbu_x')

                    #untuk TB/U
                    prtbu = pd.read_excel('gizi.xlsx', sheet_name='Prtbu')

                    data_prtbu = prtbu[prtbu['Usia'] == int(usia_bln)].index

                    y = prtbu.iloc[data_prtbu]
                    minus_tiga_ptbu = y['SD-3'].values[0]
                    minus_dua_ptbu = y['SD-2'].values[0]
                    plus_satu_ptbu = y['SD+1'].values[0]
                    

                    if float(tb_x) < minus_tiga_ptbu :
                        stat_tbu_x= right.text_input('TB/U', value='Sangat Pendek', disabled=True, key='stat_tbu_x')
                    elif minus_tiga_ptbu <= float(tb_x) < minus_dua_ptbu:
                        stat_tbu_x=right.text_input('TB/U', value='Pendek', disabled=True, key='stat_tbu_x')
                    elif minus_dua_ptbu <= float(tb_x) <= plus_satu_ptbu:
                        stat_tbu_x= right.text_input('TB/U', value='Tinggi Badan Normal', disabled=True, key='stat_tbu_x')
                    else:
                        stat_tbu_x= right.text_input('TB/U', value='Tinggi', disabled=True, key='stat_tbu_x')



                    if st.session_state.posisi_x == 'Berdiri':
                        #untuk BB/TB
                        prbbtb = pd.read_excel('gizi.xlsx', sheet_name='Prbbtb')

                        # Mendapatkan list tinggi badan yang tersedia
                        tinggi_badan_teravailable = prbbtb['Tinggi Badan'].unique()

                        # Fungsi untuk melakukan interpolasi
                        def interpolasi_sd_values(tinggi_input):
                            # Urutkan tinggi badan yang tersedia
                            tinggi_badan_teravailable.sort()
                            
                            # Buat interpolator untuk masing-masing kolom SD-3, SD-2, SD+1, SD+2, SD+3
                            interpolator_sd_minus_3 = interp1d(tinggi_badan_teravailable, prbbtb['SD-3'], kind='linear', fill_value='extrapolate')
                            interpolator_sd_minus_2 = interp1d(tinggi_badan_teravailable, prbbtb['SD-2'], kind='linear', fill_value='extrapolate')
                            interpolator_sd_plus_1 = interp1d(tinggi_badan_teravailable, prbbtb['SD+1'], kind='linear', fill_value='extrapolate')
                            interpolator_sd_plus_2 = interp1d(tinggi_badan_teravailable, prbbtb['SD+2'], kind='linear', fill_value='extrapolate')
                            interpolator_sd_plus_3 = interp1d(tinggi_badan_teravailable, prbbtb['SD+3'], kind='linear', fill_value='extrapolate')

                            # Menghitung nilai interpolasi berdasarkan tinggi badan input
                            minus_tiga_pbbtb = interpolator_sd_minus_3(tinggi_input)
                            minus_dua_pbbtb = interpolator_sd_minus_2(tinggi_input)
                            plus_satu_pbbtb = interpolator_sd_plus_1(tinggi_input)
                            plus_dua_pbbtb = interpolator_sd_plus_2(tinggi_input)
                            plus_tiga_pbbtb = interpolator_sd_plus_3(tinggi_input)

                            return minus_tiga_pbbtb, minus_dua_pbbtb, plus_satu_pbbtb, plus_dua_pbbtb, plus_tiga_pbbtb
                                # Cek apakah input tinggi badan valid
                        try:
                            tb_x = float(tb_x)
                            bb_x = float(bb_x)

                            # Melakukan interpolasi dan mendapatkan nilai SD untuk tinggi badan yang tidak ada di tabel
                            minus_tiga_pbbtb, minus_dua_pbbtb, plus_satu_pbbtb, plus_dua_pbbtb, plus_tiga_pbbtb = interpolasi_sd_values(tb_x)

                            # Menentukan status BB/TB berdasarkan berat badan yang diinputkan
                            if bb_x < minus_tiga_pbbtb:
                                stat_bbtb_x = right.text_input('BB/TB', value='Gizi Buruk', disabled=True, key='stat_bbtb_x')
                            elif minus_tiga_pbbtb <= bb_x < minus_dua_pbbtb:
                                stat_bbtb_x = right.text_input('BB/TB', value='Gizi Kurang', disabled=True, key='stat_bbtb_x')
                            elif minus_dua_pbbtb <= bb_x <= plus_satu_pbbtb:
                                stat_bbtb_x = right.text_input('BB/TB', value='Normal', disabled=True, key='stat_bbtb_x')
                            elif plus_satu_pbbtb < bb_x <= plus_dua_pbbtb:
                                stat_bbtb_x = right.text_input('BB/TB', value='Berisiko Gizi Lebih', disabled=True, key='stat_bbtb_x')
                            elif plus_dua_pbbtb < bb_x <= plus_tiga_pbbtb:
                                stat_bbtb_x = right.text_input('BB/TB', value='Gizi Lebih', disabled=True, key='stat_bbtb_x')
                            elif bb_x > plus_tiga_pbbtb:
                                stat_bbtb_x = right.text_input('BB/TB', value='Obesitas', disabled=True, key='stat_bbtb_x')
                            else:
                                stat_bbtb_x = right.text_input('BB/TB', value=None, disabled=True, key='stat_bbtb_x')
                        except ValueError:
                            st.error("Input tinggi badan dan berat badan harus berupa angka.")
                            
                    elif st.session_state.posisi_x == 'Terlentang':
                        #untuk BB/PB
                        prbbpb = pd.read_excel('gizi.xlsx', sheet_name='Prbbpb')

                        # Mendapatkan list panjang badan yang tersedia
                        panjang_badan_teravailable = prbbpb['Panjang Badan'].unique()

                        # Fungsi untuk melakukan interpolasi
                        def interpolasi_sd_values(panjang_input):
                            # Urutkan tinggi badan yang tersedia
                            panjang_badan_teravailable.sort()
                            
                            # Buat interpolator untuk masing-masing kolom SD-3, SD-2, SD+1, SD+2, SD+3
                            interpolator_sd_minus_3 = interp1d(panjang_badan_teravailable, prbbpb['SD-3'], kind='linear', fill_value='extrapolate')
                            interpolator_sd_minus_2 = interp1d(panjang_badan_teravailable, prbbpb['SD-2'], kind='linear', fill_value='extrapolate')
                            interpolator_sd_plus_1 = interp1d(panjang_badan_teravailable, prbbpb['SD+1'], kind='linear', fill_value='extrapolate')
                            interpolator_sd_plus_2 = interp1d(panjang_badan_teravailable, prbbpb['SD+2'], kind='linear', fill_value='extrapolate')
                            interpolator_sd_plus_3 = interp1d(panjang_badan_teravailable, prbbpb['SD+3'], kind='linear', fill_value='extrapolate')

                            # Menghitung nilai interpolasi berdasarkan tinggi badan input
                            minus_tiga_pbbpb = interpolator_sd_minus_3(panjang_input)
                            minus_dua_pbbpb = interpolator_sd_minus_2(panjang_input)
                            plus_satu_pbbpb = interpolator_sd_plus_1(panjang_input)
                            plus_dua_pbbpb = interpolator_sd_plus_2(panjang_input)
                            plus_tiga_pbbpb = interpolator_sd_plus_3(panjang_input)

                            return minus_tiga_pbbpb, minus_dua_pbbpb, plus_satu_pbbpb, plus_dua_pbbpb, plus_tiga_pbbpb
                                # Cek apakah input tinggi badan valid
                        try:
                            tb_x = float(tb_x)
                            bb_x = float(bb_x)

                            # Melakukan interpolasi dan mendapatkan nilai SD untuk tinggi badan yang tidak ada di tabel
                            minus_tiga_pbbpb, minus_dua_pbbpb, plus_satu_pbbpb, plus_dua_pbbpb, plus_tiga_pbbpb = interpolasi_sd_values(tb_x)

                            # Menentukan status BB/PB berdasarkan berat badan yang diinputkan
                            if bb_x < minus_tiga_pbbpb:
                                stat_bbtb_x = right.text_input('BB/TB', value='Gizi Buruk', disabled=True, key='stat_bbtb_x')
                            elif minus_tiga_pbbpb <= bb_x < minus_dua_pbbpb:
                                stat_bbtb_x = right.text_input('BB/TB', value='Gizi Kurang', disabled=True, key='stat_bbtb_x')
                            elif minus_dua_pbbpb <= bb_x <= plus_satu_pbbpb:
                                stat_bbtb_x = right.text_input('BB/TB', value='Normal', disabled=True, key='stat_bbtb_x')
                            elif plus_satu_pbbpb < bb_x <= plus_dua_pbbpb:
                                stat_bbtb_x = right.text_input('BB/TB', value='Berisiko Gizi Lebih', disabled=True, key='stat_bbtb_x')
                            elif plus_dua_pbbpb < bb_x <= plus_tiga_pbbpb:
                                stat_bbtb_x = right.text_input('BB/TB', value='Gizi Lebih', disabled=True, key='stat_bbtb_x')
                            elif bb_x > plus_tiga_pbbpb:
                                stat_bbtb_x = right.text_input('BB/TB', value='Obesitas', disabled=True, key='stat_bbtb_x')
                            else:
                                stat_bbtb_x = right.text_input('BB/TB', value=None, disabled=True, key='stat_bbtb_x')
                        except ValueError:
                            st.error("Input tinggi badan dan berat badan harus berupa angka.")

                    #untuk IMT/U
                    primtu = pd.read_excel('gizi.xlsx', sheet_name='Primtu')

                    data_primtu = primtu[primtu['Usia'] == int(usia_bln)].index

                    if len(data_primtu) > 0:
                        r = primtu.iloc[data_primtu]
                        try:
                            minus_tiga_pimtu = r['SD-3'].values[0]
                            minus_dua_pimtu = r['SD-2'].values[0]
                            plus_satu_pimtu = r['SD+1'].values[0]
                            plus_dua_pimtu = r['SD+2'].values[0]
                            plus_tiga_pimtu = r['SD+3'].values[0]

                            if float(bmi_x) < minus_tiga_pimtu:
                                stat_imtu_x = right.text_input('IMT/U', value='Gizi Buruk', disabled=True, key='stat_imtu_x')
                            elif minus_tiga_pimtu <= float(bmi_x) < minus_dua_pimtu:
                                stat_imtu_x = right.text_input('IMT/U', value='Gizi Kurang', disabled=True, key='stat_imtu_x')
                            elif minus_dua_pimtu <= float(bmi_x) <= plus_satu_pimtu:
                                stat_imtu_x = right.text_input('IMT/U', value='Normal', disabled=True, key='stat_imtu_x')
                            elif plus_satu_pimtu < float(bmi_x) <= plus_dua_pimtu:
                                stat_imtu_x = right.text_input('IMT/U', value='Berisiko Gizi Lebih', disabled=True, key='stat_imtu_x')
                            elif plus_dua_pimtu < float(bmi_x) <= plus_tiga_pimtu:
                                stat_imtu_x = right.text_input('IMT/U', value='Gizi Lebih', disabled=True, key='stat_imtu_x')
                            else:
                                stat_imtu_x = right.text_input('IMT/U', value='Obesitas', disabled=True, key='stat_imtu_x')

                        except IndexError:
                            stat_imtu_x = right.text_input('IMT/U', value=None, disabled=True, key='stat_imtu_x')
                    else:
                        stat_imtu_x = right.text_input('IMT/U', value=None, disabled=True, key='stat_imtu_x')
                    
                    
                    #untuk LK/U
                    prlku = pd.read_excel('gizi.xlsx', sheet_name='Prlku')

                    data_prlku = prlku[prlku['Usia'] == int(usia_bln)].index

                    if len(data_prlku) > 0:
                        s = prlku.iloc[data_prlku]
                        try:
                            minus_dua_plku = s['SD-2'].values[0]
                            plus_dua_plku = s['SD+2'].values[0]

                            if float(lk_x) < minus_dua_plku:
                                stat_lku_x = right.text_input('LK/U', value='Mikrosefali', disabled=True, key='stat_lku_x')
                            elif minus_dua_plku <= float(lk_x) <= plus_dua_plku:
                                stat_lku_x = right.text_input('LK/U', value='Normosefali', disabled=True, key='stat_lku_x')
                            else:
                                stat_lku_x = right.text_input('LK/U', value='Makrosefali', disabled=True, key='stat_lku_x')

                        except IndexError:
                            stat_lku_x = right.text_input('LK/U', value=None, disabled=True, key='stat_lku_x')
                    else:
                        stat_lku_x = right.text_input('LK/U', value=None, disabled=True, key='stat_lku_x')
        
                elif 60 < usia_bln <= 72:
                    stat_bbu_x = right.text_input('BB/U', value=None, disabled=True, key='stat_bbu_x')
                    stat_tbu_x = right.text_input('TB/U', value=None, disabled=True, key='stat_tbu_x')
                    stat_bbtb_x = right.text_input('BB/TB', value=None, disabled=True, key='stat_bbtb_x')
                    primtu = pd.read_excel('gizi.xlsx', sheet_name='Primtu')

                    data_primtu = primtu[primtu['Usia'] == int(usia_bln)].index

                    if len(data_primtu) > 0:
                        r = primtu.iloc[data_primtu]
                        try:
                            minus_tiga_pimtu = r['SD-3'].values[0]
                            minus_dua_pimtu = r['SD-2'].values[0]
                            plus_satu_pimtu = r['SD+1'].values[0]
                            plus_dua_pimtu = r['SD+2'].values[0]
                            plus_tiga_pimtu = r['SD+3'].values[0]

                            if float(bmi_x) < minus_tiga_pimtu:
                                stat_imtu_x = right.text_input('IMT/U', value='Gizi Buruk', disabled=True, key='stat_imtu_x')
                            elif minus_tiga_pimtu <= float(bmi_x) < minus_dua_pimtu:
                                stat_imtu_x = right.text_input('IMT/U', value='Gizi Kurang', disabled=True, key='stat_imtu_x')
                            elif minus_dua_pimtu <= float(bmi_x) <= plus_satu_pimtu:
                                stat_imtu_x = right.text_input('IMT/U', value='Normal', disabled=True, key='stat_imtu_x')
                            elif plus_satu_pimtu < float(bmi_x) <= plus_dua_pimtu:
                                stat_imtu_x = right.text_input('IMT/U', value='Berisiko Gizi Lebih', disabled=True, key='stat_imtu_x')
                            elif plus_dua_pimtu < float(bmi_x) <= plus_tiga_pimtu:
                                stat_imtu_x = right.text_input('IMT/U', value='Gizi Lebih', disabled=True, key='stat_imtu_x')
                            else:
                                stat_imtu_x = right.text_input('IMT/U', value='Obesitas', disabled=True, key='stat_imtu_x')

                        except IndexError:
                            stat_imtu_x = right.text_input('IMT/U', value=None, disabled=True, key='stat_imtu_x')
                    else:
                        stat_imtu_x = right.text_input('IMT/U', value=None, disabled=True, key='stat_imtu_x')
                    
                    stat_lku_x = right.text_input('LK/U', value=None, disabled=True, key='stat_lku_x')
                    
                else:
                    stat_bbu_x = right.text_input('BB/U', value=None, disabled=True, key='stat_bbu_x')
                    stat_tbu_x = right.text_input('TB/U', value=None, disabled=True, key='stat_tbu_x')
                    stat_bbtb_x = right.text_input('BB/TB', value=None, disabled=True, key='stat_bbtb_x')
                    stat_imtu_x = right.text_input('IMT/U', value=None, disabled=True, key='stat_imtu_x')
                    stat_lku_x = right.text_input('LK/U', value=None, disabled=True, key='stat_lku_x')
            
        with st.expander('**SKRINING PERKEMBANGAN**'):
            if 3 <= usia_bln < 6: 
                st.write('### KPSP Umur 3 bulan')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Menentukan lebar kolom (3 bagian untuk caption, 1 bagian untuk opsi)

                with col1:
                    st.image('.img/3_1.png')
                with col2:
                    st.empty()
                    kpsp1_value = st.session_state.input_data.get('KPSP1', '')
                    if pd.isna(kpsp1_value):
                        kpsp1_x = st.radio('kpsp1', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp1_x', label_visibility='collapsed')
                    else:
                        kpsp1_x = st.radio('kpsp1', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp1_value), horizontal=True, key='kpsp1_x', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/3_2.png')
                with col2:
                    st.empty()
                    kpsp2_value = st.session_state.input_data.get('KPSP2', '')
                    if pd.isna(kpsp1_value):
                        kpsp2_x = st.radio('kpsp2', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp2_x', label_visibility='collapsed')
                    else:
                        kpsp2_x = st.radio('kpsp2', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp2_value), horizontal=True, key='kpsp2_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/3_3.png')
                with col2:
                    st.empty()
                    kpsp3_value = st.session_state.input_data.get('KPSP3', '')
                    if pd.isna(kpsp1_value):
                        kpsp3_x = st.radio('kpsp3', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp3_x', label_visibility='collapsed')
                    else:
                        kpsp3_x = st.radio('kpsp3', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp3_value), horizontal=True, key='kpsp3_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/3_4.png')
                with col2:
                    st.empty()
                    kpsp4_value = st.session_state.input_data.get('KPSP4', '')
                    if pd.isna(kpsp4_value):
                        kpsp4_x = st.radio('kpsp4', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp4_x', label_visibility='collapsed')
                    else:
                        kpsp4_x = st.radio('kpsp4', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp4_value), horizontal=True, key='kpsp4_x', label_visibility='collapsed')
                
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/3_5.png')
                with col2:
                    st.empty()
                    kpsp5_value = st.session_state.input_data.get('KPSP5', '')
                    if pd.isna(kpsp5_value):
                        kpsp5_x = st.radio('kpsp5', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp5_x', label_visibility='collapsed')
                    else:
                        kpsp5_x = st.radio('kpsp5', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp5_value), horizontal=True, key='kpsp5_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/3_6.png')
                with col2:
                    st.empty()
                    kpsp6_value = st.session_state.input_data.get('KPSP6', '')
                    if pd.isna(kpsp6_value):
                        kpsp6_x = st.radio('kpsp6', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp6_x', label_visibility='collapsed')
                    else:
                        kpsp6_x = st.radio('kpsp6', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp6_value), horizontal=True, key='kpsp6_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/3_7.png')
                with col2:
                    st.empty()
                    kpsp7_value = st.session_state.input_data.get('KPSP7', '')
                    if pd.isna(kpsp7_value):
                        kpsp7_x = st.radio('kpsp7', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp7_x', label_visibility='collapsed')
                    else:
                        kpsp7_x = st.radio('kpsp7', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp7_value), horizontal=True, key='kpsp7_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/3_8.png')
                with col2:
                    st.empty()
                    kpsp8_value = st.session_state.input_data.get('KPSP8', '')
                    if pd.isna(kpsp8_value):
                        kpsp8_x = st.radio('kpsp8', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp8_x', label_visibility='collapsed')
                    else:
                        kpsp8_x = st.radio('kpsp8', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp8_value), horizontal=True, key='kpsp8_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/3_9.png')
                with col2:
                    st.empty()
                    kpsp9_value = st.session_state.input_data.get('KPSP9', '')
                    if pd.isna(kpsp9_value):
                        kpsp9_x = st.radio('kpsp9', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp9_x', label_visibility='collapsed')
                    else:
                        kpsp9_x = st.radio('kpsp9', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp9_value), horizontal=True, key='kpsp9_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/3_10.png')
                with col2:
                    st.empty()
                    kpsp10_value = st.session_state.input_data.get('KPSP10', '')
                    if pd.isna(kpsp10_value):
                        kpsp10_x = st.radio('kpsp10', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp10_x', label_visibility='collapsed')
                    else:
                        kpsp10_x = st.radio('kpsp10', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp10_value), horizontal=True, key='kpsp10_x', label_visibility='collapsed')



            elif 6 <= usia_bln < 9:

                st.write('### KPSP Umur 6 bulan')

                # Membuat kolom untuk menempatkan caption di kiri dan opsi di kanan
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Menentukan lebar kolom (3 bagian untuk caption, 1 bagian untuk opsi)

                with col1:
                    st.image('.img/6_1.png')
                with col2:
                    st.empty()
                    kpsp1_value = st.session_state.input_data.get('KPSP1', '')
                    if pd.isna(kpsp1_value):
                        kpsp1_x = st.radio('kpsp1', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp1_x', label_visibility='collapsed')
                    else:
                        kpsp1_x = st.radio('kpsp1', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp1_value), horizontal=True, key='kpsp1_x', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/6_2.png')
                with col2:
                    st.empty()
                    kpsp2_value = st.session_state.input_data.get('KPSP2', '')
                    if pd.isna(kpsp1_value):
                        kpsp2_x = st.radio('kpsp2', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp2_x', label_visibility='collapsed')
                    else:
                        kpsp2_x = st.radio('kpsp2', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp2_value), horizontal=True, key='kpsp2_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/6_3.png')
                with col2:
                    st.empty()
                    kpsp3_value = st.session_state.input_data.get('KPSP3', '')
                    if pd.isna(kpsp1_value):
                        kpsp3_x = st.radio('kpsp3', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp3_x', label_visibility='collapsed')
                    else:
                        kpsp3_x = st.radio('kpsp3', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp3_value), horizontal=True, key='kpsp3_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/6_4.png')
                with col2:
                    st.empty()
                    kpsp4_value = st.session_state.input_data.get('KPSP4', '')
                    if pd.isna(kpsp4_value):
                        kpsp4_x = st.radio('kpsp4', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp4_x', label_visibility='collapsed')
                    else:
                        kpsp4_x = st.radio('kpsp4', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp4_value), horizontal=True, key='kpsp4_x', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/6_5.png')
                with col2:
                    st.empty()
                    kpsp5_value = st.session_state.input_data.get('KPSP5', '')
                    if pd.isna(kpsp5_value):
                        kpsp5_x = st.radio('kpsp5', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp5_x', label_visibility='collapsed')
                    else:
                        kpsp5_x = st.radio('kpsp5', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp5_value), horizontal=True, key='kpsp5_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/6_6.png')
                with col2:
                    st.empty()
                    kpsp6_value = st.session_state.input_data.get('KPSP6', '')
                    if pd.isna(kpsp6_value):
                        kpsp6_x = st.radio('kpsp6', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp6_x', label_visibility='collapsed')
                    else:
                        kpsp6_x = st.radio('kpsp6', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp6_value), horizontal=True, key='kpsp6_x', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/6_7.png')
                with col2:
                    st.empty()
                    kpsp7_value = st.session_state.input_data.get('KPSP7', '')
                    if pd.isna(kpsp7_value):
                        kpsp7_x = st.radio('kpsp7', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp7_x', label_visibility='collapsed')
                    else:
                        kpsp7_x = st.radio('kpsp7', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp7_value), horizontal=True, key='kpsp7_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/6_8.png')
                with col2:
                    st.empty()
                    kpsp8_value = st.session_state.input_data.get('KPSP8', '')
                    if pd.isna(kpsp8_value):
                        kpsp8_x = st.radio('kpsp8', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp8_x', label_visibility='collapsed')
                    else:
                        kpsp8_x = st.radio('kpsp8', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp8_value), horizontal=True, key='kpsp8_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/6_9.png')
                with col2:
                    st.empty()
                    kpsp9_value = st.session_state.input_data.get('KPSP9', '')
                    if pd.isna(kpsp9_value):
                        kpsp9_x = st.radio('kpsp9', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp9_x', label_visibility='collapsed')
                    else:
                        kpsp9_x = st.radio('kpsp9', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp9_value), horizontal=True, key='kpsp9_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/6_10.png')
                with col2:
                    st.empty()
                    kpsp10_value = st.session_state.input_data.get('KPSP10', '')
                    if pd.isna(kpsp10_value):
                        kpsp10_x = st.radio('kpsp10', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp10_x', label_visibility='collapsed')
                    else:
                        kpsp10_x = st.radio('kpsp10', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp10_value), horizontal=True, key='kpsp10_x', label_visibility='collapsed')
                    
            elif 9 <= usia_bln < 12:

                st.write('### KPSP Umur 9 bulan')

                # Membuat kolom untuk menempatkan caption di kiri dan opsi di kanan
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Menentukan lebar kolom (3 bagian untuk caption, 1 bagian untuk opsi)

                with col1:
                    st.image('.img/9_1.png')
                with col2:
                    st.empty()
                    kpsp1_value = st.session_state.input_data.get('KPSP1', '')
                    if pd.isna(kpsp1_value):
                        kpsp1_x = st.radio('kpsp1', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp1_x', label_visibility='collapsed')
                    else:
                        kpsp1_x = st.radio('kpsp1', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp1_value), horizontal=True, key='kpsp1_x', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/9_2.png')
                with col2:
                    st.empty()
                    kpsp2_value = st.session_state.input_data.get('KPSP2', '')
                    if pd.isna(kpsp1_value):
                        kpsp2_x = st.radio('kpsp2', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp2_x', label_visibility='collapsed')
                    else:
                        kpsp2_x = st.radio('kpsp2', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp2_value), horizontal=True, key='kpsp2_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/9_3.png')
                with col2:
                    st.empty()
                    kpsp3_value = st.session_state.input_data.get('KPSP3', '')
                    if pd.isna(kpsp1_value):
                        kpsp3_x = st.radio('kpsp3', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp3_x', label_visibility='collapsed')
                    else:
                        kpsp3_x = st.radio('kpsp3', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp3_value), horizontal=True, key='kpsp3_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/9_4.png')
                with col2:
                    st.empty()
                    kpsp4_value = st.session_state.input_data.get('KPSP4', '')
                    if pd.isna(kpsp4_value):
                        kpsp4_x = st.radio('kpsp4', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp4_x', label_visibility='collapsed')
                    else:
                        kpsp4_x = st.radio('kpsp4', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp4_value), horizontal=True, key='kpsp4_x', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/9_5.png')
                with col2:
                    st.empty()
                    kpsp5_value = st.session_state.input_data.get('KPSP5', '')
                    if pd.isna(kpsp5_value):
                        kpsp5_x = st.radio('kpsp5', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp5_x', label_visibility='collapsed')
                    else:
                        kpsp5_x = st.radio('kpsp5', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp5_value), horizontal=True, key='kpsp5_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/9_6.png')
                with col2:
                    st.empty()
                    kpsp6_value = st.session_state.input_data.get('KPSP6', '')
                    if pd.isna(kpsp6_value):
                        kpsp6_x = st.radio('kpsp6', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp6_x', label_visibility='collapsed')
                    else:
                        kpsp6_x = st.radio('kpsp6', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp6_value), horizontal=True, key='kpsp6_x', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/9_7.png')
                with col2:
                    st.empty()
                    kpsp7_value = st.session_state.input_data.get('KPSP7', '')
                    if pd.isna(kpsp7_value):
                        kpsp7_x = st.radio('kpsp7', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp7_x', label_visibility='collapsed')
                    else:
                        kpsp7_x = st.radio('kpsp7', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp7_value), horizontal=True, key='kpsp7_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/9_8.png')
                with col2:
                    st.empty()
                    kpsp8_value = st.session_state.input_data.get('KPSP8', '')
                    if pd.isna(kpsp8_value):
                        kpsp8_x = st.radio('kpsp8', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp8_x', label_visibility='collapsed')
                    else:
                        kpsp8_x = st.radio('kpsp8', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp8_value), horizontal=True, key='kpsp8_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/9_9.png')
                with col2:
                    st.empty()
                    kpsp9_value = st.session_state.input_data.get('KPSP9', '')
                    if pd.isna(kpsp9_value):
                        kpsp9_x = st.radio('kpsp9', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp9_x', label_visibility='collapsed')
                    else:
                        kpsp9_x = st.radio('kpsp9', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp9_value), horizontal=True, key='kpsp9_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/9_10.png')
                with col2:
                    st.empty()
                    kpsp10_value = st.session_state.input_data.get('KPSP10', '')
                    if pd.isna(kpsp10_value):
                        kpsp10_x = st.radio('kpsp10', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp10_x', label_visibility='collapsed')
                    else:
                        kpsp10_x = st.radio('kpsp10', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp10_value), horizontal=True, key='kpsp10_x', label_visibility='collapsed')
                    
            elif 12 <= usia_bln < 15:

                st.write('### KPSP Umur 12 bulan')

                # Membuat kolom untuk menempatkan caption di kiri dan opsi di kanan
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Menentukan lebar kolom (3 bagian untuk caption, 1 bagian untuk opsi)

                with col1:
                    st.image('.img/12_1.png')
                with col2:
                    st.empty()
                    kpsp1_value = st.session_state.input_data.get('KPSP1', '')
                    if pd.isna(kpsp1_value):
                        kpsp1_x = st.radio('kpsp1', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp1_x', label_visibility='collapsed')
                    else:
                        kpsp1_x = st.radio('kpsp1', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp1_value), horizontal=True, key='kpsp1_x', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/12_2.png')
                with col2:
                    st.empty()
                    kpsp2_value = st.session_state.input_data.get('KPSP2', '')
                    if pd.isna(kpsp1_value):
                        kpsp2_x = st.radio('kpsp2', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp2_x', label_visibility='collapsed')
                    else:
                        kpsp2_x = st.radio('kpsp2', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp2_value), horizontal=True, key='kpsp2_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/12_3.png')
                with col2:
                    st.empty()
                    kpsp3_value = st.session_state.input_data.get('KPSP3', '')
                    if pd.isna(kpsp1_value):
                        kpsp3_x = st.radio('kpsp3', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp3_x', label_visibility='collapsed')
                    else:
                        kpsp3_x = st.radio('kpsp3', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp3_value), horizontal=True, key='kpsp3_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/12_4.png')
                with col2:
                    st.empty()
                    kpsp4_value = st.session_state.input_data.get('KPSP4', '')
                    if pd.isna(kpsp4_value):
                        kpsp4_x = st.radio('kpsp4', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp4_x', label_visibility='collapsed')
                    else:
                        kpsp4_x = st.radio('kpsp4', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp4_value), horizontal=True, key='kpsp4_x', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/12_5.png')
                with col2:
                    st.empty()
                    kpsp5_value = st.session_state.input_data.get('KPSP5', '')
                    if pd.isna(kpsp5_value):
                        kpsp5_x = st.radio('kpsp5', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp5_x', label_visibility='collapsed')
                    else:
                        kpsp5_x = st.radio('kpsp5', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp5_value), horizontal=True, key='kpsp5_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/12_6.png')
                with col2:
                    st.empty()
                    kpsp6_value = st.session_state.input_data.get('KPSP6', '')
                    if pd.isna(kpsp6_value):
                        kpsp6_x = st.radio('kpsp6', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp6_x', label_visibility='collapsed')
                    else:
                        kpsp6_x = st.radio('kpsp6', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp6_value), horizontal=True, key='kpsp6_x', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/12_7.png')
                with col2:
                    st.empty()
                    kpsp7_value = st.session_state.input_data.get('KPSP7', '')
                    if pd.isna(kpsp7_value):
                        kpsp7_x = st.radio('kpsp7', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp7_x', label_visibility='collapsed')
                    else:
                        kpsp7_x = st.radio('kpsp7', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp7_value), horizontal=True, key='kpsp7_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/12_8.png')
                with col2:
                    st.empty()
                    kpsp8_value = st.session_state.input_data.get('KPSP8', '')
                    if pd.isna(kpsp8_value):
                        kpsp8_x = st.radio('kpsp8', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp8_x', label_visibility='collapsed')
                    else:
                        kpsp8_x = st.radio('kpsp8', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp8_value), horizontal=True, key='kpsp8_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/12_9.png')
                with col2:
                    st.empty()
                    kpsp9_value = st.session_state.input_data.get('KPSP9', '')
                    if pd.isna(kpsp9_value):
                        kpsp9_x = st.radio('kpsp9', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp9_x', label_visibility='collapsed')
                    else:
                        kpsp9_x = st.radio('kpsp9', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp9_value), horizontal=True, key='kpsp9_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/12_10.png')
                with col2:
                    st.empty()
                    kpsp10_value = st.session_state.input_data.get('KPSP10', '')
                    if pd.isna(kpsp10_value):
                        kpsp10_x = st.radio('kpsp10', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp10_x', label_visibility='collapsed')
                    else:
                        kpsp10_x = st.radio('kpsp10', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp10_value), horizontal=True, key='kpsp10_x', label_visibility='collapsed')
            
            elif 15 <= usia_bln < 18:

                st.write('### KPSP Umur 15 bulan')

                # Membuat kolom untuk menempatkan caption di kiri dan opsi di kanan
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Menentukan lebar kolom (3 bagian untuk caption, 1 bagian untuk opsi)

                with col1:
                    st.image('.img/15_1.png')
                with col2:
                    st.empty()
                    kpsp1_value = st.session_state.input_data.get('KPSP1', '')
                    if pd.isna(kpsp1_value):
                        kpsp1_x = st.radio('kpsp1', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp1_x', label_visibility='collapsed')
                    else:
                        kpsp1_x = st.radio('kpsp1', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp1_value), horizontal=True, key='kpsp1_x', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/15_2.png')
                with col2:
                    st.empty()
                    kpsp2_value = st.session_state.input_data.get('KPSP2', '')
                    if pd.isna(kpsp1_value):
                        kpsp2_x = st.radio('kpsp2', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp2_x', label_visibility='collapsed')
                    else:
                        kpsp2_x = st.radio('kpsp2', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp2_value), horizontal=True, key='kpsp2_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/15_3.png')
                with col2:
                    st.empty()
                    kpsp3_value = st.session_state.input_data.get('KPSP3', '')
                    if pd.isna(kpsp1_value):
                        kpsp3_x = st.radio('kpsp3', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp3_x', label_visibility='collapsed')
                    else:
                        kpsp3_x = st.radio('kpsp3', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp3_value), horizontal=True, key='kpsp3_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/15_4.png')
                with col2:
                    st.empty()
                    kpsp4_value = st.session_state.input_data.get('KPSP4', '')
                    if pd.isna(kpsp4_value):
                        kpsp4_x = st.radio('kpsp4', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp4_x', label_visibility='collapsed')
                    else:
                        kpsp4_x = st.radio('kpsp4', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp4_value), horizontal=True, key='kpsp4_x', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/15_5.png')
                with col2:
                    st.empty()
                    kpsp5_value = st.session_state.input_data.get('KPSP5', '')
                    if pd.isna(kpsp5_value):
                        kpsp5_x = st.radio('kpsp5', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp5_x', label_visibility='collapsed')
                    else:
                        kpsp5_x = st.radio('kpsp5', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp5_value), horizontal=True, key='kpsp5_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/15_6.png')
                with col2:
                    st.empty()
                    kpsp6_value = st.session_state.input_data.get('KPSP6', '')
                    if pd.isna(kpsp6_value):
                        kpsp6_x = st.radio('kpsp6', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp6_x', label_visibility='collapsed')
                    else:
                        kpsp6_x = st.radio('kpsp6', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp6_value), horizontal=True, key='kpsp6_x', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/15_7.png')
                with col2:
                    st.empty()
                    kpsp7_value = st.session_state.input_data.get('KPSP7', '')
                    if pd.isna(kpsp7_value):
                        kpsp7_x = st.radio('kpsp7', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp7_x', label_visibility='collapsed')
                    else:
                        kpsp7_x = st.radio('kpsp7', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp7_value), horizontal=True, key='kpsp7_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/15_8.png')
                with col2:
                    st.empty()
                    kpsp8_value = st.session_state.input_data.get('KPSP8', '')
                    if pd.isna(kpsp8_value):
                        kpsp8_x = st.radio('kpsp8', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp8_x', label_visibility='collapsed')
                    else:
                        kpsp8_x = st.radio('kpsp8', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp8_value), horizontal=True, key='kpsp8_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/15_9.png')
                with col2:
                    st.empty()
                    kpsp9_value = st.session_state.input_data.get('KPSP9', '')
                    if pd.isna(kpsp9_value):
                        kpsp9_x = st.radio('kpsp9', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp9_x', label_visibility='collapsed')
                    else:
                        kpsp9_x = st.radio('kpsp9', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp9_value), horizontal=True, key='kpsp9_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/15_10.png')
                with col2:
                    st.empty()
                    kpsp10_value = st.session_state.input_data.get('KPSP10', '')
                    if pd.isna(kpsp10_value):
                        kpsp10_x = st.radio('kpsp10', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp10_x', label_visibility='collapsed')
                    else:
                        kpsp10_x = st.radio('kpsp10', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp10_value), horizontal=True, key='kpsp10_x', label_visibility='collapsed')
                    
            elif 18 <= usia_bln < 21:

                st.write('### KPSP Umur 18 bulan')

                # Membuat kolom untuk menempatkan caption di kiri dan opsi di kanan
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Menentukan lebar kolom (3 bagian untuk caption, 1 bagian untuk opsi)

                with col1:
                    st.image('.img/18_1.png')
                with col2:
                    st.empty()
                    kpsp1_value = st.session_state.input_data.get('KPSP1', '')
                    if pd.isna(kpsp1_value):
                        kpsp1_x = st.radio('kpsp1', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp1_x', label_visibility='collapsed')
                    else:
                        kpsp1_x = st.radio('kpsp1', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp1_value), horizontal=True, key='kpsp1_x', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/18_2.png')
                with col2:
                    st.empty()
                    kpsp2_value = st.session_state.input_data.get('KPSP2', '')
                    if pd.isna(kpsp1_value):
                        kpsp2_x = st.radio('kpsp2', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp2_x', label_visibility='collapsed')
                    else:
                        kpsp2_x = st.radio('kpsp2', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp2_value), horizontal=True, key='kpsp2_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/18_3.png')
                with col2:
                    st.empty()
                    kpsp3_value = st.session_state.input_data.get('KPSP3', '')
                    if pd.isna(kpsp1_value):
                        kpsp3_x = st.radio('kpsp3', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp3_x', label_visibility='collapsed')
                    else:
                        kpsp3_x = st.radio('kpsp3', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp3_value), horizontal=True, key='kpsp3_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/18_4.png')
                with col2:
                    st.empty()
                    kpsp4_value = st.session_state.input_data.get('KPSP4', '')
                    if pd.isna(kpsp4_value):
                        kpsp4_x = st.radio('kpsp4', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp4_x', label_visibility='collapsed')
                    else:
                        kpsp4_x = st.radio('kpsp4', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp4_value), horizontal=True, key='kpsp4_x', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/18_5.png')
                with col2:
                    st.empty()
                    kpsp5_value = st.session_state.input_data.get('KPSP5', '')
                    if pd.isna(kpsp5_value):
                        kpsp5_x = st.radio('kpsp5', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp5_x', label_visibility='collapsed')
                    else:
                        kpsp5_x = st.radio('kpsp5', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp5_value), horizontal=True, key='kpsp5_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/18_6.png')
                with col2:
                    st.empty()
                    kpsp6_value = st.session_state.input_data.get('KPSP6', '')
                    if pd.isna(kpsp6_value):
                        kpsp6_x = st.radio('kpsp6', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp6_x', label_visibility='collapsed')
                    else:
                        kpsp6_x = st.radio('kpsp6', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp6_value), horizontal=True, key='kpsp6_x', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/18_7.png')
                with col2:
                    st.empty()
                    kpsp7_value = st.session_state.input_data.get('KPSP7', '')
                    if pd.isna(kpsp7_value):
                        kpsp7_x = st.radio('kpsp7', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp7_x', label_visibility='collapsed')
                    else:
                        kpsp7_x = st.radio('kpsp7', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp7_value), horizontal=True, key='kpsp7_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/18_8.png')
                with col2:
                    st.empty()
                    kpsp8_value = st.session_state.input_data.get('KPSP8', '')
                    if pd.isna(kpsp8_value):
                        kpsp8_x = st.radio('kpsp8', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp8_x', label_visibility='collapsed')
                    else:
                        kpsp8_x = st.radio('kpsp8', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp8_value), horizontal=True, key='kpsp8_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/18_9.png')
                with col2:
                    st.empty()
                    kpsp9_value = st.session_state.input_data.get('KPSP9', '')
                    if pd.isna(kpsp9_value):
                        kpsp9_x = st.radio('kpsp9', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp9_x', label_visibility='collapsed')
                    else:
                        kpsp9_x = st.radio('kpsp9', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp9_value), horizontal=True, key='kpsp9_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/18_10.png')
                with col2:
                    st.empty()
                    kpsp10_value = st.session_state.input_data.get('KPSP10', '')
                    if pd.isna(kpsp10_value):
                        kpsp10_x = st.radio('kpsp10', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp10_x', label_visibility='collapsed')
                    else:
                        kpsp10_x = st.radio('kpsp10', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp10_value), horizontal=True, key='kpsp10_x', label_visibility='collapsed')
                    
            elif 21 <= usia_bln < 24:

                st.write('### KPSP Umur 21 bulan')

                # Membuat kolom untuk menempatkan caption di kiri dan opsi di kanan
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Menentukan lebar kolom (3 bagian untuk caption, 1 bagian untuk opsi)

                with col1:
                    st.image('.img/21_1.png')
                with col2:
                    st.empty()
                    kpsp1_value = st.session_state.input_data.get('KPSP1', '')
                    if pd.isna(kpsp1_value):
                        kpsp1_x = st.radio('kpsp1', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp1_x', label_visibility='collapsed')
                    else:
                        kpsp1_x = st.radio('kpsp1', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp1_value), horizontal=True, key='kpsp1_x', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/21_2.png')
                with col2:
                    st.empty()
                    kpsp2_value = st.session_state.input_data.get('KPSP2', '')
                    if pd.isna(kpsp1_value):
                        kpsp2_x = st.radio('kpsp2', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp2_x', label_visibility='collapsed')
                    else:
                        kpsp2_x = st.radio('kpsp2', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp2_value), horizontal=True, key='kpsp2_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/21_3.png')
                with col2:
                    st.empty()
                    kpsp3_value = st.session_state.input_data.get('KPSP3', '')
                    if pd.isna(kpsp1_value):
                        kpsp3_x = st.radio('kpsp3', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp3_x', label_visibility='collapsed')
                    else:
                        kpsp3_x = st.radio('kpsp3', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp3_value), horizontal=True, key='kpsp3_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/21_4.png')
                with col2:
                    st.empty()
                    kpsp4_value = st.session_state.input_data.get('KPSP4', '')
                    if pd.isna(kpsp4_value):
                        kpsp4_x = st.radio('kpsp4', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp4_x', label_visibility='collapsed')
                    else:
                        kpsp4_x = st.radio('kpsp4', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp4_value), horizontal=True, key='kpsp4_x', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/21_5.png')
                with col2:
                    st.empty()
                    kpsp5_value = st.session_state.input_data.get('KPSP5', '')
                    if pd.isna(kpsp5_value):
                        kpsp5_x = st.radio('kpsp5', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp5_x', label_visibility='collapsed')
                    else:
                        kpsp5_x = st.radio('kpsp5', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp5_value), horizontal=True, key='kpsp5_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/21_6.png')
                with col2:
                    st.empty()
                    kpsp6_value = st.session_state.input_data.get('KPSP6', '')
                    if pd.isna(kpsp6_value):
                        kpsp6_x = st.radio('kpsp6', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp6_x', label_visibility='collapsed')
                    else:
                        kpsp6_x = st.radio('kpsp6', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp6_value), horizontal=True, key='kpsp6_x', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/21_7.png')
                with col2:
                    st.empty()
                    kpsp7_value = st.session_state.input_data.get('KPSP7', '')
                    if pd.isna(kpsp7_value):
                        kpsp7_x = st.radio('kpsp7', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp7_x', label_visibility='collapsed')
                    else:
                        kpsp7_x = st.radio('kpsp7', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp7_value), horizontal=True, key='kpsp7_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/21_8.png')
                with col2:
                    st.empty()
                    kpsp8_value = st.session_state.input_data.get('KPSP8', '')
                    if pd.isna(kpsp8_value):
                        kpsp8_x = st.radio('kpsp8', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp8_x', label_visibility='collapsed')
                    else:
                        kpsp8_x = st.radio('kpsp8', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp8_value), horizontal=True, key='kpsp8_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/21_9.png')
                with col2:
                    st.empty()
                    kpsp9_value = st.session_state.input_data.get('KPSP9', '')
                    if pd.isna(kpsp9_value):
                        kpsp9_x = st.radio('kpsp9', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp9_x', label_visibility='collapsed')
                    else:
                        kpsp9_x = st.radio('kpsp9', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp9_value), horizontal=True, key='kpsp9_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/21_10.png')
                with col2:
                    st.empty()
                    kpsp10_value = st.session_state.input_data.get('KPSP10', '')
                    if pd.isna(kpsp10_value):
                        kpsp10_x = st.radio('kpsp10', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp10_x', label_visibility='collapsed')
                    else:
                        kpsp10_x = st.radio('kpsp10', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp10_value), horizontal=True, key='kpsp10_x', label_visibility='collapsed')
                    
            elif 24 <= usia_bln < 30:

                st.write('### KPSP Umur 24 bulan')

                # Membuat kolom untuk menempatkan caption di kiri dan opsi di kanan
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Menentukan lebar kolom (3 bagian untuk caption, 1 bagian untuk opsi)

                with col1:
                    st.image('.img/24_1.png')
                with col2:
                    st.empty()
                    kpsp1_value = st.session_state.input_data.get('KPSP1', '')
                    if pd.isna(kpsp1_value):
                        kpsp1_x = st.radio('kpsp1', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp1_x', label_visibility='collapsed')
                    else:
                        kpsp1_x = st.radio('kpsp1', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp1_value), horizontal=True, key='kpsp1_x', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/24_2.png')
                with col2:
                    st.empty()
                    kpsp2_value = st.session_state.input_data.get('KPSP2', '')
                    if pd.isna(kpsp1_value):
                        kpsp2_x = st.radio('kpsp2', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp2_x', label_visibility='collapsed')
                    else:
                        kpsp2_x = st.radio('kpsp2', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp2_value), horizontal=True, key='kpsp2_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/24_3.png')
                with col2:
                    st.empty()
                    kpsp3_value = st.session_state.input_data.get('KPSP3', '')
                    if pd.isna(kpsp1_value):
                        kpsp3_x = st.radio('kpsp3', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp3_x', label_visibility='collapsed')
                    else:
                        kpsp3_x = st.radio('kpsp3', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp3_value), horizontal=True, key='kpsp3_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/24_4.png')
                with col2:
                    st.empty()
                    kpsp4_value = st.session_state.input_data.get('KPSP4', '')
                    if pd.isna(kpsp4_value):
                        kpsp4_x = st.radio('kpsp4', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp4_x', label_visibility='collapsed')
                    else:
                        kpsp4_x = st.radio('kpsp4', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp4_value), horizontal=True, key='kpsp4_x', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/24_5.png')
                with col2:
                    st.empty()
                    kpsp5_value = st.session_state.input_data.get('KPSP5', '')
                    if pd.isna(kpsp5_value):
                        kpsp5_x = st.radio('kpsp5', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp5_x', label_visibility='collapsed')
                    else:
                        kpsp5_x = st.radio('kpsp5', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp5_value), horizontal=True, key='kpsp5_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/24_6.png')
                with col2:
                    st.empty()
                    kpsp6_value = st.session_state.input_data.get('KPSP6', '')
                    if pd.isna(kpsp6_value):
                        kpsp6_x = st.radio('kpsp6', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp6_x', label_visibility='collapsed')
                    else:
                        kpsp6_x = st.radio('kpsp6', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp6_value), horizontal=True, key='kpsp6_x', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/24_7.png')
                with col2:
                    st.empty()
                    kpsp7_value = st.session_state.input_data.get('KPSP7', '')
                    if pd.isna(kpsp7_value):
                        kpsp7_x = st.radio('kpsp7', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp7_x', label_visibility='collapsed')
                    else:
                        kpsp7_x = st.radio('kpsp7', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp7_value), horizontal=True, key='kpsp7_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/24_8.png')
                with col2:
                    st.empty()
                    kpsp8_value = st.session_state.input_data.get('KPSP8', '')
                    if pd.isna(kpsp8_value):
                        kpsp8_x = st.radio('kpsp8', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp8_x', label_visibility='collapsed')
                    else:
                        kpsp8_x = st.radio('kpsp8', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp8_value), horizontal=True, key='kpsp8_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/24_9.png')
                with col2:
                    st.empty()
                    kpsp9_value = st.session_state.input_data.get('KPSP9', '')
                    if pd.isna(kpsp9_value):
                        kpsp9_x = st.radio('kpsp9', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp9_x', label_visibility='collapsed')
                    else:
                        kpsp9_x = st.radio('kpsp9', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp9_value), horizontal=True, key='kpsp9_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/24_10.png')
                with col2:
                    st.empty()
                    kpsp10_value = st.session_state.input_data.get('KPSP10', '')
                    if pd.isna(kpsp10_value):
                        kpsp10_x = st.radio('kpsp10', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp10_x', label_visibility='collapsed')
                    else:
                        kpsp10_x = st.radio('kpsp10', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp10_value), horizontal=True, key='kpsp10_x', label_visibility='collapsed')
                    
            elif 30 <= usia_bln < 36:

                st.write('### KPSP Umur 30 bulan')

                # Membuat kolom untuk menempatkan caption di kiri dan opsi di kanan
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Menentukan lebar kolom (3 bagian untuk caption, 1 bagian untuk opsi)

                with col1:
                    st.image('.img/30_1.png')
                with col2:
                    st.empty()
                    kpsp1_value = st.session_state.input_data.get('KPSP1', '')
                    if pd.isna(kpsp1_value):
                        kpsp1_x = st.radio('kpsp1', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp1_x', label_visibility='collapsed')
                    else:
                        kpsp1_x = st.radio('kpsp1', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp1_value), horizontal=True, key='kpsp1_x', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/30_2.png')
                with col2:
                    st.empty()
                    kpsp2_value = st.session_state.input_data.get('KPSP2', '')
                    if pd.isna(kpsp1_value):
                        kpsp2_x = st.radio('kpsp2', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp2_x', label_visibility='collapsed')
                    else:
                        kpsp2_x = st.radio('kpsp2', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp2_value), horizontal=True, key='kpsp2_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/30_3.png')
                with col2:
                    st.empty()
                    kpsp3_value = st.session_state.input_data.get('KPSP3', '')
                    if pd.isna(kpsp1_value):
                        kpsp3_x = st.radio('kpsp3', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp3_x', label_visibility='collapsed')
                    else:
                        kpsp3_x = st.radio('kpsp3', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp3_value), horizontal=True, key='kpsp3_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/30_4.png')
                with col2:
                    st.empty()
                    kpsp4_value = st.session_state.input_data.get('KPSP4', '')
                    if pd.isna(kpsp4_value):
                        kpsp4_x = st.radio('kpsp4', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp4_x', label_visibility='collapsed')
                    else:
                        kpsp4_x = st.radio('kpsp4', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp4_value), horizontal=True, key='kpsp4_x', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/30_5.png')
                with col2:
                    st.empty()
                    kpsp5_value = st.session_state.input_data.get('KPSP5', '')
                    if pd.isna(kpsp5_value):
                        kpsp5_x = st.radio('kpsp5', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp5_x', label_visibility='collapsed')
                    else:
                        kpsp5_x = st.radio('kpsp5', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp5_value), horizontal=True, key='kpsp5_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/30_6.png')
                with col2:
                    st.empty()
                    kpsp6_value = st.session_state.input_data.get('KPSP6', '')
                    if pd.isna(kpsp6_value):
                        kpsp6_x = st.radio('kpsp6', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp6_x', label_visibility='collapsed')
                    else:
                        kpsp6_x = st.radio('kpsp6', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp6_value), horizontal=True, key='kpsp6_x', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/30_7.png')
                with col2:
                    st.empty()
                    kpsp7_value = st.session_state.input_data.get('KPSP7', '')
                    if pd.isna(kpsp7_value):
                        kpsp7_x = st.radio('kpsp7', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp7_x', label_visibility='collapsed')
                    else:
                        kpsp7_x = st.radio('kpsp7', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp7_value), horizontal=True, key='kpsp7_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/30_8.png')
                with col2:
                    st.empty()
                    kpsp8_value = st.session_state.input_data.get('KPSP8', '')
                    if pd.isna(kpsp8_value):
                        kpsp8_x = st.radio('kpsp8', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp8_x', label_visibility='collapsed')
                    else:
                        kpsp8_x = st.radio('kpsp8', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp8_value), horizontal=True, key='kpsp8_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/30_9.png')
                with col2:
                    st.empty()
                    kpsp9_value = st.session_state.input_data.get('KPSP9', '')
                    if pd.isna(kpsp9_value):
                        kpsp9_x = st.radio('kpsp9', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp9_x', label_visibility='collapsed')
                    else:
                        kpsp9_x = st.radio('kpsp9', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp9_value), horizontal=True, key='kpsp9_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/30_10.png')
                with col2:
                    st.empty()
                    kpsp10_value = st.session_state.input_data.get('KPSP10', '')
                    if pd.isna(kpsp10_value):
                        kpsp10_x = st.radio('kpsp10', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp10_x', label_visibility='collapsed')
                    else:
                        kpsp10_x = st.radio('kpsp10', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp10_value), horizontal=True, key='kpsp10_x', label_visibility='collapsed')
                    
            elif 36 <= usia_bln < 42:

                st.write('### KPSP Umur 36 bulan')

                # Membuat kolom untuk menempatkan caption di kiri dan opsi di kanan
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Menentukan lebar kolom (3 bagian untuk caption, 1 bagian untuk opsi)

                with col1:
                    st.image('.img/36_1.png')
                with col2:
                    st.empty()
                    kpsp1_value = st.session_state.input_data.get('KPSP1', '')
                    if pd.isna(kpsp1_value):
                        kpsp1_x = st.radio('kpsp1', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp1_x', label_visibility='collapsed')
                    else:
                        kpsp1_x = st.radio('kpsp1', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp1_value), horizontal=True, key='kpsp1_x', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/36_2.png')
                with col2:
                    st.empty()
                    kpsp2_value = st.session_state.input_data.get('KPSP2', '')
                    if pd.isna(kpsp1_value):
                        kpsp2_x = st.radio('kpsp2', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp2_x', label_visibility='collapsed')
                    else:
                        kpsp2_x = st.radio('kpsp2', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp2_value), horizontal=True, key='kpsp2_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/36_3.png')
                with col2:
                    st.empty()
                    kpsp3_value = st.session_state.input_data.get('KPSP3', '')
                    if pd.isna(kpsp1_value):
                        kpsp3_x = st.radio('kpsp3', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp3_x', label_visibility='collapsed')
                    else:
                        kpsp3_x = st.radio('kpsp3', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp3_value), horizontal=True, key='kpsp3_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/36_4.png')
                with col2:
                    st.empty()
                    kpsp4_value = st.session_state.input_data.get('KPSP4', '')
                    if pd.isna(kpsp4_value):
                        kpsp4_x = st.radio('kpsp4', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp4_x', label_visibility='collapsed')
                    else:
                        kpsp4_x = st.radio('kpsp4', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp4_value), horizontal=True, key='kpsp4_x', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/36_5.png')
                with col2:
                    st.empty()
                    kpsp5_value = st.session_state.input_data.get('KPSP5', '')
                    if pd.isna(kpsp5_value):
                        kpsp5_x = st.radio('kpsp5', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp5_x', label_visibility='collapsed')
                    else:
                        kpsp5_x = st.radio('kpsp5', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp5_value), horizontal=True, key='kpsp5_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/36_6.png')
                with col2:
                    st.empty()
                    kpsp6_value = st.session_state.input_data.get('KPSP6', '')
                    if pd.isna(kpsp6_value):
                        kpsp6_x = st.radio('kpsp6', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp6_x', label_visibility='collapsed')
                    else:
                        kpsp6_x = st.radio('kpsp6', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp6_value), horizontal=True, key='kpsp6_x', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/36_7.png')
                with col2:
                    st.empty()
                    kpsp7_value = st.session_state.input_data.get('KPSP7', '')
                    if pd.isna(kpsp7_value):
                        kpsp7_x = st.radio('kpsp7', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp7_x', label_visibility='collapsed')
                    else:
                        kpsp7_x = st.radio('kpsp7', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp7_value), horizontal=True, key='kpsp7_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/36_8.png')
                with col2:
                    st.empty()
                    kpsp8_value = st.session_state.input_data.get('KPSP8', '')
                    if pd.isna(kpsp8_value):
                        kpsp8_x = st.radio('kpsp8', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp8_x', label_visibility='collapsed')
                    else:
                        kpsp8_x = st.radio('kpsp8', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp8_value), horizontal=True, key='kpsp8_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/36_9.png')
                with col2:
                    st.empty()
                    kpsp9_value = st.session_state.input_data.get('KPSP9', '')
                    if pd.isna(kpsp9_value):
                        kpsp9_x = st.radio('kpsp9', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp9_x', label_visibility='collapsed')
                    else:
                        kpsp9_x = st.radio('kpsp9', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp9_value), horizontal=True, key='kpsp9_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/36_10.png')
                with col2:
                    st.empty()
                    kpsp10_value = st.session_state.input_data.get('KPSP10', '')
                    if pd.isna(kpsp10_value):
                        kpsp10_x = st.radio('kpsp10', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp10_x', label_visibility='collapsed')
                    else:
                        kpsp10_x = st.radio('kpsp10', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp10_value), horizontal=True, key='kpsp10_x', label_visibility='collapsed')
                    
            elif 42 <= usia_bln < 48:

                st.write('### KPSP Umur 42 bulan')

                # Membuat kolom untuk menempatkan caption di kiri dan opsi di kanan
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Menentukan lebar kolom (3 bagian untuk caption, 1 bagian untuk opsi)

                with col1:
                    st.image('.img/42_1.png')
                with col2:
                    st.empty()
                    kpsp1_value = st.session_state.input_data.get('KPSP1', '')
                    if pd.isna(kpsp1_value):
                        kpsp1_x = st.radio('kpsp1', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp1_x', label_visibility='collapsed')
                    else:
                        kpsp1_x = st.radio('kpsp1', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp1_value), horizontal=True, key='kpsp1_x', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/42_2.png')
                with col2:
                    st.empty()
                    kpsp2_value = st.session_state.input_data.get('KPSP2', '')
                    if pd.isna(kpsp1_value):
                        kpsp2_x = st.radio('kpsp2', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp2_x', label_visibility='collapsed')
                    else:
                        kpsp2_x = st.radio('kpsp2', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp2_value), horizontal=True, key='kpsp2_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/42_3.png')
                with col2:
                    st.empty()
                    kpsp3_value = st.session_state.input_data.get('KPSP3', '')
                    if pd.isna(kpsp1_value):
                        kpsp3_x = st.radio('kpsp3', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp3_x', label_visibility='collapsed')
                    else:
                        kpsp3_x = st.radio('kpsp3', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp3_value), horizontal=True, key='kpsp3_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/42_4.png')
                with col2:
                    st.empty()
                    kpsp4_value = st.session_state.input_data.get('KPSP4', '')
                    if pd.isna(kpsp4_value):
                        kpsp4_x = st.radio('kpsp4', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp4_x', label_visibility='collapsed')
                    else:
                        kpsp4_x = st.radio('kpsp4', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp4_value), horizontal=True, key='kpsp4_x', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/42_5.png')
                with col2:
                    st.empty()
                    kpsp5_value = st.session_state.input_data.get('KPSP5', '')
                    if pd.isna(kpsp5_value):
                        kpsp5_x = st.radio('kpsp5', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp5_x', label_visibility='collapsed')
                    else:
                        kpsp5_x = st.radio('kpsp5', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp5_value), horizontal=True, key='kpsp5_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/42_6.png')
                with col2:
                    st.empty()
                    kpsp6_value = st.session_state.input_data.get('KPSP6', '')
                    if pd.isna(kpsp6_value):
                        kpsp6_x = st.radio('kpsp6', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp6_x', label_visibility='collapsed')
                    else:
                        kpsp6_x = st.radio('kpsp6', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp6_value), horizontal=True, key='kpsp6_x', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/42_7.png')
                with col2:
                    st.empty()
                    kpsp7_value = st.session_state.input_data.get('KPSP7', '')
                    if pd.isna(kpsp7_value):
                        kpsp7_x = st.radio('kpsp7', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp7_x', label_visibility='collapsed')
                    else:
                        kpsp7_x = st.radio('kpsp7', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp7_value), horizontal=True, key='kpsp7_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/42_8.png')
                with col2:
                    st.empty()
                    kpsp8_value = st.session_state.input_data.get('KPSP8', '')
                    if pd.isna(kpsp8_value):
                        kpsp8_x = st.radio('kpsp8', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp8_x', label_visibility='collapsed')
                    else:
                        kpsp8_x = st.radio('kpsp8', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp8_value), horizontal=True, key='kpsp8_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/42_9.png')
                with col2:
                    st.empty()
                    kpsp9_value = st.session_state.input_data.get('KPSP9', '')
                    if pd.isna(kpsp9_value):
                        kpsp9_x = st.radio('kpsp9', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp9_x', label_visibility='collapsed')
                    else:
                        kpsp9_x = st.radio('kpsp9', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp9_value), horizontal=True, key='kpsp9_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/42_10.png')
                with col2:
                    st.empty()
                    kpsp10_value = st.session_state.input_data.get('KPSP10', '')
                    if pd.isna(kpsp10_value):
                        kpsp10_x = st.radio('kpsp10', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp10_x', label_visibility='collapsed')
                    else:
                        kpsp10_x = st.radio('kpsp10', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp10_value), horizontal=True, key='kpsp10_x', label_visibility='collapsed')
                    
            elif 48 <= usia_bln < 54:

                st.write('### KPSP Umur 48 bulan')

                # Membuat kolom untuk menempatkan caption di kiri dan opsi di kanan
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Menentukan lebar kolom (3 bagian untuk caption, 1 bagian untuk opsi)

                with col1:
                    st.image('.img/48_1.png')
                with col2:
                    st.empty()
                    kpsp1_value = st.session_state.input_data.get('KPSP1', '')
                    if pd.isna(kpsp1_value):
                        kpsp1_x = st.radio('kpsp1', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp1_x', label_visibility='collapsed')
                    else:
                        kpsp1_x = st.radio('kpsp1', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp1_value), horizontal=True, key='kpsp1_x', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/48_2.png')
                with col2:
                    st.empty()
                    kpsp2_value = st.session_state.input_data.get('KPSP2', '')
                    if pd.isna(kpsp1_value):
                        kpsp2_x = st.radio('kpsp2', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp2_x', label_visibility='collapsed')
                    else:
                        kpsp2_x = st.radio('kpsp2', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp2_value), horizontal=True, key='kpsp2_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/48_3.png')
                with col2:
                    st.empty()
                    kpsp3_value = st.session_state.input_data.get('KPSP3', '')
                    if pd.isna(kpsp1_value):
                        kpsp3_x = st.radio('kpsp3', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp3_x', label_visibility='collapsed')
                    else:
                        kpsp3_x = st.radio('kpsp3', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp3_value), horizontal=True, key='kpsp3_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/48_4.png')
                with col2:
                    st.empty()
                    kpsp4_value = st.session_state.input_data.get('KPSP4', '')
                    if pd.isna(kpsp4_value):
                        kpsp4_x = st.radio('kpsp4', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp4_x', label_visibility='collapsed')
                    else:
                        kpsp4_x = st.radio('kpsp4', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp4_value), horizontal=True, key='kpsp4_x', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/48_5.png')
                with col2:
                    st.empty()
                    kpsp5_value = st.session_state.input_data.get('KPSP5', '')
                    if pd.isna(kpsp5_value):
                        kpsp5_x = st.radio('kpsp5', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp5_x', label_visibility='collapsed')
                    else:
                        kpsp5_x = st.radio('kpsp5', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp5_value), horizontal=True, key='kpsp5_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/48_6.png')
                with col2:
                    st.empty()
                    kpsp6_value = st.session_state.input_data.get('KPSP6', '')
                    if pd.isna(kpsp6_value):
                        kpsp6_x = st.radio('kpsp6', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp6_x', label_visibility='collapsed')
                    else:
                        kpsp6_x = st.radio('kpsp6', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp6_value), horizontal=True, key='kpsp6_x', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/48_7.png')
                with col2:
                    st.empty()
                    kpsp7_value = st.session_state.input_data.get('KPSP7', '')
                    if pd.isna(kpsp7_value):
                        kpsp7_x = st.radio('kpsp7', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp7_x', label_visibility='collapsed')
                    else:
                        kpsp7_x = st.radio('kpsp7', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp7_value), horizontal=True, key='kpsp7_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/48_8.png')
                with col2:
                    st.empty()
                    kpsp8_value = st.session_state.input_data.get('KPSP8', '')
                    if pd.isna(kpsp8_value):
                        kpsp8_x = st.radio('kpsp8', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp8_x', label_visibility='collapsed')
                    else:
                        kpsp8_x = st.radio('kpsp8', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp8_value), horizontal=True, key='kpsp8_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/48_9.png')
                with col2:
                    st.empty()
                    kpsp9_value = st.session_state.input_data.get('KPSP9', '')
                    if pd.isna(kpsp9_value):
                        kpsp9_x = st.radio('kpsp9', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp9_x', label_visibility='collapsed')
                    else:
                        kpsp9_x = st.radio('kpsp9', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp9_value), horizontal=True, key='kpsp9_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/48_10.png')
                with col2:
                    st.empty()
                    kpsp10_value = st.session_state.input_data.get('KPSP10', '')
                    if pd.isna(kpsp10_value):
                        kpsp10_x = st.radio('kpsp10', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp10_x', label_visibility='collapsed')
                    else:
                        kpsp10_x = st.radio('kpsp10', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp10_value), horizontal=True, key='kpsp10_x', label_visibility='collapsed')
                    
            elif 54 <= usia_bln < 60:

                st.write('### KPSP Umur 54 bulan')

                # Membuat kolom untuk menempatkan caption di kiri dan opsi di kanan
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Menentukan lebar kolom (3 bagian untuk caption, 1 bagian untuk opsi)

                with col1:
                    st.image('.img/54_1.png')
                with col2:
                    st.empty()
                    kpsp1_value = st.session_state.input_data.get('KPSP1', '')
                    if pd.isna(kpsp1_value):
                        kpsp1_x = st.radio('kpsp1', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp1_x', label_visibility='collapsed')
                    else:
                        kpsp1_x = st.radio('kpsp1', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp1_value), horizontal=True, key='kpsp1_x', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/54_2.png')
                with col2:
                    st.empty()
                    kpsp2_value = st.session_state.input_data.get('KPSP2', '')
                    if pd.isna(kpsp1_value):
                        kpsp2_x = st.radio('kpsp2', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp2_x', label_visibility='collapsed')
                    else:
                        kpsp2_x = st.radio('kpsp2', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp2_value), horizontal=True, key='kpsp2_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/54_3.png')
                with col2:
                    st.empty()
                    kpsp3_value = st.session_state.input_data.get('KPSP3', '')
                    if pd.isna(kpsp1_value):
                        kpsp3_x = st.radio('kpsp3', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp3_x', label_visibility='collapsed')
                    else:
                        kpsp3_x = st.radio('kpsp3', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp3_value), horizontal=True, key='kpsp3_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/54_4.png')
                with col2:
                    st.empty()
                    kpsp4_value = st.session_state.input_data.get('KPSP4', '')
                    if pd.isna(kpsp4_value):
                        kpsp4_x = st.radio('kpsp4', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp4_x', label_visibility='collapsed')
                    else:
                        kpsp4_x = st.radio('kpsp4', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp4_value), horizontal=True, key='kpsp4_x', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/54_5.png')
                with col2:
                    st.empty()
                    kpsp5_value = st.session_state.input_data.get('KPSP5', '')
                    if pd.isna(kpsp5_value):
                        kpsp5_x = st.radio('kpsp5', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp5_x', label_visibility='collapsed')
                    else:
                        kpsp5_x = st.radio('kpsp5', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp5_value), horizontal=True, key='kpsp5_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/54_6.png')
                with col2:
                    st.empty()
                    kpsp6_value = st.session_state.input_data.get('KPSP6', '')
                    if pd.isna(kpsp6_value):
                        kpsp6_x = st.radio('kpsp6', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp6_x', label_visibility='collapsed')
                    else:
                        kpsp6_x = st.radio('kpsp6', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp6_value), horizontal=True, key='kpsp6_x', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/54_7.png')
                with col2:
                    st.empty()
                    kpsp7_value = st.session_state.input_data.get('KPSP7', '')
                    if pd.isna(kpsp7_value):
                        kpsp7_x = st.radio('kpsp7', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp7_x', label_visibility='collapsed')
                    else:
                        kpsp7_x = st.radio('kpsp7', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp7_value), horizontal=True, key='kpsp7_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/54_8.png')
                with col2:
                    st.empty()
                    kpsp8_value = st.session_state.input_data.get('KPSP8', '')
                    if pd.isna(kpsp8_value):
                        kpsp8_x = st.radio('kpsp8', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp8_x', label_visibility='collapsed')
                    else:
                        kpsp8_x = st.radio('kpsp8', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp8_value), horizontal=True, key='kpsp8_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/54_9.png')
                with col2:
                    st.empty()
                    kpsp9_value = st.session_state.input_data.get('KPSP9', '')
                    if pd.isna(kpsp9_value):
                        kpsp9_x = st.radio('kpsp9', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp9_x', label_visibility='collapsed')
                    else:
                        kpsp9_x = st.radio('kpsp9', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp9_value), horizontal=True, key='kpsp9_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/54_10.png')
                with col2:
                    st.empty()
                    kpsp10_value = st.session_state.input_data.get('KPSP10', '')
                    if pd.isna(kpsp10_value):
                        kpsp10_x = st.radio('kpsp10', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp10_x', label_visibility='collapsed')
                    else:
                        kpsp10_x = st.radio('kpsp10', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp10_value), horizontal=True, key='kpsp10_x', label_visibility='collapsed')
                    
            elif 60 <= usia_bln < 66:

                st.write('### KPSP Umur 60 bulan')

                # Membuat kolom untuk menempatkan caption di kiri dan opsi di kanan
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Menentukan lebar kolom (3 bagian untuk caption, 1 bagian untuk opsi)

                with col1:
                    st.image('.img/60_1.png')
                with col2:
                    st.empty()
                    kpsp1_value = st.session_state.input_data.get('KPSP1', '')
                    if pd.isna(kpsp1_value):
                        kpsp1_x = st.radio('kpsp1', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp1_x', label_visibility='collapsed')
                    else:
                        kpsp1_x = st.radio('kpsp1', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp1_value), horizontal=True, key='kpsp1_x', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/60_2.png')
                with col2:
                    st.empty()
                    kpsp2_value = st.session_state.input_data.get('KPSP2', '')
                    if pd.isna(kpsp1_value):
                        kpsp2_x = st.radio('kpsp2', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp2_x', label_visibility='collapsed')
                    else:
                        kpsp2_x = st.radio('kpsp2', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp2_value), horizontal=True, key='kpsp2_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/60_3.png')
                with col2:
                    st.empty()
                    kpsp3_value = st.session_state.input_data.get('KPSP3', '')
                    if pd.isna(kpsp1_value):
                        kpsp3_x = st.radio('kpsp3', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp3_x', label_visibility='collapsed')
                    else:
                        kpsp3_x = st.radio('kpsp3', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp3_value), horizontal=True, key='kpsp3_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/60_4.png')
                with col2:
                    st.empty()
                    kpsp4_value = st.session_state.input_data.get('KPSP4', '')
                    if pd.isna(kpsp4_value):
                        kpsp4_x = st.radio('kpsp4', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp4_x', label_visibility='collapsed')
                    else:
                        kpsp4_x = st.radio('kpsp4', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp4_value), horizontal=True, key='kpsp4_x', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/60_5.png')
                with col2:
                    st.empty()
                    kpsp5_value = st.session_state.input_data.get('KPSP5', '')
                    if pd.isna(kpsp5_value):
                        kpsp5_x = st.radio('kpsp5', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp5_x', label_visibility='collapsed')
                    else:
                        kpsp5_x = st.radio('kpsp5', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp5_value), horizontal=True, key='kpsp5_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/60_6.png')
                with col2:
                    st.empty()
                    kpsp6_value = st.session_state.input_data.get('KPSP6', '')
                    if pd.isna(kpsp6_value):
                        kpsp6_x = st.radio('kpsp6', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp6_x', label_visibility='collapsed')
                    else:
                        kpsp6_x = st.radio('kpsp6', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp6_value), horizontal=True, key='kpsp6_x', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/60_7.png')
                with col2:
                    st.empty()
                    kpsp7_value = st.session_state.input_data.get('KPSP7', '')
                    if pd.isna(kpsp7_value):
                        kpsp7_x = st.radio('kpsp7', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp7_x', label_visibility='collapsed')
                    else:
                        kpsp7_x = st.radio('kpsp7', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp7_value), horizontal=True, key='kpsp7_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/60_8.png')
                with col2:
                    st.empty()
                    kpsp8_value = st.session_state.input_data.get('KPSP8', '')
                    if pd.isna(kpsp8_value):
                        kpsp8_x = st.radio('kpsp8', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp8_x', label_visibility='collapsed')
                    else:
                        kpsp8_x = st.radio('kpsp8', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp8_value), horizontal=True, key='kpsp8_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/60_9.png')
                with col2:
                    st.empty()
                    kpsp9_value = st.session_state.input_data.get('KPSP9', '')
                    if pd.isna(kpsp9_value):
                        kpsp9_x = st.radio('kpsp9', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp9_x', label_visibility='collapsed')
                    else:
                        kpsp9_x = st.radio('kpsp9', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp9_value), horizontal=True, key='kpsp9_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/60_10.png')
                with col2:
                    st.empty()
                    kpsp10_value = st.session_state.input_data.get('KPSP10', '')
                    if pd.isna(kpsp10_value):
                        kpsp10_x = st.radio('kpsp10', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp10_x', label_visibility='collapsed')
                    else:
                        kpsp10_x = st.radio('kpsp10', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp10_value), horizontal=True, key='kpsp10_x', label_visibility='collapsed')
                    
            elif 66 <= usia_bln < 72:

                st.write('### KPSP Umur 66 bulan')

                # Membuat kolom untuk menempatkan caption di kiri dan opsi di kanan
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Menentukan lebar kolom (3 bagian untuk caption, 1 bagian untuk opsi)

                with col1:
                    st.image('.img/66_1.png')
                with col2:
                    st.empty()
                    kpsp1_value = st.session_state.input_data.get('KPSP1', '')
                    if pd.isna(kpsp1_value):
                        kpsp1_x = st.radio('kpsp1', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp1_x', label_visibility='collapsed')
                    else:
                        kpsp1_x = st.radio('kpsp1', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp1_value), horizontal=True, key='kpsp1_x', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/66_2.png')
                with col2:
                    st.empty()
                    kpsp2_value = st.session_state.input_data.get('KPSP2', '')
                    if pd.isna(kpsp1_value):
                        kpsp2_x = st.radio('kpsp2', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp2_x', label_visibility='collapsed')
                    else:
                        kpsp2_x = st.radio('kpsp2', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp2_value), horizontal=True, key='kpsp2_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/66_3.png')
                with col2:
                    st.empty()
                    kpsp3_value = st.session_state.input_data.get('KPSP3', '')
                    if pd.isna(kpsp1_value):
                        kpsp3_x = st.radio('kpsp3', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp3_x', label_visibility='collapsed')
                    else:
                        kpsp3_x = st.radio('kpsp3', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp3_value), horizontal=True, key='kpsp3_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/66_4.png')
                with col2:
                    st.empty()
                    kpsp4_value = st.session_state.input_data.get('KPSP4', '')
                    if pd.isna(kpsp4_value):
                        kpsp4_x = st.radio('kpsp4', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp4_x', label_visibility='collapsed')
                    else:
                        kpsp4_x = st.radio('kpsp4', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp4_value), horizontal=True, key='kpsp4_x', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/66_5.png')
                with col2:
                    st.empty()
                    kpsp5_value = st.session_state.input_data.get('KPSP5', '')
                    if pd.isna(kpsp5_value):
                        kpsp5_x = st.radio('kpsp5', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp5_x', label_visibility='collapsed')
                    else:
                        kpsp5_x = st.radio('kpsp5', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp5_value), horizontal=True, key='kpsp5_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/66_6.png')
                with col2:
                    st.empty()
                    kpsp6_value = st.session_state.input_data.get('KPSP6', '')
                    if pd.isna(kpsp6_value):
                        kpsp6_x = st.radio('kpsp6', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp6_x', label_visibility='collapsed')
                    else:
                        kpsp6_x = st.radio('kpsp6', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp6_value), horizontal=True, key='kpsp6_x', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/66_7.png')
                with col2:
                    st.empty()
                    kpsp7_value = st.session_state.input_data.get('KPSP7', '')
                    if pd.isna(kpsp7_value):
                        kpsp7_x = st.radio('kpsp7', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp7_x', label_visibility='collapsed')
                    else:
                        kpsp7_x = st.radio('kpsp7', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp7_value), horizontal=True, key='kpsp7_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/66_8.png')
                with col2:
                    st.empty()
                    kpsp8_value = st.session_state.input_data.get('KPSP8', '')
                    if pd.isna(kpsp8_value):
                        kpsp8_x = st.radio('kpsp8', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp8_x', label_visibility='collapsed')
                    else:
                        kpsp8_x = st.radio('kpsp8', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp8_value), horizontal=True, key='kpsp8_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/66_9.png')
                with col2:
                    st.empty()
                    kpsp9_value = st.session_state.input_data.get('KPSP9', '')
                    if pd.isna(kpsp9_value):
                        kpsp9_x = st.radio('kpsp9', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp9_x', label_visibility='collapsed')
                    else:
                        kpsp9_x = st.radio('kpsp9', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp9_value), horizontal=True, key='kpsp9_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/66_10.png')
                with col2:
                    st.empty()
                    kpsp10_value = st.session_state.input_data.get('KPSP10', '')
                    if pd.isna(kpsp10_value):
                        kpsp10_x = st.radio('kpsp10', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp10_x', label_visibility='collapsed')
                    else:
                        kpsp10_x = st.radio('kpsp10', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp10_value), horizontal=True, key='kpsp10_x', label_visibility='collapsed')
                    
            elif usia_bln >= 72:

                st.write('### KPSP Umur 72 bulan')

                # Membuat kolom untuk menempatkan caption di kiri dan opsi di kanan
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Menentukan lebar kolom (3 bagian untuk caption, 1 bagian untuk opsi)

                with col1:
                    st.image('.img/72_1.png')
                with col2:
                    st.empty()
                    kpsp1_value = st.session_state.input_data.get('KPSP1', '')
                    if pd.isna(kpsp1_value):
                        kpsp1_x = st.radio('kpsp1', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp1_x', label_visibility='collapsed')
                    else:
                        kpsp1_x = st.radio('kpsp1', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp1_value), horizontal=True, key='kpsp1_x', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/72_2.png')
                with col2:
                    st.empty()
                    kpsp2_value = st.session_state.input_data.get('KPSP2', '')
                    if pd.isna(kpsp1_value):
                        kpsp2_x = st.radio('kpsp2', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp2_x', label_visibility='collapsed')
                    else:
                        kpsp2_x = st.radio('kpsp2', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp2_value), horizontal=True, key='kpsp2_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/72_3.png')
                with col2:
                    st.empty()
                    kpsp3_value = st.session_state.input_data.get('KPSP3', '')
                    if pd.isna(kpsp1_value):
                        kpsp3_x = st.radio('kpsp3', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp3_x', label_visibility='collapsed')
                    else:
                        kpsp3_x = st.radio('kpsp3', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp3_value), horizontal=True, key='kpsp3_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/72_4.png')
                with col2:
                    st.empty()
                    kpsp4_value = st.session_state.input_data.get('KPSP4', '')
                    if pd.isna(kpsp4_value):
                        kpsp4_x = st.radio('kpsp4', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp4_x', label_visibility='collapsed')
                    else:
                        kpsp4_x = st.radio('kpsp4', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp4_value), horizontal=True, key='kpsp4_x', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/72_5.png')
                with col2:
                    st.empty()
                    kpsp5_value = st.session_state.input_data.get('KPSP5', '')
                    if pd.isna(kpsp5_value):
                        kpsp5_x = st.radio('kpsp5', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp5_x', label_visibility='collapsed')
                    else:
                        kpsp5_x = st.radio('kpsp5', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp5_value), horizontal=True, key='kpsp5_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/72_6.png')
                with col2:
                    st.empty()
                    kpsp6_value = st.session_state.input_data.get('KPSP6', '')
                    if pd.isna(kpsp6_value):
                        kpsp6_x = st.radio('kpsp6', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp6_x', label_visibility='collapsed')
                    else:
                        kpsp6_x = st.radio('kpsp6', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp6_value), horizontal=True, key='kpsp6_x', label_visibility='collapsed')

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/72_7.png')
                with col2:
                    st.empty()
                    kpsp7_value = st.session_state.input_data.get('KPSP7', '')
                    if pd.isna(kpsp7_value):
                        kpsp7_x = st.radio('kpsp7', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp7_x', label_visibility='collapsed')
                    else:
                        kpsp7_x = st.radio('kpsp7', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp7_value), horizontal=True, key='kpsp7_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/72_8.png')
                with col2:
                    st.empty()
                    kpsp8_value = st.session_state.input_data.get('KPSP8', '')
                    if pd.isna(kpsp8_value):
                        kpsp8_x = st.radio('kpsp8', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp8_x', label_visibility='collapsed')
                    else:
                        kpsp8_x = st.radio('kpsp8', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp8_value), horizontal=True, key='kpsp8_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/72_9.png')
                with col2:
                    st.empty()
                    kpsp9_value = st.session_state.input_data.get('KPSP9', '')
                    if pd.isna(kpsp9_value):
                        kpsp9_x = st.radio('kpsp9', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp9_x', label_visibility='collapsed')
                    else:
                        kpsp9_x = st.radio('kpsp9', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp9_value), horizontal=True, key='kpsp9_x', label_visibility='collapsed')
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/72_10.png')
                with col2:
                    st.empty()
                    kpsp10_value = st.session_state.input_data.get('KPSP10', '')
                    if pd.isna(kpsp10_value):
                        kpsp10_x = st.radio('kpsp10', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp10_x', label_visibility='collapsed')
                    else:
                        kpsp10_x = st.radio('kpsp10', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(kpsp10_value), horizontal=True, key='kpsp10_x', label_visibility='collapsed')
            
            else:
                # st.warning('Bukan Termasuk Kriteria Umur Untuk Pemeriksaan KPSP')
                st.write('### KPSP Umur 3 bulan')

                # Membuat kolom untuk menempatkan caption di kiri dan opsi di kanan
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Menentukan lebar kolom (3 bagian untuk caption, 1 bagian untuk opsi)

                with col1:
                    st.image('.img/3_1.png')
                with col2:
                    st.empty()
                    kpsp1_x = st.radio('kpsp1', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp1_x', label_visibility='collapsed', disabled=True)

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/3_2.png')
                with col2:
                    st.empty()
                    kpsp2_x = st.radio('kpsp2', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp2_x', label_visibility='collapsed', disabled=True)
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/3_3.png')
                with col2:
                    st.empty()
                    kpsp3_x = st.radio('kpsp3', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp3_x', label_visibility='collapsed', disabled=True)
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/3_4.png')
                with col2:
                    st.empty()
                    kpsp4_x = st.radio('kpsp4', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp4_x', label_visibility='collapsed', disabled=True)

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/3_5.png')
                with col2:
                    st.empty()
                    kpsp5_x = st.radio('kpsp5', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp5_x', label_visibility='collapsed', disabled=True)
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/3_6.png')
                with col2:
                    st.empty()
                    kpsp6_x = st.radio('kpsp6', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp6_x', label_visibility='collapsed', disabled=True)

                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/3_7.png')
                with col2:
                    st.empty()
                    kpsp7_x = st.radio('kpsp7', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp7_x', label_visibility='collapsed', disabled=True)
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/3_8.png')
                with col2:
                    st.empty()
                    kpsp8_x = st.radio('kpsp8', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp8_x', label_visibility='collapsed', disabled=True)
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/3_9.png')
                with col2:
                    st.empty()
                    kpsp9_x = st.radio('kpsp9', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp9_x', label_visibility='collapsed', disabled=True)
                    
                col1, col2 = st.columns([3, 1], vertical_alignment="top", border=True)  # Kolom baru untuk pertanyaan selanjutnya

                with col1:
                    st.image('.img/3_10.png')
                with col2:
                    st.empty()
                    kpsp10_x = st.radio('kpsp10', ['Ya', 'Tidak'], index=None, horizontal=True, key='kpsp10_x', label_visibility='collapsed', disabled=True)
                
            
            def calculate_score(kpsp1_x, kpsp2_x, kpsp3_x, kpsp4_x, kpsp5_x, kpsp6_x, kpsp7_x, kpsp8_x, kpsp9_x, kpsp10_x):
                score = 0
                # Penentuan skor
                if kpsp1_x == 'Ya':
                    score += 1
                elif kpsp1_x == 'Tidak':
                    score += 0

                if kpsp2_x == 'Ya':
                    score += 1
                elif kpsp2_x == 'Tidak':
                    score += 0
                    
                if kpsp3_x == 'Ya':
                    score += 1
                elif kpsp3_x == 'Tidak':
                    score += 0
                    
                if kpsp4_x == 'Ya':
                    score += 1
                elif kpsp4_x == 'Tidak':
                    score += 0
                    
                if kpsp5_x == 'Ya':
                    score += 1
                elif kpsp5_x == 'Tidak':
                    score += 0
                    
                if kpsp6_x == 'Ya':
                    score += 1
                elif kpsp6_x == 'Tidak':
                    score += 0
                    
                if kpsp7_x == 'Ya':
                    score += 1
                elif kpsp7_x == 'Tidak':
                    score += 0
                    
                if kpsp8_x == 'Ya':
                    score += 1
                elif kpsp8_x == 'Tidak':
                    score += 0
                    
                if kpsp9_x == 'Ya':
                    score += 1
                elif kpsp9_x == 'Tidak':
                    score += 0
                    
                if kpsp10_x == 'Ya':
                    score += 1
                elif kpsp10_x == 'Tidak':
                    score += 0

                return score
                
            # Hitung total skor
            total_score = calculate_score(kpsp1_x, kpsp2_x, kpsp3_x, kpsp4_x, kpsp5_x, kpsp6_x, kpsp7_x, kpsp8_x, kpsp9_x, kpsp10_x)

            if 9 <= total_score <= 10:
                kesimpulan_kpsp_x = st.text_input('Kesimpulan KPSP', value='Sesuai Umur', disabled=True, key='kesimpulan_kpsp_x')
            elif 7 <= total_score <= 8:
                kesimpulan_kpsp_x = st.text_input('Kesimpulan KPSP', value='Meragukan', disabled=True, key='kesimpulan_kpsp_x')
            elif 0 <= total_score <= 6:
                kesimpulan_kpsp_x = st.text_input('Kesimpulan KPSP', value='Ada Kemungkinan Penyimpangan', disabled=True, key='kesimpulan_kpsp_x')
            else:
                kesimpulan_kpsp_x = st.text_input('Kesimpulan KPSP', value=None, disabled=True, key='kesimpulan_kpsp_x')
                    
        with st.expander('**SKRINING DIABETES**'):
            left, right = st.columns(2)
            dm1_value = st.session_state.input_data.get('DM1', '')
            if pd.isna(dm1_value):
                dm1_x = left.radio('Apakah anak anda sering lapar atau banyak makan dalam 1 bulan terakhir?', ['Ya', 'Tidak'], index=None, horizontal=True, key='dm1_x')
            else:
                dm1_x = left.radio('Apakah anak anda sering lapar atau banyak makan dalam 1 bulan terakhir?', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(dm1_value), horizontal=True, key='dm1_x')
            
            dm2_value = st.session_state.input_data.get('DM2', '')
            if pd.isna(dm2_value):
                dm2_x = left.radio('Apakah anak anda sering haus atau banyak minum dalam 1 bulan terakhir?', ['Ya', 'Tidak'], index=None, horizontal=True, key='dm2_x')
            else:
                dm2_x = left.radio('Apakah anak anda sering haus atau banyak minum dalam 1 bulan terakhir?', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(dm2_value), horizontal=True, key='dm2_x')
            
            dm3_value = st.session_state.input_data.get('DM3', '')
            if pd.isna(dm3_value):   
                dm3_x = left.radio('Apakah anak anda sering BAK dalam 1 bulan terakhir?', ['Ya', 'Tidak'], index=None, horizontal=True, key='dm3_x')
            else:
                dm3_x = left.radio('Apakah anak anda sering BAK dalam 1 bulan terakhir?', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(dm3_value), horizontal=True, key='dm3_x')
            
            dm4_value = st.session_state.input_data.get('DM4', '')
            if pd.isna(dm4_value):
                dm4_x = right.radio('Apakah anak anda sering mengompol dalam 1 bulan terakhir', ['Ya', 'Tidak'], index=None, horizontal=True, key='dm4_x')
            else:
                dm4_x = right.radio('Apakah anak anda sering mengompol dalam 1 bulan terakhir', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(dm4_value), horizontal=True, key='dm4_x')
                
            dm5_value = st.session_state.input_data.get('DM5', '')
            if pd.isna(dm5_value):
                dm5_x = right.radio('Apakah berat badan anak anda turun secara drastis?', ['Ya', 'Tidak'], index=None, horizontal=True, key='dm5_x')
            else:
                dm5_x = right.radio('Apakah berat badan anak anda turun secara drastis?', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(dm5_value), horizontal=True, key='dm5_x')
                
            dm6_value = st.session_state.input_data.get('DM6', '')
            if pd.isna(dm6_value):
                dm6_x = right.radio('Apakah orangtua memiliki riwayat penyakit diabetes?', ['Ya', 'Tidak'], index=None, horizontal=True, key='dm6_x')
            else:
                dm6_x = right.radio('Apakah orangtua memiliki riwayat penyakit diabetes?', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(dm6_value), horizontal=True, key='dm6_x')

        with st.expander('**SKRINING TALASEMIA**'):
            talasemia1_value = st.session_state.input_data.get('Talasemia1', '')
            if pd.isna(talasemia1_value):
                talasemia1_x = st.radio('Apakah ada anggota keluarga kandung  Anda dinyatakan menderita Talasemia,  atau kelainan darah atau pernah menjalani transfusi darah secara rutin?', ['Ya', 'Tidak'], index=None, horizontal=True, key='talasemia1_x')
            else:
                talasemia1_x = st.radio('Apakah ada anggota keluarga kandung  Anda dinyatakan menderita Talasemia,  atau kelainan darah atau pernah menjalani transfusi darah secara rutin?', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(talasemia1_value), horizontal=True, key='talasemia1_x')
            
            talasemia2_value = st.session_state.input_data.get('Talasemia2', '')
            if pd.isna(talasemia2_value):
                talasemia2_x = st.radio('Apakah ada anggota keluarga  kandung Anda dinyatakan sebagai pembawa sifat talasemia (mereka yang memiliki genetik yang tidak normal sehingga berpotensi menurunkan penyakit Talasemia)?', ['Ya', 'Tidak'], index=None, horizontal=True, key='talasemia2_x')
            else:
                talasemia2_x = st.radio('Apakah ada anggota keluarga  kandung Anda dinyatakan sebagai pembawa sifat talasemia (mereka yang memiliki genetik yang tidak normal sehingga berpotensi menurunkan penyakit Talasemia)?', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(talasemia2_value), horizontal=True, key='talasemia2_x')

        with st.expander('**SKRINING TB**'):
            tb1_value = st.session_state.input_data.get('TB1', '')
            if pd.isna(tb1_value):
                tb1_x = st.radio('Apakah anak Anda pernah atau sedang mengalami batuk yang tidak sembuh-sembuh selama lebih dari 2 minggu?', ['Ya', 'Tidak'], index=None, horizontal=True, key='tb1_x')
            else:
                tb1_x = st.radio('Apakah anak Anda pernah atau sedang mengalami batuk yang tidak sembuh-sembuh selama lebih dari 2 minggu?', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(tb1_value), horizontal=True, key='tb1_x')
            
            tb2_value = st.session_state.input_data.get('TB2', '')
            if pd.isna(tb2_value):
                tb2_x = st.radio('Apakah berat badan anak Anda turun tanpa alasan yang jelas?', ['Ya', 'Tidak'], index=None, horizontal=True, key='tb2_x')
            else:
                tb2_x = st.radio('Apakah berat badan anak Anda turun tanpa alasan yang jelas?', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(tb2_value), horizontal=True, key='tb2_x')
            
            tb3_value = st.session_state.input_data.get('TB3', '')
            if pd.isna(tb3_value):
                tb3_x = st.radio('Apakah berat badan anak Anda tidak naik dalam dua bulan terakhir?', ['Ya', 'Tidak'], index=None, horizontal=True, key='tb3_x')
            else:
                tb3_x = st.radio('Apakah berat badan anak Anda tidak naik dalam dua bulan terakhir?', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(tb3_value), horizontal=True, key='tb3_x')
            
            tb4_value = st.session_state.input_data.get('TB4', '')
            if pd.isna(tb4_value):
                tb4_x = st.radio('Apakah anak Anda tidak atau berkurang nafsu makan?', ['Ya', 'Tidak'], index=None, horizontal=True, key='tb4_x')
            else:
                tb4_x = st.radio('Apakah anak Anda tidak atau berkurang nafsu makan?', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(tb4_value), horizontal=True, key='tb4_x')
            
            tb5_value = st.session_state.input_data.get('TB5', '')
            if pd.isna(tb5_value):
                tb5_x = st.radio ('Apakah Anda tinggal serumah atau sering bertemu dengan orang yang menderita Tuberkulosis (TBC) atau batuk berkepanjangan?', ['Ya', 'Tidak'], index=None, horizontal=True, key='tb5_x')
            else:
                tb5_x = st.radio ('Apakah Anda tinggal serumah atau sering bertemu dengan orang yang menderita Tuberkulosis (TBC) atau batuk berkepanjangan?', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(tb5_value), horizontal=True, key='tb5_x')
        
        with st.expander('**SKRINING MATA DAN TELINGA**'):
            left, right = st.columns(2)
            visusod_value = st.session_state.input_data.get('Visus OD', '')
            if pd.isna(visusod_value):
                visusod_x = left.text_input('Visus OD', value=None, key='visusod_x')
            else:
                visusod_x = left.text_input('Visus OD', value=visusod_value, key='visusod_x')
                
            visusos_value = st.session_state.input_data.get('Visus OS', '')
            if pd.isna(visusos_value):
                visusos_x = right.text_input('Visus OS', value=None, key='visusos_x')
            else:
                visusos_x = right.text_input('Visus OS', value=visusos_value, key='visusos_x')
                
            pupil_putih_od_value = st.session_state.input_data.get('Pupil Putih OD', '')
            if pd.isna(pupil_putih_od_value):
                pupil_putih_od_x = left.radio('Pemeriksaan Pupil Putih OD', ['Negatif', 'Positif'], index=None, horizontal=True, key='pupil_putih_od_x')
            else:
                pupil_putih_od_x = left.radio('Pemeriksaan Pupil Putih OD', ['Negatif', 'Positif'], index= ['Negatif', 'Positif'].index(pupil_putih_od_value), horizontal=True, key='pupil_putih_od_x')
            
            pupil_putih_os_value = st.session_state.input_data.get('Pupil Putih OS', '')
            if pd.isna(pupil_putih_os_value):
                pupil_putih_os_x = right.radio('Pemeriksaan Pupil Putih OS', ['Negatif', 'Positif'], index=None, horizontal=True, key='pupil_putih_os_x')
            else:
                pupil_putih_os_x = right.radio('Pemeriksaan Pupil Putih OS', ['Negatif', 'Positif'], index= ['Negatif', 'Positif'].index(pupil_putih_os_value), horizontal=True, key='pupil_putih_os_x')
            
            if usia_bln <=3:
                st.write('***Tes Daya Dengar umur <= 3 bulan***')
                tdd1_value = st.session_state.input_data.get('TDD1', '')
                if pd.isna(tdd1_value):
                    tdd1_x = st.radio('''Apakah bayi dapat mengatakan "Aaaaa", "Oooo"?
                            \nApakah bayi menatap wajah dan tampak mendenagrkan Anda, lalu berbicara saat anda diam?
                            \nApakah anda sesolah-olah berbicara dengan bayi anda?''', ['Ya', 'Tidak'], index=None, horizontal=True, key='tdd1_x')
                else:
                    tdd1_x = st.radio('''Apakah bayi dapat mengatakan "Aaaaa", "Oooo"?
                            \nApakah bayi menatap wajah dan tampak mendenagrkan Anda, lalu berbicara saat anda diam?
                            \nApakah anda sesolah-olah berbicara dengan bayi anda?''', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(tdd1_value), horizontal=True, key='tdd1_x')
                
                tdd2_value = st.session_state.input_data.get('TDD2', '')
                if pd.isna(tdd2_value):
                    tdd2_x = st.radio('''Apakah bayi kaget bila mendengar suara (mengejapkan mata, napas lebih cepat)?
                                \nApakah bayi kelihatan menoleh bila anda berbicara di sebelahnya?''', ['Ya', 'Tidak'], index=None, horizontal=True, key='tdd2_x')
                else:
                    tdd2_x = st.radio('''Apakah bayi kaget bila mendengar suara (mengejapkan mata, napas lebih cepat)?
                                \nApakah bayi kelihatan menoleh bila anda berbicara di sebelahnya?''', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(tdd2_index), horizontal=True, key='tdd2_x')
                    
                tdd3_value = st.session_state.input_data.get('TDD3', '')
                if pd.isna(tdd3_value):     
                    tdd3_x = st.radio('''Apakah bayi anda dapat tersenyum?
                                \nApakah bayi anda kenal dengan anda, seperti senyum lebih cepat pada anda dibandingkan orang lain?''', ['Ya', 'Tidak'], index=None, horizontal=True, key='tdd3_x')
                else:
                    tdd3_x = st.radio('''Apakah bayi anda dapat tersenyum?
                                \nApakah bayi anda kenal dengan anda, seperti senyum lebih cepat pada anda dibandingkan orang lain?''', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(tdd3_value), horizontal=True, key='tdd3_x')

            elif 3 < usia_bln <= 6:
                st.write('***Tes Daya Dengar umur 3-6 bulan***')
                tdd1_value = st.session_state.input_data.get('TDD1', '')
                if pd.isna(tdd1_value):
                    tdd1_x = st.radio('''Apakah bayi anda dapat tertawa keras?
                                    \nApakah bayi dapat bermain menggelembungkan mulut seperti meniup balon?''', ['Ya', 'Tidak'], index=None, horizontal=True, key='tdd1_x')
                else:
                        tdd1_x = st.radio('''Apakah bayi anda dapat tertawa keras?
                                    \nApakah bayi dapat bermain menggelembungkan mulut seperti meniup balon?''', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(tdd1_value), horizontal=True, key='tdd1_x')
                
                tdd2_value = st.session_state.input_data.get('TDD2', '')
                if pd.isna(tdd2_value):       
                    tdd2_x = st.radio('''Apakah bayi memberi respons tertentu, seperti menjadi lebih riang bila Anda datang? 
                                    \nPemeriksa duduk menghadap bayi yang dipangku orang tuanya, bunyikan bel disamping tanpa terlihat bayi, apakah bayi itu menoleh ke samping?''', ['Ya', 'Tidak'], index=None, horizontal=True, key='tdd2_x')
                else:
                    tdd2_x = st.radio('''Apakah bayi memberi respons tertentu, seperti menjadi lebih riang bila Anda datang? 
                                \nPemeriksa duduk menghadap bayi yang dipangku orang tuanya, bunyikan bel disamping tanpa terlihat bayi, apakah bayi itu menoleh ke samping?''', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(tdd2_value), horizontal=True, key='tdd2_x')
                
                tdd3_value = st.session_state.input_data.get('TDD3', '')
                if pd.isna(tdd3_value):
                    tdd3_x = st.radio('''Pemeriksa menatap mata bayi sekitar 45 cm, lalu gunakan mainan untuk menarik pandangan bayi ke kiri, kanan, atas, dan bawah. Apakah bayi dapat mengikutinya?
                                    \nApakah bayi berkedip bila pemeriksa melakukan gerakan menusuk mata, lalu berhenti sekitar 3 cm tanpa menyentuh mata? ''', ['Ya', 'Tidak'], index=None, horizontal=True, key='tdd3_x')
                else:
                    tdd3_x = st.radio('''Pemeriksa menatap mata bayi sekitar 45 cm, lalu gunakan mainan untuk menarik pandangan bayi ke kiri, kanan, atas, dan bawah. Apakah bayi dapat mengikutinya?
                                    \nApakah bayi berkedip bila pemeriksa melakukan gerakan menusuk mata, lalu berhenti sekitar 3 cm tanpa menyentuh mata? ''', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(tdd3_value), horizontal=True, key='tdd3_x')

            elif 6 < usia_bln <= 12:
                st.write('***Tes Daya Dengar 6-12 bulan***')
                tdd1_value = st.session_state.input_data.get('TDD1', '')
                if pd.isna(tdd1_value):
                    tdd1_x = st.radio('''Apakah bayi dapat membuat suara berulang seperti ‘mamamama’, ‘babababa’? 
                                    \nApakah bayi dapat memanggil mama atau papa, walaupun tidak untuk memanggil orang tuanya?''', ['Ya', 'Tidak'], index=None, horizontal=True, key='tdd1_x')
                else:
                    tdd1_x = st.radio('''Apakah bayi dapat membuat suara berulang seperti ‘mamamama’, ‘babababa’? 
                                    \nApakah bayi dapat memanggil mama atau papa, walaupun tidak untuk memanggil orang tuanya?''', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(tdd1_value), horizontal=True, key='tdd1_x')
                    
                tdd2_value = st.session_state.input_data.get('TDD2', '')
                if pd.isna(tdd2_value):   
                    tdd2_x = st.radio('''Pemeriksa duduk mengahadap bayi yang dipangku orang tuanya, bunyikan bel di samping bawah tanpa terlihat bayi, apakah bayi langsung menoleh ke samping bawah?
                                    \nApakah bayi mengikuti perintah tanpa dibantu gerakan badan, seperti “Stop, berikan mainanmu”?''', ['Ya', 'Tidak'], index=None, horizontal=True, key='tdd2_x')
                else:
                    tdd2_x = st.radio('''Pemeriksa duduk mengahadap bayi yang dipangku orang tuanya, bunyikan bel di samping bawah tanpa terlihat bayi, apakah bayi langsung menoleh ke samping bawah?
                                    \nApakah bayi mengikuti perintah tanpa dibantu gerakan badan, seperti “Stop, berikan mainanmu”?''', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(tdd2_value), horizontal=True, key='tdd2_x')
                
                tdd3_value = st.session_state.input_data.get('TDD3', '')
                if pd.isna(tdd3_value):
                    tdd3_x = st.radio('''Apakah bayi mengikuti perintah dengan dibantu gerakan badan, seperti “Stop, berikan mainanmu”?
                                    \nApakah bayi secara spontan memulai permainan dengan gerakan tubuh, seperti ‘Pok Ame-Ame’ atau ‘Cilukba’? ''', ['Ya', 'Tidak'], index=None, horizontal=True, key='tdd3_x')
                else:
                    tdd3_x = st.radio('''Apakah bayi mengikuti perintah dengan dibantu gerakan badan, seperti “Stop, berikan mainanmu”?
                                    \nApakah bayi secara spontan memulai permainan dengan gerakan tubuh, seperti ‘Pok Ame-Ame’ atau ‘Cilukba’? ''', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(tdd3_value), horizontal=True, key='tdd3_x')

            elif 12 < usia_bln <=18:
                st.write('***Tes Daya Dengar 12-18 bulan***')
                tdd1_value = st.session_state.input_data.get('TDD1', '')
                if pd.isna(tdd1_value):
                    tdd1_x = st.radio('''Apakah anak dapat memanggil ‘mama’ atau ‘papa’, hanya untuk memanggil orang tuanya?
                                    \nApakah anak memulai menggunakan kata-kata lain, selain kata ‘mama’, ‘papa’, anggota keluarga lain, dan hewan peliharaan?''', ['Ya', 'Tidak'], index=None, horizontal=True, key='tdd1_x')
                else:
                    tdd1_x = st.radio('''Apakah anak dapat memanggil ‘mama’ atau ‘papa’, hanya untuk memanggil orang tuanya?
                                    \nApakah anak memulai menggunakan kata-kata lain, selain kata ‘mama’, ‘papa’, anggota keluarga lain, dan hewan peliharaan?''', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(tdd1_value), horizontal=True, key='tdd1_x')
                
                tdd2_value = st.session_state.input_data.get('TDD2', '')
                if pd.isna(tdd2_value):    
                    tdd2_x = st.radio('''Pemeriksa duduk menghadap bayi yang dipangku orang tuanya, bunyikan bel di samping bawah tanpa terlihat bayi, apakah bayi langsung menoleh ke samping bawah?
                                    \nApakah anak mengikuti perintah tanpa dibantu gerakan badan, seperti “Stop, berikan mainanmu”?''', ['Ya', 'Tidak'], index=None, horizontal=True, key='tdd2_x')
                else:
                    tdd2_x = st.radio('''Pemeriksa duduk menghadap bayi yang dipangku orang tuanya, bunyikan bel di samping bawah tanpa terlihat bayi, apakah bayi langsung menoleh ke samping bawah?
                                    \nApakah anak mengikuti perintah tanpa dibantu gerakan badan, seperti “Stop, berikan mainanmu”?''', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(tdd2_value), horizontal=True, key='tdd2_x')
                
                tdd3_value = st.session_state.input_data.get('TDD3', '')
                if pd.isna(tdd3_value):
                    tdd3_x = st.radio('''Apakah anak secara spontan memulai permainan dengan gerakan tubuh, seperti ‘Pok Ame-Ame’ atau ‘Cilukba’?
                                    \nApakah anak Anda menunjuk dengan jari telunjuk bila ingin sesuatu, bukan dengan cara memegang dengan semua jari?''', ['Ya', 'Tidak'], index=None, horizontal=True, key='tdd3_x')
                else:
                    tdd3_x = st.radio('''Apakah anak secara spontan memulai permainan dengan gerakan tubuh, seperti ‘Pok Ame-Ame’ atau ‘Cilukba’?
                                    \nApakah anak Anda menunjuk dengan jari telunjuk bila ingin sesuatu, bukan dengan cara memegang dengan semua jari?''', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(tdd3_value), horizontal=True, key='tdd3_x')

            elif 18 < usia_bln <= 24:
                st.write('***Tes Daya Dengar 18-24 bulan***')
                tdd1_value = st.session_state.input_data.get('TDD1', '')
                if pd.isna(tdd1_value):
                    tdd1_x = st.radio('''Apakah anak dapat mengucapkan 2 atau lebih kata yang menunjukkan keinginan, seperti “Susu”, “Minum”, “Lagi”? 
                                    \nApakah anak secara spontan mengatakan 2 kombinasi kata, seperti “Mau bobo”, “Lihat Papa”?''', ['Ya', 'Tidak'], index=None, horizontal=True, key='tdd1_x')
                else:
                    tdd1_x = st.radio('''Apakah anak dapat mengucapkan 2 atau lebih kata yang menunjukkan keinginan, seperti “Susu”, “Minum”, “Lagi”? 
                                    \nApakah anak secara spontan mengatakan 2 kombinasi kata, seperti “Mau bobo”, “Lihat Papa”?''', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(tdd1_value), horizontal=True, key='tdd1_x')
                
                tdd2_value = st.session_state.input_data.get('TDD2', '')
                if pd.isna(tdd2_value):    
                    tdd2_x = st.radio('''Apakah anak dapat menunjukkan paling sedikit 1 anggota badan, misal “Mana hidungmu?”, “Mana matamu?” tanpa diberi contoh?
                                    \nApakah anak dapat mengerjakan 2 macam perintah dalam satu kalimat, seperti “Ambil sepatumu dan taruh disini” tanpa diberi contoh?''', ['Ya', 'Tidak'], index=None, horizontal=True, key='tdd2_x')
                else:
                    tdd2_x = st.radio('''Apakah anak dapat menunjukkan paling sedikit 1 anggota badan, misal “Mana hidungmu?”, “Mana matamu?” tanpa diberi contoh?
                                    \nApakah anak dapat mengerjakan 2 macam perintah dalam satu kalimat, seperti “Ambil sepatumu dan taruh disini” tanpa diberi contoh?''', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(tdd2_value), horizontal=True, key='tdd2_x')
                
                tdd3_value = st.session_state.input_data.get('TDD3', '')
                if pd.isna(tdd3_value):
                    tdd3_x = st.radio('''Apakah anak secara spontan memulai permainan dengan gerakan tubuh, seperti ‘Pok Ame-Ame’ atau ‘Cilukba’?
                                    \nApakah anak Anda menunjuk dengan jari telunjuk bila ingin sesuatu, bukan dengan cara memegang dengan semua jari?''', ['Ya', 'Tidak'], index=None, horizontal=True, key='tdd3_x')
                else:
                    tdd3_x = st.radio('''Apakah anak secara spontan memulai permainan dengan gerakan tubuh, seperti ‘Pok Ame-Ame’ atau ‘Cilukba’?
                                    \nApakah anak Anda menunjuk dengan jari telunjuk bila ingin sesuatu, bukan dengan cara memegang dengan semua jari?''', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(tdd3_value), horizontal=True, key='tdd3_x')

            elif 24 < usia_bln <= 30:
                st.write('***Tes Daya Dengar 24-30 bulan***')
                tdd1_value = st.session_state.input_data.get('TDD1', '')
                if pd.isna(tdd1_value):
                    tdd1_x = st.radio('''Apakah anak mulai menggunakan kata-kata lain, selain kata ‘mama’, ‘papa’, anggota keluarga lain, dan hewan peliharaan?
                                    \nApakah anak mulai mengungkapkan kata yang berarti ‘milik’ misal “Susu kamu”, “Bonekaku”? ''', ['Ya', 'Tidak'], index=None, horizontal=True, key='tdd1_x')
                else:
                    tdd1_x = st.radio('''Apakah anak mulai menggunakan kata-kata lain, selain kata ‘mama’, ‘papa’, anggota keluarga lain, dan hewan peliharaan?
                                    \nApakah anak mulai mengungkapkan kata yang berarti ‘milik’ misal “Susu kamu”, “Bonekaku”? ''', ['Ya', 'Tidak'], index=['Ya', 'Tidak'].index(tdd1_value), horizontal=True, key='tdd1_x')
                
                tdd2_value = st.session_state.input_data.get('TDD2', '')
                if pd.isna(tdd2_value):   
                    tdd2_x = st.radio('''Apakah anak dapat mengerjakan 2 macam perintah dalam satu kalimat, seperti “Ambil sepatu dan taruh disini” tanpa diberi contoh?
                                    \nApakah anak dapat menunjuk minimal 2 nama benda di depannya (cangkir, bola, sendok)?''', ['Ya', 'Tidak'], index=None, horizontal=True, key='tdd2_x')
                else:
                    tdd2_x = st.radio('''Apakah anak dapat mengerjakan 2 macam perintah dalam satu kalimat, seperti “Ambil sepatu dan taruh disini” tanpa diberi contoh?
                                    \nApakah anak dapat menunjuk minimal 2 nama benda di depannya (cangkir, bola, sendok)?''', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(tdd2_value), horizontal=True, key='tdd2_x')
                
                tdd3_value = st.session_state.input_data.get('TDD3', '')
                if pd.isna(tdd3_value):
                    tdd3_x = st.radio('''Apakah anak secara spontan memulai permainan dengan gerakan tubuh, seperti ‘Pok Ame-Ame’ atau ‘Cilukba’?
                                    \nApakah anak Anda menunjuk dengan jari telunjuk bila ingin sesuatu, bukan dengan cara memegang dengan semua jari?''', ['Ya', 'Tidak'], index=None, horizontal=True, key='tdd3_x')
                else:
                    tdd3_x = st.radio('''Apakah anak secara spontan memulai permainan dengan gerakan tubuh, seperti ‘Pok Ame-Ame’ atau ‘Cilukba’?
                                    \nApakah anak Anda menunjuk dengan jari telunjuk bila ingin sesuatu, bukan dengan cara memegang dengan semua jari?''', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(tdd3_value), horizontal=True, key='tdd3_x')

            elif 30 < usia_bln <= 36:
                st.write('***Tes Daya Dengar 30-36 bulan***')
                tdd1_value = st.session_state.input_data.get('TDD1', '')
                if pd.isna(tdd1_value):
                    tdd1_x = st.radio('''Apakah anak dapat menyebutkan nama benda dan kegunaannya, seperi cangkir untuk minum, bola untuk dilempar, pensil warna untuk menggambar, sendok untuk makan?
                                    \nApakah lebih dari tiga perempat orang mengerti apa yang dibicarakan anak Anda?''', ['Ya', 'Tidak'], index=None, horizontal=True, key='tdd1_x')
                else:
                    tdd1_x = st.radio('''Apakah anak dapat menyebutkan nama benda dan kegunaannya, seperi cangkir untuk minum, bola untuk dilempar, pensil warna untuk menggambar, sendok untuk makan?
                                    \nApakah lebih dari tiga perempat orang mengerti apa yang dibicarakan anak Anda?''', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(tdd1_value), horizontal=True, key='tdd1_x')
                
                tdd2_value = st.session_state.input_data.get('TDD2', '')
                if pd.isna(tdd2_value):   
                    tdd2_x = st.radio('''Apakah anak dapat menunjukkan minimal 2 nama benda di depannya sesuai fungsinya (misal untuk minum: cangkir, untuk dilempar: bola, untuk makan: sendok, untuk menggambar: pensil warna)?
                                    \nApakah anak dapat mengerjakan perintah yang disertai kata depan? (misal: “Sekarang kubus itu di bawah meja, tolong taruh di atas meja”)?''', ['Ya', 'Tidak'], index=None, horizontal=True, key='tdd2_x')
                else:
                    tdd2_x = st.radio('''Apakah anak dapat menunjukkan minimal 2 nama benda di depannya sesuai fungsinya (misal untuk minum: cangkir, untuk dilempar: bola, untuk makan: sendok, untuk menggambar: pensil warna)?
                                    \nApakah anak dapat mengerjakan perintah yang disertai kata depan? (misal: “Sekarang kubus itu di bawah meja, tolong taruh di atas meja”)?''', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(tdd2_value), horizontal=True, key='tdd2_x')
                    
                tdd3_value = st.session_state.input_data.get('TDD3', '')
                if pd.isna(tdd3_value):
                    tdd3_x = st.radio('''Apakah anak secara spontan memulai permainan dengan gerakan tubuh? Seperti ‘Pok Ame−Ame’ atau ‘Cilukba’?
                                    \nApakah anak Anda menunjuk dengan jari telunjuk bila ingin sesuatu, bukan dengan cara memegang dengan semua jari?''', ['Ya', 'Tidak'], index=None, horizontal=True, key='tdd3_x')
                else:
                    tdd3_x = st.radio('''Apakah anak secara spontan memulai permainan dengan gerakan tubuh? Seperti ‘Pok Ame−Ame’ atau ‘Cilukba’?
                                    \nApakah anak Anda menunjuk dengan jari telunjuk bila ingin sesuatu, bukan dengan cara memegang dengan semua jari?''', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(tdd3_value), horizontal=True, key='tdd3_x')

            elif usia_bln >36:
                st.write('***Tes Daya Dengar >36 bulan***')
                tdd1_value = st.session_state.input_data.get('TDD1', '')
                if pd.isna(tdd1_value):
                    tdd1_x = st.radio('''Apakah anak dapat menyebutkan nama benda dan kegunaannya, seperti cangkir untuk minum, bola untuk dilempar, pensil warna untuk menggambar, sendok untuk makan?
                                    \nApakah lebih dari tiga perempat orang mengerti apa yang dibicarakan anak Anda?''', ['Ya', 'Tidak'], index=None, horizontal=True, key='tdd1_x')
                else:
                    tdd1_x = st.radio('''Apakah anak dapat menyebutkan nama benda dan kegunaannya, seperti cangkir untuk minum, bola untuk dilempar, pensil warna untuk menggambar, sendok untuk makan?
                                    \nApakah lebih dari tiga perempat orang mengerti apa yang dibicarakan anak Anda?''', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(tdd1_value), horizontal=True, key='tdd1_x')
                
                tdd2_value = st.session_state.input_data.get('TDD2', '')
                if pd.isna(tdd2_value):    
                    tdd2_x = st.radio('Apakah anak Anda dapat menunjukkan minimal 2 nama benda di depannya sesuai fungsi (misal untuk minum: cangkir, untuk dilempar: bola, untuk makan: sendok, untuk menggambar: pensil warna?)', ['Ya', 'Tidak'], index=None, horizontal=True, key='tdd2_x')
                else:
                    tdd2_x = st.radio('Apakah anak Anda dapat menunjukkan minimal 2 nama benda di depannya sesuai fungsi (misal untuk minum: cangkir, untuk dilempar: bola, untuk makan: sendok, untuk menggambar: pensil warna?)', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(tdd2_value), horizontal=True, key='tdd2_x')
                
                tdd3_value = st.session_state.input_data.get('TDD3', '')
                if pd.isna(tdd3_value):
                    tdd3_x = st.radio('''Apakah anak secara spontan memulai permainan dengan gerakan tubuh, seperti ‘Pok Ame-Ame’ atau ‘Cilukba’?
                                    \nApakah anak Anda menunjuk dengan jari telunjuk bila ingin sesuatu, bukan dengan cara memegang dengan semua jari?''', ['Ya', 'Tidak'], index=None, horizontal=True, key='tdd3_value')
                else:
                    tdd3_x = st.radio('''Apakah anak secara spontan memulai permainan dengan gerakan tubuh, seperti ‘Pok Ame-Ame’ atau ‘Cilukba’?
                                    \nApakah anak Anda menunjuk dengan jari telunjuk bila ingin sesuatu, bukan dengan cara memegang dengan semua jari?''', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(tdd3_value), horizontal=True, key='tdd3_value')
                
            else:
                tdd1_x = st.radio('''Apakah bayi dapat mengatakan "Aaaaa", "Oooo"?
                        \nApakah bayi menatap wajah dan tampak mendenagrkan Anda, lalu berbicara saat anda diam?
                        \nApakah anda sesolah-olah berbicara dengan bayi anda?''', ['Ya', 'Tidak'], index=None, horizontal=True, key='tdd1_x', disabled=True)
                tdd2_x = st.radio('''Apakah bayi kaget bila mendengar suara (mengejapkan mata, napas lebih cepat)?
                                \nApakah bayi kelihatan menoleh bila anda berbicara di sebelahnya?''', ['Ya', 'Tidak'], index=None, horizontal=True, key='tdd2_x', disabled=True)
                tdd3_x = st.radio('''Apakah bayi anda dapat tersenyum?
                                \nApakah bayi anda kenal dengan anda, seperti senyum lebih cepat pada anda dibandingkan orang lain?''', ['Ya', 'Tidak'], index=None, horizontal=True, key='tdd3_x', disabled=True)

            def calculate_score(tdd1_x, tdd2_x, tdd3_x):
                score = 0
                # Penentuan skor berdasarkan kelompok usia
                if tdd1_x == 'Ya':
                    score += 0
                elif tdd1_x == 'Tidak':
                    score += 1

                if tdd2_x == 'Ya':
                    score += 0
                elif tdd2_x == 'Tidak':
                    score += 1
                
                if tdd3_x == 'Ya':
                    score += 0
                elif tdd3_x == 'Tidak':
                    score += 1

                return score
            
            # Hitung total skor
            total_score = calculate_score(tdd1_x, tdd2_x, tdd3_x)

            if total_score >= 1:
                kesimpulan_tdd_x = st.text_input('Kesimpulan Tes Daya Dengar', value='Ada Kemungkinan Penyimpangan', disabled=True, key='kesimpulan_tdd_x')
            else:
                kesimpulan_tdd_x = st.text_input('Kesimpulan Tes Daya Dengar', value='Sesuai Umur', disabled=True, key='kesimpulan_tdd_x')

        with st.expander('**SKRINING GPPH**'):
            gpph1_value = st.session_state.input_data.get('GPPH1', '')
            if pd.isna(gpph1_value):
                gpph1_x = st.radio('Tidak kenal lelah atau aktivitas yang berlebihan', ['Tidak', 'Kadang-kadang', 'Sering', 'Selalu'], index=None, horizontal=True, key='gpph1_x')
            else:
                gpph1_x = st.radio('Tidak kenal lelah atau aktivitas yang berlebihan', ['Tidak', 'Kadang-kadang', 'Sering', 'Selalu'], index= ['Tidak', 'Kadang-kadang', 'Sering', 'Selalu'].index(gpph1_value), horizontal=True, key='gpph1_x')
                
            gpph2_value = st.session_state.input_data.get('GPPH2', '')
            if pd.isna(gpph2_value):
                gpph2_x = st.radio('Mudah menjadi gembira, impulsif', ['Tidak', 'Kadang-kadang', 'Sering', 'Selalu'], index=None, horizontal=True, key='gpph2_x')
            else:
                gpph2_x = st.radio('Mudah menjadi gembira, impulsif', ['Tidak', 'Kadang-kadang', 'Sering', 'Selalu'], index=['Tidak', 'Kadang-kadang', 'Sering', 'Selalu'].index(gpph2_value), horizontal=True, key='gpph2_x')

            gpph3_value = st.session_state.input_data.get('GPPH3', '')
            if pd.isna(gpph3_value):
                gpph3_x = st.radio('Mengganggu anak-anak lain', ['Tidak', 'Kadang-kadang', 'Sering', 'Selalu'], index=None, horizontal=True, key='gpph3_x')
            else:
                gpph3_x = st.radio('Mengganggu anak-anak lain', ['Tidak', 'Kadang-kadang', 'Sering', 'Selalu'], index=['Tidak', 'Kadang-kadang', 'Sering', 'Selalu'].index(gpph3_value), horizontal=True, key='gpph3_x')

            gpph4_value = st.session_state.input_data.get('GPPH4', '')
            if pd.isna(gpph4_value):
                gpph4_x = st.radio('Gagal menyelesaikan kegiatan yang telah dimulai; rentang perhayian pendek', ['Tidak', 'Kadang-kadang', 'Sering', 'Selalu'], index=None, horizontal=True, key='gpph4_x')
            else:
                gpph4_x = st.radio('Gagal menyelesaikan kegiatan yang telah dimulai; rentang perhayian pendek', ['Tidak', 'Kadang-kadang', 'Sering', 'Selalu'], index=['Tidak', 'Kadang-kadang', 'Sering', 'Selalu'].index(gpph4_value), horizontal=True, key='gpph4_x')

            gpph5_value = st.session_state.input_data.get('GPPH5', '')
            if pd.isna(gpph5_value):
                gpph5_x = st.radio('Menggerak-gerakkan anggota badan atau kepala secara terus menerus', ['Tidak', 'Kadang-kadang', 'Sering', 'Selalu'], index=None, horizontal=True, key='gpph5_x')
            else:
                gpph5_x = st.radio('Menggerak-gerakkan anggota badan atau kepala secara terus menerus', ['Tidak', 'Kadang-kadang', 'Sering', 'Selalu'], index=['Tidak', 'Kadang-kadang', 'Sering', 'Selalu'].index(gpph5_value), horizontal=True, key='gpph5_x')

            gpph6_value = st.session_state.input_data.get('GPPH6', '')
            if pd.isna(gpph6_value):
                gpph6_x = st.radio('Kurang memperhatikan, mudah teralihkan', ['Tidak', 'Kadang-kadang', 'Sering', 'Selalu'], index=None, horizontal=True, key='gpph6_x')
            else:
                gpph6_x = st.radio('Kurang memperhatikan, mudah teralihkan', ['Tidak', 'Kadang-kadang', 'Sering', 'Selalu'], index=['Tidak', 'Kadang-kadang', 'Sering', 'Selalu'].index(gpph6_value), horizontal=True, key='gpph6_x')

            gpph7_value = st.session_state.input_data.get('GPPH7', '')
            if pd.isna(gpph7_value):
                gpph7_x = st.radio('Permintaannya harus segera dipenuhi; mudah menjadi frustasi', ['Tidak', 'Kadang-kadang', 'Sering', 'Selalu'], index=None, horizontal=True, key='gpph7_x')
            else:
                gpph7_x = st.radio('Permintaannya harus segera dipenuhi; mudah menjadi frustasi', ['Tidak', 'Kadang-kadang', 'Sering', 'Selalu'], index=['Tidak', 'Kadang-kadang', 'Sering', 'Selalu'].index(gpph7_value), horizontal=True, key='gpph7_x')

            gpph8_value = st.session_state.input_data.get('GPPH8', '')
            if pd.isna(gpph8_value):
                gpph8_x = st.radio('Sering dan mudah menangis', ['Tidak', 'Kadang-kadang', 'Sering', 'Selalu'], index=None, horizontal=True, key='gpph8_x')
            else:
                gpph8_x = st.radio('Sering dan mudah menangis', ['Tidak', 'Kadang-kadang', 'Sering', 'Selalu'], index=['Tidak', 'Kadang-kadang', 'Sering', 'Selalu'].index(gpph8_value), horizontal=True, key='gpph8_x')

            gpph9_value = st.session_state.input_data.get('GPPH9', '')
            if pd.isna(gpph9_value):
                gpph9_x = st.radio('Suasana hatinya mudah berubah dengan cepat dan drastis', ['Tidak', 'Kadang-kadang', 'Sering', 'Selalu'], index=None, horizontal=True, key='gpph9_x')
            else:
                gpph9_x = st.radio('Suasana hatinya mudah berubah dengan cepat dan drastis', ['Tidak', 'Kadang-kadang', 'Sering', 'Selalu'], index=['Tidak', 'Kadang-kadang', 'Sering', 'Selalu'].index(gpph9_value), horizontal=True, key='gpph9_x')

            gpph10_value = st.session_state.input_data.get('GPPH10', '')
            if pd.isna(gpph10_value):
                gpph10_x = st.radio('Ledakan kekesalan, tingkah laku ekspolsif dan tak terduga', ['Tidak', 'Kadang-kadang', 'Sering', 'Selalu'], index=None, horizontal=True, key='gpph10_x')
            else:
                gpph10_x = st.radio('Ledakan kekesalan, tingkah laku ekspolsif dan tak terduga', ['Tidak', 'Kadang-kadang', 'Sering', 'Selalu'], index=['Tidak', 'Kadang-kadang', 'Sering', 'Selalu'].index(gpph10_value), horizontal=True, key='gpph10_x')
            
            # Fungsi untuk menghitung skor
            def calculate_score(gpph1_x, gpph2_x, gpph3_x, gpph4_x, gpph5_x, gpph6_x, gpph7_x, gpph8_x, gpph9_x, gpph10_x):
                score = 0
                if gpph1_x == 'Kadang-kadang':
                    score += 1
                elif gpph1_x == 'Sering':
                    score += 2
                elif gpph1_x == 'Selalu':
                    score += 3
                else:
                    score += 0

                if gpph2_x == 'Kadang-kadang':
                    score += 1
                elif gpph2_x == 'Sering':
                    score += 2
                elif gpph2_x == 'Selalu':
                    score += 3
                else:
                    score += 0
                
                if gpph3_x == 'Kadang-kadang':
                    score += 1
                elif gpph3_x == 'Sering':
                    score += 2
                elif gpph3_x == 'Selalu':
                    score += 3
                else:
                    score += 0
                
                if gpph4_x == 'Kadang-kadang':
                    score += 1
                elif gpph4_x == 'Sering':
                    score += 2
                elif gpph4_x == 'Selalu':
                    score += 3
                else:
                    score += 0
                    
                if gpph5_x == 'Kadang-kadang':
                    score += 1
                elif gpph5_x == 'Sering':
                    score += 2
                elif gpph5_x == 'Selalu':
                    score += 3
                else:
                    score += 0
                    
                if gpph6_x == 'Kadang-kadang':
                    score += 1
                elif gpph6_x == 'Sering':
                    score += 2
                elif gpph6_x == 'Selalu':
                    score += 3
                else:
                    score += 0
                    
                if gpph7_x == 'Kadang-kadang':
                    score += 1
                elif gpph7_x == 'Sering':
                    score += 2
                elif gpph7_x == 'Selalu':
                    score += 3
                else:
                    score += 0
                    
                if gpph8_x == 'Kadang-kadang':
                    score += 1
                elif gpph8_x == 'Sering':
                    score += 2
                elif gpph8_x == 'Selalu':
                    score += 3
                else:
                    score += 0
                    
                if gpph9_x == 'Kadang-kadang':
                    score += 1
                elif gpph9_x == 'Sering':
                    score += 2
                elif gpph9_x == 'Selalu':
                    score += 3
                else:
                    score += 0
                    
                if gpph10_x == 'Kadang-kadang':
                    score += 1
                elif gpph10_x == 'Sering':
                    score += 2
                elif gpph10_x == 'Selalu':
                    score += 3
                else:
                    score += 0

                return score
            
            # Hitung total skor
            total_score = calculate_score(gpph1_x, gpph2_x, gpph3_x, gpph4_x, gpph5_x, gpph6_x, gpph7_x, gpph8_x, gpph9_x, gpph10_x)

            # Kesimpulan
            if total_score < 13:
                kesimpulan_gpph_x = st.text_input('Kesimpulan', value='Normal', disabled=True, key='kesimpulan_gpph_x')
            else:
                kesimpulan_gpph_x = st.text_input('Kesimpulan', value='Kemungkinan GPPH', disabled=True, key='kesimpulan_gpph_x')

            # tidak=0
            # kadang2=1
            # sering=2
            # selalu=3
            
            #<13 = normal
            #>= 13 = kemungkinan gpph
            
        with st.expander('**SKRINING MASALAH PERILAKU EMOSIONAL**'):
            emosi1_value = st.session_state.input_data.get('Emosi1', '')
            if pd.isna(emosi1_value):
                emosi1_x = st.radio('Apakah anak Anda sering bereaksi negatif, marah atau tegang tanpa sebab yang jelas? (Bereaksi negatif contohnya rewel, tidak sabaran, banyak menangis, mudah tersinggung atau bereaksi berlebihan bila merasa situasi tidak seperti yang diharapkannya atau kemauannya tidak terpenuhi)', ['Ya', 'Tidak'], index=None, horizontal=True, key='emosi1_x')
            else:
                emosi1_x = st.radio('Apakah anak Anda sering bereaksi negatif, marah atau tegang tanpa sebab yang jelas? (Bereaksi negatif contohnya rewel, tidak sabaran, banyak menangis, mudah tersinggung atau bereaksi berlebihan bila merasa situasi tidak seperti yang diharapkannya atau kemauannya tidak terpenuhi)', ['Ya', 'Tidak'], index= ['Ya', 'Tidak'].index(emosi1_value), horizontal=True, key='emosi1_x')
            
            emosi2_value = st.session_state.input_data.get('Emosi2', '')
            if pd.isna(emosi2_value):
                emosi2_x = st.radio('Apakah anak Anda tampak lebih memilih untuk menyendiri, bermain sendiri, atau menghindar dari anak seumurnya atau orang dewasa? (Ingin sendirian, menyendiri dengan ekspresi murung, tidak bersemangat, sedih, atau kehilangan minat terhadap hal-hal yang biasa sangat dinikmati)', ['Ya', 'Tidak'], index=None, horizontal=True, key='emosi2_x')
            else:
                emosi2_x = st.radio('Apakah anak Anda tampak lebih memilih untuk menyendiri, bermain sendiri, atau menghindar dari anak seumurnya atau orang dewasa? (Ingin sendirian, menyendiri dengan ekspresi murung, tidak bersemangat, sedih, atau kehilangan minat terhadap hal-hal yang biasa sangat dinikmati)', ['Ya', 'Tidak'], index=['Ya', 'Tidak'].index(emosi2_value), horizontal=True, key='emosi2_x')

            emosi3_value = st.session_state.input_data.get('Emosi3', '')
            if pd.isna(emosi3_value):
                emosi3_x = st.radio('Apakah anak Anda cenderung bersikap menentang? (Membantah, melawan, tidak mau menurut atau melakukan hal yang sebaliknya dari apa yang diminta, serta tampak tidak peduli ketika diberitahu atau ditegur)', ['Ya', 'Tidak'], index=None, horizontal=True, key='emosi3_x')
            else:
                emosi3_x = st.radio('Apakah anak Anda cenderung bersikap menentang? (Membantah, melawan, tidak mau menurut atau melakukan hal yang sebaliknya dari apa yang diminta, serta tampak tidak peduli ketika diberitahu atau ditegur)', ['Ya', 'Tidak'], index=['Ya', 'Tidak'].index(emosi3_value), horizontal=True, key='emosi3_x')

            emosi4_value = st.session_state.input_data.get('Emosi4', '')
            if pd.isna(emosi4_value):
                emosi4_x = st.radio('Apakah anak Anda mudah takut atau cemas berlebihan tanpa sebab yang jelas?(Misalnya takut pada binatang atau benda yang tidak berbahaya, terlihat cemas ketika tidak melihat ibu atau pengasuh)', ['Ya', 'Tidak'], index=None, horizontal=True, key='emosi4_x')
            else:
                emosi4_x = st.radio('Apakah anak Anda mudah takut atau cemas berlebihan tanpa sebab yang jelas?(Misalnya takut pada binatang atau benda yang tidak berbahaya, terlihat cemas ketika tidak melihat ibu atau pengasuh)', ['Ya', 'Tidak'], index=['Ya', 'Tidak'].index(emosi4_value), horizontal=True, key='emosi4_x')

            emosi5_value = st.session_state.input_data.get('Emosi5', '')
            if pd.isna(emosi5_value):
                emosi5_x = st.radio('Apakah anak Anda sering sulit konsentrasi, perhatiannya mudah teralihkan atau banyak bergerak atau tidak bisa diam? (Misalnya anak tidak bisa bertahan lama untuk bermain dengan satu permainan, mudah mengalihkan perhatian bila ada hal lain yang lebih menarik perhatian seperti bunyi atau gerakan, tidak bisa duduk dengan tenang, banyak bergerak atau cenderung berjalan atau berlari mondar-mandir)', ['Ya', 'Tidak'], index=None, horizontal=True, key='emosi5_x')
            else:
                emosi5_x = st.radio('Apakah anak Anda sering sulit konsentrasi, perhatiannya mudah teralihkan atau banyak bergerak atau tidak bisa diam? (Misalnya anak tidak bisa bertahan lama untuk bermain dengan satu permainan, mudah mengalihkan perhatian bila ada hal lain yang lebih menarik perhatian seperti bunyi atau gerakan, tidak bisa duduk dengan tenang, banyak bergerak atau cenderung berjalan atau berlari mondar-mandir)', ['Ya', 'Tidak'], index=['Ya', 'Tidak'].index(emosi5_value), horizontal=True, key='emosi5_x')

            emosi6_value = st.session_state.input_data.get('Emosi6', '')
            if pd.isna(emosi6_value):
                emosi6_x = st.radio('Apakah anak Anda lebih banyak menempel atau selalu minta ditemani, mudah cemas, dan tidak percaya diri? (Seakan minta perlindungan atau minta ditemanipada berbagai situasi, terutama ketika berada dalam situasi baru atau ada orang yang baru dikenalnya; mengekspresikan kecemasan serta terlihat tidak percaya diri)', ['Ya', 'Tidak'], index=None, horizontal=True, key='emosi6_x')
            else:
                emosi6_x = st.radio('Apakah anak Anda lebih banyak menempel atau selalu minta ditemani, mudah cemas, dan tidak percaya diri? (Seakan minta perlindungan atau minta ditemanipada berbagai situasi, terutama ketika berada dalam situasi baru atau ada orang yang baru dikenalnya; mengekspresikan kecemasan serta terlihat tidak percaya diri)', ['Ya', 'Tidak'], index=['Ya', 'Tidak'].index(emosi6_value), horizontal=True, key='emosi6_x')

            emosi7_value = st.session_state.input_data.get('Emosi7', '')
            if pd.isna(emosi7_value):
                emosi7_x = st.radio('Apakah anak Anda menunjukkan adanya perubahan pola tidur? (Misalnya sulit tidur, terjaga sepanjang hari, sering terbangun di waktu tidur malam oleh karena mimpi buruk, mengigau, menangis di dalam tidurnya)', ['Ya', 'Tidak'], index=None, horizontal=True, key='emosi7_x')
            else:
                emosi7_x = st.radio('Apakah anak Anda menunjukkan adanya perubahan pola tidur? (Misalnya sulit tidur, terjaga sepanjang hari, sering terbangun di waktu tidur malam oleh karena mimpi buruk, mengigau, menangis di dalam tidurnya)', ['Ya', 'Tidak'], index=['Ya', 'Tidak'].index(emosi7_value), horizontal=True, key='emosi7_x')

            emosi8_value = st.session_state.input_data.get('Emosi8', '')
            if pd.isna(emosi8_value):
                emosi8_x = st.radio('Apakah anak Anda mengalami perubahan pola makan dari yang biasanya?(Kehilangan nafsu makan, tidak mau makan sama sekali, atau sebaliknya makan berlebihan, sangat memilih jenis makanan, atau membiarkan makanan lama dimulut tanpa dikunyah atau diemut)', ['Ya', 'Tidak'], index=None, horizontal=True, key='emosi8_x')
            else:
                emosi8_x = st.radio('Apakah anak Anda mengalami perubahan pola makan dari yang biasanya?(Kehilangan nafsu makan, tidak mau makan sama sekali, atau sebaliknya makan berlebihan, sangat memilih jenis makanan, atau membiarkan makanan lama dimulut tanpa dikunyah atau diemut)', ['Ya', 'Tidak'], index=['Ya', 'Tidak'].index(emosi8_value), horizontal=True, key='emosi8_x')

            emosi9_value = st.session_state.input_data.get('Emosi9', '')
            if pd.isna(emosi9_value):
                emosi9_x = st.radio('Apakah anak Anda seringkali mengeluh sakit kepala, sakit perut, atau keluhan fisik lainnya pada waktu-waktu tertentu?', ['Ya', 'Tidak'], index=None, horizontal=True, key='emosi9_x')
            else:
                emosi9_x = st.radio('Apakah anak Anda seringkali mengeluh sakit kepala, sakit perut, atau keluhan fisik lainnya pada waktu-waktu tertentu?', ['Ya', 'Tidak'], index=['Ya', 'Tidak'].index(emosi9_value), horizontal=True, key='emosi9_x')

            emosi10_value = st.session_state.input_data.get('Emosi10', '')
            if pd.isna(emosi10_value):
                emosi10_x = st.radio('Apakah anak Anda mudah putus asa atau frustrasi dan sering menunjukkan emosi yang negatif? (Misalnya sedih atau kecewa yang berkepanjangan, mudah mengeluh, marah, atau protes. Misal ketika anak merasa kesulitan dalam menggambar, lalu berteriak minta tolong, marah, atau kertasnya disobek)', ['Ya', 'Tidak'], index=None, horizontal=True, key='emosi10_x')
            else:
                emosi10_x = st.radio('Apakah anak Anda mudah putus asa atau frustrasi dan sering menunjukkan emosi yang negatif? (Misalnya sedih atau kecewa yang berkepanjangan, mudah mengeluh, marah, atau protes. Misal ketika anak merasa kesulitan dalam menggambar, lalu berteriak minta tolong, marah, atau kertasnya disobek)', ['Ya', 'Tidak'], index=['Ya', 'Tidak'].index(emosi10_value), horizontal=True, key='emosi10_x')

            emosi11_value = st.session_state.input_data.get('Emosi11', '')
            if pd.isna(emosi11_value):
                emosi11_x = st.radio('Apakah anak Anda menunjukkan kemunduran pola perilaku dari kemampuan yang sudah dimilikinya? (Misalnya mengompol kembali, menghisap jempol, atau tidak mau berpisah dengan orangtua atau pengasuhnya)', ['Ya', 'Tidak'], index=None, horizontal=True, key='emosi11_x')
            else:
                emosi11_x = st.radio('Apakah anak Anda menunjukkan kemunduran pola perilaku dari kemampuan yang sudah dimilikinya? (Misalnya mengompol kembali, menghisap jempol, atau tidak mau berpisah dengan orangtua atau pengasuhnya)', ['Ya', 'Tidak'], index=['Ya', 'Tidak'].index(emosi11_value), horizontal=True, key='emosi11_x')

            emosi12_value = st.session_state.input_data.get('Emosi12', '')
            if pd.isna(emosi12_value):
                emosi12_x = st.radio('Apakah anak Anda sering berkelahi, bertengkar, atau menyerang anak lain baik secara verbal maupun non verbal? (Misalnya mengejek, meneriaki, merebut permainan, atau memukul temannya)', ['Ya', 'Tidak'], index=None, horizontal=True, key='emosi12_x')
            else:
                emosi12_x = st.radio('Apakah anak Anda sering berkelahi, bertengkar, atau menyerang anak lain baik secara verbal maupun non verbal? (Misalnya mengejek, meneriaki, merebut permainan, atau memukul temannya)', ['Ya', 'Tidak'], index=['Ya', 'Tidak'].index(emosi12_value), horizontal=True, key='emosi12_x')

            emosi13_value = st.session_state.input_data.get('Emosi13', '')
            if pd.isna(emosi13_value):
                emosi13_x = st.radio('Apakah anak Anda sering diperlakukan tidak menyenangkan oleh anak lain atau orang dewasa? (Misalnya ditinggal bermain, dihindari, diejek, dikata-katai, direbut mainannya, atau disakiti secara fisik)', ['Ya', 'Tidak'], index=None, horizontal=True, key='emosi13_x')
            else:
                emosi13_x = st.radio('Apakah anak Anda sering diperlakukan tidak menyenangkan oleh anak lain atau orang dewasa? (Misalnya ditinggal bermain, dihindari, diejek, dikata-katai, direbut mainannya, atau disakiti secara fisik)', ['Ya', 'Tidak'], index=['Ya', 'Tidak'].index(emosi13_value), horizontal=True, key='emosi13_x')

            emosi14_value = st.session_state.input_data.get('Emosi14', '')
            if pd.isna(emosi14_value):
                emosi14_x = st.radio('Apakah anak Anda cenderung berperilaku merusak atau cenderung selalu ingin menang atau menguasai? (Misalnya merusak benda, menyakiti dirinya atau binatang)', ['Ya', 'Tidak'], index=None, horizontal=True, key='emosi14_x')
            else:
                emosi14_x = st.radio('Apakah anak Anda cenderung berperilaku merusak atau cenderung selalu ingin menang atau menguasai? (Misalnya merusak benda, menyakiti dirinya atau binatang)', ['Ya', 'Tidak'], index=['Ya', 'Tidak'].index(emosi14_value), horizontal=True, key='emosi14_x')
            
            # Fungsi untuk menghitung skor
            def calculate_score(emosi1_x, emosi2_x, emosi3_x, emosi4_x, emosi5_x, emosi6_x, emosi7_x, emosi8_x, emosi9_x, emosi10_x, emosi11_x, emosi12_x, emosi13_x, emosi14_x):
                score = 0
                if emosi1_x == 'Ya':
                    score += 1
                elif emosi1_x == 'Tidak':
                    score += 0
                
                if emosi2_x == 'Ya':
                    score += 1
                elif emosi2_x == 'Tidak':
                    score += 0
                    
                if emosi3_x == 'Ya':
                    score += 1
                elif emosi3_x == 'Tidak':
                    score += 0
                    
                if emosi4_x == 'Ya':
                    score += 1
                elif emosi4_x == 'Tidak':
                    score += 0
                
                if emosi5_x == 'Ya':
                    score += 1
                elif emosi5_x == 'Tidak':
                    score += 0
                    
                if emosi6_x == 'Ya':
                    score += 1
                elif emosi6_x == 'Tidak':
                    score += 0
                    
                if emosi7_x == 'Ya':
                    score += 1
                elif emosi7_x == 'Tidak':
                    score += 0
                
                if emosi8_x == 'Ya':
                    score += 1
                elif emosi8_x == 'Tidak':
                    score += 0
                    
                if emosi9_x == 'Ya':
                    score += 1
                elif emosi9_x == 'Tidak':
                    score += 0
                    
                if emosi10_x == 'Ya':
                    score += 1
                elif emosi10_x == 'Tidak':
                    score += 0
                
                if emosi11_x == 'Ya':
                    score += 1
                elif emosi11_x == 'Tidak':
                    score += 0
                    
                if emosi12_x == 'Ya':
                    score += 1
                elif emosi12_x == 'Tidak':
                    score += 0
                    
                if emosi13_x == 'Ya':
                    score += 1
                elif emosi13_x == 'Tidak':
                    score += 0
                
                if emosi14_x == 'Ya':
                    score += 1
                elif emosi14_x == 'Tidak':
                    score += 0
                    
                return score
            
            # Hitung total skor
            total_score = calculate_score(emosi1_x, emosi2_x, emosi3_x, emosi4_x, emosi5_x, emosi6_x, emosi7_x, emosi8_x, emosi9_x, emosi10_x, emosi11_x, emosi12_x, emosi13_x, emosi14_x)

            # Kesimpulan
            if 0 < total_score <= 1:
                kesimpulan_emosi_x = st.text_input('Kesimpulan', value='Meragukan', disabled=True, key='kesimpulan_emosi_x')
            elif total_score >= 2:
                kesimpulan_emosi_x = st.text_input('Kesimpulan', value='Kemungkinan Anak Mengalami Masalah Perilaku Emosional', disabled=True, key='kesimpulan_emosi_x')
            else:
                kesimpulan_emosi_x = st.text_input('Kesimpulan', value='Normal', disabled=True, key='kesimpulan_emosi_x')

            
            #tidak ada jawaban ya= normal
            #1 jawaban ya = meragukan
            #>=2 jawaban ya = kemungkinan anak mengalami masalah perilaku emosional
            
        with st.expander('**SKRINING GIGI**'):
            gigi_value = st.session_state.input_data.get('Karies Dentis', '')
            if pd.isna(gigi_value):
                gigi_x = st.text_input('Karies Dentis', value=None, key='gigi_x')
            else:
                gigi_x = st.text_input('Karies Dentis', value= gigi_value, key='gigi_x')

        with st.expander('**PEMERIKSAAN LABORATORIUM**'):
            left, right = st.columns(2)
            hb_value = st.session_state.input_data.get('HB', '')
            if pd.isna(hb_value):
                hb_x = left.text_input('HB', value=None, key='hb_x')
            else:
                hb_x = left.text_input('HB', value=hb_value, key='hb_x')
            
            eritrosit_value = st.session_state.input_data.get('Eritrosit', '')
            if pd.isna(eritrosit_value):   
                eritrosit_x = left.text_input('Eritrosit(X10*6)', value=None, key='eritrosit_x')
            else:
                eritrosit_x = left.text_input('Eritrosit(X10*6)', value=eritrosit_value, key='eritrosit_x')
                
            htc_value = st.session_state.input_data.get('Hematokrit', '')
            if pd.isna(htc_value):
                htc_x = left.text_input('Hematokrit', value=None, key='htc_x')
            else:
                htc_x = left.text_input('Hematokrit', value=htc_value, key='htc_x')
                
            leukosit_value = st.session_state.input_data.get('Leukosit', '')
            if pd.isna(leukosit_value):
                leukosit_x = left.text_input('Leukosit', value=None, key='leukosit_x')
            else:
                leukosit_x = left.text_input('Leukosit', value=leukosit_value, key='leukosit_x')
                
            trombosit_value = st.session_state.input_data.get('Trombosit', '')
            if pd.isna(trombosit_value):
                trombosit_x = left.text_input('Trombosit', value=None, key='trombosit_x')
            else:
                trombosit_x = left.text_input('Trombosit', value=trombosit_value, key='trombosit_x')
                
            mcv_value = st.session_state.input_data.get('MCV', '')
            if pd.isna(mcv_value):
                mcv_x = left.text_input('MCV', value=None, key='mcv_x')
            else:
                mcv_x = left.text_input('MCV', value=mcv_value, key='mcv_x')
                
            mch_value = st.session_state.input_data.get('MCH', '')
            if pd.isna(mch_value):
                mch_x = right.text_input('MCH', value=None, key='mch_x')
            else:
                mch_x = right.text_input('MCH', value=mch_value, key='mch_x')
                
            mchc_value = st.session_state.input_data.get('MCHC', '')
            if pd.isna(mchc_value):
                mchc_x = right.text_input('MCHC', value=None, key='mchc_x')
            else:
                mchc_x = right.text_input('MCHC', value=mchc_value, key='mchc_x')
            
            rdw_value = st.session_state.input_data.get('RDW', '')
            if pd.isna(rdw_value):
                rdw_x = right.text_input('RDW', value=None, key='rdw_x')
            else:
                rdw_x = right.text_input('RDW', value=rdw_value, key='rdw_x')
            
            gds_value = st.session_state.input_data.get('GDS', '')
            if pd.isna(gds_value):    
                gds_x = right.text_input('GDS', value=None, key='gds_x')
            else:
                gds_x = right.text_input('GDS', value=gds_value, key='gds_x')
                
            if mcv_x is not None and eritrosit_x is not None:
                mcv_x = float(mcv_x)
                eritrosit_x = float(eritrosit_x)
                mi = mcv_x/eritrosit_x
                mentzer_x = right.text_input('Index Mentzer', value=mi, key='mentzer_x', disabled=True)
            else:
                mentzer_x = right.text_input('Index Mentzer', value=0, key='mentzer_x', disabled=True)
        

        # Tombol untuk menyimpan data yang diubah
        btn_save = st.button('Update Data', key='btn_save')

        if btn_save:
            # Menyimpan data yang diubah ke dalam Google Sheets
            updated_data = pd.DataFrame(
                [
                    {
                        "Tanggal Pemeriksaan": tgl_pem_x,
                        "Nama": nama_x,
                        "NIK": nik_x.strip(),
                        "Jenis Kelamin": jk_x,
                        "Tanggal Lahir": tgl_lhr_x,
                        "Usia_Tahun": ut_x,
                        "Usia_Bulan": ub_x,
                        "Alamat": alamat_x,
                        "Nomor HP": hp_x,
                        "Nama Wali": wali_x,
                        "NIK Wali": nik_wali_x,
                        "Disabilitas": disabilitas_x,
                        "BB": bb_x,
                        "TB/PB": tb_x,
                        "Posisi": posisi_x,
                        "IMT": bmi_x,
                        "Lingkar Kepala": lk_x,
                        "BB/U": stat_bbu_x, 
                        "TB/U": stat_tbu_x,
                        "BB/TB": stat_bbtb_x,
                        "IMT/U": stat_imtu_x,
                        "LK/U": stat_lku_x,
                        "LLA": lla_x,
                        "Status LLA": stat_lla_x,
                        "KPSP1": kpsp1_x,
                        "KPSP2": kpsp2_x,
                        "KPSP3": kpsp3_x,
                        "KPSP4": kpsp4_x,
                        "KPSP5": kpsp5_x,
                        "KPSP6": kpsp6_x,
                        "KPSP7": kpsp7_x,
                        "KPSP8": kpsp8_x,
                        "KPSP9": kpsp9_x,
                        "KPSP10": kpsp10_x,
                        "Kesimpulan KPSP": kesimpulan_kpsp_x,
                        "DM1": dm1_x,
                        "DM2": dm2_x,
                        "DM3": dm3_x,
                        "DM4": dm4_x,
                        "DM5": dm5_x,
                        "DM6": dm6_x,
                        "Talasemia1": talasemia1_x,
                        "Talasemia2": talasemia2_x,
                        "TB1": tb1_x,
                        "TB2": tb2_x,
                        "TB3": tb3_x,
                        "TB4": tb4_x,
                        "TB5": tb5_x,
                        "Visus OD": visusod_x,
                        "Visus OS": visusos_x,
                        "Pupil Putih OD": pupil_putih_od_x,
                        "Pupil Putih OS": pupil_putih_os_x,
                        "TDD1": tdd1_x,
                        "TDD2": tdd2_x,
                        "TDD3": tdd3_x,
                        "Kesimpulan TDD": kesimpulan_tdd_x,
                        "GPPH1": gpph1_x,
                        "GPPH2": gpph2_x,
                        "GPPH3": gpph3_x,
                        "GPPH4": gpph4_x,
                        "GPPH5": gpph5_x,
                        "GPPH6": gpph6_x,
                        "GPPH7": gpph7_x,
                        "GPPH8": gpph8_x,
                        "GPPH9": gpph9_x,
                        "GPPH10": gpph10_x,
                        "Kesimpulan GPPH": kesimpulan_gpph_x,
                        "Emosi1": emosi1_x,
                        "Emosi2": emosi2_x,
                        "Emosi3": emosi3_x,
                        "Emosi4": emosi4_x,
                        "Emosi5": emosi5_x,
                        "Emosi6": emosi6_x,
                        "Emosi7": emosi7_x,
                        "Emosi8": emosi8_x,
                        "Emosi9": emosi9_x,
                        "Emosi10": emosi10_x,
                        "Emosi11": emosi11_x,
                        "Emosi12": emosi12_x,
                        "Emosi13": emosi13_x,
                        "Emosi14": emosi14_x,
                        "Kesimpulan Emosi": kesimpulan_emosi_x,
                        "Karies Dentis": gigi_x,
                        "HB": hb_x,
                        "Eritrosit": eritrosit_x,
                        "Hematokrit": htc_x,
                        "Leukosit": leukosit_x,
                        "Trombosit": trombosit_x,
                        "MCV": mcv_x,
                        "MCH": mch_x,
                        "MCHC": mchc_x,
                        "RDW": rdw_x,
                        "GDS": gds_x,
                        "Index Mentzer": mentzer_x
                    }
                ]
            )


            # Cari baris yang sesuai dengan nama yang ada
            df['NIK'] = df['NIK'].astype(str)
            idx = df[df['NIK'].str.contains(st.session_state.input_nik.strip(), case=False, na=False)].index
            
            ########################################
            if len(idx) > 0:
                # Jika nik ditemukan, update data pada baris tersebut
                df.loc[idx, "Tanggal Pemeriksaan"]= tgl_pem_x,
                df.loc[idx, "Nama"]= nama_x,
                df.loc[idx, "Jenis Kelamin"]= jk_x,
                df.loc[idx, "Tanggal Lahir"]= tgl_lhr_x,
                df.loc[idx, "Usia_Tahun"]= ut_x,
                df.loc[idx, "Usia_Bulan"]= ub_x,
                df.loc[idx, "Alamat"]= alamat_x,
                df.loc[idx, "Nomor HP"]= hp_x,
                df.loc[idx, "Nama Wali"]= wali_x,
                df.loc[idx, "NIK Wali"]= nik_wali_x,
                df.loc[idx, "Disabilitas"]= disabilitas_x,
                df.loc[idx, "BB"]= bb_x,
                df.loc[idx, "TB/PB"]= tb_x,
                df.loc[idx, "Posisi"]= posisi_x,
                df.loc[idx, "IMT"]= bmi_x,
                df.loc[idx, "Lingkar Kepala"]= lk_x,
                df.loc[idx, "BB/U"]= stat_bbu_x, 
                df.loc[idx, "TB/U"]= stat_tbu_x,
                df.loc[idx, "BB/TB"]= stat_bbtb_x,
                df.loc[idx, "IMT/U"]= stat_imtu_x,
                df.loc[idx, "LK/U"]= stat_lku_x,
                df.loc[idx, "LLA"]= lla_x,
                df.loc[idx, "Status LLA"]= stat_lla_x,
                df.loc[idx, "KPSP1"]= kpsp1_x,
                df.loc[idx, "KPSP2"]= kpsp2_x,
                df.loc[idx, "KPSP3"]= kpsp3_x,
                df.loc[idx, "KPSP4"]= kpsp4_x,
                df.loc[idx, "KPSP5"]= kpsp5_x,
                df.loc[idx, "KPSP6"]= kpsp6_x,
                df.loc[idx, "KPSP7"]= kpsp7_x,
                df.loc[idx, "KPSP8"]= kpsp8_x,
                df.loc[idx, "KPSP9"]= kpsp9_x,
                df.loc[idx, "KPSP10"]= kpsp10_x,
                df.loc[idx, "Kesimpulan KPSP"]= kesimpulan_kpsp_x,
                df.loc[idx, "DM1"]= dm1_x,
                df.loc[idx, "DM2"]= dm2_x,
                df.loc[idx, "DM3"]= dm3_x,
                df.loc[idx, "DM4"]= dm4_x,
                df.loc[idx, "DM5"]= dm5_x,
                df.loc[idx, "DM6"]= dm6_x,
                df.loc[idx, "Talasemia1"]= talasemia1_x,
                df.loc[idx, "Talasemia2"]= talasemia2_x,
                df.loc[idx, "TB1"]= tb1_x,
                df.loc[idx, "TB2"]= tb2_x,
                df.loc[idx, "TB3"]= tb3_x,
                df.loc[idx, "TB4"]= tb4_x,
                df.loc[idx, "TB5"]= tb5_x,
                df.loc[idx, "Visus OD"]= visusod_x,
                df.loc[idx, "Visus OS"]= visusos_x,
                df.loc[idx, "Pupil Putih OD"]= pupil_putih_od_x,
                df.loc[idx, "Pupil Putih OS"]= pupil_putih_os_x,
                df.loc[idx, "TDD1"]= tdd1_x,
                df.loc[idx, "TDD2"]= tdd2_x,
                df.loc[idx, "TDD3"]= tdd3_x,
                df.loc[idx, "Kesimpulan TDD"]= kesimpulan_tdd_x,
                df.loc[idx, "GPPH1"]= gpph1_x,
                df.loc[idx, "GPPH2"]= gpph2_x,
                df.loc[idx, "GPPH3"]= gpph3_x,
                df.loc[idx, "GPPH4"]= gpph4_x,
                df.loc[idx, "GPPH5"]= gpph5_x,
                df.loc[idx, "GPPH6"]= gpph6_x,
                df.loc[idx, "GPPH7"]= gpph7_x,
                df.loc[idx, "GPPH8"]= gpph8_x,
                df.loc[idx, "GPPH9"]= gpph9_x,
                df.loc[idx, "GPPH10"]= gpph10_x,
                df.loc[idx, "Kesimpulan GPPH"]= kesimpulan_gpph_x,
                df.loc[idx, "Emosi1"]= emosi1_x,
                df.loc[idx, "Emosi2"]= emosi2_x,
                df.loc[idx, "Emosi3"]= emosi3_x,
                df.loc[idx, "Emosi4"]= emosi4_x,
                df.loc[idx, "Emosi5"]= emosi5_x,
                df.loc[idx, "Emosi6"]= emosi6_x,
                df.loc[idx, "Emosi7"]= emosi7_x,
                df.loc[idx, "Emosi8"]= emosi8_x,
                df.loc[idx, "Emosi9"]= emosi9_x,
                df.loc[idx, "Emosi10"]= emosi10_x,
                df.loc[idx, "Emosi11"]= emosi11_x,
                df.loc[idx, "Emosi12"]= emosi12_x,
                df.loc[idx, "Emosi13"]= emosi13_x,
                df.loc[idx, "Emosi14"]= emosi14_x,
                df.loc[idx, "Kesimpulan Emosi"]= kesimpulan_emosi_x,
                df.loc[idx, "Karies Dentis"]= gigi_x,
                df.loc[idx, "HB"]= hb_x,
                df.loc[idx, "Eritrosit"]= eritrosit_x,
                df.loc[idx, "Hematokrit"]= htc_x,
                df.loc[idx, "Leukosit"]= leukosit_x,
                df.loc[idx, "Trombosit"]= trombosit_x,
                df.loc[idx, "MCV"]= mcv_x,
                df.loc[idx, "MCH"]= mch_x,
                df.loc[idx, "MCHC"]= mchc_x,
                df.loc[idx, "RDW"]= rdw_x,
                df.loc[idx, "GDS"]= gds_x,
                df.loc[idx, "Index Mentzer"]= mentzer_x
                
                
            else:
                # Jika nama tidak ditemukan, tambahkan data baru
                df = pd.concat([df, updated_data], ignore_index=True)

            # Update data ke Google Sheets
            conn.update(worksheet='pkg_balita', data=df)
            st.success("Data berhasil disimpan.")

            st.cache_data.clear()
    
elif selected == 'Pemeriksaan Dewasa':
    st.markdown(
        """
        <style>
        .stApp {
            # background-color: #EDE0D4;
            background-color: #FFCBA4;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.title('FORMULIR PEMERIKSAAN USIA DEWASA (18-59 TAHUN)')

    # Inisialisasi koneksi ke Google Sheets
    conn = st.connection("gsheets", type=GSheetsConnection)

    @st.cache_data
    # Cache untuk mengambil data dari Google Sheets dan menghindari pemrosesan ulang
    def load_data_from_gsheet():
        df = conn.read(worksheet="pkg", usecols=list(range(174)), ttl=5)
        df = df.dropna(how='all')
        return df

    # Load the data from Google Sheets
    df = load_data_from_gsheet()

    nik = st.text_input('NIK', key='input_nik')

    # Menggunakan session_state untuk menyimpan data yang di-load
    if 'input_nik_loaded' not in st.session_state:
        st.session_state.input_nik_loaded = False
    if 'input_data' not in st.session_state:
        st.session_state.input_data = {}
        
    # Fungsi untuk mengisi form berdasarkan nik
    def load_data_by_nik():
        nik_input = st.session_state.input_nik.strip()
        if nik_input:
            # Convert the 'NIK' column to string before using str.contains
            df['NIK'] = df['NIK'].astype(str)
            
            # Search for NIK in the dataframe
            data = df[df['NIK'].str.contains(nik_input, case=False, na=False)]
            
            if not data.empty:
                # If found, store the data in session_state
                st.session_state.input_data = data.iloc[0].to_dict()
                st.session_state.input_nik_loaded = True
                st.success("Data berhasil dimuat.")
            else:
                st.warning("NIK tidak ditemukan.")
        else:
            st.warning("NIK tidak boleh kosong.")

    # Button to load data based on NIK
    btn_load = st.button('Load', key='btn_load')

    if btn_load:
        load_data_by_nik()

    # Tombol untuk menambahkan data baru
    btn_add = st.button('Tambah Data Baru', key='btn_add')

    if btn_add:
        # Set session state untuk memastikan inputan muncul
        st.session_state.add_new_data = True  # Menandakan kita menambah data baru

    # Formulir inputan untuk data baru hanya tampil jika btn_add ditekan
    if 'add_new_data' in st.session_state and st.session_state.add_new_data:
        # Menampilkan form inputan untuk data baru
        with st.expander('**Identitas Pasien**'):
            left, right = st.columns(2, vertical_alignment='top')
            
            nama = left.text_input('Nama Lengkap', key='nama')
            nik = left.text_input('NIK', key='nik')
            jk = left.selectbox('Jenis Kelamin', ('Laki-laki', 'Perempuan'), index=None, key='jk')
            
            if st.session_state.jk == 'Laki-laki':
                st.session_state.caparu1 = 'Laki-laki'
                st.session_state.ppok1 = 'Laki-laki'
                st.session_state.caco2 = 'Laki-laki'
                st.session_state.jcs1 = 'Laki-laki'
            elif st.session_state.jk == 'Perempuan':
                st.session_state.caparu1 = 'Perempuan'
                st.session_state.ppok1 = 'Perempuan'
                st.session_state.caco2 = 'Perempuan'
                st.session_state.jcs1 = 'Perempuan'
            
            from datetime import datetime
            tanggal_lahir = right.date_input("Pilih Tanggal Lahir", format='DD/MM/YYYY', value=None, max_value="today", min_value=datetime(1930, 1, 1).date(), key='tl')
            def hitung_usia(tanggal_lahir):
                # Mendapatkan tanggal saat ini
                tanggal_sekarang = datetime.now().date()
                usia = tanggal_sekarang.year - tanggal_lahir.year
                if (tanggal_sekarang.month, tanggal_sekarang.day) < (tanggal_lahir.month, tanggal_lahir.day):
                    usia -= 1
                return usia
            if tanggal_lahir:
                usia = hitung_usia(tanggal_lahir)
                umur=right.number_input('Usia (tahun)', value=usia, disabled=True, key='umur')
            else:
                umur=right.number_input('Usia (tahun)', value=0, disabled=True, key='umur')
                
                if st.session_state.umur is not None:
                    if st.session_state.umur <= 45:
                        st.session_state.caparu2 = '</=45 tahun'
                    elif 46 <= st.session_state.umur <= 65:
                        st.session_state.caparu2 = '46-65 tahun'
                    else:
                        st.session_state.caparu2 = '>65 tahun'
                        
                if st.session_state.umur is not None:
                    if 40 <= st.session_state.umur <= 49:
                        st.session_state.ppok2 = '40-49 tahun'
                    elif 50 <= st.session_state.umur <= 59:
                        st.session_state.ppok2 = '50-59 tahun'
                    elif st.session_state.umur >=60:
                        st.session_state.ppok2 = '>/=60 tahun'
                    else:
                        st.session_state.ppok2 = None
                
                if st.session_state.umur is not None:
                    if st.session_state.umur < 50:
                        st.session_state.caco1 = '<50 tahun'
                    elif 50 <= st.session_state.umur <= 69:
                        st.session_state.caco1 = '50-69 tahun'
                    else:
                        st.session_state.caco1 = '>/=70 tahun'
                        
                if st.session_state.umur is not None:
                    if 23 <= st.session_state.umur <= 34:
                        st.session_state.jcs2 = '25-34 tahun'
                    elif 35 <= st.session_state.umur <= 39:
                        st.session_state.jcs2 = '35-39 tahun'
                    elif 40 <= st.session_state.umur <= 44:
                        st.session_state.jcs2 = '40-44 tahun'
                    elif 45 <= st.session_state.umur <= 49:
                        st.session_state.jcs2 = '45-49 tahun'
                    elif 50 <= st.session_state.umur <= 54:
                        st.session_state.jcs2 = '50-54 tahun'
                    elif 55 <= st.session_state.umur <= 59:
                        st.session_state.jcs2 = '55-59 tahun'
                    elif 60 <= st.session_state.umur <= 64:
                        st.session_state.jcs2 = '60-64 tahun'
                    else:
                        st.session_state.jcs2 = None
            
            alamat=left.text_input('Alamat (Harus meliputi kelurahan dan RT)', key='alamat')
            hp=right.text_input('Nomor HP', key='hp')
            
        with st.expander('**Riwayat Penyakit Dahulu**'):
            left, right = st.columns(2, vertical_alignment="top")
            def update_radio_buttons():
                if st.session_state.rpd_semua == 'Ya':
                    st.session_state.rpd_ht = 'Ya'
                    st.session_state.rpd_dm = 'Ya'
                    st.session_state.rpd_jtg = 'Ya'
                    st.session_state.rpd_stroke = 'Ya'
                    st.session_state.rpd_asma = 'Ya'
                    st.session_state.rpd_ca = 'Ya'
                    st.session_state.rpd_cho = 'Ya'
                    st.session_state.rpd_ppok = 'Ya'
                    st.session_state.rpd_talasemia = 'Ya'
                    st.session_state.rpd_lupus = 'Ya'
                    st.session_state.rpd_lihat = 'Ya'
                    st.session_state.rpd_katarak = 'Ya'
                    st.session_state.rpd_dengar = 'Ya'
                elif st.session_state.rpd_semua == 'Tidak':
                    st.session_state.rpd_ht = 'Tidak'
                    st.session_state.rpd_dm = 'Tidak'
                    st.session_state.rpd_jtg = 'Tidak'
                    st.session_state.rpd_stroke = 'Tidak'
                    st.session_state.rpd_asma = 'Tidak'
                    st.session_state.rpd_ca = 'Tidak'
                    st.session_state.rpd_cho = 'Tidak'
                    st.session_state.rpd_ppok = 'Tidak'
                    st.session_state.rpd_talasemia = 'Tidak'
                    st.session_state.rpd_lupus = 'Tidak'
                    st.session_state.rpd_lihat = 'Tidak'
                    st.session_state.rpd_katarak = 'Tidak'
                    st.session_state.rpd_dengar = 'Tidak'
                elif st.session_state.rpd_semua == 'Tidak Tahu':
                    st.session_state.rpd_ht = 'Tidak Tahu'
                    st.session_state.rpd_dm = 'Tidak Tahu'
                    st.session_state.rpd_jtg = 'Tidak Tahu'
                    st.session_state.rpd_stroke = 'Tidak Tahu'
                    st.session_state.rpd_asma = 'Tidak Tahu'
                    st.session_state.rpd_ca = 'Tidak Tahu'
                    st.session_state.rpd_cho = 'Tidak Tahu'
                    st.session_state.rpd_ppok = 'Tidak Tahu'
                    st.session_state.rpd_talasemia = 'Tidak Tahu'
                    st.session_state.rpd_lupus = 'Tidak Tahu'
                    st.session_state.rpd_lihat = 'Tidak Tahu'
                    st.session_state.rpd_katarak = 'Tidak Tahu'
                    st.session_state.rpd_dengar = 'Tidak Tahu'
            rpd_semua = left.radio('**Pilih Semua**', ['Ya', 'Tidak', 'Tidak Tahu'], horizontal=True, index=None, key='rpd_semua', on_change=update_radio_buttons)
            rpd_ht = left.radio('Hipertensi', ['Ya', 'Tidak', 'Tidak Tahu'], horizontal=True, index=None, key='rpd_ht')
            rpd_dm = left.radio('Diabetes Melitus', ['Ya', 'Tidak', 'Tidak Tahu'], horizontal=True, index=None, key='rpd_dm')
            rpd_jtg = left.radio('Penyakit Jantung', ['Ya', 'Tidak', 'Tidak Tahu'], horizontal=True, index=None, key='rpd_jtg')
            rpd_stroke = left.radio('Penyakit Stroke', ['Ya', 'Tidak', 'Tidak Tahu'], horizontal=True, index=None, key='rpd_stroke')
            rpd_asma = left.radio('Asma', ['Ya', 'Tidak', 'Tidak Tahu'], horizontal=True, index=None, key='rpd_asma')
            rpd_ca = left.radio('Penyakit Kanker', ['Ya', 'Tidak', 'Tidak Tahu'], horizontal=True, index=None, key='rpd_ca')
            rpd_cho = right.radio('Kolesterol Tinggi', ['Ya', 'Tidak', 'Tidak Tahu'], horizontal=True, index=None, key='rpd_cho')
            rpd_ppok = right.radio('PPOK', ['Ya', 'Tidak', 'Tidak Tahu'], horizontal=True, index=None, key='rpd_ppok')
            rpd_talasemia = right.radio('Thalasemia', ['Ya', 'Tidak', 'Tidak Tahu'], horizontal=True, index=None, key='rpd_talasemia')
            rpd_lupus = right.radio('Lupus', ['Ya', 'Tidak', 'Tidak Tahu'], horizontal=True, index=None, key='rpd_lupus')
            rpd_lihat = right.radio('Gangguan Pengelihatan', ['Ya', 'Tidak', 'Tidak Tahu'], horizontal=True, index=None, key='rpd_lihat')
            rpd_katarak = right.radio('Katarak', ['Ya', 'Tidak', 'Tidak Tahu'], horizontal=True, index=None, key='rpd_katarak')
            rpd_dengar = right.radio('Gangguan Pendengaran', ['Ya', 'Tidak', 'Tidak Tahu'], horizontal=True, index=None, key='rpd_dengar')
        
        with st.expander('**Riwayat Penyakit Keluarga**'):
            left, right = st.columns(2, vertical_alignment="top")
            def update_radio_buttons():
                if st.session_state.rpk_semua == 'Ya':
                    st.session_state.rpk_ht = 'Ya'
                    st.session_state.rpk_dm = 'Ya'
                    st.session_state.rpk_jtg = 'Ya'
                    st.session_state.rpk_stroke = 'Ya'
                    st.session_state.rpk_ca = 'Ya'
                    st.session_state.rpk_talasemia = 'Ya'
                elif st.session_state.rpk_semua == 'Tidak':
                    st.session_state.rpk_ht = 'Tidak'
                    st.session_state.rpk_dm = 'Tidak'
                    st.session_state.rpk_jtg = 'Tidak'
                    st.session_state.rpk_stroke = 'Tidak'
                    st.session_state.rpk_ca = 'Tidak'
                    st.session_state.rpk_talasemia = 'Tidak'
                elif st.session_state.rpk_semua == 'Tidak Tahu':
                    st.session_state.rpk_ht = 'Tidak Tahu'
                    st.session_state.rpk_dm = 'Tidak Tahu'
                    st.session_state.rpk_jtg = 'Tidak Tahu'
                    st.session_state.rpk_stroke = 'Tidak Tahu'
                    st.session_state.rpk_ca = 'Tidak Tahu'
                    st.session_state.rpk_talasemia = 'Tidak Tahu'
            rpk_semua = left.radio('**Pilih Semua**', ['Ya', 'Tidak', 'Tidak Tahu'], horizontal=True, index=None, key='rpk_semua', on_change=update_radio_buttons)
            rpk_ht = left.radio('Hipertensi', ['Ya', 'Tidak', 'Tidak Tahu'], horizontal=True, index=None, key='rpk_ht')
            rpk_dm = left.radio('Diabetes Melitus', ['Ya', 'Tidak', 'Tidak Tahu'], horizontal=True, index=None, key='rpk_dm')
            rpk_jtg = left.radio('Penyakit Jantung', ['Ya', 'Tidak', 'Tidak Tahu'], horizontal=True, index=None, key='rpk_jtg')
            rpk_stroke = right.radio('Penyakit Stroke', ['Ya', 'Tidak', 'Tidak Tahu'], horizontal=True, index=None, key='rpk_stroke')
            rpk_ca = right.radio('Penyakit Kanker', ['Ya', 'Tidak', 'Tidak Tahu'], horizontal=True, index=None, key='rpk_ca')
            rpk_talasemia = right.radio('Thalasemia atau Transfusi Darah Rutin', ['Ya', 'Tidak', 'Tidak Tahu'], horizontal=True, index=None, key='rpk_talasemia')
        
        with st.expander('**Riwayat Kebiasaan**'):  
            rk_rokok = st.radio('Kebiasaan Merokok', ['Ya', 'Tidak'], horizontal=True, index=None, key='rk_rokok')
            if rk_rokok == 'Ya':
                rk_rokokperhari = st.number_input('Rata-rata Jumlah Rokok/hari', value=0, key='rokokperhari', disabled=False)
                rk_lamamerokok = st.number_input('Lama Merokok dalam Tahun', value=0, key='lamarokok', disabled=False)
                rph = float(rk_rokokperhari)
                lmr = float(rk_lamamerokok)
                packyear = rph*lmr/20
                rk_packyear = st.number_input('Pack Year', value=packyear, key='packyear', disabled=True)
                
            else:
                rk_rokokperhari = st.number_input('Rata-rata Jumlah Rokok/hari', value=0, key='rokokperhari', disabled=True)
                rk_lamamerokok = st.number_input('Lama Merokok dalam Tahun', value=0, key='lamarokok', disabled=True)
                rk_packyear = st.number_input('Pack Year', value=0, key='packyear', disabled=True)
           
            if st.session_state.packyear is not None:
                if 0 < st.session_state.packyear < 20:
                    st.session_state.ppok3 = '<20 packs/years'
                elif 20 <= st.session_state.packyear <= 30:
                    st.session_state.ppok3 = '20-30 packs/years'
                elif st.session_state.packyear >30:
                    st.session_state.ppok3 = '>30 packs/years'
                else:
                    st.session_state.ppok3 = None

            rk_manis = st.radio('Apakah anda menambahkan gula pada makanan/minuman >4 sendok makan/hari?', ['Ya, Setiap Hari', 'Ya, Tidak Setiap Hari', 'Tidak'], horizontal=True, index=None, key='rk_manis')
            rk_asin = st.radio('Apakah anda menggunakan garam pada makanan >1 sendok teh/hari?', ['Ya, Setiap Hari', 'Ya, Tidak Setiap Hari', 'Tidak'], horizontal=True, index=None, key='rk_asin')
            rk_lemak = st.radio('Apakah anda mengonsumsi makanan yang diolah dengan minyak >5 sendok makan/hari?', ['Ya, Setiap Hari', 'Ya, Tidak Setiap Hari', 'Tidak'], horizontal=True, index=None, key='rk_lemak')
            rk_sayur = st.radio('Apakah anda mengonsumsi sayur/buah?', ['Ya, Setiap Hari', 'Ya, Tidak Setiap Hari', 'Tidak'], horizontal=True, index=None, key='rk_sayur')
            rk_olahraga = st.radio('Apakah anda berolahraga?', ['Ya, >30 menit/hari(>150 menit/minggu)', 'Ya, <30 menit/hari(<150 menit/minggu)', 'Tidak'], horizontal=False, index=None, key='rk_olahraga')
            rk_alkohol = st.radio('Apakah anda mengonsumsi alkohol 1 bulan terakhir?', ['Ya, Setiap Hari', 'Ya, Tidak Setiap Hari', 'Tidak'], horizontal=True, index=None, key='rk_alkohol')
            
        with st.expander('**Pemeriksaan Dasar**'):
            left, right = st.columns(2, vertical_alignment="top")
            tds = left.text_input('Tekanan Darah Sistole', key='tds')
            tdd= left.text_input('Tekanan Darah Diastole', key='tdd')
            hr=left.text_input('Frekuensi Nadi', key='hr')
            rr=left.text_input('Frekuensi Napas', key='rr')
            temp=left.text_input('Suhu Badan', key='temp')
            bb=right.text_input('Berat Badan(kg)', key='bb')
            tb=right.text_input('Tinggi Badan(cm)', key='tb')
            def hitung_bmi(tb,bb):
                a= float(tb)**2/10000
                b= float(bb)
                imt= b/a
                return imt
    
            if st.session_state.tb and st.session_state.bb is not None:
                imt = hitung_bmi(tb, bb)
                bmi=right.number_input('Indeks Massa Tubuh', value=imt, disabled=True, key='bmi')
            else:
                bmi=right.number_input('Indeks Massa Tubuh', value=0, disabled=True, key='bmi')
            
            if st.session_state.bmi is not None:
                if 13.79 <= st.session_state.bmi <= 25.99:
                    st.session_state.jcs4 = '13.79-25.99'
                elif 26 <= st.session_state.bmi <= 29.9:
                    st.session_state.jcs4 = '26-29.99'
                elif 30 <= st.session_state.bmi <= 35.58:
                    st.session_state.jcs4 = '30-35.58'
                else:
                    st.session_state.jcs4 = None
            
            lp=right.text_input('Lingkar Perut(cm)', key='lp')
            lla=right.text_input('Lingkar Lengan Atas(Untuk Wanita dan Lansia)', key='lla')
                    
        with st.expander('**Skrining Kesehatan Jiwa**'):
            st.markdown('**Pilihlah salah satu jawaban untuk setiap pertanyaan yang sesuai dengan perasaan anda dalam 2 minggu terakhir!**')
            left, right = st.columns(2, vertical_alignment="top")
            with left:
                phq1=st.radio('Dalam 2 minggu terakhir, seberapa sering anda kurang/tidak bersemangat dalam melakukan kegiatan sehari-hari?', ['Tidak sama sekali', 'Kurang dari 1 minggu', 'Lebih dari 1 minggu', 'Hampir setiap hari'], index=None, key='phq1') 
            with right:
                gad1=st.radio('Dalam 2 minggu terakhir, seberapa sering anda merasa gugup, cemas, atau gelisah?', ['Tidak sama sekali', 'Kurang dari 1 minggu', 'Lebih dari 1 minggu', 'Hampir setiap hari'], index=None, key='gad1')
            
            left, right = st.columns(2, vertical_alignment="top")
            with left:
                phq2=st.radio('Dalam 2 minggu terakhir, seberapa sering anda merasa murung, tertekan, atau putus asa?', ['Tidak sama sekali', 'Kurang dari 1 minggu', 'Lebih dari 1 minggu', 'Hampir setiap hari'], index=None, key='phq2')
            with right:
                gad2=st.radio('Dalam 2 minggu terakhir, seberapa sering anda tidak mampu mengendalikan rasa khawatir?', ['Tidak sama sekali', 'Kurang 1 minggu', 'Lebih dari 1 minggu', 'Hampir setiap hari'], index=None, key='gad2')
            
            def calculate_score1(phq1, phq2):
                score = 0

                if phq1 == 'Tidak sama sekali':
                    score += 0
                elif phq1 == 'Kurang dari 1 minggu':
                    score += 1
                elif phq1 == 'Lebih dari 1 minggu':
                    score += 2
                elif phq1 == 'Hampir setiap hari':
                    score += 3
                    
                if phq2 == 'Tidak sama sekali':
                    score += 0
                elif phq2 == 'Kurang dari 1 minggu':
                    score += 1
                elif phq2 == 'Lebih dari 1 minggu':
                    score += 2
                elif phq2 == 'Hampir setiap hari':
                    score += 3
                
                return score
            
            # Hitung total skor
            total_score1 = calculate_score1(phq1, phq2)

            # Penjelasan untuk hasil skor
            if total_score1 < 3:
                depresi = st.text_input('Subskor Depresi', value='Tidak ada gejala signifikan', disabled=True, key='depresi')
            elif total_score1 >= 3:
                depresi = st.text_input('Subskor Depresi', value='Kemungkinan gejala depresi', disabled=True, key='depresi')
            
            
            def calculate_score2(gad1, gad2):
                score = 0

                if gad1 == 'Tidak sama sekali':
                    score += 0
                elif gad1 == 'Kurang dari 1 minggu':
                    score += 1
                elif gad1 == 'Lebih dari 1 minggu':
                    score += 2
                elif gad1 == 'Hampir setiap hari':
                    score += 3
                    
                if gad2 == 'Tidak sama sekali':
                    score += 0
                elif gad2 == 'Kurang dari 1 minggu':
                    score += 1
                elif gad2 == 'Lebih dari 1 minggu':
                    score += 2
                elif gad2 == 'Hampir setiap hari':
                    score += 3
                
                return score
            
            # Hitung total skor
            total_score2 = calculate_score2(gad1, gad2)

            # Penjelasan untuk hasil skor
            if total_score2 < 3:
                cemas = st.text_input('Subskor Kecemasan', value='Tidak ada gejala signifikan', disabled=True, key='cemas')
            elif total_score2 >= 3:
                cemas = st.text_input('Subskor Kecemasan', value='Kemungkinan gejala kecemasan', disabled=True, key='cemas')
            
        with st.expander('**Skrining Indera Pendengaran**'):
            left, right = st.columns(2, vertical_alignment="top")
            bisikad=left.text_input('Tes Bisik AD', key='bisikad')
            bisikas=right.text_input('Tes Bisik AS', key='bisikas')
            otoskopiad=left.text_input('Otoskopi AD', key='otoskopiad')
            otoskopias=right.text_input('Otoskopi AS', key='otoskopias')
            rinne=left.text_input('Rinne Test', key='rinne')
            weber=left.text_input('Weber Test', key='weber')
            schwabach=right.text_input('Schwabach Test', key='schwabach')
                        
        with st.expander('**Skrining Kanker Paru**'):
            caparu1=st.radio('Jenis Kelamain', ['Laki-laki', 'Perempuan'], horizontal=True, index=None, key='caparu1')
            caparu2=st.radio('Kelompok Usia', ['>65 tahun', '46-65 tahun', '</=45 tahun'], horizontal=True, index=None, key='caparu2')
            caparu3=st.radio('Pernah menderita/didiagnosis kanker?', ['Ya, Pernah tahun lalu', 'Ya, Pernah <5 tahun yang lalu', 'Tidak Pernah'], horizontal=True, index=None, key='caparu3')
            caparu4=st.radio('Apakah ada keluarga (ayah/ibu/saudara kandung) didiagnosis atau menderita kanker sebelumnya?', ['Ya, ada kanker paru', 'Ya, ada kanker jenis lain', 'Tidak'], horizontal=True, index=None, key='caparu4')   
            caparu5=st.radio('Riwayat merokok/paparan asap rokok (rokok kretek/rokok putih/vape/shisya/cerutu/rokok linting, dll)', ['Perokok aktif (dalam 1 tahun ini masih merokok)', 'Bekas perokok, berhenti <15 tahun yang lalu', 'Perokok pasif (paparan dari lingkungan rumah/tempat kerja)', 'Tidak merokok'], horizontal=False, index=None, key='caparu5')
            caparu6=st.radio('Riwayat tempat kerja mengandung zat karsinogenik (pertambangan/ pabrik/ bengkel/ garmen/ bangunan/ laboratorium kimia/ galangan kapal, dll)', ['Ya', 'Tidak Yakin/Ragu-ragu', 'Tidak'], horizontal=True, index=None, key='caparu6')
            caparu7=st.radio('Lingkungan tempat tinggal berpotensi tinggi (lingkungan pabrik/ pertambangan/ tempat pembuangan sampah/ tepi jalan besar)', ['Ya', 'Tidak Yakin/Ragu-ragu', 'Tidak'], horizontal=True, index=None, key='caparu7')
            caparu8=st.radio('Lingkungan dalam rumah yang berisiko (ventilasi buruk/ atap dari asbes/ lantai tanah/ dapur kayu bakar/ dapur breket/ menggunakan rutin obat nyamuk bakar/ semprot, dll)', ['Ya', 'Tidak Yakin/Ragu-ragu', 'Tidak'], horizontal=True, index=None, key='caparu8')
            caparu9=st.radio('Pernah didiagnosis/diobati penyakit paru kronik', ['Ya, Pernah. TB', 'Ya, Pernah. Penyakit Paru kronik Lain (PPOK)', 'Tidak Pernah'], horizontal=True, index=None, key='caparu9')

            # Fungsi untuk menghitung skor
            def calculate_score(caparu1, caparu2, caparu3, caparu4, caparu5, caparu6, caparu7, caparu8, caparu9):
                score = 0

                if caparu1 == 'Laki-laki':
                    score += 3
                elif caparu1 == 'Perempuan':
                    score += 1
                
                if caparu2 == '65 tahun':
                    score += 3
                elif caparu2 == '46-65 tahun':
                    score += 2
                elif caparu2 == '</=45 tahun':
                    score += 1
                
                if caparu3 == 'Ya, Pernah tahun lalu':
                    score += 3
                elif caparu3 == 'Ya, Pernah <5 tahun yang lalu':
                    score += 2
                elif caparu3 == 'Tidak Pernah':
                    score += 1
                    
                if caparu4 == 'Ya, ada kanker paru':
                    score += 3
                elif caparu4 == 'Ya, ada kanker jenis lain':
                    score += 2
                elif caparu4 == 'Tidak':
                    score += 1
                    
                if caparu5 == 'Perokok aktif (dalam 1 tahun ini masih merokok)':
                    score += 4
                elif caparu5 == 'Bekas perokok, berhenti <15 tahun yang lalu':
                    score += 3
                elif caparu5 == 'Perokok pasif (paparan dari lingkungan rumah/tempat kerja)':
                    score += 2
                elif caparu5 == 'Tidak merokok':
                    score += 1

                if caparu6 == 'Ya':
                    score += 3
                elif caparu6 == 'Tidak Yakin/Ragu-ragu':
                    score += 2
                elif caparu6 == 'Tidak':
                    score += 1
                
                if caparu7 == 'Ya':
                    score += 3
                elif caparu7 == 'Tidak Yakin/Ragu-ragu':
                    score += 2
                elif caparu7 == 'Tidak':
                    score += 1
                    
                if caparu8 == 'Ya':
                    score += 3
                elif caparu8 == 'Tidak Yakin/Ragu-ragu':
                    score += 2
                elif caparu8 == 'Tidak':
                    score += 1
                
                if caparu9 == 'Ya, Pernah. TB':
                    score += 3
                elif caparu9 == 'Ya, Pernah. Penyakit Paru kronik Lain (PPOK)':
                    score += 2
                elif caparu9 == 'Tidak Pernah':
                    score += 0
                
                return score

            # Hitung total skor
            total_score = calculate_score(caparu1, caparu2, caparu3, caparu4, caparu5, caparu6, caparu7, caparu8, caparu9)

            # Tampilkan total skor
            caparu_tot=st.text_input('Jumlah Skor', value=str(total_score), disabled=True, key='caparu_tot')

            # Penjelasan untuk hasil skor
            if total_score <= 11:
                st.success("Risiko Ringan Kanker Paru.")
            elif 12<=total_score <= 16:
                st.warning("Risiko Sedang Kanker Paru.")
            elif 17<=total_score <= 29:
                st.warning("Risiko Berat Kanker Paru.")

        with st.expander('**Skrining PPOK(PUMA)**'):
            ppok1=st.radio('Jenis Kelamain', ['Perempuan', 'Laki-laki'], horizontal=True, index=None, key='ppok1')
            ppok2=st.radio('Kelompok Usia', ['40-49 tahun', '50-59 tahun', '>/=60 tahun'], horizontal=True, index=None, key='ppok2')
            ppok3=st.radio('Kebiasaan merokok', ['Tidak', '<20 packs/years', '20-30 packs/years', '>30 packs/years'], horizontal=False, index=None, key='ppok3')
            ppok4=st.radio('Apakah anda pernah merasa napas pendek ketika anda berjalan lebih cepat pada jalan yang datar atau pada jalan yang sedikit menanjak?', ['Tidak', 'Ya'], horizontal=True, index=None, key='ppok4')   
            ppok5=st.radio('Apakah anda biasanya mempunyai dahak yang berasal dari paru atau kesulitan mengeluarkan dahak saat anda tidak sedang menderita salesma/flu?', ['Tidak', 'Ya'], horizontal=True, index=None, key='ppok5')
            ppok6=st.radio('Apakah anda biasanya batuk saat anda tidak sedang menderita salesma/flu?', ['Tidak', 'Ya'], horizontal=True, index=None, key='ppok6')
            ppok7=st.radio('Apakah dokter atau tenaga medis lainnya pernah meminta anda untuk melakukan pemeriksaan spirometri?', ['Tidak', 'Ya'], horizontal=True, index=None, key='ppok7')

            # Fungsi untuk menghitung skor
            def calculate_score(ppok1, ppok2, ppok3, ppok4, ppok5, ppok6, ppok7):
                score = 0

                if ppok1 == 'Laki-laki':
                    score += 1

                if ppok2 == '40-49 tahun':
                    score += 0
                elif ppok2 == '50-59 tahun':
                    score += 1
                elif ppok2 == '>/=60 tahun':
                    score += 2  
                
                if ppok3 == 'Tidak':
                    score += 0
                elif ppok3 == '<20 packs/years':
                    score += 0
                elif ppok3 == '20-30 packs/years':
                    score += 1
                elif ppok3 == '>30 packs/years':
                    score += 2
                
                if ppok4 == 'Tidak':
                    score += 0
                elif ppok4 == 'Ya':
                    score += 1
                
                if ppok5 == 'Tidak':
                    score += 0
                elif ppok5 == 'Ya':
                    score += 1
                    
                if ppok6 == 'Tidak':
                    score += 0
                elif ppok6 == 'Ya':
                    score += 1
                    
                if ppok7 == 'Tidak':
                    score += 0
                elif ppok7 == 'Ya':
                    score += 1

                return score

            # Hitung total skor
            total_score = calculate_score(ppok1, ppok2, ppok3, ppok4, ppok5, ppok6, ppok7)

            # Tampilkan total skor
            ppok_tot=st.text_input('Jumlah Skor', value=str(total_score), disabled=True, key='ppok_tot')

            # Penjelasan untuk hasil skor
            if total_score < 6:
                st.success("Risiko Rendah PPOK.")
            elif total_score >= 6:
                st.warning("Risiko Tinggi PPOK.")
        
        with st.expander('**Skrining Gejala TB**'):
            left, right = st.columns(2, vertical_alignment='top')
            tb1 = left.radio('Batuk >1 minggu?', ['Ya', 'Tidak'], horizontal=True, index=None, key='tb1')
            tb2 = left.radio('Demam yang tidak diketahui penyebabnya?', ['Ya', 'Tidak'], horizontal=True, index=None, key='tb2')
            tb3 = left.radio('Batuk disertai darah?', ['Ya', 'Tidak'], horizontal=True, index=None, key='tb3')
            tb4 = left.radio('Keringat malam tanpa beraktivitas?', ['Ya', 'Tidak'], horizontal=True, index=None, key='tb4')
            tb5 = right.radio('Penurunan Berat Badan tanpa penyebab yang jelas?', ['Ya', 'Tidak'], horizontal=True, index=None, key='tb5')
            tb6 = right.radio('Pernah minum pengobatan TB sebelumnya?', ['Ya', 'Tidak'], horizontal=True, index=None, key='tb6')
            tb7 = right.radio('Terdapat keluarga atau tetangga yang batuk lama/pengobatan TB?', ['Ya', 'Tidak'], horizontal=True, index=None, key='tb7')

        with st.expander('**Skrining Kanker Kolorektal**'):
            caco1 = st.radio('Kelompok Usia?', ['<50 tahun', '50-69 tahun', '>/=70 tahun'], horizontal=True, index=None, key='caco1')
            caco2 = st.radio('Jenis Kelamin?', ['Perempuan', 'Laki-laki'], horizontal=True, index=None, key='caco2')
            caco3 = st.radio('Riwayat keluarga kanker kolorektal generasi pertama (Ayah, ibu, kakak dan adik kandung)?', ['Ada', 'Tidak ada'], horizontal=True, index=None, key='caco3')
            caco4 = st.radio('Riwayat Merokok?', ['Tidak Pernah', 'Saat ini merokok atau dulu pernah merokok'], horizontal=True, index=None, key='caco4')
            
            # Fungsi untuk menghitung skor
            def calculate_score(caco1, caco2, caco3, caco4):
                score = 0
                # Penentuan skor berdasarkan kelompok usia
                if caco1 == '<50 tahun':
                    score += 0
                elif caco1 == '50-69 tahun':
                    score += 2
                elif caco1 == '>/=70 tahun':
                    score += 3

                if caco2 == 'Laki-laki':
                    score += 1 

                if caco3 == 'Ada':
                    score += 2 

                if caco4 == 'Saat ini merokok atau dulu pernah merokok':
                    score += 1  

                return score
            
            # Hitung total skor
            total_score = calculate_score(caco1, caco2, caco3, caco4)

            # Tampilkan total skor
            caco_tot = st.text_input('Jumlah Skor', value=str(total_score), disabled=True, key='caco_tot')

            # Penjelasan untuk hasil skor
            if total_score < 2:
                st.success("Risiko Rendah kanker kolorektal.")
            elif 2<= total_score <= 3:
                st.warning("Risiko Sedang kanker kolorektal.")
            else:
                st.warning("Risiko Tinggi kanker kolorektal.")

            caco5 = st.text_input('Rectal Toucher', key='caco5')
            caco6 = st.radio('Fecal Occult Bleeding Test', ['Negatif', '+1', '+2', '+3', '+4'], horizontal=False, index=None, key='caco6')

        with st.expander('**Skrining Kanker Payudara dan Serviks**'):
            left, right = st.columns(2, vertical_alignment='top' )
            menarche=left.number_input('Usia haid pertama (tahun)', key='menarche')
            hpht=left.date_input('HPHT', key='hpht', format='DD/MM/YYYY', value=None)
            seks_pertama=left.number_input('Usia pertama kali berhubungan seksual (tahun)', key='seks_pertama')
            hamil_pertama=left.number_input('Usia kehamilan pertama (tahun)', key='hamil_pertama')
            jml_melahirkan=left.number_input('Jumlah melahirkan', key='jml_melahirkan')
            menyusui=left.radio('Pernah menyusui', ['Ya', 'Tidak'], index=None, key='menyusui', horizontal=True)
            left.text('Riwayat Pemakaian KB')
            pil=left.radio('Pil', ['Ya', 'Tidak'], index=None, key='pil', horizontal=True)
            if st.session_state.pil == 'Ya':
                lama_pil=left.text_input('Lama Penggunaan (pil)', key='lama_pil', disabled=False)
            else:
                lama_pil=left.text_input('Lama Penggunaan (pil)', key='lama_pil', disabled=True)
            suntik=left.radio('Suntik', ['Ya', 'Tidak'], index=None, key='suntik', horizontal=True)
            if st.session_state.suntik == 'Ya':
                lama_suntik=left.text_input('Lama Penggunaan (suntik)', key='lama_suntik', disabled=False)
            else:
                lama_suntik=left.text_input('Lama Penggunaan (suntik)', key='lama_suntik', disabled=True)
            implan=left.radio('Implan', ['Ya', 'Tidak'], index=None, key='implan', horizontal=True)
            if st.session_state.implan == 'Ya':
                lama_implan=left.text_input('Lama Penggunaan (implan)', key='lama_implan', disabled=False)
            else:
                lama_implan=left.text_input('Lama Penggunaan (implan)', key='lama_implan', disabled=True) 
            iud=left.radio('IUD', ['Ya', 'Tidak'], index=None, key='iud', horizontal=True)
            if st.session_state.iud == 'Ya':
                lama_iud=left.text_input('Lama Penggunaan (iud)', key='lama_iud', disabled=False)
            else:
                lama_iud=left.text_input('Lama Penggunaan (iud)', key='lama_iud', disabled=True)
                
            ca_keluarga=left.radio('Riwayat kanker dalam keluarga', ['Ya', 'Tidak'], index=None, key='ca_keluarga', horizontal=True)
            if st.session_state.ca_keluarga == 'Ya':
                #Jika ya, siapa?
                keluarga_siapa=left.text_input('Siapa yang menderita kanker?', value=None, key='keluarga_siapa', disabled=False)
                #kanker jenis apa
                ca_apa=left.text_input('Kanker jenis apa?', value=None, key='ca_apa', disabled= False)
            else:
                #Jika ya, siapa?
                keluarga_siapa=left.text_input('Siapa yang menderita kanker?', value=None, key='keluarga_siapa', disabled=True)
                #kanker jenis apa
                ca_apa=left.text_input('Kanker jenis apa?', value=None, key='ca_apa', disabled= True)
                
            tumorjinak=left.radio('Riwayat tumor jinak payudara', ['Ya', 'Tidak'], index=None, key='tumorjinak', horizontal=True)
            menopause=left.radio('Apakah sudah menopause', ['Sudah', 'Belum'], index=None, key='menopause', horizontal=True)
            usia_menopause=left.number_input('Usia menopause (tahun)', key='usia_menopause')
            pernah_pap=right.radio('Pernah Pap Smear', ['Ya', 'Tidak'], index=None, key='pernah_pap', horizontal=True)
            if st.session_state.pernah_pap == 'Ya':
                kapan_pap=right.text_input('Kapan', key='kapan_pap', disabled=False)
                hasil_pap=right.text_input('Hasil Pap Smear', key='hasil_pap', disabled= False)
            else:
                kapan_pap=right.text_input('Kapan', key='kapan_pap', disabled=True)
                hasil_pap=right.text_input('Hasil Pap Smear', key='hasil_pap', disabled= True)
            pernah_iva=right.radio('Pernah IVA', ['Ya', 'Tidak'], index=None, key='pernah_iva', horizontal=True)
            if st.session_state.pernah_iva == 'Ya':
                kapan_iva=right.text_input('Kapan', key='kapan_iva', disabled= False)
                hasil_iva=right.text_input('Hasil IVA', key='hasil_iva', disabled= False)
            else:
                kapan_iva=right.text_input('Kapan', key='kapan_iva', disabled= True)
                hasil_iva=right.text_input('Hasil IVA', key='hasil_iva', disabled= True)
            benjolan_payudara=right.radio('Apakah terdapat benjolan di payudara dan ketiak?', ['Ya', 'Tidak'], index=None, key='benjolan_payudara', horizontal=True)
            cairan_puting=right.radio('Apakah terdapat cairan keluar dari puting susu?', ['Ya', 'Tidak'], index=None, horizontal=True, key='cairan_puting')
            perubahan=right.radio('Apakah terdapat perubahan lainnya pada payudara?', ['Ya', 'Tidak'], index=None, horizontal=True, key='perubahan')
            #jika ya, sebutkan kelainannya
            if st.session_state.perubahan == 'Ya':
                jenis_perubahan=right.text_input('Sebutkan jenis perubahannya?', value=None, key='jenis_perubahan', disabled=False)
            else:
                jenis_perubahan=right.text_input('Sebutkan jenis perubahannya?', value=None, key='jenis_perubahan', disabled=True)
            metroragi=right.radio('Apakah terdapat perdarahan di luar massa haid?', ['Ya', 'Tidak'], index=None, horizontal=True, key='metroragi')
            darah_seks=right.radio('Apakah terdapat perdarahan saat/setelah berhubungan seks?', ['Ya', 'Tidak'], index=None, horizontal=True, key='darah_seks')
            keputihan=right.radio('Apakah anda sering keputihan?', ['Ya', 'Tidak'], index=None, horizontal=True, key='keputihan')
            lap=right.radio('Apakah anda mengalami nyeri perut bagian bawah?', ['Ya', 'Tidak'], index=None, horizontal=True, key='lap')
            sadanisd=right.text_area('SADANIS Payudara Kanan', key='sadanisd')
            sadaniss=right.text_area('SADANIS Payudara Kiri', key='sadaniss')
            iva=right.text_area('Inspeksi Visual Asam Asetat', key='iva')
            hpv=right.text_area('Pemeriksaan HPV DNA', key='hpv')
                    
        with st.expander('**Skrining Hepatitis**'):
            left, right = st.columns(2, vertical_alignment='top')
            hep1=left.radio('Apakah anda pernah menjalani tes untuk Hepatitis B dan hasilnya positif?', ['Ya', 'Tidak'], index=None, horizontal=True, key='hep1')
            hep2=left.radio('Apakah anda memiliki saudara kandung yang menderita Hepatitis B?', ['Ya', 'Tidak'], index=None, horizontal=True, key='hep2')
            hep3=left.radio('Apakah anda pernah pernah berhubungan seksual dengan orang yang bukan pasangan resmi anda?', ['Ya', 'Tidak'], index=None, horizontal=True, key='hep3')
            hep4=left.radio('Apakah anda pernah menerima transfusi darah sebelumnya?', ['Ya', 'Tidak'], index=None, horizontal=True, key='hep4')
            hep5=right.radio('Apakah anda pernah menjalani cuci darah/hemodialisis sebelumnya?', ['Ya', 'Tidak'], index=None, horizontal=True, key='hep5')
            hep6=right.radio('Apakah anda pernah menggunakan narkoba, obat terlarang, atau bahan adiktif lainnya dengan cara disuntik?', ['Ya', 'Tidak'], index=None, horizontal=True, key='hep6')
            hep7=right.radio('Apakah anda adalah orang dengan HIV (ODHIV)?', ['Ya', 'Tidak'], index=None, horizontal=True, key='hep7')
            hep8=right.radio('Apakah anda pernah mendapatkan pengobatan Hepatitis C dan tidak sembuh?', ['Ya', 'Tidak'], index=None, horizontal=True, key='hep8')
            
        with st.expander('**Skrining Indera Pengelihatan**'):
            left, right = st.columns(2, vertical_alignment='top')
            visusod=left.text_input('Visus OD', key='visusod')
            visusos=right.text_input('Visus OS', key='visusos')
            katarakod=left.radio('Katarak OD', ['Ya', 'Tidak'], index=None, horizontal=True, key='katarakod')
            katarakos=right.radio('Katarak OS', ['Ya', 'Tidak'], index=None, horizontal=True, key='katarakos')
            
        with st.expander('**Skrining Jantung**'):
            st.markdown('**Jakarta Cardiovascular Score**')
            jcs1=st.radio('Jenis Kelamin', ['Perempuan', 'Laki-laki'], index=None, key='jcs1', horizontal=True)
            jcs2=st.radio('Kelompok Umur', ['25-34 tahun', '35-39 tahun', '40-44 tahun', '45-49 tahun', '50-54 tahun', '55-59 tahun', '60-64 tahun'], index=None, key='jcs2', horizontal=True)
            jcs3=st.radio('Kelompok Tekanan Darah', ['<130/<84', '130-139/85-89', '140-159/90-99', '160-179/100-109', '>=180/>=110'], index=None, key='jcs3', horizontal=True)
            jcs4=st.radio('Kelompok IMT', ['13.79-25.99', '26-29.99', '30-35.58'], index=None, key='jcs4', horizontal=True)
            jcs5=st.radio('Status Merokok', ['Tidak Pernah', 'Mantan Perokok', 'Perokok Aktif'], index=None, key='jcs5', horizontal=True)
            jcs6=st.radio('Diabetes Melitus', ['Tidak', 'Ya'], index=None, key='jcs6', horizontal=True)
            jcs7=st.radio('Aktivitas Fisik Mingguan', ['Tidak Ada', 'Rendah', 'Sedang', 'Berat'], index=None, key='jcs7', horizontal=True)

            # Fungsi untuk menghitung skor
            def calculate_score(jcs1, jcs2, jcs3, jcs4, jcs5, jcs6, jcs7):
                score = 0

                if jcs1 == 'Laki-laki':
                    score += 1
                elif jcs1 == 'Perempuan':
                    score += 0
                
                if jcs2 == '25-34 tahun':
                    score -= 4
                elif jcs2 == '35-39 tahun':
                    score -= 3
                elif jcs2 == '40-44 tahun':
                    score -= 2
                elif jcs2 == '45-49 tahun':
                    score += 0
                elif jcs2 == '50-54 tahun':
                    score += 1
                elif jcs2 == '55-59 tahun':
                    score += 2
                elif jcs2 == '60-64 tahun':
                    score += 3
                
                if jcs3 == '<130/<84':
                    score += 0
                elif jcs3 == '130-139/85-89':
                    score += 1
                elif jcs3 == '140-159/90-99':
                    score += 2
                elif jcs3 == '160-179/100-109':
                    score += 3
                elif jcs3 == '>=180/>=110':
                    score += 4
                
                # '13.79-25.99', '26-29.99', '30-35.58'
                if jcs4 == '13.79-25.99':
                    score += 0
                elif jcs4 == '26-29.99':
                    score += 1
                elif jcs4 == '30-35.58':
                    score += 2
                
                # 'Tidak Pernah', 'Mantan Perokok', 'Perokok Aktif'
                if jcs5 == 'Tidak Pernah':
                    score += 0
                elif jcs5 == 'Mantan Perokok':
                    score += 3
                elif jcs5 == 'Perokok Aktif':
                    score += 4
                # 'Tidak', 'Ya'
                if jcs6 == 'Tidak':
                    score += 0
                elif jcs6 == 'Ya':
                    score += 2
                # 'Tidak Ada', 'Rendah', 'Sedang', 'Berat'
                if jcs7 == 'Tidak Ada':
                    score += 2
                elif jcs7 == 'Rendah':
                    score += 1
                elif jcs7 == 'Sedang':
                    score += 0
                elif jcs7 == 'Berat':
                    score -= 3
                
                return score

            # Hitung total skor
            total_score = calculate_score(jcs1, jcs2, jcs3, jcs4, jcs5, jcs6, jcs7)

            # Tampilkan total skor
            jcs_tot=st.text_input('Jumlah Skor', value=str(total_score), disabled=True, key='jcs_tot')

            # Penjelasan untuk hasil skor
            if -7<=total_score <= 1:
                st.success("Risiko Rendah Penyakit Kardiovaskular.")
            elif 2<=total_score <= 4:
                st.warning("Risiko Sedang Penyakit Kardiovaskular.")
            elif total_score >=5:
                st.warning("Risiko Tinggi Penyakit Kardiovaskular.")        
        
            ekg=st.text_area('Interpretasi Hasil Pemeriksaan EKG', key='ekg')

        with st.expander('**Skrining Gigi**'):
            left, right = st.columns(2, vertical_alignment='top')
            karies=left.text_input('Karies', value=None, key='karies')
            missing=left.text_input('Missing', value=None, key='missing')
            pocket=right.radio('Periodontal Pocket', ['Ya', 'Tidak'], index=None, horizontal=True, key='pocket')
            goyang=right.text_input('Gigi Goyang', value=None, key='goyang')

        with st.expander('**Pemeriksaan Laboratorium**'):
            left, middle, right = st.columns(3, vertical_alignment="top")
            hb=left.text_input('Hb', key='hb')
            wbc=left.text_input('Leukosit', key='wbc')
            hct=left.text_input('Hematokrit', key='hct')
            rbc=left.text_input('Eritrosit', key='rbc')
            plt=left.text_input('Trombosit', key='plt')
            mcv=left.text_input('MCV', key='mcv')
            mch=left.text_input('MCH', key='mch')
            mchc=middle.text_input('MCHC', key='mchc')
            gds=middle.text_input('Gula Darah Sewaktu', key='gds')
            gdp=middle.text_input('Gula Darah Puasa', key='gdp')
            cho=middle.text_input('Kolesterol Total', key='cho')
            hdl=middle.text_input('HDL', key='hdl')
            ldl=middle.text_input('LDL', key='ldl')
            tg=middle.text_input('Trigliserida', key='tg')
            ur=right.text_input('Ureum', key='ur')
            cr=right.text_input('Kreatinin', key='cr')
            ot=right.text_input('SGOT', key='ot')
            pt=right.text_input('SGPT', key='pt')
            hepb=right.selectbox('Hepatitis B', ['Reaktif', 'Non-Reaktif'], index=None, key='hepb')
            hepc=right.selectbox('Hepatitis C', ['Reaktif', 'Non-Reaktif'], index=None, key='hepc')   
            tcm=right.text_input('Sputum TCM', key='tcm')
            
            
        # Tombol untuk menyimpan data baru
        btn_save_add = st.button('Simpan Data Baru', key='btn_save_add')
        
        if btn_save_add:
            # Menyimpan data baru ke dalam Google Sheets
            new_data = pd.DataFrame(
                [
                    {
                        "Nama": nama,
                        "NIK": nik.strip(),
                        "Jenis Kelamin": jk,
                        "Tanggal Lahir": tanggal_lahir,
                        "Usia": umur,
                        "Alamat": alamat,
                        "Nomor HP": hp,
                        "RPD Hipertensi": rpd_ht,
                        "RPD DM":rpd_dm,
                        "RPD Penyakit Jantung": rpd_jtg,
                        "RPD Stroke": rpd_stroke,
                        "RPD Asma": rpd_asma,
                        "RPD Kanker": rpd_ca,
                        "RPD Kolesterol": rpd_cho,
                        "RPD PPOK": rpd_ppok,
                        "RPD Talasemia":rpd_talasemia,
                        "RPD Lupus": rpd_lupus,
                        "RPD Gangguan Pengelihatan": rpd_lihat,
                        "RPD Katarak": rpd_katarak,
                        "RPD Gangguan Pendengaran": rpd_dengar,
                        "RPK Hipertensi": rpk_ht,
                        "RPK DM": rpk_dm,
                        "RPK Penyakit Jantung": rpk_jtg,
                        "RPK Stroke": rpk_stroke,
                        "RPK Kanker": rpk_ca,
                        "RPK Talasemia": rpk_talasemia,
                        "RK Merokok": rk_rokok,
                        "RK Rokok PerHari": rk_rokokperhari,
                        "RK Lama Merokok": rk_lamamerokok,
                        "Pack Years": rk_packyear,
                        "RK Makan Manis": rk_manis,
                        "RK Makan Asin": rk_asin,
                        "RK Makan Berlemak": rk_lemak,
                        "RK Makan Sayur": rk_sayur,
                        "RK Olahraga": rk_olahraga,
                        "RK Konsumsi Alkohol": rk_alkohol,
                        "TD Sistole": tds,
                        "TD Diastole":tdd,
                        "Heart Rate": hr,
                        "Respiration Rate": rr,
                        "Suhu Badan": temp,
                        "Berat Badan":bb,
                        "Tinggi Badan":tb,
                        "IMT": bmi,
                        "Lingkar Perut": lp,
                        "Lingkar Lengan Atas": lla,
                        "PHQ1" : phq1,
                        "PHQ2" : phq2,
                        "GAD1" : gad1,
                        "GAD2" : gad2,
                        "Depresi" : depresi,
                        "Cemas" : cemas,
                        "Tes Bisik AD": bisikad,
                        "Tes Bisik AS": bisikas,
                        "Otoskopi AD": otoskopiad,
                        "Otoskopi AS": otoskopias,
                        "Rinne": rinne,
                        "Weber": weber,
                        "Schwabach": schwabach,
                        "Ca Paru 1": caparu1,
                        "Ca Paru 2": caparu2,
                        "Ca Paru 3": caparu3,
                        "Ca Paru 4": caparu4,
                        "Ca Paru 5": caparu5,
                        "Ca Paru 6": caparu6,
                        "Ca Paru 7": caparu7,
                        "Ca Paru 8": caparu8,
                        "Ca Paru 9": caparu9,
                        "Total Skor Ca Paru": caparu_tot,
                        "PPOK 1": ppok1,
                        "PPOK 2": ppok2,
                        "PPOK 3": ppok3,
                        "PPOK 4": ppok4,
                        "PPOK 5": ppok5,
                        "PPOK 6": ppok6,
                        "PPOK 7": ppok7,
                        "Total Skor PPOK": ppok_tot,
                        "TB 1": tb1,
                        "TB 2": tb2,
                        "TB 3": tb3,
                        "TB 4": tb4,
                        "TB 5": tb5,
                        "TB 6": tb6,
                        "TB 7": tb7,
                        "Ca Kolorektal 1": caco1,
                        "Ca Kolorektal 2": caco2,
                        "Ca Kolorektal 3": caco3,
                        "Ca Kolorektal 4": caco4,
                        "Total Skor Ca Kolorektal": caco_tot,
                        "Rectal Toucher": caco5,
                        "FOBT": caco6,
                        "Menarche": menarche,
                        "HPHT": hpht,
                        "Usia Pertama Kali Seks": seks_pertama,
                        "Usia Kehamilan Pertama": hamil_pertama,
                        "Jumlah Melahirkan": jml_melahirkan,
                        "Menyusui": menyusui,
                        "Pil": pil,
                        "Lama Pil": lama_pil,
                        "Suntik": suntik,
                        "Lama Suntik": lama_suntik,
                        "Implan": implan,
                        "Lama Implan": lama_implan,
                        "IUD": iud,
                        "Lama IUD": lama_iud,
                        "Riwayat Kanker Keluarga": ca_keluarga,
                        "Siapa Yang Menderita Kanker": keluarga_siapa,
                        "Kanker Jenis Apa": ca_apa,
                        "Riwayat Tumor Jinak Payudara": tumorjinak,
                        "Menopause": menopause,
                        "Usia Menopause": usia_menopause,
                        "Pernah PAP Smear": pernah_pap,
                        "Kapan PAP Smear": kapan_pap,
                        "Hasil PAP Smear": hasil_pap,
                        "Pernah IVA": pernah_iva,
                        "Kapan IVA": kapan_iva,
                        "Hasil IVA": hasil_iva,
                        "Benjolan Di Payudara Dan Ketiak": benjolan_payudara,
                        "Cairan Dari Puting": cairan_puting,
                        "Perubahan Pada Payudara": perubahan,
                        "Jenis Perubahan Payudara": jenis_perubahan,
                        "Perdarahan Di Luar Haid": metroragi,
                        "Perdarahan Saat Berhubungan": darah_seks,
                        "Sering Keputihan": keputihan,
                        "Nyeri Perut Bawah": lap,
                        "Sadanis Payudara Kanan": sadanisd,
                        "Sadanis Payudara Kiri": sadaniss,
                        "IVA": iva,
                        "HPV DNA": hpv,
                        "Hepatitis 1": hep1,
                        "Hepatitis 2": hep2,
                        "Hepatitis 3": hep3,
                        "Hepatitis 4": hep4,
                        "Hepatitis 5": hep5,
                        "Hepatitis 6": hep6,
                        "Hepatitis 7": hep7,
                        "Hepatitis 8": hep8,
                        "Hepatitis B": hepb,
                        "Hepatitis C": hepc,
                        "Visus OD": visusod,
                        "Visus OS": visusos,
                        "Katarak OD": katarakod,
                        "Katarak OS": katarakos,
                        "JCS 1": jcs1,
                        "JCS 2": jcs2,
                        "JCS 3": jcs3,
                        "JCS 4": jcs4,
                        "JCS 5": jcs5,
                        "JCS 6": jcs6,
                        "JCS 7": jcs7,
                        "Total Skor JCS": jcs_tot,
                        "Interpretasi EKG": ekg,
                        "Karies": karies,
                        "Missing": missing,
                        "Periodontal Pocket": pocket,
                        "Gigi Goyang": goyang,
                        "Hb": hb,
                        "Leukosit": wbc,
                        "Hematokrit": hct,
                        "Eritrosit": rbc,
                        "Trombosit": plt,
                        "MCV": mcv, 
                        "MCH": mch,
                        "MCHC": mchc,
                        "GDS": gds,
                        "GDP": gdp,
                        "Kolesterol Total": cho,
                        "HDL": hdl,
                        "LDL": ldl,
                        "Trigliserida": tg,
                        "Ureum": ur,
                        "Kreatinin": cr,
                        "SGOT": ot,
                        "SGPT":pt,
                        "Sputum TCM": tcm
                    }
                ]
            )
            
            # Menambahkan data baru ke DataFrame yang ada
            df = pd.concat([df, new_data], ignore_index=True)

            # Update data ke Google Sheets
            conn.update(worksheet='pkg', data=df)
            st.success("Data baru berhasil disimpan.")
            
            # Reset session_state after save to clear the form
            st.cache_data.clear()


    # Formulir input dengan pre-filled data jika ada
    if st.session_state.input_nik_loaded:
        with st.expander('**Identitas Pasien**', expanded=True):
            left, right = st.columns(2, vertical_alignment='top')
            
            nama_x = left.text_input('Nama Lengkap', value=st.session_state.input_data.get('Nama', ''), key='nama_x')
            nik_x = left.text_input('NIK', value=st.session_state.input_data.get('NIK', ''), key='nik_x', disabled=True)
            
            jenis_kelamin_value = st.session_state.input_data.get('Jenis Kelamin', None)    
            if pd.isna(jenis_kelamin_value):
                jk_x = st.radio('Jenis Kelamin', ['Laki-laki', 'Perempuan'], index=None, horizontal=True, key='jk_x')
            else:
                jk_x = st.radio('Jenis Kelamin', ['Laki-laki', 'Perempuan'],
                            index=['Laki-laki', 'Perempuan'].index(jenis_kelamin_value),
                            horizontal=True, key='jk_x')
            
            if st.session_state.jk_x == 'Laki-laki':
                st.session_state.caparu1_x = 'Laki-laki'
                st.session_state.ppok1_x = 'Laki-laki'
                st.session_state.caco2_x = 'Laki-laki'
                st.session_state.jcs1_x = 'Laki-laki'
            elif st.session_state.jk_x == 'Perempuan':
                st.session_state.caparu1_x = 'Perempuan'
                st.session_state.ppok1_x = 'Perempuan'
                st.session_state.caco2_x = 'Perempuan'
                st.session_state.jcs1_x = 'Perempuan'
            
            from datetime import datetime
            # tanggal_lahir_x = right.date_input("Pilih Tanggal Lahir", format='DD/MM/YYYY', value=st.session_state.input_data.get('Tanggal Lahir', None), max_value="today", min_value=datetime(1930, 1, 1).date(), key='tl_x')
            tanggal_lahir_x_value = st.session_state.input_data.get('Tanggal Lahir', None)
            if pd.isna(tanggal_lahir_x_value):
                tanggal_lahir_x = right.date_input("Pilih Tanggal Lahir", format='DD/MM/YYYY', value=None, max_value="today", min_value=datetime(1930, 1, 1).date(), key='tl_x')
            else:
                tanggal_lahir_x = right.date_input("Pilih Tanggal Lahir", format='DD/MM/YYYY', value=tanggal_lahir_x_value, max_value="today", min_value=datetime(1930, 1, 1).date(), key='tl_x')

            def hitung_usia(tanggal_lahir_x):
                # Mendapatkan tanggal saat ini
                tanggal_sekarang = datetime.now().date()
                usia = tanggal_sekarang.year - tanggal_lahir_x.year
                if (tanggal_sekarang.month, tanggal_sekarang.day) < (tanggal_lahir_x.month, tanggal_lahir_x.day):
                    usia -= 1
                return usia
            if tanggal_lahir_x:
                usia = hitung_usia(tanggal_lahir_x)
                umur_x=right.number_input('Usia (tahun)', value=usia, disabled=True, key='umur_x')
            else:
                umur_x=right.number_input('Usia (tahun)', value=0, disabled=True, key='umur_x')
                
                if st.session_state.umur_x is not None:
                    if st.session_state.umur_x <= 45:
                        st.session_state.caparu2_x = '</=45 tahun'
                    elif 46 <= st.session_state.umur_x <= 65:
                        st.session_state.caparu2_x = '46-65 tahun'
                    else:
                        st.session_state.caparu2_x = '>65 tahun'
                        
                if st.session_state.umur_x is not None:
                    if 40 <= st.session_state.umur_x <= 49:
                        st.session_state.ppok2_x = '40-49 tahun'
                    elif 50 <= st.session_state.umur_x <= 59:
                        st.session_state.ppok2_x = '50-59 tahun'
                    elif st.session_state.umur_x >=60:
                        st.session_state.ppok2_x = '>/=60 tahun'
                    else:
                        st.session_state.ppok2_x = None
                
                if st.session_state.umur_x is not None:
                    if st.session_state.umur_x < 50:
                        st.session_state.caco1_x = '<50 tahun'
                    elif 50 <= st.session_state.umur_x <= 69:
                        st.session_state.caco1_x = '50-69 tahun'
                    else:
                        st.session_state.caco1_x = '>/=70 tahun'
                
                if st.session_state.umur_x is not None:
                    if 23 <= st.session_state.umur_x <= 34:
                        st.session_state.jcs2_x = '25-34 tahun'
                    elif 35 <= st.session_state.umur_x <= 39:
                        st.session_state.jcs2_x = '35-39 tahun'
                    elif 40 <= st.session_state.umur_x <= 44:
                        st.session_state.jcs2_x = '40-44 tahun'
                    elif 45 <= st.session_state.umur_x <= 49:
                        st.session_state.jcs2_x = '45-49 tahun'
                    elif 50 <= st.session_state.umur_x <= 54:
                        st.session_state.jcs2_x = '50-54 tahun'
                    elif 55 <= st.session_state.umur_x <= 59:
                        st.session_state.jcs2_x = '55-59 tahun'
                    elif 60 <= st.session_state.umur_x <= 64:
                        st.session_state.jcs2_x = '60-64 tahun'
                    else:
                        st.session_state.jcs2_x = None
            
            # alamat_x=left.text_input('Alamat (Harus meliputi kelurahan dan RT)', value=st.session_state.input_data.get('Alamat', ''), key='alamat_x')
            # hp_x=right.text_input('Nomor HP', value=st.session_state.input_data.get('Nomor HP', ''), key='hp_x')

            alamat_x_value = st.session_state.input_data.get('Alamat', '')
            if pd.isna(alamat_x_value):
                alamat_x = left.text_input('Alamat (Harus meliputi kelurahan dan RT)', value=None, key='alamat_x')
            else:
                alamat_x = left.text_input('Alamat (Harus meliputi kelurahan dan RT)', value=alamat_x_value, key='alamat_x')

            # Right column: HP
            hp_x_value = st.session_state.input_data.get('Nomor HP', '')
            if pd.isna(hp_x_value):
                hp_x = right.text_input('Nomor HP', value=None, key='hp_x')
            else:
                hp_x = right.text_input('Nomor HP', value=hp_x_value, key='hp_x')

        with st.expander('**Riwayat Penyakit Dahulu**'):
            left, right = st.columns(2, vertical_alignment="top")
            def update_radio_buttons():
                if st.session_state.rpd_semua_x == 'Ya':
                    st.session_state.rpd_ht_x = 'Ya'
                    st.session_state.rpd_dm_x = 'Ya'
                    st.session_state.rpd_jtg_x = 'Ya'
                    st.session_state.rpd_stroke_x = 'Ya'
                    st.session_state.rpd_asma_x = 'Ya'
                    st.session_state.rpd_ca_x = 'Ya'
                    st.session_state.rpd_cho_x = 'Ya'
                    st.session_state.rpd_ppok_x = 'Ya'
                    st.session_state.rpd_talasemia_x = 'Ya'
                    st.session_state.rpd_lupus_x = 'Ya'
                    st.session_state.rpd_lihat_x = 'Ya'
                    st.session_state.rpd_katarak_x = 'Ya'
                    st.session_state.rpd_dengar_x = 'Ya'
                elif st.session_state.rpd_semua_x == 'Tidak':
                    st.session_state.rpd_ht_x = 'Tidak'
                    st.session_state.rpd_dm_x = 'Tidak'
                    st.session_state.rpd_jtg_x = 'Tidak'
                    st.session_state.rpd_stroke_x = 'Tidak'
                    st.session_state.rpd_asma_x = 'Tidak'
                    st.session_state.rpd_ca_x = 'Tidak'
                    st.session_state.rpd_cho_x = 'Tidak'
                    st.session_state.rpd_ppok_x = 'Tidak'
                    st.session_state.rpd_talasemia_x = 'Tidak'
                    st.session_state.rpd_lupus_x = 'Tidak'
                    st.session_state.rpd_lihat_x = 'Tidak'
                    st.session_state.rpd_katarak_x = 'Tidak'
                    st.session_state.rpd_dengar_x = 'Tidak'
                elif st.session_state.rpd_semua_x == 'Tidak Tahu':
                    st.session_state.rpd_ht_x = 'Tidak Tahu'
                    st.session_state.rpd_dm_x = 'Tidak Tahu'
                    st.session_state.rpd_jtg_x = 'Tidak Tahu'
                    st.session_state.rpd_stroke_x = 'Tidak Tahu'
                    st.session_state.rpd_asma_x = 'Tidak Tahu'
                    st.session_state.rpd_ca_x = 'Tidak Tahu'
                    st.session_state.rpd_cho_x = 'Tidak Tahu'
                    st.session_state.rpd_ppok_x = 'Tidak Tahu'
                    st.session_state.rpd_talasemia_x = 'Tidak Tahu'
                    st.session_state.rpd_lupus_x = 'Tidak Tahu'
                    st.session_state.rpd_lihat_x = 'Tidak Tahu'
                    st.session_state.rpd_katarak_x = 'Tidak Tahu'
                    st.session_state.rpd_dengar_x = 'Tidak Tahu'
            rpd_semua_x = left.radio('**Pilih Semua**', ['Ya', 'Tidak', 'Tidak Tahu'], horizontal=True, index=None, key='rpd_semua_x', on_change=update_radio_buttons)
            rpd_ht_value = st.session_state.input_data.get('RPD Hipertensi', None)
            if pd.isna(rpd_ht_value):
                rpd_ht_x = left.radio('Hipertensi', ['Ya', 'Tidak', 'Tidak Tahu'], horizontal=True, index=None, key='rpd_ht_x')
            else:
                rpd_ht_x = left.radio('Hipertensi', ['Ya', 'Tidak', 'Tidak Tahu'],
                                    index=['Ya', 'Tidak', 'Tidak Tahu'].index(rpd_ht_value),
                                    horizontal=True, key='rpd_ht_x')

            rpd_dm_value = st.session_state.input_data.get('RPD DM', None)
            if pd.isna(rpd_dm_value):
                rpd_dm_x = left.radio('Diabetes Melitus', ['Ya', 'Tidak', 'Tidak Tahu'], horizontal=True, index=None, key='rpd_dm_x')
            else:
                rpd_dm_x = left.radio('Diabetes Melitus', ['Ya', 'Tidak', 'Tidak Tahu'],
                                    index=['Ya', 'Tidak', 'Tidak Tahu'].index(rpd_dm_value),
                                    horizontal=True, key='rpd_dm_x')

            rpd_jtg_value = st.session_state.input_data.get('RPD Penyakit Jantung', None)
            if pd.isna(rpd_jtg_value):
                rpd_jtg_x = left.radio('Penyakit Jantung', ['Ya', 'Tidak', 'Tidak Tahu'], horizontal=True, index=None, key='rpd_jtg_x')
            else:
                rpd_jtg_x = left.radio('Penyakit Jantung', ['Ya', 'Tidak', 'Tidak Tahu'],
                                    index=['Ya', 'Tidak', 'Tidak Tahu'].index(rpd_jtg_value),
                                    horizontal=True, key='rpd_jtg_x')

            rpd_stroke_value = st.session_state.input_data.get('RPD Stroke', None)
            if pd.isna(rpd_stroke_value):
                rpd_stroke_x = left.radio('Penyakit Stroke', ['Ya', 'Tidak', 'Tidak Tahu'], horizontal=True, index=None, key='rpd_stroke_x')
            else:
                rpd_stroke_x = left.radio('Penyakit Stroke', ['Ya', 'Tidak', 'Tidak Tahu'],
                                        index=['Ya', 'Tidak', 'Tidak Tahu'].index(rpd_stroke_value),
                                        horizontal=True, key='rpd_stroke_x')

            rpd_asma_value = st.session_state.input_data.get('RPD Asma', None)
            if pd.isna(rpd_asma_value):
                rpd_asma_x = left.radio('Asma', ['Ya', 'Tidak', 'Tidak Tahu'], horizontal=True, index=None, key='rpd_asma_x')
            else:
                rpd_asma_x = left.radio('Asma', ['Ya', 'Tidak', 'Tidak Tahu'],
                                    index=['Ya', 'Tidak', 'Tidak Tahu'].index(rpd_asma_value),
                                    horizontal=True, key='rpd_asma_x')

            rpd_ca_value = st.session_state.input_data.get('RPD Kanker', None)
            if pd.isna(rpd_ca_value):
                rpd_ca_x = left.radio('Penyakit Kanker', ['Ya', 'Tidak', 'Tidak Tahu'], horizontal=True, index=None, key='rpd_ca_x')
            else:
                rpd_ca_x = left.radio('Penyakit Kanker', ['Ya', 'Tidak', 'Tidak Tahu'],
                                    index=['Ya', 'Tidak', 'Tidak Tahu'].index(rpd_ca_value),
                                    horizontal=True, key='rpd_ca_x')

            rpd_cho_value = st.session_state.input_data.get('RPD Kolesterol', None)
            if pd.isna(rpd_cho_value):
                rpd_cho_x = right.radio('Kolesterol Tinggi', ['Ya', 'Tidak', 'Tidak Tahu'], horizontal=True, index=None, key='rpd_cho_x')
            else:
                rpd_cho_x = right.radio('Kolesterol Tinggi', ['Ya', 'Tidak', 'Tidak Tahu'],
                                    index=['Ya', 'Tidak', 'Tidak Tahu'].index(rpd_cho_value),
                                    horizontal=True, key='rpd_cho_x')

            rpd_ppok_value = st.session_state.input_data.get('RPD PPOK', None)
            if pd.isna(rpd_ppok_value):
                rpd_ppok_x = right.radio('PPOK', ['Ya', 'Tidak', 'Tidak Tahu'], horizontal=True, index=None, key='rpd_ppok_x')
            else:
                rpd_ppok_x = right.radio('PPOK', ['Ya', 'Tidak', 'Tidak Tahu'],
                                    index=['Ya', 'Tidak', 'Tidak Tahu'].index(rpd_ppok_value),
                                    horizontal=True, key='rpd_ppok_x')

            rpd_talasemia_value = st.session_state.input_data.get('RPD Talasemia', None)
            if pd.isna(rpd_talasemia_value):
                rpd_talasemia_x = right.radio('Thalasemia', ['Ya', 'Tidak', 'Tidak Tahu'], horizontal=True, index=None, key='rpd_talasemia_x')
            else:
                rpd_talasemia_x = right.radio('Thalasemia', ['Ya', 'Tidak', 'Tidak Tahu'],
                                        index=['Ya', 'Tidak', 'Tidak Tahu'].index(rpd_talasemia_value),
                                        horizontal=True, key='rpd_talasemia_x')

            rpd_lupus_value = st.session_state.input_data.get('RPD Lupus', None)
            if pd.isna(rpd_lupus_value):
                rpd_lupus_x = right.radio('Lupus', ['Ya', 'Tidak', 'Tidak Tahu'], horizontal=True, index=None, key='rpd_lupus_x')
            else:
                rpd_lupus_x = right.radio('Lupus', ['Ya', 'Tidak', 'Tidak Tahu'],
                                        index=['Ya', 'Tidak', 'Tidak Tahu'].index(rpd_lupus_value),
                                        horizontal=True, key='rpd_lupus_x')

            rpd_lihat_value = st.session_state.input_data.get('RPD Gangguan Pengelihatan', None)
            if pd.isna(rpd_lihat_value):
                rpd_lihat_x = right.radio('Gangguan Pengelihatan', ['Ya', 'Tidak', 'Tidak Tahu'], horizontal=True, index=None, key='rpd_lihat_x')
            else:
                rpd_lihat_x = right.radio('Gangguan Pengelihatan', ['Ya', 'Tidak', 'Tidak Tahu'],
                                    index=['Ya', 'Tidak', 'Tidak Tahu'].index(rpd_lihat_value),
                                    horizontal=True, key='rpd_lihat_x')

            rpd_katarak_value = st.session_state.input_data.get('RPD Katarak', None)
            if pd.isna(rpd_katarak_value):
                rpd_katarak_x = right.radio('Katarak', ['Ya', 'Tidak', 'Tidak Tahu'], horizontal=True, index=None, key='rpd_katarak_x')
            else:
                rpd_katarak_x = right.radio('Katarak', ['Ya', 'Tidak', 'Tidak Tahu'],
                                        index=['Ya', 'Tidak', 'Tidak Tahu'].index(rpd_katarak_value),
                                        horizontal=True, key='rpd_katarak_x')

            rpd_dengar_value = st.session_state.input_data.get('RPD Gangguan Pendengaran', None)
            if pd.isna(rpd_dengar_value):
                rpd_dengar_x = right.radio('Gangguan Pendengaran', ['Ya', 'Tidak', 'Tidak Tahu'], horizontal=True, index=None, key='rpd_dengar_x')
            else:
                rpd_dengar_x = right.radio('Gangguan Pendengaran', ['Ya', 'Tidak', 'Tidak Tahu'],
                                        index=['Ya', 'Tidak', 'Tidak Tahu'].index(rpd_dengar_value),
                                        horizontal=True, key='rpd_dengar_x')
        
        with st.expander('**Riwayat Penyakit Keluarga**'):
            left, right = st.columns(2, vertical_alignment="top")
            def update_radio_buttons():
                if st.session_state.rpk_semua_x == 'Ya':
                    st.session_state.rpk_ht_x = 'Ya'
                    st.session_state.rpk_dm_x = 'Ya'
                    st.session_state.rpk_jtg_x = 'Ya'
                    st.session_state.rpk_stroke_x = 'Ya'
                    st.session_state.rpk_ca_x = 'Ya'
                    st.session_state.rpk_talasemia_x = 'Ya'
                elif st.session_state.rpk_semua_x == 'Tidak':
                    st.session_state.rpk_ht_x = 'Tidak'
                    st.session_state.rpk_dm_x = 'Tidak'
                    st.session_state.rpk_jtg_x = 'Tidak'
                    st.session_state.rpk_stroke_x = 'Tidak'
                    st.session_state.rpk_ca_x = 'Tidak'
                    st.session_state.rpk_talasemia_x = 'Tidak'
                elif st.session_state.rpk_semua_x == 'Tidak Tahu':
                    st.session_state.rpk_ht_x = 'Tidak Tahu'
                    st.session_state.rpk_dm_x = 'Tidak Tahu'
                    st.session_state.rpk_jtg_x = 'Tidak Tahu'
                    st.session_state.rpk_stroke_x = 'Tidak Tahu'
                    st.session_state.rpk_ca_x = 'Tidak Tahu'
                    st.session_state.rpk_talasemia_x = 'Tidak Tahu'
            rpk_semua_x = left.radio('**Pilih Semua**', ['Ya', 'Tidak', 'Tidak Tahu'], horizontal=True, index=None, key='rpk_semua_x', on_change=update_radio_buttons)
            # Retrieve existing values from session_state and set radio buttons accordingly
            rpk_ht_x_value = st.session_state.input_data.get('RPK Hipertensi', None)
            if pd.isna(rpk_ht_x_value):
                rpk_ht_x = left.radio('Hipertensi', ['Ya', 'Tidak', 'Tidak Tahu'], horizontal=True, index=None, key='rpk_ht_x')
            else:
                rpk_ht_x = left.radio('Hipertensi', ['Ya', 'Tidak', 'Tidak Tahu'],
                                    index=['Ya', 'Tidak', 'Tidak Tahu'].index(rpk_ht_x_value),
                                    horizontal=True, key='rpk_ht_x')

            rpk_dm_x_value = st.session_state.input_data.get('RPK DM', None)
            if pd.isna(rpk_dm_x_value):
                rpk_dm_x = left.radio('Diabetes Melitus', ['Ya', 'Tidak', 'Tidak Tahu'], horizontal=True, index=None, key='rpk_dm_x')
            else:
                rpk_dm_x = left.radio('Diabetes Melitus', ['Ya', 'Tidak', 'Tidak Tahu'],
                                    index=['Ya', 'Tidak', 'Tidak Tahu'].index(rpk_dm_x_value),
                                    horizontal=True, key='rpk_dm_x')

            rpk_jtg_x_value = st.session_state.input_data.get('RPK Penyakit Jantung', None)
            if pd.isna(rpk_jtg_x_value):
                rpk_jtg_x = left.radio('Penyakit Jantung', ['Ya', 'Tidak', 'Tidak Tahu'], horizontal=True, index=None, key='rpk_jtg_x')
            else:
                rpk_jtg_x = left.radio('Penyakit Jantung', ['Ya', 'Tidak', 'Tidak Tahu'],
                                    index=['Ya', 'Tidak', 'Tidak Tahu'].index(rpk_jtg_x_value),
                                    horizontal=True, key='rpk_jtg_x')

            rpk_stroke_x_value = st.session_state.input_data.get('RPK Stroke', None)
            if pd.isna(rpk_stroke_x_value):
                rpk_stroke_x = right.radio('Penyakit Stroke', ['Ya', 'Tidak', 'Tidak Tahu'], horizontal=True, index=None, key='rpk_stroke_x')
            else:
                rpk_stroke_x = right.radio('Penyakit Stroke', ['Ya', 'Tidak', 'Tidak Tahu'],
                                        index=['Ya', 'Tidak', 'Tidak Tahu'].index(rpk_stroke_x_value),
                                        horizontal=True, key='rpk_stroke_x')

            rpk_ca_x_value = st.session_state.input_data.get('RPK Kanker', None)
            if pd.isna(rpk_ca_x_value):
                rpk_ca_x = right.radio('Penyakit Kanker', ['Ya', 'Tidak', 'Tidak Tahu'], horizontal=True, index=None, key='rpk_ca_x')
            else:
                rpk_ca_x = right.radio('Penyakit Kanker', ['Ya', 'Tidak', 'Tidak Tahu'],
                                    index=['Ya', 'Tidak', 'Tidak Tahu'].index(rpk_ca_x_value),
                                    horizontal=True, key='rpk_ca_x')

            rpk_talasemia_x_value = st.session_state.input_data.get('RPK Talasemia', None)
            if pd.isna(rpk_talasemia_x_value):
                rpk_talasemia_x = right.radio('Thalasemia atau Transfusi Darah Rutin', ['Ya', 'Tidak', 'Tidak Tahu'], horizontal=True, index=None, key='rpk_talasemia_x')
            else:
                rpk_talasemia_x = right.radio('Thalasemia atau Transfusi Darah Rutin', ['Ya', 'Tidak', 'Tidak Tahu'],
                                            index=['Ya', 'Tidak', 'Tidak Tahu'].index(rpk_talasemia_x_value),
                                            horizontal=True, key='rpk_talasemia_x')
        
        with st.expander('**Riwayat Kebiasaan**'):  
            rk_rokok_x_value = st.session_state.input_data.get('RK Merokok', None)    
            if pd.isna(rk_rokok_x_value):
                rk_rokok_x = st.radio('Kebiasaan Merokok', ['Ya', 'Tidak'], 
                                    index=None, horizontal=True, key='rk_rokok_x')
            else:
                rk_rokok_x = st.radio('Kebiasaan Merokok', ['Ya', 'Tidak'], 
                                    index=['Ya', 'Tidak'].index(rk_rokok_x_value), 
                                    horizontal=True, key='rk_rokok_x')

            if rk_rokok_x == 'Ya':
                rk_rokokperhari_x = st.number_input('Rata-rata Jumlah Rokok/hari', value=float(st.session_state.input_data.get('RK Rokok PerHari', 0)), key='rokokperhari_x', disabled=False)
                rk_lamamerokok_x = st.number_input('Lama Merokok dalam Tahun', value=float(st.session_state.input_data.get('RK Lama Merokok', 0)), key='lamarokok_x', disabled=False)
                packyear = rk_rokokperhari_x*rk_lamamerokok_x/20
                rk_packyear_x = st.number_input('Pack Years', value=packyear, key='packyear_x', disabled=True)
            else:
                rk_rokokperhari_x = st.number_input('Rata-rata Jumlah Rokok/hari', value=0, key='rokokperhari_x', disabled=True)
                rk_lamamerokok_x = st.number_input('Lama Merokok dalam Tahun', value=0, key='lamarokok_x', disabled=True)
                rk_packyear_x = st.number_input('Pack Years', value=0, key='packyear_x', disabled=True)

            if st.session_state.packyear_x is not None:
                if 0 < st.session_state.packyear_x < 20:
                    st.session_state.ppok3_x = '<20 packs/years'
                elif 20 <= st.session_state.packyear_x <= 30:
                    st.session_state.ppok3_x = '20-30 packs/years'
                elif st.session_state.packyear_x >30:
                    st.session_state.ppok3_x = '>30 packs/years'
                else:
                    st.session_state.ppok3_x = None
            
            
            rk_manis_x_value = st.session_state.input_data.get('RK Makan Manis', None)    
            if pd.isna(rk_manis_x_value):
                rk_manis_x = st.radio('Apakah anda menambahkan gula pada makanan/minuman >4 sendok makan/hari?', 
                                    ['Ya, Setiap Hari', 'Ya, Tidak Setiap Hari', 'Tidak'], 
                                    index=None, horizontal=True, key='rk_manis_x')
            else:
                rk_manis_x = st.radio('Apakah anda menambahkan gula pada makanan/minuman >4 sendok makan/hari?', 
                                    ['Ya, Setiap Hari', 'Ya, Tidak Setiap Hari', 'Tidak'], 
                                    index=['Ya, Setiap Hari', 'Ya, Tidak Setiap Hari', 'Tidak'].index(rk_manis_x_value),
                                    horizontal=True, key='rk_manis_x')

            rk_asin_x_value = st.session_state.input_data.get('RK Makan Asin', None)    
            if pd.isna(rk_asin_x_value):
                rk_asin_x = st.radio('Apakah anda menggunakan garam pada makanan >1 sendok teh/hari?', 
                                    ['Ya, Setiap Hari', 'Ya, Tidak Setiap Hari', 'Tidak'], 
                                    index=None, horizontal=True, key='rk_asin_x')
            else:
                rk_asin_x = st.radio('Apakah anda menggunakan garam pada makanan >1 sendok teh/hari?', 
                                    ['Ya, Setiap Hari', 'Ya, Tidak Setiap Hari', 'Tidak'], 
                                    index=['Ya, Setiap Hari', 'Ya, Tidak Setiap Hari', 'Tidak'].index(rk_asin_x_value),
                                    horizontal=True, key='rk_asin_x')

            rk_lemak_x_value = st.session_state.input_data.get('RK Makan Berlemak', None)    
            if pd.isna(rk_lemak_x_value):
                rk_lemak_x = st.radio('Apakah anda mengonsumsi makanan yang diolah dengan minyak >5 sendok makan/hari?', 
                                    ['Ya, Setiap Hari', 'Ya, Tidak Setiap Hari', 'Tidak'], 
                                    index=None, horizontal=True, key='rk_lemak_x')
            else:
                rk_lemak_x = st.radio('Apakah anda mengonsumsi makanan yang diolah dengan minyak >5 sendok makan/hari?', 
                                    ['Ya, Setiap Hari', 'Ya, Tidak Setiap Hari', 'Tidak'], 
                                    index=['Ya, Setiap Hari', 'Ya, Tidak Setiap Hari', 'Tidak'].index(rk_lemak_x_value),
                                    horizontal=True, key='rk_lemak_x')

            rk_sayur_x_value = st.session_state.input_data.get('RK Makan Sayur', None)    
            if pd.isna(rk_sayur_x_value):
                rk_sayur_x = st.radio('Apakah anda mengonsumsi sayur/buah?', 
                                    ['Ya, Setiap Hari', 'Ya, Tidak Setiap Hari', 'Tidak'], 
                                    index=None, horizontal=True, key='rk_sayur_x')
            else:
                rk_sayur_x = st.radio('Apakah anda mengonsumsi sayur/buah?', 
                                    ['Ya, Setiap Hari', 'Ya, Tidak Setiap Hari', 'Tidak'], 
                                    index=['Ya, Setiap Hari', 'Ya, Tidak Setiap Hari', 'Tidak'].index(rk_sayur_x_value),
                                    horizontal=True, key='rk_sayur_x')

            rk_olahraga_x_value = st.session_state.input_data.get('RK Olahraga', None)    
            if pd.isna(rk_olahraga_x_value):
                rk_olahraga_x = st.radio('Apakah anda berolahraga?', 
                                        ['Ya, >30 menit/hari(>150 menit/minggu)', 'Ya, <30 menit/hari(<150 menit/minggu)', 'Tidak'], 
                                        index=None, horizontal=False, key='rk_olahraga_x')
            else:
                rk_olahraga_x = st.radio('Apakah anda berolahraga?', 
                                        ['Ya, >30 menit/hari(>150 menit/minggu)', 'Ya, <30 menit/hari(<150 menit/minggu)', 'Tidak'], 
                                        index=['Ya, >30 menit/hari(>150 menit/minggu)', 'Ya, <30 menit/hari(<150 menit/minggu)', 'Tidak'].index(rk_olahraga_x_value),
                                        horizontal=False, key='rk_olahraga_x')

            rk_alkohol_x_value = st.session_state.input_data.get('RK Konsumsi Alkohol', None)    
            if pd.isna(rk_alkohol_x_value):
                rk_alkohol_x = st.radio('Apakah anda mengonsumsi alkohol 1 bulan terakhir?', 
                                        ['Ya, Setiap Hari', 'Ya, Tidak Setiap Hari', 'Tidak'], 
                                        index=None, horizontal=True, key='rk_alkohol_x')
            else:
                rk_alkohol_x = st.radio('Apakah anda mengonsumsi alkohol 1 bulan terakhir?', 
                                        ['Ya, Setiap Hari', 'Ya, Tidak Setiap Hari', 'Tidak'], 
                                        index=['Ya, Setiap Hari', 'Ya, Tidak Setiap Hari', 'Tidak'].index(rk_alkohol_x_value),
                                        horizontal=True, key='rk_alkohol_x')
                
        with st.expander('**Pemeriksaan Dasar**'):
            left, right = st.columns(2, vertical_alignment="top")
            tds_x_value = st.session_state.input_data.get('TD Sistole', '')
            if pd.isna(tds_x_value):
                tds_x = left.text_input('Tekanan Darah Sistole', value=None, key='tds_x')
            else:
                tds_x = left.text_input('Tekanan Darah Sistole', value=tds_x_value, key='tds_x')

            tdd_x_value = st.session_state.input_data.get('TD Diastole', '')
            if pd.isna(tdd_x_value):
                tdd_x = left.text_input('Tekanan Darah Diastole', value=None, key='tdd_x')
            else:
                tdd_x = left.text_input('Tekanan Darah Diastole', value=tdd_x_value, key='tdd_x')

            hr_x_value = st.session_state.input_data.get('Heart Rate', '')
            if pd.isna(hr_x_value):
                hr_x = left.text_input('Frekuensi Nadi', value=None, key='hr_x')
            else:
                hr_x = left.text_input('Frekuensi Nadi', value=hr_x_value, key='hr_x')

            rr_x_value = st.session_state.input_data.get('Respiration Rate', '')
            if pd.isna(rr_x_value):
                rr_x = left.text_input('Frekuensi Napas', value=None, key='rr_x')
            else:
                rr_x = left.text_input('Frekuensi Napas', value=rr_x_value, key='rr_x')

            temp_x_value = st.session_state.input_data.get('Suhu Badan', '')
            if pd.isna(temp_x_value):
                temp_x = left.text_input('Suhu Badan', value=None, key='temp_x')
            else:
                temp_x = left.text_input('Suhu Badan', value=temp_x_value, key='temp_x')

            # Right column inputs
            bb_x_value = st.session_state.input_data.get('Berat Badan', '')
            if pd.isna(bb_x_value):
                bb_x = right.text_input('Berat Badan(kg)', value=None, key='bb_x')
            else:
                bb_x = right.text_input('Berat Badan(kg)', value=bb_x_value, key='bb_x')

            tb_x_value = st.session_state.input_data.get('Tinggi Badan', '')
            if pd.isna(tb_x_value):
                tb_x = right.text_input('Tinggi Badan(cm)', value=None, key='tb_x')
            else:
                tb_x = right.text_input('Tinggi Badan(cm)', value=tb_x_value, key='tb_x')
                
            def hitung_bmi(tb_x,bb_x):
                a= float(tb_x)**2/10000
                b= float(bb_x)
                imt= b/a
                return imt
            if tb_x:
                imt = hitung_bmi(tb_x, bb_x)
                bmi_x=right.number_input('Indeks Massa Tubuh', value=imt, disabled=True, key='bmi_x')
            else:
                bmi_x=right.number_input('Indeks Massa Tubuh', value=0, disabled=True, key='bmi_x')
                
            if st.session_state.bmi_x is not None:
                if 13.79 <= st.session_state.bmi_x <= 25.99:
                    st.session_state.jcs4_x = '13.79-25.99'
                elif 26 <= st.session_state.bmi_x <= 29.9:
                    st.session_state.jcs4_x = '26-29.99'
                elif 30 <= st.session_state.bmi_x <= 35.58:
                    st.session_state.jcs4_x = '30-35.58'
                else:
                    st.session_state.jcs4_x = None

            lp_x_value = st.session_state.input_data.get('Lingkar Perut', '')
            if pd.isna(lp_x_value):
                lp_x = right.text_input('Lingkar Perut(cm)', value=None, key='lp_x')
            else:
                lp_x = right.text_input('Lingkar Perut(cm)', value=lp_x_value, key='lp_x')

            lla_x_value = st.session_state.input_data.get('Lingkar Lengan Atas', '')
            if pd.isna(lla_x_value):
                lla_x = right.text_input('Lingkar Lengan Atas(Untuk Wanita dan Lansia)', value=None, key='lla_x')
            else:
                lla_x = right.text_input('Lingkar Lengan Atas(Untuk Wanita dan Lansia)', value=lla_x_value, key='lla_x')
    
        with st.expander('**Skrining Kesehatan Jiwa**'):
            st.markdown('**Pilihlah salah satu jawaban untuk setiap pertanyaan yang sesuai dengan perasaan anda dalam 2 minggu terakhir!**')
            left, right = st.columns(2, vertical_alignment="top")
            with left:
                phq1_value = st.session_state.input_data.get('PHQ1', None)
                if pd.isna(phq1_value):
                    phq1_x = st.radio('Dalam 2 minggu terakhir, seberapa sering anda kurang/tidak bersemangat dalam melakukan kegiatan sehari-hari?', ['Tidak sama sekali', 'Kurang dari 1 minggu', 'Lebih dari 1 minggu', 'Hampir setiap hari'], horizontal=True, index=None, key='phq1_x')
                else:
                    phq1_x = st.radio('Dalam 2 minggu terakhir, seberapa sering anda kurang/tidak bersemangat dalam melakukan kegiatan sehari-hari?', ['Tidak sama sekali', 'Kurang dari 1 minggu', 'Lebih dari 1 minggu', 'Hampir setiap hari'],
                                        index=['Tidak sama sekali', 'Kurang dari 1 minggu', 'Lebih dari 1 minggu', 'Hampir setiap hari'].index(phq1_value),
                                        horizontal=True, key='phq1_x')
            with right:
                gad1_value = st.session_state.input_data.get('GAD1', None)
                if pd.isna(gad1_value):
                    gad1_x = st.radio('Dalam 2 minggu terakhir, seberapa sering anda merasa gugup, cemas, atau gelisah?', ['Tidak sama sekali', 'Kurang dari 1 minggu', 'Lebih dari 1 minggu', 'Hampir setiap hari'], horizontal=True, index=None, key='gad1_x')
                else:
                    gad1_x = st.radio('Dalam 2 minggu terakhir, seberapa sering anda merasa gugup, cemas, atau gelisah?', ['Tidak sama sekali', 'Kurang dari 1 minggu', 'Lebih dari 1 minggu', 'Hampir setiap hari'],
                                        index=['Tidak sama sekali', 'Kurang dari 1 minggu', 'Lebih dari 1 minggu', 'Hampir setiap hari'].index(gad1_value),
                                        horizontal=True, key='gad1_x')
                    
            left, right = st.columns(2, vertical_alignment="top")
            with left:   
                phq2_value = st.session_state.input_data.get('PHQ2', None)
                if pd.isna(phq2_value):
                    phq2_x = st.radio('Dalam 2 minggu terakhir, seberapa sering anda merasa murung, tertekan, atau putus asa?', ['Tidak sama sekali', 'Kurang dari 1 minggu', 'Lebih dari 1 minggu', 'Hampir setiap hari'], horizontal=True, index=None, key='phq2_x')
                else:
                    phq2_x = st.radio('Dalam 2 minggu terakhir, seberapa sering anda merasa murung, tertekan, atau putus asa?', ['Tidak sama sekali', 'Kurang dari 1 minggu', 'Lebih dari 1 minggu', 'Hampir setiap hari'],
                                        index=['Tidak sama sekali', 'Kurang dari 1 minggu', 'Lebih dari 1 minggu', 'Hampir setiap hari'].index(phq2_value),
                                        horizontal=True, key='phq2_x')
            
            with right:
                gad2_value = st.session_state.input_data.get('GAD2', None)
                if pd.isna(gad2_value):
                    gad2_x = st.radio('Dalam 2 minggu terakhir, seberapa sering anda tidak mampu mengendalikan rasa khawatir?', ['Tidak sama sekali', 'Kurang dari 1 minggu', 'Lebih dari 1 minggu', 'Hampir setiap hari'], horizontal=True, index=None, key='gad2_x')
                else:
                    gad2_x = st.radio('Dalam 2 minggu terakhir, seberapa sering anda tidak mampu mengendalikan rasa khawatir?', ['Tidak sama sekali', 'Kurang dari 1 minggu', 'Lebih dari 1 minggu', 'Hampir setiap hari'],
                                        index=['Tidak sama sekali', 'Kurang dari 1 minggu', 'Lebih dari 1 minggu', 'Hampir setiap hari'].index(gad2_value),
                                        horizontal=True, key='gad2_x')
            
            
            
            def calculate_score1(phq1_x, phq2_x):
                score = 0

                if phq1_x == 'Tidak sama sekali':
                    score += 0
                elif phq1_x == 'Kurang dari 1 minggu':
                    score += 1
                elif phq1_x == 'Lebih dari 1 minggu':
                    score += 2
                elif phq1_x == 'Hampir setiap hari':
                    score += 3
                    
                if phq2_x == 'Tidak sama sekali':
                    score += 0
                elif phq2_x == 'Kurang dari 1 minggu':
                    score += 1
                elif phq2_x == 'Lebih dari 1 minggu':
                    score += 2
                elif phq2_x == 'Hampir setiap hari':
                    score += 3
                
                return score
            
            # Hitung total skor
            total_score1 = calculate_score1(phq1_x, phq2_x)

            # Penjelasan untuk hasil skor
            if total_score1 < 3:
                depresi_x = st.text_input('Subskor Depresi', value='Tidak ada gejala signifikan', disabled=True, key='depresi_x')
            elif total_score1 >= 3:
                depresi_x = st.text_input('Subskor Depresi', value='Kemungkinan gejala depresi', disabled=True, key='depresi_x')
            
            
            def calculate_score2(gad1_x, gad2_x):
                score = 0

                if gad1_x == 'Tidak sama sekali':
                    score += 0
                elif gad1_x == 'Kurang dari 1 minggu':
                    score += 1
                elif gad1_x == 'Lebih dari 1 minggu':
                    score += 2
                elif gad1_x == 'Hampir setiap hari':
                    score += 3
                    
                if gad2_x == 'Tidak sama sekali':
                    score += 0
                elif gad2_x == 'Kurang dari 1 minggu':
                    score += 1
                elif gad2_x == 'Lebih dari 1 minggu':
                    score += 2
                elif gad2_x == 'Hampir setiap hari':
                    score += 3
                
                return score
            
            # Hitung total skor
            total_score2 = calculate_score2(gad1_x, gad2_x)

            # Penjelasan untuk hasil skor
            if total_score2 < 3:
                cemas_x = st.text_input('Subskor Kecemasan', value='Tidak ada gejala signifikan', disabled=True, key='cemas_x')
            elif total_score2 >= 3:
                cemas_x = st.text_input('Subskor Kecemasan', value='Kemungkinan gejala kecemasan', disabled=True, key='cemas_x')
            
        with st.expander('**Skrining Indera Pendengaran**'):
            left, right = st.columns(2, vertical_alignment="top")
        
            bisikad_x_value = st.session_state.input_data.get('Tes Bisik AD', '')
            if pd.isna(bisikad_x_value):
                bisikad_x = left.text_input('Tes Bisik AD', value=None, key='bisikad_x')
            else:
                bisikad_x = left.text_input('Tes Bisik AD', value=bisikad_x_value, key='bisikad_x')

            bisikas_x_value = st.session_state.input_data.get('Tes Bisik AS', '')
            if pd.isna(bisikas_x_value):
                bisikas_x = right.text_input('Tes Bisik AS', value=None, key='bisikas_x')
            else:
                bisikas_x = right.text_input('Tes Bisik AS', value=bisikas_x_value, key='bisikas_x')

            otoskopiad_x_value = st.session_state.input_data.get('Otoskopi AD', '')
            if pd.isna(otoskopiad_x_value):
                otoskopiad_x = left.text_input('Otoskopi AD', value=None, key='otoskopiad_x')
            else:
                otoskopiad_x = left.text_input('Otoskopi AD', value=otoskopiad_x_value, key='otoskopiad_x')

            otoskopias_x_value = st.session_state.input_data.get('Otoskopi AS', '')
            if pd.isna(otoskopias_x_value):
                otoskopias_x = right.text_input('Otoskopi AS', value=None, key='otoskopias_x')
            else:
                otoskopias_x = right.text_input('Otoskopi AS', value=otoskopias_x_value, key='otoskopias_x')

            rinne_x_value = st.session_state.input_data.get('Rinne', '')
            if pd.isna(rinne_x_value):
                rinne_x = left.text_input('Rinne Test', value=None, key='rinne_x')
            else:
                rinne_x = left.text_input('Rinne Test', value=rinne_x_value, key='rinne_x')

            weber_x_value = st.session_state.input_data.get('Weber', '')
            if pd.isna(weber_x_value):
                weber_x = left.text_input('Weber Test', value=None, key='weber_x')
            else:
                weber_x = left.text_input('Weber Test', value=weber_x_value, key='weber_x')

            schwabach_x_value = st.session_state.input_data.get('Schwabach', '')
            if pd.isna(schwabach_x_value):
                schwabach_x = right.text_input('Schwabach Test', value=None, key='schwabach_x')
            else:
                schwabach_x = right.text_input('Schwabach Test', value=schwabach_x_value, key='schwabach_x')

        with st.expander('**Skrining Kanker Paru**'):
            # Get session state for each field if available, or use the radio buttons
            caparu1_value = st.session_state.input_data.get('Ca Paru 1', None)    
            if pd.isna(caparu1_value):
                caparu1_x = st.radio('Jenis Kelamin', ['Laki-laki', 'Perempuan'], index=None, horizontal=True, key='caparu1_x')
            else:
                caparu1_x = st.radio('Jenis Kelamin', ['Laki-laki', 'Perempuan'],
                                    index=['Laki-laki', 'Perempuan'].index(caparu1_value),
                                    horizontal=True, key='caparu1_x')

            caparu2_value = st.session_state.input_data.get('Ca Paru 2', None)    
            if pd.isna(caparu2_value):
                caparu2_x = st.radio('Kelompok Usia', ['>65 tahun', '46-65 tahun', '</=45 tahun'], index=None, horizontal=True, key='caparu2_x')
            else:
                caparu2_x = st.radio('Kelompok Usia', ['>65 tahun', '46-65 tahun', '</=45 tahun'],
                                    index=['>65 tahun', '46-65 tahun', '</=45 tahun'].index(caparu2_value),
                                    horizontal=True, key='caparu2_x')

            caparu3_value = st.session_state.input_data.get('Ca Paru 3', None)    
            if pd.isna(caparu3_value):
                caparu3_x = st.radio('Pernah menderita/didiagnosis kanker?', ['Ya, Pernah tahun lalu', 'Ya, Pernah <5 tahun yang lalu', 'Tidak Pernah'], index=None, horizontal=True, key='caparu3_x')
            else:
                caparu3_x = st.radio('Pernah menderita/didiagnosis kanker?', ['Ya, Pernah tahun lalu', 'Ya, Pernah <5 tahun yang lalu', 'Tidak Pernah'],
                                    index=['Ya, Pernah tahun lalu', 'Ya, Pernah <5 tahun yang lalu', 'Tidak Pernah'].index(caparu3_value),
                                    horizontal=True, key='caparu3_x')

            caparu4_value = st.session_state.input_data.get('Ca Paru 4', None)    
            if pd.isna(caparu4_value):
                caparu4_x = st.radio('Apakah ada keluarga (ayah/ibu/saudara kandung) didiagnosis atau menderita kanker sebelumnya?', ['Ya, ada kanker paru', 'Ya, ada kanker jenis lain', 'Tidak'], index=None, horizontal=True, key='caparu4_x')
            else:
                caparu4_x = st.radio('Apakah ada keluarga (ayah/ibu/saudara kandung) didiagnosis atau menderita kanker sebelumnya?', ['Ya, ada kanker paru', 'Ya, ada kanker jenis lain', 'Tidak'],
                                    index=['Ya, ada kanker paru', 'Ya, ada kanker jenis lain', 'Tidak'].index(caparu4_value),
                                    horizontal=True, key='caparu4_x')

            caparu5_value = st.session_state.input_data.get('Ca Paru 5', None)    
            if pd.isna(caparu5_value):
                caparu5_x = st.radio('Riwayat merokok/paparan asap rokok', ['Perokok aktif (dalam 1 tahun ini masih merokok)', 'Bekas perokok, berhenti <15 tahun yang lalu', 'Perokok pasif (paparan dari lingkungan rumah/tempat kerja)', 'Tidak merokok'], index=None, horizontal=False, key='caparu5_x')
            else:
                caparu5_x = st.radio('Riwayat merokok/paparan asap rokok', ['Perokok aktif (dalam 1 tahun ini masih merokok)', 'Bekas perokok, berhenti <15 tahun yang lalu', 'Perokok pasif (paparan dari lingkungan rumah/tempat kerja)', 'Tidak merokok'],
                                    index=['Perokok aktif (dalam 1 tahun ini masih merokok)', 'Bekas perokok, berhenti <15 tahun yang lalu', 'Perokok pasif (paparan dari lingkungan rumah/tempat kerja)', 'Tidak merokok'].index(caparu5_value),
                                    horizontal=False, key='caparu5_x')

            caparu6_value = st.session_state.input_data.get('Ca Paru 6', None)    
            if pd.isna(caparu6_value):
                caparu6_x = st.radio('Riwayat tempat kerja mengandung zat karsinogenik', ['Ya', 'Tidak Yakin/Ragu-ragu', 'Tidak'], index=None, horizontal=True, key='caparu6_x')
            else:
                caparu6_x = st.radio('Riwayat tempat kerja mengandung zat karsinogenik', ['Ya', 'Tidak Yakin/Ragu-ragu', 'Tidak'],
                                    index=['Ya', 'Tidak Yakin/Ragu-ragu', 'Tidak'].index(caparu6_value),
                                    horizontal=True, key='caparu6_x')

            caparu7_value = st.session_state.input_data.get('Ca Paru 7', None)    
            if pd.isna(caparu7_value):
                caparu7_x = st.radio('Lingkungan tempat tinggal berpotensi tinggi', ['Ya', 'Tidak Yakin/Ragu-ragu', 'Tidak'], index=None, horizontal=True, key='caparu7_x')
            else:
                caparu7_x = st.radio('Lingkungan tempat tinggal berpotensi tinggi', ['Ya', 'Tidak Yakin/Ragu-ragu', 'Tidak'],
                                    index=['Ya', 'Tidak Yakin/Ragu-ragu', 'Tidak'].index(caparu7_value),
                                    horizontal=True, key='caparu7_x')

            caparu8_value = st.session_state.input_data.get('Ca Paru 8', None)    
            if pd.isna(caparu8_value):
                caparu8_x = st.radio('Lingkungan dalam rumah yang berisiko', ['Ya', 'Tidak Yakin/Ragu-ragu', 'Tidak'], index=None, horizontal=True, key='caparu8_x')
            else:
                caparu8_x = st.radio('Lingkungan dalam rumah yang berisiko', ['Ya', 'Tidak Yakin/Ragu-ragu', 'Tidak'],
                                    index=['Ya', 'Tidak Yakin/Ragu-ragu', 'Tidak'].index(caparu8_value),
                                    horizontal=True, key='caparu8_x')

            caparu9_value = st.session_state.input_data.get('Ca Paru 9', None)    
            if pd.isna(caparu9_value):
                caparu9_x = st.radio('Pernah didiagnosis/diobati penyakit paru kronik', ['Ya, Pernah. TB', 'Ya, Pernah. Penyakit Paru kronik Lain (PPOK)', 'Tidak Pernah'], index=None, horizontal=True, key='caparu9_x')
            else:
                caparu9_x = st.radio('Pernah didiagnosis/diobati penyakit paru kronik', ['Ya, Pernah. TB', 'Ya, Pernah. Penyakit Paru kronik Lain (PPOK)', 'Tidak Pernah'],
                                    index=['Ya, Pernah. TB', 'Ya, Pernah. Penyakit Paru kronik Lain (PPOK)', 'Tidak Pernah'].index(caparu9_value),
                                    horizontal=True, key='caparu9_x')

            # Fungsi untuk menghitung skor
            def calculate_score(caparu1_x, caparu2_x, caparu3_x, caparu4_x, caparu5_x, caparu6_x, caparu7_x, caparu8_x, caparu9_x):
                score = 0

                if caparu1_x == 'Laki-laki':
                    score += 3
                elif caparu1_x == 'Perempuan':
                    score += 1
                
                if caparu2_x == '65 tahun':
                    score += 3
                elif caparu2_x == '46-65 tahun':
                    score += 2
                elif caparu2_x == '</=45 tahun':
                    score += 1
                
                if caparu3_x == 'Ya, Pernah tahun lalu':
                    score += 3
                elif caparu3_x == 'Ya, Pernah <5 tahun yang lalu':
                    score += 2
                elif caparu3_x == 'Tidak Pernah':
                    score += 1
                    
                if caparu4_x == 'Ya, ada kanker paru':
                    score += 3
                elif caparu4_x == 'Ya, ada kanker jenis lain':
                    score += 2
                elif caparu4_x == 'Tidak':
                    score += 1
                    
                if caparu5_x == 'Perokok aktif (dalam 1 tahun ini masih merokok)':
                    score += 4
                elif caparu5_x == 'Bekas perokok, berhenti <15 tahun yang lalu':
                    score += 3
                elif caparu5_x == 'Perokok pasif (paparan dari lingkungan rumah/tempat kerja)':
                    score += 2
                elif caparu5_x == 'Tidak merokok':
                    score += 1

                if caparu6_x == 'Ya':
                    score += 3
                elif caparu6_x == 'Tidak Yakin/Ragu-ragu':
                    score += 2
                elif caparu6_x == 'Tidak':
                    score += 1
                
                if caparu7_x == 'Ya':
                    score += 3
                elif caparu7_x == 'Tidak Yakin/Ragu-ragu':
                    score += 2
                elif caparu7_x == 'Tidak':
                    score += 1
                    
                if caparu8_x == 'Ya':
                    score += 3
                elif caparu8_x == 'Tidak Yakin/Ragu-ragu':
                    score += 2
                elif caparu8_x == 'Tidak':
                    score += 1
                
                if caparu9_x == 'Ya, Pernah. TB':
                    score += 3
                elif caparu9_x == 'Ya, Pernah. Penyakit Paru kronik Lain (PPOK)':
                    score += 2
                elif caparu9_x == 'Tidak Pernah':
                    score += 0
                
                return score

            # Hitung total skor
            total_score = calculate_score(caparu1_x, caparu2_x, caparu3_x, caparu4_x, caparu5_x, caparu6_x, caparu7_x, caparu8_x, caparu9_x)

            # Tampilkan total skor
            caparu_tot_x=float(st.text_input('Jumlah Skor', value=total_score, disabled=True, key='caparu_tot_x'))

            # Penjelasan untuk hasil skor
            if total_score <= 11:
                st.success("Risiko Ringan Kanker Paru.")
            elif 12<=total_score <= 16:
                st.warning("Risiko Sedang Kanker Paru.")
            elif 17<=total_score <= 29:
                st.warning("Risiko Berat Kanker Paru.")

        with st.expander('**Skrining PPOK(PUMA)**'):
            # Format each radio button to check the session state first
            ppok1_x_value = st.session_state.input_data.get('PPOK 1', None)
            if pd.isna(ppok1_x_value):
                ppok1_x = st.radio('Jenis Kelamin', ['Perempuan', 'Laki-laki'], index=None, horizontal=True, key='ppok1_x')
            else:
                ppok1_x = st.radio('Jenis Kelamin', ['Perempuan', 'Laki-laki'],
                                    index=['Perempuan', 'Laki-laki'].index(ppok1_x_value),
                                    horizontal=True, key='ppok1_x')

            ppok2_x_value = st.session_state.input_data.get('PPOK 2', None)
            if pd.isna(ppok2_x_value):
                ppok2_x = st.radio('Kelompok Usia', ['40-49 tahun', '50-59 tahun', '>/=60 tahun'], index=None, horizontal=True, key='ppok2_x')
            else:
                ppok2_x = st.radio('Kelompok Usia', ['40-49 tahun', '50-59 tahun', '>/=60 tahun'],
                                    index=['40-49 tahun', '50-59 tahun', '>/=60 tahun'].index(ppok2_x_value),
                                    horizontal=True, key='ppok2_x')

            ppok3_x_value = st.session_state.input_data.get('PPOK 3', None)
            if pd.isna(ppok3_x_value):
                ppok3_x = st.radio('Kebiasaan merokok', ['Tidak', '<20 packs/years', '20-30 packs/years', '>30 packs/years'], index=None, horizontal=False, key='ppok3_x')
            else:
                ppok3_x = st.radio('Kebiasaan merokok', ['Tidak', '<20 packs/years', '20-30 packs/years', '>30 packs/years'],
                                    index=['Tidak', '<20 packs/years', '20-30 packs/years', '>30 packs/years'].index(ppok3_x_value),
                                    horizontal=False, key='ppok3_x')

            ppok4_x_value = st.session_state.input_data.get('PPOK 4', None)
            if pd.isna(ppok4_x_value):
                ppok4_x = st.radio('Apakah anda pernah merasa napas pendek ketika anda berjalan lebih cepat pada jalan yang datar atau pada jalan yang sedikit menanjak?', ['Tidak', 'Ya'], index=None, horizontal=True, key='ppok4_x')
            else:
                ppok4_x = st.radio('Apakah anda pernah merasa napas pendek ketika anda berjalan lebih cepat pada jalan yang datar atau pada jalan yang sedikit menanjak?', ['Tidak', 'Ya'],
                                    index=['Tidak', 'Ya'].index(ppok4_x_value),
                                    horizontal=True, key='ppok4_x')

            ppok5_x_value = st.session_state.input_data.get('PPOK 5', None)
            if pd.isna(ppok5_x_value):
                ppok5_x = st.radio('Apakah anda biasanya mempunyai dahak yang berasal dari paru atau kesulitan mengeluarkan dahak saat anda tidak sedang menderita salesma/flu?', ['Tidak', 'Ya'], index=None, horizontal=True, key='ppok5_x')
            else:
                ppok5_x = st.radio('Apakah anda biasanya mempunyai dahak yang berasal dari paru atau kesulitan mengeluarkan dahak saat anda tidak sedang menderita salesma/flu?', ['Tidak', 'Ya'],
                                    index=['Tidak', 'Ya'].index(ppok5_x_value),
                                    horizontal=True, key='ppok5_x')

            ppok6_x_value = st.session_state.input_data.get('PPOK 6', None)
            if pd.isna(ppok6_x_value):
                ppok6_x = st.radio('Apakah anda biasanya batuk saat anda tidak sedang menderita salesma/flu?', ['Tidak', 'Ya'], index=None, horizontal=True, key='ppok6_x')
            else:
                ppok6_x = st.radio('Apakah anda biasanya batuk saat anda tidak sedang menderita salesma/flu?', ['Tidak', 'Ya'],
                                    index=['Tidak', 'Ya'].index(ppok6_x_value),
                                    horizontal=True, key='ppok6_x')

            ppok7_x_value = st.session_state.input_data.get('PPOK 7', None)
            if pd.isna(ppok7_x_value):
                ppok7_x = st.radio('Apakah dokter atau tenaga medis lainnya pernah meminta anda untuk melakukan pemeriksaan spirometri?', ['Tidak', 'Ya'], index=None, horizontal=True, key='ppok7_x')
            else:
                ppok7_x = st.radio('Apakah dokter atau tenaga medis lainnya pernah meminta anda untuk melakukan pemeriksaan spirometri?', ['Tidak', 'Ya'],
                                    index=['Tidak', 'Ya'].index(ppok7_x_value),
                                    horizontal=True, key='ppok7_x')

            # Fungsi untuk menghitung skor
            def calculate_score(ppok1_x, ppok2_x, ppok3_x, ppok4_x, ppok5_x, ppok6_x, ppok7_x):
                score = 0

                if ppok1_x == 'Laki-laki':
                    score += 1

                if ppok2_x == '40-49 tahun':
                    score += 0
                elif ppok2_x == '50-59 tahun':
                    score += 1
                elif ppok2_x == '>/=60 tahun':
                    score += 2  
                
                if ppok3_x == 'Tidak':
                    score += 0
                elif ppok3_x == '<20 packs/years':
                    score += 0
                elif ppok3_x == '20-30 packs/years':
                    score += 1
                elif ppok3_x == '>30 packs/years':
                    score += 2
                
                if ppok4_x == 'Tidak':
                    score += 0
                elif ppok4_x == 'Ya':
                    score += 1
                
                if ppok5_x == 'Tidak':
                    score += 0
                elif ppok5_x == 'Ya':
                    score += 1
                    
                if ppok6_x == 'Tidak':
                    score += 0
                elif ppok6_x == 'Ya':
                    score += 1
                    
                if ppok7_x == 'Tidak':
                    score += 0
                elif ppok7_x == 'Ya':
                    score += 1

                return score

            # Hitung total skor
            total_score = calculate_score(ppok1_x, ppok2_x, ppok3_x, ppok4_x, ppok5_x, ppok6_x, ppok7_x)

            # Tampilkan total skor
            ppok_tot_x=float(st.text_input('Jumlah Skor', value=total_score, disabled=True, key='ppok_tot_x'))

            # Penjelasan untuk hasil skor
            if total_score < 6:
                st.success("Risiko Rendah PPOK.")
            elif total_score >= 6:
                st.warning("Risiko Tinggi PPOK.")
        
        with st.expander('**Skrining Gejala TB**'):
            left, right = st.columns(2, vertical_alignment='top')
            tb1_x_value = st.session_state.input_data.get('TB 1', None)
            if pd.isna(tb1_x_value):
                tb1_x = left.radio('Batuk >1 minggu?', ['Ya', 'Tidak'], index=None, horizontal=True, key='tb1_x')
            else:
                tb1_x = left.radio('Batuk >1 minggu?', ['Ya', 'Tidak'],
                                index=['Ya', 'Tidak'].index(tb1_x_value),
                                horizontal=True, key='tb1_x')

            tb2_x_value = st.session_state.input_data.get('TB 2', None)
            if pd.isna(tb2_x_value):
                tb2_x = left.radio('Demam yang tidak diketahui penyebabnya?', ['Ya', 'Tidak'], index=None, horizontal=True, key='tb2_x')
            else:
                tb2_x = left.radio('Demam yang tidak diketahui penyebabnya?', ['Ya', 'Tidak'],
                                index=['Ya', 'Tidak'].index(tb2_x_value),
                                horizontal=True, key='tb2_x')

            tb3_x_value = st.session_state.input_data.get('TB 3', None)
            if pd.isna(tb3_x_value):
                tb3_x = left.radio('Batuk disertai darah?', ['Ya', 'Tidak'], index=None, horizontal=True, key='tb3_x')
            else:
                tb3_x = left.radio('Batuk disertai darah?', ['Ya', 'Tidak'],
                                index=['Ya', 'Tidak'].index(tb3_x_value),
                                horizontal=True, key='tb3_x')

            tb4_x_value = st.session_state.input_data.get('TB 4', None)
            if pd.isna(tb4_x_value):
                tb4_x = left.radio('Keringat malam tanpa beraktivitas?', ['Ya', 'Tidak'], index=None, horizontal=True, key='tb4_x')
            else:
                tb4_x = left.radio('Keringat malam tanpa beraktivitas?', ['Ya', 'Tidak'],
                                index=['Ya', 'Tidak'].index(tb4_x_value),
                                horizontal=True, key='tb4_x')

            tb5_x_value = st.session_state.input_data.get('TB 5', None)
            if pd.isna(tb5_x_value):
                tb5_x = right.radio('Penurunan Berat Badan tanpa penyebab yang jelas?', ['Ya', 'Tidak'], index=None, horizontal=True, key='tb5_x')
            else:
                tb5_x = right.radio('Penurunan Berat Badan tanpa penyebab yang jelas?', ['Ya', 'Tidak'],
                                    index=['Ya', 'Tidak'].index(tb5_x_value),
                                    horizontal=True, key='tb5_x')

            tb6_x_value = st.session_state.input_data.get('TB 6', None)
            if pd.isna(tb6_x_value):
                tb6_x = right.radio('Pernah minum pengobatan TB sebelumnya?', ['Ya', 'Tidak'], index=None, horizontal=True, key='tb6_x')
            else:
                tb6_x = right.radio('Pernah minum pengobatan TB sebelumnya?', ['Ya', 'Tidak'],
                                    index=['Ya', 'Tidak'].index(tb6_x_value),
                                    horizontal=True, key='tb6_x')

            tb7_x_value = st.session_state.input_data.get('TB 7', None)
            if pd.isna(tb7_x_value):
                tb7_x = right.radio('Terdapat keluarga atau tetangga yang batuk lama/pengobatan TB?', ['Ya', 'Tidak'], index=None, horizontal=True, key='tb7_x')
            else:
                tb7_x = right.radio('Terdapat keluarga atau tetangga yang batuk lama/pengobatan TB?', ['Ya', 'Tidak'],
                                    index=['Ya', 'Tidak'].index(tb7_x_value),
                                    horizontal=True, key='tb7_x')

        with st.expander('**Skrining Kanker Kolorektal**'):
            caco1_x_value = st.session_state.input_data.get('Ca Kolorektal 1', None)
            if pd.isna(caco1_x_value):
                caco1_x = st.radio('Kelompok Usia?', ['<50 tahun', '50-69 tahun', '>/=70 tahun'], index= None, horizontal=True, key='caco1_x')
            else:
                caco1_x = st.radio('Kelompok Usia?', ['<50 tahun', '50-69 tahun', '>/=70 tahun'],
                                    index=['<50 tahun', '50-69 tahun', '>/=70 tahun'].index(caco1_x_value),
                                    horizontal=True, key='caco1_x')

            caco2_x_value = st.session_state.input_data.get('Ca Kolorektal 2', None)
            if pd.isna(caco2_x_value):
                caco2_x = st.radio('Jenis Kelamin?', ['Perempuan', 'Laki-laki'], index= None, horizontal=True, key='caco2_x')
            else:
                caco2_x = st.radio('Jenis Kelamin?', ['Perempuan', 'Laki-laki'],
                                    index=['Perempuan', 'Laki-laki'].index(caco2_x_value),
                                    horizontal=True, key='caco2_x')

            caco3_x_value = st.session_state.input_data.get('Ca Kolorektal 3', None)
            if pd.isna(caco3_x_value):
                caco3_x = st.radio('Riwayat keluarga kanker kolorektal generasi pertama (Ayah, ibu, kakak dan adik kandung)?', ['Ada', 'Tidak ada'], index= None, horizontal=True, key='caco3_x')
            else:
                caco3_x = st.radio('Riwayat keluarga kanker kolorektal generasi pertama (Ayah, ibu, kakak dan adik kandung)?', ['Ada', 'Tidak ada'],
                                    index=['Ada', 'Tidak ada'].index(caco3_x_value),
                                    horizontal=True, key='caco3_x')

            caco4_x_value = st.session_state.input_data.get('Ca Kolorektal 4', None)
            if pd.isna(caco4_x_value):
                caco4_x = st.radio('Riwayat Merokok?', ['Tidak Pernah', 'Saat ini merokok atau dulu pernah merokok'], index= None, horizontal=True, key='caco4_x')
            else:
                caco4_x = st.radio('Riwayat Merokok?', ['Tidak Pernah', 'Saat ini merokok atau dulu pernah merokok'],
                                    index=['Tidak Pernah', 'Saat ini merokok atau dulu pernah merokok'].index(caco4_x_value),
                                    horizontal=True, key='caco4_x')
            
            # Fungsi untuk menghitung skor
            def calculate_score(caco1_x, caco2_x, caco3_x, caco4_x):
                score = 0
                # Penentuan skor berdasarkan kelompok usia
                if caco1_x == '<50 tahun':
                    score += 0
                elif caco1_x == '50-69 tahun':
                    score += 2
                elif caco1_x == '>/=70 tahun':
                    score += 3

                if caco2_x == 'Laki-laki':
                    score += 1 

                if caco3_x == 'Ada':
                    score += 2 

                if caco4_x == 'Saat ini merokok atau dulu pernah merokok':
                    score += 1  

                return score
            
            # Hitung total skor
            total_score = calculate_score(caco1_x, caco2_x, caco3_x, caco4_x)

            # Tampilkan total skor
            caco_tot_x = float(st.text_input('Jumlah Skor', value=total_score, disabled=True, key='caco_tot_x'))

            # Penjelasan untuk hasil skor
            if total_score < 2:
                st.success("Risiko Rendah kanker kolorektal.")
            elif 2<= total_score <= 3:
                st.warning("Risiko Sedang kanker kolorektal.")
            else:
                st.warning("Risiko Tinggi kanker kolorektal.")

            caco5_x_value = st.session_state.input_data.get('Rectal Toucher', '')
            if pd.isna(caco5_x_value):
                caco5_x = st.text_input('Rectal Toucher', value=None, key='caco5_x')
            else:
                caco5_x = st.text_input('Rectal Toucher', value=caco5_x_value, key='caco5_x')

            caco6_x_value = st.session_state.input_data.get('FOBT', None)
            if pd.isna(caco6_x_value):
                caco6_x = st.radio('Fecal Occult Bleeding Test', ['Negatif', '+1', '+2', '+3', '+4'], index= None, horizontal=False, key='caco6_x')
            else:
                caco6_x = st.radio('Fecal Occult Bleeding Test', ['Negatif', '+1', '+2', '+3', '+4'],
                                    index=['Negatif', '+1', '+2', '+3', '+4'].index(caco6_x_value),
                                    horizontal=False, key='caco6_x')

        with st.expander('**Skrining Kanker Payudara dan Serviks**'):
            left, right = st.columns(2, vertical_alignment='top' )
            menarche_x=left.number_input('Usia haid pertama (tahun)', value=float(st.session_state.input_data.get('Menarche', '')), key='menarche_x')
            # hpht_x=left.date_input('HPHT', key='hpht_x', format='DD/MM/YYYY', max_value="today", value=st.session_state.input_data.get('HPHT', None))
            hpht_value= st.session_state.input_data.get('HPHT', None)
            if pd.isna(hpht_value):
                hpht_x=left.date_input('HPHT', key='hpht_x', format='DD/MM/YYYY', max_value="today", value=None)
            else:
                hpht_x=left.date_input('HPHT', key='hpht_x', format='DD/MM/YYYY', max_value="today", value=hpht_value) 
            seks_pertama_x=left.number_input('Usia pertama kali berhubungan seksual (tahun)', value=float(st.session_state.input_data.get('Usia Pertama Kali Seks', '')), key='seks_pertama_x')
            hamil_pertama_x=left.number_input('Usia kehamilan pertama (tahun)', value=float(st.session_state.input_data.get('Usia Kehamilan Pertama', '')), key='hamil_pertama_x')
            jml_melahirkan_x=left.number_input('Jumlah melahirkan', value=float(st.session_state.input_data.get('Jumlah Melahirkan', '')), key='jml_melahirkan_x')
            
            menyusui_value = st.session_state.input_data.get('Menyusui', None)    
            if pd.isna(menyusui_value):
                menyusui_x = left.radio('Pernah menyusui', ['Ya', 'Tidak'], index=None, horizontal=True, key='menyusui_x')
            else:
                menyusui_x = left.radio('Pernah menyusui', ['Ya', 'Tidak'],
                                    index=['Ya', 'Tidak'].index(menyusui_value),
                                    horizontal=True, key='menyusui_x')
            
            left.text('Riwayat Pemakaian KB')
            pil_x_value = st.session_state.input_data.get('Pil', None)
            if pd.isna(pil_x_value):
                pil_x = left.radio('Pil', ['Ya', 'Tidak'], index=None, horizontal=True, key='pil_x')
            else:
                pil_x = left.radio('Pil', ['Ya', 'Tidak'], index=['Ya', 'Tidak'].index(pil_x_value),horizontal=True, key='pil_x')
            if st.session_state.pil_x == 'Ya':
                lama_pil_x=left.text_input('Lama Penggunaan (pil)', value=st.session_state.input_data.get('Lama Pil', ''), key='lama_pil_x', disabled=False)
            else:
                lama_pil_x=left.text_input('Lama Penggunaan (pil)', value=None, key='lama_pil_x', disabled=True)
            
            
            suntik_x_value = st.session_state.input_data.get('Suntik', None)
            if pd.isna(suntik_x_value):
                suntik_x = left.radio('Suntik', ['Ya', 'Tidak'], index=None, horizontal=True, key='suntik_x')
            else:
                suntik_x = left.radio('Suntik', ['Ya', 'Tidak'], index=['Ya', 'Tidak'].index(suntik_x_value), horizontal=True, key='suntik_x')
            if st.session_state.suntik_x == 'Ya':
                lama_suntik_x=left.text_input('Lama Penggunaan (suntik)', value=st.session_state.input_data.get('Lama Suntik', ''), key='lama_suntik_x', disabled=False)
            else:
                lama_suntik_x=left.text_input('Lama Penggunaan (suntik)', value=None, key='lama_suntik_x', disabled=True) 
            
            
            implan_x_value = st.session_state.input_data.get('Implan', None)
            if pd.isna(implan_x_value):
                implan_x = left.radio('Implan', ['Ya', 'Tidak'], index=None, horizontal=True, key='implan_x')
            else:
                implan_x = left.radio('Implan', ['Ya', 'Tidak'], index=['Ya', 'Tidak'].index(implan_x_value), horizontal=True, key='implan_x')
            if st.session_state.implan_x == 'Ya':
                lama_implan_x=left.text_input('Lama Penggunaan (implan)', value=st.session_state.input_data.get('Lama Implan', ''), key='lama_implan_x', disabled=False)
            else:
                lama_implan_x=left.text_input('Lama Penggunaan (implan)', value=None, key='lama_implan_x', disabled=True)
            
            iud_x_value = st.session_state.input_data.get('IUD', None)
            if pd.isna(iud_x_value):
                iud_x = left.radio('IUD', ['Ya', 'Tidak'], index=None, horizontal=True, key='iud_x')
            else:
                iud_x = left.radio('IUD', ['Ya', 'Tidak'], index=['Ya', 'Tidak'].index(iud_x_value),horizontal=True, key='iud_x')
            if st.session_state.iud_x == 'Ya':
                lama_iud_x=left.text_input('Lama Penggunaan (iud)', value=st.session_state.input_data.get('Lama IUD', ''), key='lama_iud_x', disabled=False)
            else:
                lama_iud_x=left.text_input('Lama Penggunaan (iud)', value=None, key='lama_iud_x', disabled=True)
                
                
            ca_keluarga_value = st.session_state.input_data.get('Riwayat Kanker Keluarga', None)    
            if pd.isna(ca_keluarga_value):
                ca_keluarga_x = left.radio('Riwayat kanker dalam keluarga', ['Ya', 'Tidak'], index=None, horizontal=True, key='ca_keluarga_x')
            else:
                ca_keluarga_x = left.radio('Riwayat kanker dalam keluarga', ['Ya', 'Tidak'],
                                        index=['Ya', 'Tidak'].index(ca_keluarga_value),
                                        horizontal=True, key='ca_keluarga_x')        
                
            if st.session_state.ca_keluarga_x == 'Ya':
                #Jika ya, siapa?
                keluarga_siapa_x=left.text_input('Siapa yang menderita kanker?', value=st.session_state.input_data.get('Siapa Yang Menderita Kanker', ''), key='keluarga_siapa_x', disabled=False)
                #kanker jenis apa
                ca_apa_x=left.text_input('Kanker jenis apa?', value=st.session_state.input_data.get('Kanker Jenis Apa', ''), key='ca_apa_x', disabled= False)
            else:
                #Jika ya, siapa?
                keluarga_siapa_x=left.text_input('Siapa yang menderita kanker?', value=None, key='keluarga_siapa_x', disabled=True)
                #kanker jenis apa
                ca_apa_x=left.text_input('Kanker jenis apa?', value=None, key='ca_apa_x', disabled= True)
                
            tumorjinak_value = st.session_state.input_data.get('Riwayat Tumor Jinak Payudara', None)    
            if pd.isna(tumorjinak_value):
                tumorjinak_x = left.radio('Riwayat tumor jinak payudara', ['Ya', 'Tidak'], index=None, horizontal=True, key='tumorjinak_x')
            else:
                tumorjinak_x = left.radio('Riwayat tumor jinak payudara', ['Ya', 'Tidak'],
                                        index=['Ya', 'Tidak'].index(tumorjinak_value),
                                        horizontal=True, key='tumorjinak_x')

            menopause_value = st.session_state.input_data.get('Menopause', None)
            if pd.isna(menopause_value):
                menopause_x = left.radio('Apakah sudah menopause', ['Sudah', 'Belum'], index=None, horizontal=True, key='menopause_x')
            else:
                menopause_x = left.radio('Apakah sudah menopause', ['Sudah', 'Belum'],
                                    index=['Sudah', 'Belum'].index(menopause_value),
                                    horizontal=True, key='menopause_x')
            usia_menopause_x=left.number_input('Usia menopause (tahun)', value=float(st.session_state.input_data.get('Usia Menopause', '')), key='usia_menopause_x')
            pernah_pap_value = st.session_state.input_data.get('Pernah Pap Smear', None)
            if pd.isna(pernah_pap_value):
                pernah_pap_x = right.radio('Pernah Pap Smear', ['Ya', 'Tidak'], index=None, horizontal=True, key='pernah_pap_x')
            else:
                pernah_pap_x = right.radio('Pernah Pap Smear', ['Ya', 'Tidak'],
                                        index=['Ya', 'Tidak'].index(pernah_pap_value),
                                        horizontal=True, key='pernah_pap_x')   
                    
            if st.session_state.pernah_pap_x == 'Ya':
                kapan_pap_x=right.text_input('Kapan', value=st.session_state.input_data.get('Kapan PAP Smear', ''), key='kapan_pap_x', disabled=False)
                hasil_pap_x=right.text_input('Hasil Pap Smear', value=st.session_state.input_data.get('Hasil PAP Smear', ''), key='hasil_pap_x', disabled= False)
            else:
                kapan_pap_x=right.text_input('Kapan', key='kapan_pap_x', disabled=True)
                hasil_pap_x=right.text_input('Hasil Pap Smear', key='hasil_pap_x', disabled= True)
            
            pernah_iva_value = st.session_state.input_data.get('Pernah IVA', None)    
            if pd.isna(pernah_iva_value):
                pernah_iva_x = right.radio('Pernah IVA', ['Ya', 'Tidak'], index=None, horizontal=True, key='pernah_iva_x')
            else:
                pernah_iva_x = right.radio('Pernah IVA', ['Ya', 'Tidak'],
                                        index=['Ya', 'Tidak'].index(pernah_iva_value),
                                        horizontal=True, key='pernah_iva_x')

            if st.session_state.pernah_iva_x == 'Ya':
                kapan_iva_x=right.text_input('Kapan', value=st.session_state.input_data.get('Kapan IVA', ''), key='kapan_iva_x', disabled= False)
                hasil_iva_x=right.text_input('Hasil IVA', value=st.session_state.input_data.get('Hasil IVA', ''), key='hasil_iva_x', disabled= False)
            else:
                kapan_iva_x=right.text_input('Kapan', key='kapan_iva_x', disabled= True)
                hasil_iva_x=right.text_input('Hasil IVA', key='hasil_iva_x', disabled= True)
            
            benjolan_payudara_value = st.session_state.input_data.get('Benjolan Di Payudara Dan Ketiak', None)    
            if pd.isna(benjolan_payudara_value):
                benjolan_payudara_x = right.radio('Apakah terdapat benjolan di payudara dan ketiak?', ['Ya', 'Tidak'], index=None, horizontal=True, key='benjolan_payudara_x')
            else:
                benjolan_payudara_x = right.radio('Apakah terdapat benjolan di payudara dan ketiak?', ['Ya', 'Tidak'],
                                            index=['Ya', 'Tidak'].index(benjolan_payudara_value),
                                            horizontal=True, key='benjolan_payudara_x')

            cairan_puting_value = st.session_state.input_data.get('Cairan Dari Puting', None)
            if pd.isna(cairan_puting_value):
                cairan_puting_x = right.radio('Apakah terdapat cairan keluar dari puting susu?', ['Ya', 'Tidak'], index=None, horizontal=True, key='cairan_puting_x')
            else:
                cairan_puting_x = right.radio('Apakah terdapat cairan keluar dari puting susu?', ['Ya', 'Tidak'],
                                        index=['Ya', 'Tidak'].index(cairan_puting_value),
                                        horizontal=True, key='cairan_puting_x')

            perubahan_value = st.session_state.input_data.get('Perubahan Pada Payudara', None)
            if pd.isna(perubahan_value):
                perubahan_x = right.radio('Apakah terdapat perubahan lainnya pada payudara?', ['Ya', 'Tidak'], index=None, horizontal=True, key='perubahan_x')
            else:
                perubahan_x = right.radio('Apakah terdapat perubahan lainnya pada payudara?', ['Ya', 'Tidak'],
                                    index=['Ya', 'Tidak'].index(perubahan_value),
                                    horizontal=True, key='perubahan_x')
            #jika ya, sebutkan kelainannya
            if st.session_state.perubahan_x == 'Ya':
                jenis_perubahan_x=right.text_input('Sebutkan jenis perubahannya?', value=st.session_state.input_data.get('Jenis Perubahan Payudara', ''), key='jenis_perubahan_x', disabled=False)
            else:
                jenis_perubahan_x=right.text_input('Sebutkan jenis perubahannya?', value=None, key='jenis_perubahan_x', disabled=True)
            
            metroragi_value = st.session_state.input_data.get('Perdarahan Di Luar Haid', None)    
            if pd.isna(metroragi_value):
                metroragi_x = right.radio('Apakah terdapat perdarahan di luar massa haid?', ['Ya', 'Tidak'], index=None, horizontal=True, key='metroragi_x')
            else:
                metroragi_x = right.radio('Apakah terdapat perdarahan di luar massa haid?', ['Ya', 'Tidak'],
                                    index=['Ya', 'Tidak'].index(metroragi_value),
                                    horizontal=True, key='metroragi_x')

            darah_seks_value = st.session_state.input_data.get('Perdarahan Saat Berhubungan', None)
            if pd.isna(darah_seks_value):
                darah_seks_x = right.radio('Apakah terdapat perdarahan saat/setelah berhubungan seks?', ['Ya', 'Tidak'], index=None, horizontal=True, key='darah_seks_x')
            else:
                darah_seks_x = right.radio('Apakah terdapat perdarahan saat/setelah berhubungan seks?', ['Ya', 'Tidak'],
                                        index=['Ya', 'Tidak'].index(darah_seks_value),
                                        horizontal=True, key='darah_seks_x')

            keputihan_value = st.session_state.input_data.get('Sering Keputihan', None)
            if pd.isna(keputihan_value):
                keputihan_x = right.radio('Apakah anda sering keputihan?', ['Ya', 'Tidak'], index=None, horizontal=True, key='keputihan_x')
            else:
                keputihan_x = right.radio('Apakah anda sering keputihan?', ['Ya', 'Tidak'],
                                    index=['Ya', 'Tidak'].index(keputihan_value),
                                    horizontal=True, key='keputihan_x')

            lap_value = st.session_state.input_data.get('Nyeri Perut Bawah', None)
            if pd.isna(lap_value):
                lap_x = right.radio('Apakah anda mengalami nyeri perut bagian bawah?', ['Ya', 'Tidak'], index=None, horizontal=True, key='lap_x')
            else:
                lap_x = right.radio('Apakah anda mengalami nyeri perut bagian bawah?', ['Ya', 'Tidak'],
                                index=['Ya', 'Tidak'].index(lap_value),
                                horizontal=True, key='lap_x')
                
            sadanisd_x_value = st.session_state.input_data.get('Sadanis Payudara Kanan', '')
            if pd.isna(sadanisd_x_value):
                sadanisd_x = right.text_area('SADANIS Payudara Kanan', value=None, key='sadanisd_x')
            else:
                sadanisd_x = right.text_area('SADANIS Payudara Kanan', value=sadanisd_x_value, key='sadanisd_x')

            sadaniss_x_value = st.session_state.input_data.get('Sadanis Payudara Kiri', '')
            if pd.isna(sadaniss_x_value):
                sadaniss_x = right.text_area('SADANIS Payudara Kiri', value=None, key='sadaniss_x')
            else:
                sadaniss_x = right.text_area('SADANIS Payudara Kiri', value=sadaniss_x_value, key='sadaniss_x')

            iva_x_value = st.session_state.input_data.get('IVA', '')
            if pd.isna(iva_x_value):
                iva_x = right.text_area('Inspeksi Visual Asam Asetat', value=None, key='iva_x')
            else:
                iva_x = right.text_area('Inspeksi Visual Asam Asetat', value=iva_x_value, key='iva_x')

            hpv_x_value = st.session_state.input_data.get('HPV DNA', '')
            if pd.isna(hpv_x_value):
                hpv_x = right.text_area('Pemeriksaan HPV DNA', value=None, key='hpv_x')
            else:
                hpv_x = right.text_area('Pemeriksaan HPV DNA', value=hpv_x_value, key='hpv_x')
            
        with st.expander('**Skrining Hepatitis**'):
            left, right = st.columns(2, vertical_alignment='top')
            hep1_x_value = st.session_state.input_data.get('Hepatitis 1', None)
            if pd.isna(hep1_x_value):
                hep1_x = left.radio('Apakah anda pernah menjalani tes untuk Hepatitis B dan hasilnya positif?', ['Ya', 'Tidak'], index=None, horizontal=True, key='hep1_x')
            else:
                hep1_x = left.radio('Apakah anda pernah menjalani tes untuk Hepatitis B dan hasilnya positif?', ['Ya', 'Tidak'],
                                    index=['Ya', 'Tidak'].index(hep1_x_value),
                                    horizontal=True, key='hep1_x')

            hep2_x_value = st.session_state.input_data.get('Hepatitis 2', None)
            if pd.isna(hep2_x_value):
                hep2_x = left.radio('Apakah anda memiliki saudara kandung yang menderita Hepatitis B?', ['Ya', 'Tidak'], index=None, horizontal=True, key='hep2_x')
            else:
                hep2_x = left.radio('Apakah anda memiliki saudara kandung yang menderita Hepatitis B?', ['Ya', 'Tidak'],
                                    index=['Ya', 'Tidak'].index(hep2_x_value),
                                    horizontal=True, key='hep2_x')

            hep3_x_value = st.session_state.input_data.get('Hepatitis 3?', None)
            if pd.isna(hep3_x_value):
                hep3_x = left.radio('Apakah anda pernah pernah berhubungan seksual dengan orang yang bukan pasangan resmi anda?', ['Ya', 'Tidak'], index=None, horizontal=True, key='hep3_x')
            else:
                hep3_x = left.radio('Apakah anda pernah pernah berhubungan seksual dengan orang yang bukan pasangan resmi anda?', ['Ya', 'Tidak'],
                                    index=['Ya', 'Tidak'].index(hep3_x_value),
                                    horizontal=True, key='hep3_x')

            hep4_x_value = st.session_state.input_data.get('Hepatitis 4', None)
            if pd.isna(hep4_x_value):
                hep4_x = left.radio('Apakah anda pernah menerima transfusi darah sebelumnya?', ['Ya', 'Tidak'], index=None, horizontal=True, key='hep4_x')
            else:
                hep4_x = left.radio('Apakah anda pernah menerima transfusi darah sebelumnya?', ['Ya', 'Tidak'],
                                    index=['Ya', 'Tidak'].index(hep4_x_value),
                                    horizontal=True, key='hep4_x')

            hep5_x_value = st.session_state.input_data.get('Hepatitis 5', None)
            if pd.isna(hep5_x_value):
                hep5_x = right.radio('Apakah anda pernah menjalani cuci darah/hemodialisis sebelumnya?', ['Ya', 'Tidak'], index=None, horizontal=True, key='hep5_x')
            else:
                hep5_x = right.radio('Apakah anda pernah menjalani cuci darah/hemodialisis sebelumnya?', ['Ya', 'Tidak'],
                                    index=['Ya', 'Tidak'].index(hep5_x_value),
                                    horizontal=True, key='hep5_x')

            hep6_x_value = st.session_state.input_data.get('Hepatitis 6', None)
            if pd.isna(hep6_x_value):
                hep6_x = right.radio('Apakah anda pernah menggunakan narkoba, obat terlarang, atau bahan adiktif lainnya dengan cara disuntik?', ['Ya', 'Tidak'], index=None, horizontal=True, key='hep6_x')
            else:
                hep6_x = right.radio('Apakah anda pernah menggunakan narkoba, obat terlarang, atau bahan adiktif lainnya dengan cara disuntik?', ['Ya', 'Tidak'],
                                    index=['Ya', 'Tidak'].index(hep6_x_value),
                                    horizontal=True, key='hep6_x')

            hep7_x_value = st.session_state.input_data.get('Hepatitis 7', None)
            if pd.isna(hep7_x_value):
                hep7_x = right.radio('Apakah anda adalah orang dengan HIV (ODHIV)?', ['Ya', 'Tidak'], index=None, horizontal=True, key='hep7_x')
            else:
                hep7_x = right.radio('Apakah anda adalah orang dengan HIV (ODHIV)?', ['Ya', 'Tidak'],
                                    index=['Ya', 'Tidak'].index(hep7_x_value),
                                    horizontal=True, key='hep7_x')

            hep8_x_value = st.session_state.input_data.get('Hepatitis 8', None)
            if pd.isna(hep8_x_value):
                hep8_x = right.radio('Apakah anda pernah mendapatkan pegobatan Hepatitis C dan tidak sembuh?', ['Ya', 'Tidak'], index=None, horizontal=True, key='hep8_x')
            else:
                hep8_x = right.radio('Apakah anda pernah mendapatkan pengobatan Hepatitis C dan tidak sembuh?', ['Ya', 'Tidak'],
                                    index=['Ya', 'Tidak'].index(hep8_x_value),
                                    horizontal=True, key='hep8_x')
            
        with st.expander('**Skrining Indera Pengelihatan**'):
            left, right = st.columns(2, vertical_alignment='top')
            # visusod_x=left.text_input('Visus OD', value=st.session_state.input_data.get('Visus OD', ''), key='visusod_x')
            # visusos_x=right.text_input('Visus OS', value=st.session_state.input_data.get('Visus OS', ''), key='visusos_x')
            
            visusod_x_value = st.session_state.input_data.get('Visus OD', '')
            if pd.isna(visusod_x_value):
                visusod_x = left.text_input('Visus OD', value=None, key='visusod_x')
            else:
                visusod_x = left.text_input('Visus OD', value=visusod_x_value, key='visusod_x')

            visusos_x_value = st.session_state.input_data.get('Visus OS', '')
            if pd.isna(visusos_x_value):
                visusos_x = right.text_input('Visus OS', value=None, key='visusos_x')
            else:
                visusos_x = right.text_input('Visus OS', value=visusos_x_value, key='visusos_x')

            
            katarakod_x_value = st.session_state.input_data.get('Katarak OD', None)
            if pd.isna(katarakod_x_value):
                katarakod_x = left.radio('Katarak OD', ['Ya', 'Tidak'], index= None, horizontal=True, key='katarakod_x')
            else:
                katarakod_x = left.radio('Katarak OD', ['Ya', 'Tidak'],
                                        index=['Ya', 'Tidak'].index(katarakod_x_value),
                                        horizontal=True, key='katarakod_x')

            katarakos_x_value = st.session_state.input_data.get('Katarak OS', None)
            if pd.isna(katarakos_x_value):
                katarakos_x = right.radio('Katarak OS', ['Ya', 'Tidak'], index= None, horizontal=True, key='katarakos_x')
            else:
                katarakos_x = right.radio('Katarak OS', ['Ya', 'Tidak'],
                                        index=['Ya', 'Tidak'].index(katarakos_x_value),
                                        horizontal=True, key='katarakos_x')
        
        with st.expander('**Skrining Jantung**'):
            st.markdown('**Jakarta Cardiovascular Score**')
            jcs1_x_value = st.session_state.input_data.get('JCS 1', None)
            if pd.isna(jcs1_x_value):
                jcs1_x = st.radio('Jenis Kelamin', ['Perempuan', 'Laki-laki'], index=None, horizontal=True, key='jcs1_x')
            else:
                jcs1_x = st.radio('Jenis Kelamin', ['Perempuan', 'Laki-laki'],
                                index=['Perempuan', 'Laki-laki'].index(jcs1_x_value),
                                horizontal=True, key='jcs1_x')

            jcs2_x_value = st.session_state.input_data.get('JCS 2', None)
            if pd.isna(jcs2_x_value):
                jcs2_x = st.radio('Kelompok Umur', ['25-34 tahun', '35-39 tahun', '40-44 tahun', '45-49 tahun', '50-54 tahun', '55-59 tahun', '60-64 tahun'], index=None, horizontal=True, key='jcs2_x')
            else:
                jcs2_x = st.radio('Kelompok Umur', ['25-34 tahun', '35-39 tahun', '40-44 tahun', '45-49 tahun', '50-54 tahun', '55-59 tahun', '60-64 tahun'],
                                index=['25-34 tahun', '35-39 tahun', '40-44 tahun', '45-49 tahun', '50-54 tahun', '55-59 tahun', '60-64 tahun'].index(jcs2_x_value),
                                horizontal=True, key='jcs2_x')

            jcs3_x_value = st.session_state.input_data.get('JCS 3', None)
            if pd.isna(jcs3_x_value):
                jcs3_x = st.radio('Kelompok Tekanan Darah', ['<130/<84', '130-139/85-89', '140-159/90-99', '160-179/100-109', '>=180/>=110'], index=None, horizontal=True, key='jcs3_x')
            else:
                jcs3_x = st.radio('Kelompok Tekanan Darah', ['<130/<84', '130-139/85-89', '140-159/90-99', '160-179/100-109', '>=180/>=110'],
                                index=['<130/<84', '130-139/85-89', '140-159/90-99', '160-179/100-109', '>=180/>=110'].index(jcs3_x_value),
                                horizontal=True, key='jcs3_x')

            jcs4_x_value = st.session_state.input_data.get('JCS 4', None)
            if pd.isna(jcs4_x_value):
                jcs4_x = st.radio('Kelompok IMT', ['13.79-25.99', '26-29.99', '30-35.58'], index=None, horizontal=True, key='jcs4_x')
            else:
                jcs4_x = st.radio('Kelompok IMT', ['13.79-25.99', '26-29.99', '30-35.58'],
                                index=['13.79-25.99', '26-29.99', '30-35.58'].index(jcs4_x_value),
                                horizontal=True, key='jcs4_x')

            jcs5_x_value = st.session_state.input_data.get('JCS 5', None)
            if pd.isna(jcs5_x_value):
                jcs5_x = st.radio('Status Merokok', ['Tidak Pernah', 'Mantan Perokok', 'Perokok Aktif'], index=None, horizontal=True, key='jcs5_x')
            else:
                jcs5_x = st.radio('Status Merokok', ['Tidak Pernah', 'Mantan Perokok', 'Perokok Aktif'],
                                index=['Tidak Pernah', 'Mantan Perokok', 'Perokok Aktif'].index(jcs5_x_value),
                                horizontal=True, key='jcs5_x')

            jcs6_x_value = st.session_state.input_data.get('JCS 6', None)
            if pd.isna(jcs6_x_value):
                jcs6_x = st.radio('Diabetes Melitus', ['Tidak', 'Ya'], index=None, horizontal=True, key='jcs6_x')
            else:
                jcs6_x = st.radio('Diabetes Melitus', ['Tidak', 'Ya'],
                                index=['Tidak', 'Ya'].index(jcs6_x_value),
                                horizontal=True, key='jcs6_x')

            jcs7_x_value = st.session_state.input_data.get('JCS 7', None)
            if pd.isna(jcs7_x_value):
                jcs7_x = st.radio('Aktivitas Fisik Mingguan', ['Tidak Ada', 'Rendah', 'Sedang', 'Berat'], index=None, horizontal=True, key='jcs7_x')
            else:
                jcs7_x = st.radio('Aktivitas Fisik Mingguan', ['Tidak Ada', 'Rendah', 'Sedang', 'Berat'],
                                index=['Tidak Ada', 'Rendah', 'Sedang', 'Berat'].index(jcs7_x_value),
                                horizontal=True, key='jcs7_x')

            # Fungsi untuk menghitung skor
            def calculate_score(jcs1_x, jcs2_x, jcs3_x, jcs4_x, jcs5_x, jcs6_x, jcs7_x):
                score = 0

                if jcs1_x == 'Laki-laki':
                    score += 1
                elif jcs1_x == 'Perempuan':
                    score += 0
                
                if jcs2_x == '25-34 tahun':
                    score -= 4
                elif jcs2_x == '35-39 tahun':
                    score -= 3
                elif jcs2_x == '40-44 tahun':
                    score -= 2
                elif jcs2_x == '45-49 tahun':
                    score += 0
                elif jcs2_x == '50-54 tahun':
                    score += 1
                elif jcs2_x == '55-59 tahun':
                    score += 2
                elif jcs2_x == '60-64 tahun':
                    score += 3
                
                if jcs3_x == '<130/<84':
                    score += 0
                elif jcs3_x == '130-139/85-89':
                    score += 1
                elif jcs3_x == '140-159/90-99':
                    score += 2
                elif jcs3_x == '160-179/100-109':
                    score += 3
                elif jcs3_x == '>=180/>=110':
                    score += 4
                
                # '13.79-25.99', '26-29.99', '30-35.58'
                if jcs4_x == '13.79-25.99':
                    score += 0
                elif jcs4_x == '26-29.99':
                    score += 1
                elif jcs4_x == '30-35.58':
                    score += 2
                
                # 'Tidak Pernah', 'Mantan Perokok', 'Perokok Aktif'
                if jcs5_x == 'Tidak Pernah':
                    score += 0
                elif jcs5_x == 'Mantan Perokok':
                    score += 3
                elif jcs5_x == 'Perokok Aktif':
                    score += 4
                # 'Tidak', 'Ya'
                if jcs6_x == 'Tidak':
                    score += 0
                elif jcs6_x == 'Ya':
                    score += 2
                # 'Tidak Ada', 'Rendah', 'Sedang', 'Berat'
                if jcs7_x == 'Tidak Ada':
                    score += 2
                elif jcs7_x == 'Rendah':
                    score += 1
                elif jcs7_x == 'Sedang':
                    score += 0
                elif jcs7_x == 'Berat':
                    score -= 3
                
                return score

            # Hitung total skor
            total_score = calculate_score(jcs1_x, jcs2_x, jcs3_x, jcs4_x, jcs5_x, jcs6_x, jcs7_x)

            # Tampilkan total skor
            jcs_tot_x=float(st.text_input('Jumlah Skor', value=total_score, disabled=True, key='jcs_tot_x'))

            # Penjelasan untuk hasil skor
            if -7<=total_score <= 1:
                st.success("Risiko Rendah Penyakit Kardiovaskular.")
            elif 2<=total_score <= 4:
                st.warning("Risiko Sedang Penyakit Kardiovaskular.")
            elif total_score >=5:
                st.warning("Risiko Tinggi Penyakit Kardiovaskular.")        
        
            # ekg_x=st.text_area('Interpretasi Hasil Pemeriksaan EKG', value=st.session_state.input_data.get('Interpretasi EKG', ''), key='ekg_x')
            ekg_x_value = st.session_state.input_data.get('Interpretasi EKG', '')
            if pd.isna(ekg_x_value):
                ekg_x=st.text_area('Interpretasi Hasil Pemeriksaan EKG', value=None, key='ekg_x')
            else:
                ekg_x=st.text_area('Interpretasi Hasil Pemeriksaan EKG', value=ekg_x_value, key='ekg_x')

        with st.expander('**Skrining Gigi**'):
            left, right = st.columns(2, vertical_alignment='top')
            karies_x_value = st.session_state.input_data.get('Karies', '')
            if pd.isna(karies_x_value):
                karies_x = left.text_input('Karies', value=None, key='karies_x')
            else:
                karies_x = left.text_input('Karies', value=karies_x_value, key='karies_x')
    
            missing_x_value = st.session_state.input_data.get('Missing', '')
            if pd.isna(missing_x_value):
                missing_x = left.text_input('Missing', value=None, key='missing_x')
            else:
                missing_x = left.text_input('Missing', value=missing_x_value, key='missing_x')
                
            pocket_x_value = st.session_state.input_data.get('Periodontal Pocket', None)
            if pd.isna(pocket_x_value):
                pocket_x = right.radio('Periodontal Pocket', ['Ya', 'Tidak'], index= None, horizontal=True, key='pocket_x')
            else:
                pocket_x = right.radio('Periodontal Pocket', ['Ya', 'Tidak'],
                                    index=['Ya', 'Tidak'].index(pocket_x_value),
                                    horizontal=True, key='pocket_x')

            goyang_x_value = st.session_state.input_data.get('Gigi Goyang', '')
            if pd.isna(goyang_x_value):
                goyang_x = right.text_input('Gigi Goyang', value=None, key='goyang_x')
            else:
                goyang_x = right.text_input('Gigi Goyang', value=goyang_x_value, key='goyang_x')
                
        with st.expander('**Pemeriksaan Laboratorium**'):
            left, middle, right = st.columns(3, vertical_alignment="top")
            
            hb_x_value = st.session_state.input_data.get('Hb', '')
            if pd.isna(hb_x_value):
                hb_x = left.text_input('Hb', value=None, key='hb_x')
            else:
                hb_x = left.text_input('Hb', value=hb_x_value, key='hb_x')

            wbc_x_value = st.session_state.input_data.get('Leukosit', '')
            if pd.isna(wbc_x_value):
                wbc_x = left.text_input('Leukosit', value=None, key='wbc_x')
            else:
                wbc_x = left.text_input('Leukosit', value=wbc_x_value, key='wbc_x')

            hct_x_value = st.session_state.input_data.get('Hematokrit', '')
            if pd.isna(hct_x_value):
                hct_x = left.text_input('Hematokrit', value=None, key='hct_x')
            else:
                hct_x = left.text_input('Hematokrit', value=hct_x_value, key='hct_x')

            rbc_x_value = st.session_state.input_data.get('Eritrosit', '')
            if pd.isna(rbc_x_value):
                rbc_x = left.text_input('Eritrosit', value=None, key='rbc_x')
            else:
                rbc_x = left.text_input('Eritrosit', value=rbc_x_value, key='rbc_x')

            plt_x_value = st.session_state.input_data.get('Trombosit', '')
            if pd.isna(plt_x_value):
                plt_x = left.text_input('Trombosit', value=None, key='plt_x')
            else:
                plt_x = left.text_input('Trombosit', value=plt_x_value, key='plt_x')

            mcv_x_value = st.session_state.input_data.get('MCV', '')
            if pd.isna(mcv_x_value):
                mcv_x = left.text_input('MCV', value=None, key='mcv_x')
            else:
                mcv_x = left.text_input('MCV', value=mcv_x_value, key='mcv_x')

            mch_x_value = st.session_state.input_data.get('MCH', '')
            if pd.isna(mch_x_value):
                mch_x = left.text_input('MCH', value=None, key='mch_x')
            else:
                mch_x = left.text_input('MCH', value=mch_x_value, key='mch_x')

            mchc_x_value = st.session_state.input_data.get('MCHC', '')
            if pd.isna(mchc_x_value):
                mchc_x = middle.text_input('MCHC', value=None, key='mchc_x')
            else:
                mchc_x = middle.text_input('MCHC', value=mchc_x_value, key='mchc_x')

            gds_x_value = st.session_state.input_data.get('GDS', '')
            if pd.isna(gds_x_value):
                gds_x = middle.text_input('Gula Darah Sewaktu', value=None, key='gds_x')
            else:
                gds_x = middle.text_input('Gula Darah Sewaktu', value=gds_x_value, key='gds_x')
                
            gdp_x_value = st.session_state.input_data.get('GDP', '')
            if pd.isna(gdp_x_value):
                gdp_x = middle.text_input('Gula Darah Puasa', value=None, key='gdp_x')
            else:
                gdp_x = middle.text_input('Gula Darah Puasa', value=gdp_x_value, key='gdp_x')

            cho_x_value = st.session_state.input_data.get('Kolesterol Total', '')
            if pd.isna(cho_x_value):
                cho_x = middle.text_input('Kolesterol Total', value=None, key='cho_x')
            else:
                cho_x = middle.text_input('Kolesterol Total', value=cho_x_value, key='cho_x')

            hdl_x_value = st.session_state.input_data.get('HDL', '')
            if pd.isna(hdl_x_value):
                hdl_x = middle.text_input('HDL', value=None, key='hdl_x')
            else:
                hdl_x = middle.text_input('HDL', value=hdl_x_value, key='hdl_x')

            ldl_x_value = st.session_state.input_data.get('LDL', '')
            if pd.isna(ldl_x_value):
                ldl_x = middle.text_input('LDL', value=None, key='ldl_x')
            else:
                ldl_x = middle.text_input('LDL', value=ldl_x_value, key='ldl_x')

            tg_x_value = st.session_state.input_data.get('Trigliserida', '')
            if pd.isna(tg_x_value):
                tg_x = middle.text_input('Trigliserida', value=None, key='tg_x')
            else:
                tg_x = middle.text_input('Trigliserida', value=tg_x_value, key='tg_x')

            ur_x_value = st.session_state.input_data.get('Ureum', '')
            if pd.isna(ur_x_value):
                ur_x = right.text_input('Ureum', value=None, key='ur_x')
            else:
                ur_x = float(right.text_input('Ureum', value=ur_x_value, key='ur_x'))

            cr_x_value = st.session_state.input_data.get('Kreatinin', '')
            if pd.isna(cr_x_value):
                cr_x = right.text_input('Kreatinin', value=None, key='cr_x')
            else:
                cr_x = right.text_input('Kreatinin', value=cr_x_value, key='cr_x')

            ot_x_value = st.session_state.input_data.get('SGOT', '')
            if pd.isna(ot_x_value):
                ot_x = right.text_input('SGOT', value=None, key='ot_x')
            else:
                ot_x = right.text_input('SGOT', value=ot_x_value, key='ot_x')

            pt_x_value = st.session_state.input_data.get('SGPT', '')
            if pd.isna(pt_x_value):
                pt_x = right.text_input('SGPT', value=None, key='pt_x')
            else:
                pt_x = right.text_input('SGPT', value=pt_x_value, key='pt_x')

            hepb_x_value = st.session_state.input_data.get('Hepatitis B', None)    
            if pd.isna(hepb_x_value):
                hepb_x = right.selectbox('Hepatitis B', ['Reaktif', 'Non-Reaktif'], index=None, key='hepb_x')
            else:
                hepb_x = right.selectbox('Hepatitis B', ['Reaktif', 'Non-Reaktif'],
                            index=['Reaktif', 'Non-Reaktif'].index(hepb_x_value), key='hepb_x')
            
            hepc_x_value = st.session_state.input_data.get('Hepatitis C', None)    
            if pd.isna(hepc_x_value):
                hepc_x = right.selectbox('Hepatitis C', ['Reaktif', 'Non-Reaktif'], index=None, key='hepc_x')
            else:
                hepc_x = right.selectbox('Hepatitis C', ['Reaktif', 'Non-Reaktif'],
                            index=['Reaktif', 'Non-Reaktif'].index(hepc_x_value), key='hepc_x')

            tcm_x_value = st.session_state.input_data.get('Sputum TCM', '')
            if pd.isna(tcm_x_value):
                tcm_x = right.text_input('Sputum TCM', value=None, key='tcm_x')
            else:
                tcm_x = right.text_input('Sputum TCM', value=tcm_x_value, key='tcm_x')

        # Tombol untuk menyimpan data yang diubah
        btn_save = st.button('Update Data', key='btn_save')

        if btn_save:
            # Menyimpan data yang diubah ke dalam Google Sheets
            updated_data = pd.DataFrame(
                [
                    {
                        "Nama": nama_x,
                        "NIK": nik_x.strip(),
                        "Jenis Kelamin": jk_x,
                        "Tanggal Lahir": tanggal_lahir_x,
                        "Usia": umur_x,
                        "Alamat": alamat_x,
                        "Nomor HP": hp_x,
                        "RPD Hipertensi": rpd_ht_x,
                        "RPD DM":rpd_dm_x,
                        "RPD Penyakit Jantung": rpd_jtg_x,
                        "RPD Stroke": rpd_stroke_x,
                        "RPD Asma": rpd_asma_x,
                        "RPD Kanker": rpd_ca_x,
                        "RPD Kolesterol": rpd_cho_x,
                        "RPD PPOK": rpd_ppok_x,
                        "RPD Talasemia":rpd_talasemia_x,
                        "RPD Lupus": rpd_lupus_x,
                        "RPD Gangguan Pengelihatan": rpd_lihat_x,
                        "RPD Katarak": rpd_katarak_x,
                        "RPD Gangguan Pendengaran": rpd_dengar_x,
                        "RPK Hipertensi": rpk_ht_x,
                        "RPK DM": rpk_dm_x,
                        "RPK Penyakit Jantung": rpk_jtg_x,
                        "RPK Stroke": rpk_stroke_x,
                        "RPK Kanker": rpk_ca_x,
                        "RPK Talasemia": rpk_talasemia_x,
                        "RK Merokok": rk_rokok_x,
                        "RK Rokok PerHari": rk_rokokperhari_x,
                        "RK Lama Merokok": rk_lamamerokok_x,
                        "Pack Years": rk_packyear_x,
                        "RK Makan Manis": rk_manis_x,
                        "RK Makan Asin": rk_asin_x,
                        "RK Makan Berlemak": rk_lemak_x,
                        "RK Makan Sayur": rk_sayur_x,
                        "RK Olahraga": rk_olahraga_x,
                        "RK Konsumsi Alkohol": rk_alkohol_x,
                        "TD Sistole": tds_x,
                        "TD Diastole":tdd_x,
                        "Heart Rate": hr_x,
                        "Respiration Rate": rr_x,
                        "Suhu Badan": temp_x,
                        "Berat Badan":bb_x,
                        "Tinggi Badan":tb_x,
                        "IMT": bmi_x,
                        "Lingkar Perut": lp_x,
                        "Lingkar Lengan Atas": lla_x,
                        "PHQ1": phq1_x,
                        "PHQ2": phq2_x,
                        "GAD1": gad1_x,
                        "GAD2": gad2_x,
                        "Depresi": depresi_x,
                        "Cemas": cemas_x,
                        "Tes Bisik AD": bisikad_x,
                        "Tes Bisik AS": bisikas_x,
                        "Otoskopi AD": otoskopiad_x,
                        "Otoskopi AS": otoskopias_x,
                        "Rinne": rinne_x,
                        "Weber": weber_x,
                        "Schwabach": schwabach_x,
                        "Ca Paru 1": caparu1_x,
                        "Ca Paru 2": caparu2_x,
                        "Ca Paru 3": caparu3_x,
                        "Ca Paru 4": caparu4_x,
                        "Ca Paru 5": caparu5_x,
                        "Ca Paru 6": caparu6_x,
                        "Ca Paru 7": caparu7_x,
                        "Ca Paru 8": caparu8_x,
                        "Ca Paru 9": caparu9_x,
                        "Total Skor Ca Paru": caparu_tot_x,
                        "PPOK 1": ppok1_x,
                        "PPOK 2": ppok2_x,
                        "PPOK 3": ppok3_x,
                        "PPOK 4": ppok4_x,
                        "PPOK 5": ppok5_x,
                        "PPOK 6": ppok6_x,
                        "PPOK 7": ppok7_x,
                        "Total Skor PPOK": ppok_tot_x,
                        "TB 1": tb1_x,
                        "TB 2": tb2_x,
                        "TB 3": tb3_x,
                        "TB 4": tb4_x,
                        "TB 5": tb5_x,
                        "TB 6": tb6_x,
                        "TB 7": tb7_x,
                        "Ca Kolorektal 1": caco1_x,
                        "Ca Kolorektal 2": caco2_x,
                        "Ca Kolorektal 3": caco3_x,
                        "Ca Kolorektal 4": caco4_x,
                        "Total Skor Ca Kolorektal": caco_tot_x,
                        "Rectal Toucher": caco5_x,
                        "FOBT": caco6_x,
                        "Menarche": menarche_x,
                        "HPHT": hpht_x,
                        "Usia Pertama Kali Seks": seks_pertama_x,
                        "Usia Kehamilan Pertama": hamil_pertama_x,
                        "Jumlah Melahirkan": jml_melahirkan_x,
                        "Menyusui": menyusui_x,
                        "Pil": pil_x,
                        "Lama Pil": lama_pil_x,
                        "Suntik": suntik_x,
                        "Lama Suntik": lama_suntik_x,
                        "Implan": implan_x,
                        "Lama Implan": lama_implan_x,
                        "IUD": iud_x,
                        "Lama IUD": lama_iud_x,
                        "Riwayat Kanker Keluarga": ca_keluarga_x,
                        "Siapa Yang Menderita Kanker": keluarga_siapa_x,
                        "Kanker Jenis Apa": ca_apa_x,
                        "Riwayat Tumor Jinak Payudara": tumorjinak_x,
                        "Menopause": menopause_x,
                        "Usia Menopause": usia_menopause_x,
                        "Pernah PAP Smear": pernah_pap_x,
                        "Kapan PAP Smear": kapan_pap_x,
                        "Hasil PAP Smear": hasil_pap_x,
                        "Pernah IVA": pernah_iva_x,
                        "Kapan IVA": kapan_iva_x,
                        "Hasil IVA": hasil_iva_x,
                        "Benjolan Di Payudara Dan Ketiak": benjolan_payudara_x,
                        "Cairan Dari Puting": cairan_puting_x,
                        "Perubahan Pada Payudara": perubahan_x,
                        "Jenis Perubahan Payudara": jenis_perubahan_x,
                        "Perdarahan Di Luar Haid": metroragi_x,
                        "Perdarahan Saat Berhubungan": darah_seks_x,
                        "Sering Keputihan": keputihan_x,
                        "Nyeri Perut Bawah": lap_x,
                        "Sadanis Payudara Kanan": sadanisd_x,
                        "Sadanis Payudara Kiri": sadaniss_x,
                        "IVA": iva_x,
                        "HPV DNA": hpv_x,
                        "Hepatitis 1": hep1_x,
                        "Hepatitis 2": hep2_x,
                        "Hepatitis 3": hep3_x,
                        "Hepatitis 4": hep4_x,
                        "Hepatitis 5": hep5_x,
                        "Hepatitis 6": hep6_x,
                        "Hepatitis 7": hep7_x,
                        "Hepatitis 8": hep8_x,
                        "Hepatitis B": hepb_x,
                        "Hepatitis C": hepc_x,
                        "Visus OD": visusod_x,
                        "Visus OS": visusos_x,
                        "Katarak OD": katarakod_x,
                        "Katarak OS": katarakos_x,
                        "JCS 1": jcs1_x,
                        "JCS 2": jcs2_x,
                        "JCS 3": jcs3_x,
                        "JCS 4": jcs4_x,
                        "JCS 5": jcs5_x,
                        "JCS 6": jcs6_x,
                        "JCS 7": jcs7_x,
                        "Total Skor JCS": jcs_tot_x,
                        "Interpretasi EKG": ekg_x,
                        "Karies": karies_x,
                        "Missing": missing_x,
                        "Periodontal Pocket": pocket_x,
                        "Gigi Goyang": goyang_x,
                        "Hb": hb_x,
                        "Leukosit": wbc_x,
                        "Hematokrit": hct_x,
                        "Eritrosit": rbc_x,
                        "Trombosit": plt_x,
                        "MCV": mcv_x, 
                        "MCH": mch_x,
                        "MCHC": mchc_x,
                        "GDS": gds_x,
                        "GDP": gdp_x,
                        "Kolesterol Total": cho_x,
                        "HDL": hdl_x,
                        "LDL": ldl_x,
                        "Trigliserida": tg_x,
                        "Ureum": ur_x,
                        "Kreatinin": cr_x,
                        "SGOT": ot_x,
                        "SGPT":pt_x,
                        "Sputum TCM": tcm_x
                    }
                ]
            )
            
            # Cari baris yang sesuai dengan nama yang ada
            df['NIK'] = df['NIK'].astype(str)
            idx = df[df['NIK'].str.contains(st.session_state.input_nik.strip(), case=False, na=False)].index
            
            ########################################
            if len(idx) > 0:
                # Jika nik ditemukan, update data pada baris tersebut
                df.loc[idx, "Nama"] = nama_x
                df.loc[idx, "Jenis Kelamin"] = jk_x
                df.loc[idx, "Tanggal Lahir"] = tanggal_lahir_x
                df.loc[idx, "Usia"] = umur_x
                df.loc[idx, "Alamat"] = alamat_x
                df.loc[idx, "Nomor HP"] = hp_x
                df.loc[idx, "RPD Hipertensi"] = rpd_ht_x
                df.loc[idx, "RPD DM"] = rpd_dm_x
                df.loc[idx, "RPD Penyakit Jantung"] = rpd_jtg_x
                df.loc[idx, "RPD Stroke"] = rpd_stroke_x
                df.loc[idx, "RPD Asma"] = rpd_asma_x
                df.loc[idx, "RPD Kanker"] = rpd_ca_x
                df.loc[idx, "RPD Kolesterol"] = rpd_cho_x
                df.loc[idx, "RPD PPOK"] = rpd_ppok_x
                df.loc[idx, "RPD Talasemia"] = rpd_talasemia_x
                df.loc[idx, "RPD Lupus"] = rpd_lupus_x
                df.loc[idx, "RPD Gangguan Pengelihatan"] = rpd_lihat_x
                df.loc[idx, "RPD Katarak"] = rpd_katarak_x
                df.loc[idx, "RPD Gangguan Pendengaran"] = rpd_dengar_x
                df.loc[idx, "RPK Hipertensi"] = rpk_ht_x
                df.loc[idx, "RPK DM"] = rpk_dm_x
                df.loc[idx, "RPK Penyakit Jantung"] = rpk_jtg_x
                df.loc[idx, "RPK Stroke"] = rpk_stroke_x
                df.loc[idx, "RPK Kanker"] = rpk_ca_x
                df.loc[idx, "RPK Talasemia"] = rpk_talasemia_x
                df.loc[idx, "RK Merokok"] = rk_rokok_x
                df.loc[idx, "RK Rokok PerHari"] = rk_rokokperhari_x
                df.loc[idx, "RK Lama Merokok"] = rk_lamamerokok_x
                df.loc[idx, "Pack Years"] = rk_packyear_x
                df.loc[idx, "RK Makan Manis"] = rk_manis_x
                df.loc[idx, "RK Makan Asin"] = rk_asin_x
                df.loc[idx, "RK Makan Berlemak"] = rk_lemak_x
                df.loc[idx, "RK Makan Sayur"] = rk_sayur_x
                df.loc[idx, "RK Olahraga"] = rk_olahraga_x
                df.loc[idx, "RK Konsumsi Alkohol"] = rk_alkohol_x
                df.loc[idx, "TD Sistole"] = tds_x
                df.loc[idx, "TD Diastole"] =tdd_x
                df.loc[idx, "Heart Rate"] = hr_x
                df.loc[idx, "Respiration Rate"] = rr_x
                df.loc[idx, "Suhu Badan"] = temp_x
                df.loc[idx, "Berat Badan"] = bb_x
                df.loc[idx, "Tinggi Badan"] = tb_x
                df.loc[idx, "IMT"] = bmi_x
                df.loc[idx, "Lingkar Perut"] = lp_x
                df.loc[idx, "Lingkar Lengan Atas"] = lla_x
                df.loc[idx, "PHQ1"] = phq1_x
                df.loc[idx, "PHQ2"] = phq2_x
                df.loc[idx, "GAD1"] = gad1_x
                df.loc[idx, "GAD2"] = gad2_x
                df.loc[idx, "Depresi"] = depresi_x
                df.loc[idx, "Cemas"] = cemas_x
                df.loc[idx, "Tes Bisik AD"] = bisikad_x
                df.loc[idx, "Tes Bisik AS"] = bisikas_x
                df.loc[idx, "Otoskopi AD"] = otoskopiad_x
                df.loc[idx, "Otoskopi AS"] = otoskopias_x
                df.loc[idx, "Rinne"] = rinne_x
                df.loc[idx, "Weber"] = weber_x
                df.loc[idx, "Schwabach"] = schwabach_x
                df.loc[idx, "Ca Paru 1"] = caparu1_x
                df.loc[idx, "Ca Paru 2"] = caparu2_x
                df.loc[idx, "Ca Paru 3"] = caparu3_x
                df.loc[idx, "Ca Paru 4"] = caparu4_x
                df.loc[idx, "Ca Paru 5"] = caparu5_x
                df.loc[idx, "Ca Paru 6"] = caparu6_x
                df.loc[idx, "Ca Paru 7"] = caparu7_x
                df.loc[idx, "Ca Paru 8"] = caparu8_x
                df.loc[idx, "Ca Paru 9"] = caparu9_x
                df.loc[idx, "Total Skor Ca Paru"] = caparu_tot_x
                df.loc[idx, "PPOK 1"] = ppok1_x
                df.loc[idx, "PPOK 2"] = ppok2_x
                df.loc[idx, "PPOK 3"] = ppok3_x
                df.loc[idx, "PPOK 4"] = ppok4_x
                df.loc[idx, "PPOK 5"] = ppok5_x
                df.loc[idx, "PPOK 6"] = ppok6_x
                df.loc[idx, "PPOK 7"] = ppok7_x
                df.loc[idx, "Total Skor PPOK"] = ppok_tot_x
                df.loc[idx, "TB 1"] = tb1_x
                df.loc[idx, "TB 2"] = tb2_x
                df.loc[idx, "TB 3"] = tb3_x
                df.loc[idx, "TB 4"] = tb4_x
                df.loc[idx, "TB 5"] = tb5_x
                df.loc[idx, "TB 6"] = tb6_x
                df.loc[idx, "TB 7"] = tb7_x
                df.loc[idx, "Ca Kolorektal 1"] = caco1_x
                df.loc[idx, "Ca Kolorektal 2"] = caco2_x
                df.loc[idx, "Ca Kolorektal 3"] = caco3_x
                df.loc[idx, "Ca Kolorektal 4"] = caco4_x
                df.loc[idx, "Total Skor Ca Kolorektal"] = caco_tot_x
                df.loc[idx, "Rectal Toucher"] = caco5_x
                df.loc[idx, "FOBT"] = caco6_x
                df.loc[idx, "Menarche"] = menarche_x
                df.loc[idx, "HPHT"] = hpht_x
                df.loc[idx, "Usia Pertama Kali Seks"] = seks_pertama_x
                df.loc[idx, "Usia Kehamilan Pertama"] = hamil_pertama_x
                df.loc[idx, "Jumlah Melahirkan"] = jml_melahirkan_x
                df.loc[idx, "Menyusui"] = menyusui_x
                df.loc[idx, "Pil"] = pil_x
                df.loc[idx, "Lama Pil"] = lama_pil_x
                df.loc[idx, "Suntik"] = suntik_x
                df.loc[idx, "Lama Suntik"] = lama_suntik_x
                df.loc[idx, "Implan"] = implan_x
                df.loc[idx, "Lama Implan"] = lama_implan_x
                df.loc[idx, "IUD"] = iud_x
                df.loc[idx, "Lama IUD"] = lama_iud_x
                df.loc[idx, "Riwayat Kanker Keluarga"] = ca_keluarga_x
                df.loc[idx, "Siapa Yang Menderita Kanker"] = keluarga_siapa_x
                df.loc[idx, "Kanker Jenis Apa"] = ca_apa_x
                df.loc[idx, "Riwayat Tumor Jinak Payudara"] = tumorjinak_x
                df.loc[idx, "Menopause"] = menopause_x
                df.loc[idx, "Usia Menopause"] = usia_menopause_x
                df.loc[idx, "Pernah PAP Smear"] = pernah_pap_x
                df.loc[idx, "Kapan PAP Smear"] = kapan_pap_x
                df.loc[idx, "Hasil PAP Smear"] = hasil_pap_x
                df.loc[idx, "Pernah IVA"] = pernah_iva_x
                df.loc[idx, "Kapan IVA"] = kapan_iva_x
                df.loc[idx, "Hasil IVA"] = hasil_iva_x
                df.loc[idx, "Benjolan Di Payudara Dan Ketiak"] = benjolan_payudara_x
                df.loc[idx, "Cairan Dari Puting"] = cairan_puting_x
                df.loc[idx, "Perubahan Pada Payudara"] = perubahan_x
                df.loc[idx, "Jenis Perubahan Payudara"] = jenis_perubahan_x
                df.loc[idx, "Perdarahan Di Luar Haid"] = metroragi_x
                df.loc[idx, "Perdarahan Saat Berhubungan"] = darah_seks_x
                df.loc[idx, "Sering Keputihan"] = keputihan_x
                df.loc[idx, "Nyeri Perut Bawah"] = lap_x
                df.loc[idx, "Sadanis Payudara Kanan"] = sadanisd_x
                df.loc[idx, "Sadanis Payudara Kiri"] = sadaniss_x
                df.loc[idx, "IVA"] = iva_x
                df.loc[idx, "HPV DNA"] = hpv_x
                df.loc[idx, "Hepatitis 1"] = hep1_x
                df.loc[idx, "Hepatitis 2"] = hep2_x
                df.loc[idx, "Hepatitis 3"] = hep3_x
                df.loc[idx, "Hepatitis 4"] = hep4_x
                df.loc[idx, "Hepatitis 5"] = hep5_x
                df.loc[idx, "Hepatitis 6"] = hep6_x
                df.loc[idx, "Hepatitis 7"] = hep7_x
                df.loc[idx, "Hepatitis 8"] = hep8_x
                df.loc[idx, "Hepatitis B"] = hepb_x
                df.loc[idx, "Hepatitis C"] = hepc_x
                df.loc[idx, "Visus OD"] = visusod_x
                df.loc[idx, "Visus OS"] = visusos_x
                df.loc[idx, "Katarak OD"] = katarakod_x
                df.loc[idx, "Katarak OS"] = katarakos_x
                df.loc[idx, "JCS 1"] = jcs1_x
                df.loc[idx, "JCS 2"] = jcs2_x
                df.loc[idx, "JCS 3"] = jcs3_x
                df.loc[idx, "JCS 4"] = jcs4_x
                df.loc[idx, "JCS 5"] = jcs5_x
                df.loc[idx, "JCS 6"] = jcs6_x
                df.loc[idx, "JCS 7"] = jcs7_x
                df.loc[idx, "Total Skor JCS"] = jcs_tot_x
                df.loc[idx, "Interpretasi EKG"] = ekg_x
                df.loc[idx, "Karies"] = karies_x
                df.loc[idx, "Missing"] = missing_x
                df.loc[idx, "Periodontal Pocket"] = pocket_x
                df.loc[idx, "Gigi Goyang"] = goyang_x
                df.loc[idx, "Hb"] = hb_x
                df.loc[idx, "Leukosit"] = wbc_x
                df.loc[idx, "Hematokrit"] = hct_x
                df.loc[idx, "Eritrosit"] = rbc_x
                df.loc[idx, "Trombosit"] = plt_x
                df.loc[idx, "MCV"] = mcv_x
                df.loc[idx, "MCH"] = mch_x
                df.loc[idx, "MCHC"] = mchc_x
                df.loc[idx, "GDS"] = gds_x
                df.loc[idx, "GDP"] = gdp_x
                df.loc[idx, "Kolesterol Total"] = cho_x
                df.loc[idx, "HDL"] = hdl_x
                df.loc[idx, "LDL"] = ldl_x
                df.loc[idx, "Trigliserida"] = tg_x
                df.loc[idx, "Ureum"] = ur_x
                df.loc[idx, "Kreatinin"] = cr_x
                df.loc[idx, "SGOT"] = ot_x
                df.loc[idx, "SGPT"] = pt_x
                df.loc[idx, "Sputum TCM"] = tcm_x
                
            else:
                # Jika nama tidak ditemukan, tambahkan data baru
                df = pd.concat([df, updated_data], ignore_index=True)

            # Update data ke Google Sheets
            conn.update(worksheet='pkg', data=df)
            st.success("Data berhasil disimpan.")
            st.cache_data.clear()
    
elif selected == 'Pemeriksaan Lansia':
    st.title('HALAMAN PEMERIKSAAN LANSIA')
