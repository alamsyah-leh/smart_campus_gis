# 🗺️ Smart Campus GIS UNDIP

Dashboard Sistem Informasi Geografis (SIG) berbasis Python (Streamlit & Folium) untuk memetakan dan memvisualisasikan estimasi keramaian aktivitas mahasiswa di area kampus Universitas Diponegoro, Tembalang.

## ⚙️ Business Process (Alur Sistem)

1. **Tahap Input (Akuisisi Data):**
   Sistem mengumpulkan data spasial (koordinat latitude/longitude WGS 84) dan data atribut (jumlah mahasiswa, jenis aktivitas) yang disatukan ke dalam basis data lokal berformat CSV.
2. **Tahap Process (Pengolahan Geospasial):**
   Data CSV diproses menggunakan library `pandas`. Sistem melakukan geocoding dan interpolasi spasial menggunakan algoritma **Kernel Density Estimation (KDE)** untuk menghasilkan layer *Heatmap* keramaian di atas *basemap* OpenStreetMap.
3. **Tahap Output (Visualisasi):**
   Hasil olahan dirender secara dinamis menggunakan `streamlit-folium` menjadi dashboard antarmuka HTML interaktif tanpa *flickering*, lengkap dengan fitur *filtering* aktivitas dan metrik statistik.

## ❓ Frequently Asked Questions (FAQ)

**Q: Mengapa data jumlah mahasiswa di peta ini (misal: 585 mahasiswa) bersifat tetap/statis?**
A: Saat ini, aplikasi berada pada fase prototipe (*Proof of Concept*). Data statis ini merupakan representasi *cross-sectional* (snapshot pada satu waktu tertentu) menggunakan dataset simulasi. Secara arsitektur, sistem ini dirancang *scalable* dan siap diintegrasikan dengan API dinamis (seperti data traffic Wi-Fi kampus atau sensor CCTV) untuk pembaruan data secara *real-time* di masa mendatang.

## 🚀 Cara Menjalankan Project (Local)
1. Clone repositori ini: `git clone <URL_REPO_ANDA>`
2. Instal dependencies: `pip install -r requirements.txt`
3. Jalankan aplikasi: `python -m streamlit run src/app.py`