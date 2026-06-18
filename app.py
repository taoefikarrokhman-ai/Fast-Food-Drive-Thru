import streamlit as st
import base64
from datetime import datetime
from backend import MENU_DATA, add_order, generate_receipt_text, generate_audio

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Drive Thru Fast Food",
    page_icon="🍔",
    layout="wide"
)

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>
.main {
    background-color: #fff8f0;
}
h1, h2, h3 {
    color: #ff4b2b;
}
.stButton>button {
    width: 100%;
    border-radius: 12px;
    border: none;
    background: linear-gradient(90deg, #ff4b2b, #ff416c);
    color: white;
    font-weight: bold;
    padding: 12px;
    transition: 0.3s;
}
.stButton>button:hover {
    transform: scale(1.03);
    background: linear-gradient(90deg, #ff416c, #ff4b2b);
}
.card {
    background-color: white;
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}
.total-box {
    background: linear-gradient(90deg, #ff4b2b, #ff416c);
    padding: 20px;
    border-radius: 15px;
    color: white;
    text-align: center;
    font-size: 24px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# =========================
# SESSION STATE INITIALIZATION
# =========================
if "orders" not in st.session_state:
    st.session_state.orders = []
if "total" not in st.session_state:
    st.session_state.total = 0

# =========================
# HEADER
# =========================
st.markdown("""
<div style='text-align:center; padding:20px;'>
    <h1>🍔 DRIVE THRU FAST FOOD 🍟</h1>
    <p style='font-size:18px;'>Pesan makanan favoritmu dengan cepat & mudah 🚗</p>
</div>
""", unsafe_allow_html=True)

# =========================
# LAYOUT
# =========================
col1, col2 = st.columns([1, 1])

# =========================
# KOLOM KIRI (INPUT)
# =========================
with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📝 Buat Pesanan")

    customer_name = st.text_input(
        "👤 Nama Pemesan",
        placeholder="Masukkan nama pemesan",
        key="customer_name_input"
    )

    burger = st.selectbox(
        "🍔 Pilih Burger",
        [""] + list(MENU_DATA["burger"].keys()),
        key="burger_input"
    )
    burger_qty = st.number_input(
        "Jumlah Burger", min_value=1, max_value=20, value=1, key="burger_qty"
    )

    side = st.selectbox(
        "🍟 Pilih Sampingan",
        [""] + list(MENU_DATA["side"].keys()),
        key="side_input"
    )
    side_qty = st.number_input(
        "Jumlah Sampingan", min_value=1, max_value=20, value=1, key="side_qty"
    )

    drink = st.selectbox(
        "🥤 Pilih Minuman",
        [""] + list(MENU_DATA["drink"].keys()),
        key="drink_input"
    )
    drink_qty = st.number_input(
        "Jumlah Minuman", min_value=1, max_value=20, value=1, key="drink_qty"
    )

    notes = st.text_area(
        "📝 Catatan Tambahan",
        placeholder="Contoh: tanpa bawang, extra saus...",
        key="notes_input"
    )

    receipt_option = st.radio(
        "🧾 Pengambilan Struk",
        ["Ambil Struk", "Tidak Ambil Struk"],
        horizontal=True,
        key="receipt_input"
    )

    # TAMBAH PESANAN
    if st.button("➕ Tambah ke Keranjang"):
        new_orders, new_total, error = add_order(
            burger, burger_qty, side, side_qty, drink, drink_qty,
            customer_name, notes, receipt_option
        )
        if error:
            st.warning(error)
        else:
            st.session_state.orders.extend(new_orders)
            st.session_state.total += new_total
            st.session_state.customer_name = customer_name
            st.session_state.receipt_option = receipt_option
            st.session_state.notes = notes
            st.success("✅ Pesanan berhasil ditambahkan!")
            st.rerun()

    # CLEAR CART
    if st.button("🗑️ Kosongkan Keranjang"):
        st.session_state.orders = []
        st.session_state.total = 0
        st.session_state.customer_name_input = ""
        st.session_state.burger_input = ""
        st.session_state.side_input = ""
        st.session_state.drink_input = ""
        st.session_state.notes_input = ""
        st.session_state.receipt_input = "Ambil Struk"
        if "audio" in st.session_state:
            del st.session_state.audio
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# KOLOM KANAN (RINGKASAN & OUTPUT)
# =========================
with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📦 Ringkasan Pesanan")

    if st.session_state.orders:
        st.markdown("### 🧾 STRUK PESANAN")
        st.write(f"👤 Nama Pemesan: **{st.session_state.customer_name}**")
        st.write("")

        for i, item in enumerate(st.session_state.orders, start=1):
            st.write(f"**{i}.** {item}")

        if st.session_state.get("notes"):
            st.info(f"📝 Catatan: {st.session_state.notes}")

        st.write("---")
        st.markdown(
            f"""
            <div class='total-box'>
                💰 Total Bayar <br>
                Rp {st.session_state.total:,}
            </div>
            """,
            unsafe_allow_html=True
        )
        st.write("")

        # DOWNLOAD STRUK
        receipt_text = generate_receipt_text(
            st.session_state.customer_name,
            st.session_state.orders,
            st.session_state.total,
            st.session_state.get("notes", ""),
            st.session_state.get("receipt_option", "Ambil Struk")
        )
        st.download_button(
            label="🧾 Download Struk",
            data=receipt_text,
            file_name=f"struk_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )

        # AUDIO KONFIRMASI
        if st.button("📢 Panggil Pesanan"):
            audio_bytes = generate_audio(
                st.session_state.customer_name,
                st.session_state.orders,
                st.session_state.total,
                st.session_state.get("notes", ""),
                st.session_state.get("receipt_option", "Ambil Struk")
            )
            st.session_state.audio = audio_bytes
            st.success("✅ Audio konfirmasi berhasil dibuat!")

        if "audio" in st.session_state:
            audio_base64 = base64.b64encode(st.session_state.audio).decode()
            audio_html = f"""
                <audio autoplay controls style="width: 100%; margin-top: 10px;">
                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                </audio>
            """
            st.markdown(audio_html, unsafe_allow_html=True)

            st.download_button(
                label="💾 Download MP3",
                data=st.session_state.audio,
                file_name=f"pesanan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3",
                mime="audio/mp3"
            )
    else:
        st.info("🛒 Belum ada pesanan.")

    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# FOOTER
# =========================
st.markdown("""
<hr>
<div style='text-align:center;'>
    <p>🍔 Fast Food Drive Thru System | Kelompok 7 🚀</p>
</div>
""", unsafe_allow_html=True)
