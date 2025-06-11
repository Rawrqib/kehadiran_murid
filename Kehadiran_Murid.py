import streamlit as st
import pandas as pd
from datetime import date
from io import BytesIO
from fpdf import FPDF

# Simulasi login mudah
USER_CREDENTIALS = {
    "aisyah": "1234",
    "faizal": "abcd",
    "salmah": "guru25"
}

# Simpan rekod kehadiran dalam session_state
if "rekod_kehadiran" not in st.session_state:
    st.session_state.rekod_kehadiran = []

if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# Fungsi PDF
def generate_pdf(dataframe):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Laporan Kehadiran Murid", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", size=10)
    for i, row in dataframe.iterrows():
        pdf.cell(0, 8, f"{row['Tarikh']} | {row['Hari']} | Guru: {row['Guru Pertama']} | Hadir: {row['Jumlah Hadir']} | Tidak Hadir: {row['Tidak Hadir']}", ln=True)
    
    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer

# Fungsi log masuk
def login():
    st.title("🔐 Sistem Kehadiran Murid - Log Masuk")
    username = st.text_input("Nama Pengguna")
    password = st.text_input("Kata Laluan", type="password")
    if st.button("Log Masuk"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state.is_logged_in = True
            st.session_state.username = username
            st.success("Log masuk berjaya!")
        else:
            st.error("Nama pengguna atau kata laluan salah.")

# Halaman utama selepas log masuk
def main():
    st.title("📋 Sistem Kehadiran Murid")

    # Senarai murid
    murid_list = [
        "Ahmad Zaki", "Nurul Izzati", "Muhammad Danish", "Aisyah Humaira",
        "Hafiz Rahman", "Siti Sarah", "Ali Imran", "Farah Nabila",
        "Zulkifli Amir", "Haslina Mahmud"
    ]

    with st.form("borang_kehadiran"):
        tarikh = st.date_input("Tarikh", value=date.today())
        hari = st.selectbox("Hari", ["Isnin", "Selasa", "Rabu", "Khamis", "Jumaat", "Sabtu", "Ahad"])
        guru_pertama = st.text_input("Nama Guru Mata Pelajaran Pertama", value=st.session_state.username.title())

        murid_tidak_hadir = st.multiselect("Pilih Nama Murid Tidak Hadir", murid_list)
        jumlah_hadir = len(murid_list) - len(murid_tidak_hadir)

        submitted = st.form_submit_button("Simpan Kehadiran")

        if submitted:
            rekod = {
                "Tarikh": tarikh.strftime("%d/%m/%Y"),
                "Hari": hari,
                "Guru Pertama": guru_pertama,
                "Jumlah Hadir": jumlah_hadir,
                "Tidak Hadir": ", ".join(murid_tidak_hadir) if murid_tidak_hadir else "-"
            }
            st.session_state.rekod_kehadiran.append(rekod)
            st.success("✅ Rekod kehadiran disimpan!")

    # Paparkan rekod
    if st.session_state.rekod_kehadiran:
        st.subheader("📅 Rekod Kehadiran")
        df = pd.DataFrame(st.session_state.rekod_kehadiran)
        st.dataframe(df, use_container_width=True)

        # Muat turun CSV
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Muat Turun CSV", data=csv, file_name="rekod_kehadiran.csv", mime='text/csv')

        # Muat turun PDF
        pdf_buffer = generate_pdf(df)
        st.download_button("⬇️ Muat Turun PDF", data=pdf_buffer, file_name="laporan_kehadiran.pdf", mime='application/pdf')

# Jalankan log masuk atau aplikasi utama
if not st.session_state.is_logged_in:
    login()
else:
    main()
