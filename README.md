# PREDIKSI KONTEN KOPI KENANGAN DI TIKTOK

Kopi Kenangan, didirikan pada tahun 2017, sukses mempopulerkan kopi susu gula aren di Indonesia.  
Di era digital saat ini, **60,4%** pengguna internet Indonesia mencari informasi brand melalui media sosial  
(*We Are Social & Meltwater, 2024*), dan **TikTok** dengan **1,56 miliar** pengguna aktif bulanan  
(*DataReportal, 2024*) menjadi platform utama dalam strategi pemasaran.

Dengan **memprediksi performa konten TikTok**, brand seperti Kopi Kenangan dapat:
- Menciptakan konten yang lebih tepat sasaran   
- Memperkuat citra brand  
- Menjaga keunggulan kompetitif di industri F&B 

---

## Project Overview

Saya menggunakan **data publik TikTok** yang diambil melalui [Apify](https://apify.com/), dan menjalankan **alur lengkap data science** dari pengumpulan data, preprocessing, eksplorasi data, hingga modeling machine learning.

---

## Alur Project

### 1. Data Collection
- Menggunakan scraper TikTok dari Apify untuk akun [@kopikenangan.id](https://www.tiktok.com/@kopikenangan.id)
- **Dataset 1**: 16 Mei – 22 Juni 2025  
- **Dataset 2**: 22 Juni – 22 Juli 2025  

---

### 2. Cleaning & Preprocessing
- Normalisasi struktur nested (e.g., `authorMeta`, `videoMeta`, `hashtags`)
- Menangani:
  - Missing value  
  - Duplikasi  
  - Outlier  
- Transformasi:
  - Log transform (e.g., views, likes)
  - Encoding kategorikal
  - Feature engineering (engagement rate, waktu, dll)

---

### 3. Exploratory Data Analysis (EDA)
- **Top 5 View Konten**:
  - Berdasarkan jam, hari, username, lokasi (modus, mean, median)
- **Korelasi antar fitur**
- **Top 5 Save Konten**
- **Rasio Like vs View**, distribusi berdasarkan lokasi
- **Prediksi waktu terbaik posting konten** berdasarkan:
  - Hari
  - Jam
  - Lokasi

---

### 4. Modeling
- Model utama: **LightGBM** (Light Gradient Boosting Machine)
- Pipeline terintegrasi preprocessing + model
- Evaluasi menggunakan data validasi dari bulan terakhir

---

### 5. Evaluation
- **RMSLE** (Root Mean Squared Log Error): `0.0966`  
- **R² Score**: `0.8887`  
  > Menunjukkan performa model yang cukup baik dalam memprediksi.

---

## Link Aplikasi Streamlit
🔗 [https://prediksikontenkopikenanganditiktok.streamlit.app/]

---
