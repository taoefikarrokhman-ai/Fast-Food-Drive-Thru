from gtts import gTTS
from datetime import datetime
import io

# =========================
# DATA MENU
# =========================
MENU_DATA = {
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
# ORDER LOGIC
# =========================
def add_order(burger, burger_qty, side, side_qty, drink, drink_qty,
              customer_name, notes, receipt_option):
    """
    Memvalidasi dan membangun item pesanan beserta total harga.
    Return: (list item pesanan, total harga, pesan error) 
    """
    selected_orders = []
    total = 0

    if not customer_name.strip():
        return [], 0, "⚠️ Masukkan nama pemesan!"

    if burger:
        selected_orders.append(f"{burger} x{burger_qty}")
        total += MENU_DATA["burger"][burger] * burger_qty
    if side:
        selected_orders.append(f"{side} x{side_qty}")
        total += MENU_DATA["side"][side] * side_qty
    if drink:
        selected_orders.append(f"{drink} x{drink_qty}")
        total += MENU_DATA["drink"][drink] * drink_qty

    if not selected_orders:
        return [], 0, "⚠️ Pilih minimal 1 menu!"

    return selected_orders, total, None


def generate_receipt_text(customer_name, orders, total, notes, receipt_option):
    """Membuat teks struk dalam format plain text."""
    receipt = f"""====================================
    DRIVE THRU FAST FOOD
====================================

Nama Pemesan : {customer_name}
Waktu Pesan  : {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}

Daftar Pesanan:
"""
    for i, item in enumerate(orders, start=1):
        receipt += f"{i}. {item}\n"

    if notes:
        receipt += f"\nCatatan: {notes}\n"

    receipt += f"""
------------------------------------
TOTAL BAYAR : Rp {total:,}
------------------------------------

Status Struk:
{receipt_option}

Terima kasih telah memesan.
====================================
"""
    return receipt


def generate_audio(customer_name, orders, total, notes, receipt_option):
    """
    Membuat audio konfirmasi pesanan menggunakan gTTS.
    Return: bytes audio MP3.
    """
    text = f"Halo {customer_name}. Pesanan Anda adalah "
    for item in orders:
        text += f"{item}, "

    text += f"dengan total pembayaran {total} rupiah. "

    if receipt_option == "Ambil Struk":
        text += "Silakan ambil struk pesanan Anda. "
    else:
        text += "Anda memilih tidak mengambil struk pesanan. "

    if notes:
        text += f"Catatan tambahan: {notes}. "

    text += "Pesanan Anda sudah siap. Terima kasih telah memesan."

    tts = gTTS(text=text, lang='id', slow=False)
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp.read()
