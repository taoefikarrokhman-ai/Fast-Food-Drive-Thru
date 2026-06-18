import streamlit as st
from gtts import gTTS
from datetime import datetime
import io
import base64

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
# DATA MENU
# =========================
menu_data = {
    "burger": {
        "🍔 Classic Beef": 25000,
        "🧀 Cheese Burger": 28000,
        "🥩 Double Patty": 35000,
        "🌶️ Spicy Chicken": 30000
    },
    "side": {
        "🍟 French Fries": 12000,
        "🧅 Onion Rings": 15000,
        "🍗 Chicken Nuggets": 18000,
        "🧀 Mozzarella Stick": 20000
    },
    "drink": {
        "🥤 Coca Cola": 8000,
        "🥤 Sprite": 8000,
        "🍹 Teh Manis": 7000,
        "🍊 Es Jeruk": 10000,
        "🥑 Jus Alpukat": 15000
    }
}

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
    <p style='font-size:18px;'>
        Pesan makanan favoritmu dengan cepat & mudah 🚗
    </p>
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

    # NAMA PEMESAN
    customer_name = st.text_input(
        "👤 Nama Pemesan",
        placeholder="Masukkan nama pemesan",
        key="customer_name_input"
    )
    
    # BURGER
    burger = st.selectbox(
        "🍔 Pilih Burger",
        [""] + list(menu_data["burger"].keys()),
        key="burger_input"
    )
    burger_qty = st.number_input(
        "Jumlah Burger",
        min_value=1, max_value=20, value=1,
        key="burger_qty"
    )

    # SIDE
    side = st.selectbox(
        "🍟 Pilih Sampingan",
        [""] + list(menu_data["side"].keys()),
        key="side_input"
    )
    side_qty = st.number_input(
        "Jumlah Sampingan",
        min_value=1, max_value=20, value=1,
        key="side_qty"
    )

    # DRINK
    drink = st.selectbox(
        "🥤 Pilih Minuman",
        [""] + list(menu_data["drink"].keys()),
        key="drink_input"
    )
    drink_qty = st.number_input(
        "Jumlah Minuman",
        min_value=1, max_value=20, value=1,
        key="drink_qty"
    )

    # NOTES
    notes = st.text_area(
        "📝 Catatan Tambahan",
        placeholder="Contoh: tanpa bawang, extra saus...",
        key="notes_input"
    )

    # PILIHAN STRUK
    receipt_option = st.radio(
        "🧾 Pengambilan Struk",
        ["Ambil Struk", "Tidak Ambil Struk"],
        horizontal=True,
        key="receipt_input"
    )

    # TAMBAH PESANAN
    if st.button("➕ Tambah ke Keranjang"):
        selected_orders = []
        total = 0

        if burger:
            selected_orders.append(f"{burger} x{burger_qty}")
            total += menu_data["burger"][burger] * burger_qty
        if side:
            selected_orders.append(f"{side} x{side_qty}")
            total += menu_data["side"][side] * side_qty
        if drink:
            selected_orders.append(f"{drink} x{drink_qty}")
            total += menu_data["drink"][drink] * drink_qty

        # VALIDASI
        if len(selected_orders) == 0:
            st.warning("⚠️ Pilih minimal 1 menu!")
        elif customer_name.strip() == "":
            st.warning("⚠️ Masukkan nama pemesan!")
        else:
            st.session_state.orders.extend(selected_orders)
            st.session_state.total += total
            st.session_state.customer_name = customer_name
            st.session_state.receipt_option = receipt_option
            st.session_state.notes = notes
            st.success("✅ Pesanan berhasil ditambahkan!")
            st.rerun()

    # CLEAR CART
    if st.button("🗑️ Kosongkan Keranjang"):
        st.session_state.orders = []
        st.session_state.total = 0
        
        # Reset Form lewat Session State
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

    if len(st.session_state.orders) > 0:
        st.markdown("### 🧾 STRUK PESANAN")
        st.write(f"👤 Nama Pemesan: **{st.session_state.customer_name}**")
        st.write("")

        for i, item in enumerate(st.session_state.orders, start=1):
            st.write(f"**{i}.** {item}")

        if "notes" in st.session_state and st.session_state.notes:
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

        # DOWNLOAD STRUK GENERATOR
        receipt_text = f"""====================================
    DRIVE THRU FAST FOOD
====================================

Nama Pemesan : {st.session_state.customer_name}
Waktu Pesan  : {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}

Daftar Pesanan:
"""
        for i, item in enumerate(st.session_state.orders, start=1):
            receipt_text += f"{i}. {item}\n"

        if "notes" in st.session_state and st.session_state.notes:
            receipt_text += f"\nCatatan: {st.session_state.notes}\n"

        receipt_text += f"""
------------------------------------
TOTAL BAYAR : Rp {st.session_state.total:,}
------------------------------------

Status Struk:
{st.session_state.receipt_option}

Terima kasih telah memesan.
====================================
"""

        st.download_button(
            label="🧾 Download Struk",
            data=receipt_text,
            file_name=f"struk_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )

        # AUDIO KONFIRMASI (gTTS)
        if st.button("📢 Panggil Pesanan"):
            text = f"Halo {st.session_state.customer_name}. Pesanan Anda adalah "
            for item in st.session_state.orders:
                text += f"{item}, "
            
            text += f"dengan total pembayaran {st.session_state.total} rupiah. "

            if st.session_state.receipt_option == "Ambil Struk":
                text += "Silakan ambil struk pesanan Anda. "
            else:
                text += "Anda memilih tidak mengambil struk pesanan. "

            if "notes" in st.session_state and st.session_state.notes:
                text += f"Catatan tambahan: {st.session_state.notes}. "

            text += "Pesanan Anda sudah siap. Terima kasih telah memesan."

            tts = gTTS(text=text, lang='id', slow=False)
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            audio_bytes = fp.read()

            st.session_state.audio = audio_bytes
            st.success("✅ Audio konfirmasi berhasil dibuat!")

        # Menampilkan audio player jika data audio ada di session state
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
