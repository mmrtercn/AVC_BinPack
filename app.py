import streamlit as st
from profiles_db import get_profiles, get_profile_names
from fpdf import FPDF
from io import BytesIO
from datetime import datetime

# 📄 Profil isimlerini al
profile_names = get_profile_names()

st.set_page_config(page_title="Profile Bin Packing", layout="centered")

# 🎨 Başlık
header_html = """
<div style="background-color:black; padding:15px; border-radius:10px; text-align:center;">
    <h1 style="color:#FFD700; margin-bottom:5px;">AVC Gemino</h1>
    <h3 style="color:white; margin-top:0px; margin-bottom:5px;">Engineering Department</h3>
    <h5 style="color:gray; margin-top:0px;">by MER</h5>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

# 🧹 Reset Fonksiyonu
def reset_app():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.session_state.step = 1
    st.session_state.max_length = 5880  # Default value
    st.rerun()

# ✅ Session State Başlat
for state_var, default in {
    "step": 1,
    "num_walls": 1,
    "wall_names": [],
    "profile_inputs": {},
    "project_name": "",
    "project_number": "",
    "max_length": 5880  # Add max_length to session state
}.items():
    if state_var not in st.session_state:
        st.session_state[state_var] = default

# 🔄 Sayfa Geçiş Fonksiyonları
def next_step(): 
    st.session_state.step += 1
    st.rerun()

def prev_step():
    if st.session_state.step > 1:
        st.session_state.step -= 1
        st.rerun()

def go_home(): 
    st.session_state.step = 1
    st.rerun()

# 🏠 Ana Kontrol Butonları
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("🏠 Home", use_container_width=True):
        go_home()
with col2:
    if st.button("🔄 Reset/New Project", use_container_width=True):
        reset_app()

# 🧮 Bin Packing Fonksiyonu
def bin_packing(lengths_with_walls):
    sorted_lengths = sorted(lengths_with_walls, key=lambda x: x[0], reverse=True)
    bins = []
    for length, wall in sorted_lengths:
        for bin_ in bins:
            if sum(item[0] for item in bin_) + length <= st.session_state.max_length:
                bin_.append((length, wall))
                break
        else:
            bins.append([(length, wall)])
    return bins

# 📝 PDF Oluşturma Fonksiyonu
def generate_pdf(project_name, project_number, profile_groups, bin_packing_func):
    pdf = FPDF()
    pdf.add_page()

    # 📄 Şirket Bilgisi ve Tarih
    pdf.set_font("Arial", style='B', size=12)
    pdf.set_xy(160, 10)
    pdf.cell(40, 8, "AVC Gemino", ln=True, align='R')
    pdf.set_font("Arial", style='', size=11)
    pdf.set_xy(160, 18)
    pdf.cell(40, 6, "Engineering Department", ln=True, align='R')
    pdf.set_font("Arial", style='I', size=10)
    pdf.set_xy(160, 24)
    pdf.cell(40, 5, "by MER", ln=True, align='R')

    pdf.set_xy(10, 10)
    pdf.set_font("Arial", style='B', size=14)
    pdf.cell(100, 10, f"Project Name: {project_name}", ln=True)
    pdf.cell(100, 10, f"Project Number: {project_number}", ln=True)
    pdf.cell(100, 10, f"Date: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}", ln=True)
    pdf.cell(100, 10, f"Maximum Profile Length: {st.session_state.max_length} mm", ln=True)
    pdf.ln(5)

    # 🔩 Profiller ve Kesim Listeleri
    for profile, lengths_with_walls in profile_groups.items():
        packed_bins = bin_packing_func(lengths_with_walls)
        pdf.set_font("Arial", style='B', size=12)
        pdf.cell(200, 8, f"Profile: {profile} ({len(packed_bins)} pcs)", ln=True)

        for i, bin_ in enumerate(packed_bins, start=1):
            total = sum(length for length, _ in bin_)
            leftover = st.session_state.max_length - total

            pdf.set_font("Arial", style='B', size=11)
            pdf.cell(200, 6, f"Cut Group {i} | Total: {total} mm | Leftover: {leftover} mm", ln=True)
            pdf.set_font("Arial", size=10)
            for length, wall in bin_:
                pdf.cell(200, 5, f"- {length} mm ---> {wall}", ln=True)
            pdf.ln(2)
        pdf.ln(5)

    pdf_bytes = pdf.output(dest='S')
    return BytesIO(pdf_bytes)

# 🏗️ 1️⃣ Proje Bilgileri ve Duvar Sayısı Girişi
if st.session_state.step == 1:
    with st.form("project_form"):
        st.title("🏗️ Project Details")

        st.session_state.project_name = st.text_input("📄 Project Name", value=st.session_state.project_name)
        st.session_state.project_number = st.text_input("🔢 Project Number", value=st.session_state.project_number)
        num_walls_input = st.number_input("🧱 Number of Walls", min_value=1, step=1, value=st.session_state.num_walls)
        max_length_input = st.number_input(
            "📏 Maximum Profile Length (mm)", 
            min_value=1000, 
            max_value=12000, 
            value=st.session_state.max_length,
            step=10,
            help="Enter the maximum length of profiles in millimeters"
        )

        if st.form_submit_button("Next ➡️"):
            st.session_state.num_walls = num_walls_input
            st.session_state.max_length = max_length_input
            st.session_state.wall_names = [f"Wall {i+1}" for i in range(st.session_state.num_walls)]
            next_step()

# 🧱 2️⃣ Duvar Profilleri Girişi
elif 2 <= st.session_state.step <= st.session_state.num_walls + 1:
    wall_index = st.session_state.step - 2
    wall_name = st.session_state.wall_names[wall_index]
    st.title(f"🧱 {wall_name} Profiles")

    if wall_name not in st.session_state.profile_inputs:
        st.session_state.profile_inputs[wall_name] = [{"profile": None, "lengths": ""} for _ in range(5)]

    with st.form(f"profile_form_{wall_name}"):
        for i, profile_data in enumerate(st.session_state.profile_inputs[wall_name]):
            col1, col2 = st.columns([2, 3])
            with col1:
                options = ["Select Profile"] + profile_names
                selected_profile = st.selectbox(
                    f"Profile {i+1}",
                    options=options,
                    index=options.index(profile_data["profile"]) if profile_data["profile"] in options else 0,
                    key=f"profile_select_{wall_name}_{i}"
                )
                profile_data["profile"] = None if selected_profile == "Select Profile" else selected_profile

            with col2:
                profile_data["lengths"] = st.text_input(
                    "Lengths (comma-separated)",
                    value=profile_data["lengths"],
                    key=f"length_input_{wall_name}_{i}"
                )

        col_form1, col_form2 = st.columns([1, 1])
        with col_form1:
            if st.form_submit_button("⬅️ Back"):
                prev_step()
        with col_form2:
            if st.form_submit_button("Next ➡️"):
                next_step()

# 📝 3️⃣ Özet ve Bin Packing Sonuçları
if st.session_state.step == st.session_state.num_walls + 2:
    profile_groups = {}
    for wall, profiles in st.session_state.profile_inputs.items():
        for profile_data in profiles:
            if profile_data["profile"] and profile_data["lengths"]:
                lengths = [int(length.strip()) for length in profile_data["lengths"].split(",") if length.strip().isdigit()]
                profile_groups.setdefault(profile_data["profile"], []).extend([(length, wall) for length in lengths])

    st.title("📝 Summary & Bin Packing Results")

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("📤 Export as PDF"):
            if profile_groups:
                pdf_file = generate_pdf(
                    st.session_state.project_name,
                    st.session_state.project_number,
                    profile_groups,
                    bin_packing
                )
                st.download_button(
                    label="📄 Download PDF",
                    data=pdf_file,
                    file_name=f"{st.session_state.project_name.replace(' ', '_')}_Cut_Lists.pdf",
                    mime="application/pdf"
                )
            else:
                st.warning("⚠️ PDF oluşturmak için profil verisi bulunamadı.")

    with col2:
        if st.button("⬅️ Back"):
            prev_step()

    with col3:
        if st.button("✅ Finish"):
            st.success("✅ İşlem tamamlandı!")

    if not profile_groups:
        st.warning("⚠️ Profil ve uzunluk bilgileri girilmedi.")
    else:
        for profile, lengths_with_walls in profile_groups.items():
            packed_bins = bin_packing(lengths_with_walls)
            st.subheader(f"🔩 Profile: {profile} ({len(packed_bins)} pcs)")

            for i, bin_ in enumerate(packed_bins, start=1):
                total_length = sum(length for length, _ in bin_)
                leftover = st.session_state.max_length - total_length
                cut_list_html = "".join(
                    [f"<li><strong>{length} mm</strong> ---> <span style='color:#007acc;'>{wall}</span></li>" for length, wall in bin_]
                )

                st.markdown(
                    f"""
                    <div style="border: 2px solid #FFD700; border-radius: 10px; padding: 10px; margin-bottom: 15px; background-color:#f9f9f9;">
                        <h5>✂️ Cut Group {i} | <span style="color:green;">Total: {total_length} mm</span> | 
                        <span style="color:orange;">Leftover: {leftover} mm</span></h5>
                        <ul style="list-style-type:square; padding-left:20px;">{cut_list_html}</ul>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
