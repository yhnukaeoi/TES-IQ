import streamlit as st
import pandas as pd
from fpdf import FPDF
import base64

# Load data dari CSV
data = pd.read_csv('Datatesiq.csv')

# Mengganti spasi di nama kolom dengan underscore untuk memudahkan akses
data.columns = data.columns.str.replace(' ', '_')

# Fungsi untuk mendapatkan informasi IQ
def get_iq_info(skor_mentah):
    entry = data[data['Skor_Mentah'] == skor_mentah]
    if not entry.empty:
        return entry['Nilai_IQ'].values[0], entry['Keterangan'].values[0]
    return None, None  # Jika skor mentah tidak ditemukan

# Fungsi untuk membuat PDF dengan desain sertifikat
def create_certificate(name, iq_score, description):
    pdf = FPDF(orientation='P', unit='mm', format='A4')  # Mengatur orientasi potret
    pdf.add_page()
    
    # Menambahkan gambar latar belakang sertifikat
    pdf.image('sertifikat IQ.jpg', 0, 0, 210, 297)  # Ganti dengan path ke gambar yang dimiliki
    
    # Menambahkan teks ke sertifikat
    
  # Posisi untuk nama
    pdf.set_xy(0, 135)  # Tepat di bawah teks sebelumnya
    pdf.set_font("Helvetica", size= 28, style='B')  # Font besar dan bold
    pdf.set_text_color(0, 102, 204)  # Warna teks biru gelap 
    pdf.cell(210, 10, f"{name}", ln=True, align='C')
    
    # Posisi untuk nilai IQ
    pdf.set_xy(0, 200)
    pdf.set_font("Arial", size=18)
    pdf.cell(210, 10, f"Nilai IQ: {iq_score}", ln=True, align='C')
    
    # Posisi untuk keterangan
    pdf.set_xy(0, 210)
    pdf.set_font("Arial", size=16, style='I')
    pdf.cell(210, 10, f"Keterangan: {description}", ln=True, align='C')
    
    # Menyimpan PDF ke file sementara
    pdf_file = "sertifikat.pdf"
    pdf.output(pdf_file)
    
    return pdf_file

# Fungsi untuk membuat tautan unduh
def create_download_link(file_path):
    with open(file_path, "rb") as f:
        pdf_data = f.read()
    b64 = base64.b64encode(pdf_data).decode()
    return f'<a href="data:application/octet-stream;base64,{b64}" download="{file_path}">Download Sertifikat</a>'

# Halaman Streamlit
st.title("Tes IQ")
st.write("Masukkan nama dan skor mentah Anda untuk mendapatkan nilai IQ dan keterangan.")
st.write("Skor mentah harus dalam rentang 38-63")

# Input nama dari pengguna
nama_input = st.text_input("Nama", placeholder="Masukkan nama Anda")

# Input skor mentah dari pengguna
skor_mentah_input = st.text_input("Skor Mentah", placeholder="Masukkan skor mentah Anda")

# Tombol untuk submit
if st.button("Dapatkan Sertifikat"):
    if nama_input:  # Memastikan nama tidak kosong
        if skor_mentah_input:  # Memastikan input tidak kosong
            try:
                skor_mentah = float(skor_mentah_input)  # Mengonversi input ke float
                nilai_iq, keterangan = get_iq_info(skor_mentah)
                if nilai_iq is not None:
                    st.success(f"Nama: {nama_input}\nNilai IQ: {nilai_iq}\nKeterangan: {keterangan}")
                    
                    # Membuat sertifikat
                    pdf_file_path = create_certificate(nama_input, nilai_iq, keterangan)
                    download_link = create_download_link(pdf_file_path)
                    st.markdown(download_link, unsafe_allow_html=True)
                else:
                    st.error("Skor mentah tidak ditemukan. Silakan masukkan skor yang valid.")
            except ValueError:
                st.error("Silakan masukkan skor yang valid (angka).")
        else:
            st.warning("Masukkan skor mentah Anda terlebih dahulu.")