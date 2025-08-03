import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import cloudpickle
from datetime import datetime
from fpdf import FPDF
import tempfile
import os

st.set_page_config(page_title="Prediksi View TikTok - Konten Kopi Kenangan", layout="wide")
st.title("📊 Prediksi View TikTok - Konten Kopi Kenangan")
uploaded_file = st.file_uploader("📤 Upload file CSV", type=["csv"])

# Mapping hari ke bahasa Indonesia
hari_mapping = {
    'Monday': 'Senin', 'Tuesday': 'Selasa', 'Wednesday': 'Rabu',
    'Thursday': 'Kamis', 'Friday': 'Jumat', 'Saturday': 'Sabtu', 'Sunday': 'Minggu'
}

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        # Ubah waktu
        if 'createTimeISO' in df.columns:
            df['createTimeISO'] = pd.to_datetime(df['createTimeISO'], errors='coerce')
            df['tanggal'] = df['createTimeISO'].dt.date
            df['jam'] = df['createTimeISO'].dt.hour
            df['hari_en'] = df['createTimeISO'].dt.day_name()
            df['hari'] = df['hari_en'].map(hari_mapping)
            df['is_weekend'] = df['createTimeISO'].dt.dayofweek >= 5
            df['is_night'] = df['jam'].between(18, 23) | df['jam'].between(0, 5)
        else:
            st.error("❌ Kolom 'createTimeISO' tidak ditemukan.")
            st.stop()

        # Isi nilai null untuk kolom engagement
        for col in ['diggCount', 'collectCount', 'commentCount', 'shareCount', 'playCount']:
            df[col] = df.get(col, 0).fillna(0)

        df['kota'] = df.get('locationMeta/city', df.get('locationMeta/locationName', 'Tidak Diketahui'))
        df['authorMeta/name'] = df.get('authorMeta/name', 'Tidak Diketahui')
        df['webVideoUrl'] = df.get('webVideoUrl', 'Tidak Tersedia')

        # Fitur tambahan
        df['engagement'] = df['diggCount'] + df['collectCount']
        df['interaksi'] = df['engagement']
        df['engagement_log'] = np.log1p(df['engagement'])
        df['playCount_log'] = np.log1p(df['playCount'])

        st.success("✅ File berhasil dimuat dan diproses!")

        # === Analisis dan tampilan
        top_views = df.nlargest(5, 'playCount')[['authorMeta/name', 'webVideoUrl', 'playCount', 'tanggal', 'hari', 'jam', 'kota']]
        st.subheader("🏆 Top 5 Konten Berdasarkan View")
        st.dataframe(top_views.rename(columns={'authorMeta/name': 'Username', 'webVideoUrl': 'Link Video', 'playCount': 'Jumlah View'}))

        top_interaksi = df.nlargest(5, 'interaksi')[['authorMeta/name', 'webVideoUrl', 'diggCount', 'collectCount', 'interaksi', 'tanggal', 'hari', 'jam', 'kota']]
        st.subheader("Top 5 Konten Berdasarkan Interaksi (Like + Simpan)")
        st.dataframe(top_interaksi.rename(columns={'authorMeta/name': 'Username', 'webVideoUrl': 'Link Video'}))

        st.subheader("📍 Lokasi Terbanyak View dan Interaksi")
        lokasi_stats = df.groupby('kota').agg({
            'playCount': 'sum',
            'diggCount': 'sum',
            'collectCount': 'sum',
            'interaksi': 'sum'
        }).sort_values(by='playCount', ascending=False).head(10)
        st.dataframe(lokasi_stats)

        st.subheader("📊 Korelasi Antar Fitur")
        num_cols = ['playCount', 'diggCount', 'collectCount', 'engagement', 'playCount_log', 'engagement_log']
        corr = df[num_cols].corr()
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
        st.pyplot(fig)

        # Simpan heatmap sebagai gambar untuk PDF
        tmp_heatmap_path = os.path.join(tempfile.gettempdir(), "heatmap.png")
        fig.savefig(tmp_heatmap_path)

        st.subheader("📅 Rekomendasi Waktu & Lokasi Terbaik untuk Konten")
        rekomendasi = df.groupby(['hari', 'jam', 'kota']).agg({'playCount': 'sum', 'interaksi': 'sum'}).reset_index()
        top_rekom = rekomendasi.sort_values(by=['playCount', 'interaksi'], ascending=False).head(10)
        st.dataframe(top_rekom.rename(columns={'playCount': 'Total View', 'interaksi': 'Total Interaksi'}))

        # === Generate PDF
        st.markdown("### 📥 Unduh Laporan PDF")
        if st.button("📄 Buat dan Unduh Laporan"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Laporan Analisis TikTok", ln=True, align="C")

            pdf.ln(10)
            pdf.multi_cell(0, 10, "Top 5 Konten Berdasarkan View:")
            for i, row in top_views.iterrows():
                pdf.multi_cell(0, 8, f"- {row['authorMeta/name']} | {row['playCount']} view | {row['hari']} {row['jam']} WIB")

            pdf.ln(5)
            pdf.multi_cell(0, 10, "Top 5 Interaksi:")
            for i, row in top_interaksi.iterrows():
                pdf.multi_cell(0, 8, f"- {row['authorMeta/name']} | Interaksi: {row['interaksi']} | {row['hari']} {row['jam']} WIB")

            pdf.ln(5)
            pdf.multi_cell(0, 10, "Lokasi dengan View dan Interaksi Tertinggi:")
            for kota, row in lokasi_stats.iterrows():
                pdf.multi_cell(0, 8, f"- {kota}: {int(row['playCount'])} view, {int(row['interaksi'])} interaksi")

            pdf.ln(5)
            pdf.multi_cell(0, 10, "Rekomendasi Waktu & Tempat:")
            for i, row in top_rekom.iterrows():
                pdf.multi_cell(0, 8, f"- {row['hari']} jam {row['jam']} di {row['kota']}: {int(row['playCount'])} view")

            pdf.ln(5)
            pdf.multi_cell(0, 10, "Heatmap Korelasi Fitur:")
            pdf.image(tmp_heatmap_path, x=10, y=pdf.get_y(), w=180)

            # Simpan PDF
            pdf_path = os.path.join(tempfile.gettempdir(), "laporan_tiktok.pdf")
            pdf.output(pdf_path)

            with open(pdf_path, "rb") as f:
                st.download_button(label="⬇️ Unduh PDF Laporan", data=f, file_name="laporan_tiktok.pdf", mime="application/pdf")

    except Exception as e:
        st.error(f"❌ Terjadi kesalahan saat memproses: {e}")
else:
    st.warning("📎 Silakan upload file CSV terlebih dahulu.")