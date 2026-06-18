# 🍔 Drive Thru Fast Food System

Aplikasi pemesanan makanan drive thru berbasis web menggunakan **Streamlit**, lengkap dengan konfirmasi audio dan download struk.

> Dibuat oleh **Kelompok 7**

---

## 📁 Struktur Proyek

```
drive_thru/
├── app.py          # Frontend — tampilan UI Streamlit
├── backend.py      # Backend — data menu, logika pesanan, struk, audio
├── requirements.txt
└── README.md
```

### Pembagian Tanggung Jawab

| File | Tanggung Jawab |
|------|----------------|
| `app.py` | Tampilan UI, session state, interaksi pengguna |
| `backend.py` | Data menu, validasi pesanan, generate struk & audio |

---

## ✨ Fitur

- 🍔 Pilih menu burger, sampingan, dan minuman
- 🛒 Keranjang pesanan dengan kalkulasi total otomatis
- 📝 Catatan tambahan per pesanan
- 🧾 Download struk dalam format `.txt`
- 📢 Konfirmasi pesanan via audio (Text-to-Speech Bahasa Indonesia)
- 💾 Download audio konfirmasi format `.mp3`

---

## 🚀 Cara Menjalankan

### 1. Install dependensi

```bash
pip install -r requirements.txt
```

### 2. Jalankan aplikasi

```bash
streamlit run app.py
```

Aplikasi akan terbuka di browser pada `http://localhost:8501`.

---

## 📦 requirements.txt

```
streamlit
gtts
```

---

## 🗂️ Penjelasan File

### `backend.py`

Berisi semua logika bisnis aplikasi, terpisah dari tampilan:

- **`MENU_DATA`** — dictionary berisi seluruh item menu dan harga
- **`add_order()`** — memvalidasi input dan menghitung total harga pesanan
- **`generate_receipt_text()`** — membuat teks struk dalam format plain text
- **`generate_audio()`** — membuat audio konfirmasi pesanan menggunakan gTTS

### `app.py`

Berisi tampilan dan alur interaksi pengguna:

- Konfigurasi halaman dan CSS kustom
- Form input (nama, pilihan menu, catatan, opsi struk)
- Memanggil fungsi dari `backend.py` untuk memproses pesanan
- Menampilkan ringkasan pesanan, tombol download struk & audio

---

## 📋 Cara Penggunaan

1. Masukkan **nama pemesan**
2. Pilih **burger**, **sampingan**, dan/atau **minuman** beserta jumlahnya
3. Tambahkan **catatan** jika diperlukan (opsional)
4. Pilih opsi **pengambilan struk**
5. Klik **➕ Tambah ke Keranjang**
6. Lihat ringkasan pesanan di kolom kanan
7. Klik **🧾 Download Struk** untuk menyimpan struk
8. Klik **📢 Panggil Pesanan** untuk memutar konfirmasi audio
9. Klik **🗑️ Kosongkan Keranjang** untuk mereset semua pesanan
