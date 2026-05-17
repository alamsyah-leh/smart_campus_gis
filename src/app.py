import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

# 1. Konfigurasi Halaman (Harus selalu di paling atas)
st.set_page_config(page_title="Smart Campus GIS UNDIP", page_icon="🗺️", layout="wide")

# 2. Judul dan Deskripsi
st.title("🗺️ Smart Campus GIS: Pemetaan Aktivitas Mahasiswa")
st.markdown("Dashboard Sistem Informasi Geografis (SIG) untuk memantau keramaian dan aktivitas mahasiswa di area kampus Universitas Diponegoro, Tembalang.")

# 3. Fungsi Load Data (Menggunakan Cache agar efisien)
@st.cache_data
def load_data():
    # Membaca data CSV dari folder data/
    return pd.read_csv("data/simulasi_aktivitas.csv")

df = load_data()

# 4. Pengaturan Sidebar
st.sidebar.header("⚙️ Filter Peta")
st.sidebar.markdown("Silakan pilih aktivitas mahasiswa yang ingin divisualisasikan pada peta.")

# Filter Aktivitas
pilihan_aktivitas = st.sidebar.multiselect(
    "Jenis Aktivitas:",
    options=df["aktivitas"].unique(),
    default=df["aktivitas"].unique()
)

# Terapkan filter ke dataframe
df_filtered = df[df["aktivitas"].isin(pilihan_aktivitas)]

# 5. Menampilkan Statistik / Metrik Utama
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total Titik Lokasi", value=len(df_filtered))
with col2:
    st.metric(label="Total Estimasi Mahasiswa", value=df_filtered["jumlah_mahasiswa"].sum())
with col3:
    st.metric(label="Kategori Aktivitas Aktif", value=len(pilihan_aktivitas))

st.markdown("---")

# 6. Setup dan Render Peta Folium
# Koordinat tengah Universitas Diponegoro Tembalang
UNDIP_COORDS = [-7.0510, 110.4380]

# Inisialisasi basemap dengan OpenStreetMap
m = folium.Map(location=UNDIP_COORDS, zoom_start=15, tiles="OpenStreetMap")

heat_data = []

# Iterasi baris dataframe untuk memasang marker
for index, row in df_filtered.iterrows():
    # Penentuan warna marker berdasarkan aktivitas
    color_map = {
        "belajar": "blue",
        "makan": "green",
        "nongkrong": "purple",
        "transit": "orange"
    }
    marker_color = color_map.get(row["aktivitas"], "gray")
    
    # Popup berupa teks/HTML kecil ketika marker diklik
    popup_text = f"""
    <div style="font-family: Arial; font-size: 12px;">
        <b>Lokasi:</b> {row['lokasi']}<br>
        <b>Aktivitas:</b> {row['aktivitas'].capitalize()}<br>
        <b>Keramaian:</b> {row['jumlah_mahasiswa']} Mahasiswa
    </div>
    """
    
    # Memasang Marker
    folium.Marker(
        location=[row["lat"], row["lon"]],
        popup=folium.Popup(popup_text, max_width=250),
        tooltip=row["lokasi"], # Teks yang muncul saat mouse hover
        icon=folium.Icon(color=marker_color, icon="info-sign")
    ).add_to(m)
    
    # Memasukkan array [Lat, Lon, Bobot/Jumlah] ke data Heatmap
    heat_data.append([row["lat"], row["lon"], row["jumlah_mahasiswa"]])

# Tambahkan layer Heatmap ke dalam peta
if heat_data:
    HeatMap(heat_data, radius=22, blur=15, max_zoom=1).add_to(m)

# Tampilkan peta di Streamlit
# PENTING: returned_objects=[] memastikan peta statis dan tidak me-rerun aplikasi 
# ketika user sekadar mengklik atau menggeser peta (menghilangkan flicker).
st_folium(m, width=1200, height=600, returned_objects=[])

# 7. Menampilkan Tabel Data sebagai pelengkap Dashboard
st.markdown("### 📊 Detail Data Spasial & Atribut")
st.dataframe(df_filtered, use_container_width=True, hide_index=True)