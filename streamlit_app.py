import streamlit as st
import pandas as pd

# =============================
# PAGE CONFIG (WAJIB PALING ATAS)
# =============================
st.set_page_config(
    page_title="Kalkulator SPNL - Regula Falsi",
    layout="centered"
)

# =============================
# SESSION STATE
# =============================
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# =============================
# SIDEBAR (RESMI)
# =============================
with st.sidebar:
    st.header("⚙️ Pengaturan")
    st.session_state.dark_mode = st.toggle(
        "🌙 Dark Mode",
        value=st.session_state.dark_mode
    )

# =============================
# TEMA WARNA (LOGIC, BUKAN HACK)
# =============================
if st.session_state.dark_mode:
    BG_COLOR = "#0f172a"
    TEXT_COLOR = "#e5e7eb"
    INPUT_COLOR = "#334155"
else:
    BG_COLOR = "#f4f7f9"
    TEXT_COLOR = "#1f2937"
    INPUT_COLOR = "#f1f3f5"

# =============================
# CSS MINIMAL & AMAN
# =============================
st.markdown(
    f"""
    <style>
        .stApp {{
            background-color: {BG_COLOR};
            color: {TEXT_COLOR};
        }}

        input {{
            background-color: {INPUT_COLOR};
            color: {TEXT_COLOR};
            border-radius: 10px;
        }}

        button {{
            border-radius: 10px;
            padding: 0.5rem 1.2rem;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# =============================
# JUDUL
# =============================
st.markdown(
    f"""
    <h1 style="text-align:center; color:{TEXT_COLOR}; font-family:Georgia;">
        Kalkulator SPNL – Metode Regula Falsi
    </h1>
    """,
    unsafe_allow_html=True
)

# =============================
# INPUT (TANPA KOMPONEN KOSONG)
# =============================
st.subheader("Step 1: Masukkan Persamaan f(x)")
fungsi = st.text_input(
    "Persamaan",
    placeholder="Contoh: x**3 - x - 2"
)

st.subheader("Step 2: Interval Awal")
a = st.number_input("Nilai a", value=1.0)
b = st.number_input("Nilai b", value=2.0)

st.subheader("Step 3: Parameter Iterasi")
tol = st.number_input("Toleransi Error", value=0.0001)
max_iter = st.number_input("Maksimum Iterasi", value=20, step=1)

# =============================
# FUNGSI REGULA FALSI
# =============================
def regula_falsi(f, a, b, tol, max_iter):
    hasil = []
    fa, fb = f(a), f(b)

    if fa * fb > 0:
        return None

    for i in range(1, max_iter + 1):
        c = b - fb * (b - a) / (fb - fa)
        fc = f(c)

        hasil.append([i, a, b, c, fc])

        if abs(fc) < tol:
            break

        if fa * fc < 0:
            b, fb = c, fc
        else:
            a, fa = c, fc

    return hasil

# =============================
# PROSES
# =============================
if st.button("Hitung Akar"):
    if not fungsi.strip():
        st.warning("Masukkan persamaan terlebih dahulu.")
    else:
        try:
            f = lambda x: eval(fungsi)
            data = regula_falsi(f, a, b, tol, int(max_iter))

            if data is None:
                st.error("f(a) dan f(b) harus berlainan tanda.")
            else:
                df = pd.DataFrame(
                    data,
                    columns=["Iterasi", "a", "b", "c", "f(c)"]
                )
                st.success(f"Akar ≈ {df.iloc[-1]['c']}")
                st.dataframe(df, use_container_width=True)

        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")
