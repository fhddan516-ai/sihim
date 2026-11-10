import json

# ==============================================================================
# TAHAP 1: DATA INGESTION (Simulasi Payload Data Mentah API BMKG/SPKUA)
# ==============================================================================
bmkg_raw_json = """
{
    "station_id": "SPKUA_SABANGAU_01",
    "location": "Kecamatan Sabangau, Kota Palangka Raya",
    "timestamp": "2026-11-10T14:30:00Z",
    "measurements": {
        "pm25_value": 168.5,
        "unit": "µg/m³",
        "category": "Sangat Tidak Sehat"
    },
    "wind_vector": {
        "speed_kmh": 14.2,
        "direction_deg": 180,
        "heading_towards": "Kelurahan Ketinggi & Kalampangan"
    }
}
"""

def process_bmkg_to_whatsapp(raw_json_input):
    # ==========================================================================
    # TAHAP 2: DATA PARSING & EXTRACTION (Ekstraksi Variabel Kunci)
    # ==========================================================================
    data = json.loads(raw_json_input)
    
    pm25 = data["measurements"]["pm25_value"]
    location = data["location"]
    target_area = data["wind_vector"]["heading_towards"]
    
    # ==========================================================================
    # TAHAP 3: DECISION ENGINE (Logika Evaluasi Ambang Batas ISPU / PM2.5)
    # ==========================================================================
    # Ambang batas Baku Mutu PM2.5 (Perpres / Standar ISPU Kemenhut)
    if pm25 <= 55.4:
        status_code = "AMAN"
    elif 55.4 < pm25 <= 150.0:
        status_code = "WASPADA"
    else: # pm25 > 150.0 µg/m³
        status_code = "BAHAYA"

    # Evaluasi Keputusan: Jika status AMAN, hentikan proses (tidak broadcast)
    if status_code == "AMAN":
        return None, "LOG: Kualitas udara aman, tidak ada notifikasi dikirim."

    # ==========================================================================
    # TAHAP 4: MESSAGE GENERATOR (Transformasi Kode Teknis ke Teks WhatsApp)
    # ==========================================================================
    if status_code == "BAHAYA":
        wa_message = (
            f"🚨 *PERINGATAN BAHAYA KARHUTLA (SI-HIMBAU)* 🚨\n\n"
            f"📍 *Lokasi:* {location}\n"
            f"📊 *Kadar PM2.5:* {pm25} µg/m³ ({data['measurements']['category']})\n"
            f"💨 *Arah Sebaran Asap:* Menuju {target_area}\n\n"
            f"⚠️ *INSTRUKSI AKSI MEDIS DARURAT:*\n"
            f"1. *KELOMPOK RENTAN (Balita, Lansia, Penderita ISPA/Asma):*\n"
            f"   Tetap di dalam rumah. Petugas/Relawan SI-HIMBAU sedang bergerak menuju lokasi Anda untuk penjemputan ke Posko Bertekanan Positif.\n\n"
            f"2. *MASYARAKAT KONDISI NORMAL:*\n"
            f"   Gunakan masker N95/KN95 dan batasi aktivitas fisik outdoor. Jadwal MCU berkala tersedia di Posko Kesehatan.\n\n"
            f"📞 *Call Center / Posko Sabangau:* 0812-3456-7890"
        )
    else: # Status WASPADA
        wa_message = (
            f"⚠️ *HIMBAUAN WASPADA ASAP (SI-HIMBAU)* ⚠️\n\n"
            f"📍 *Lokasi:* {location}\n"
            f"📊 *Kadar PM2.5:* {pm25} µg/m³ (Kategori: Tidak Sehat)\n\n"
            f"💡 *INSTRUKSI:* Gunakan masker N95 saat beraktivitas di luar rumah. Segera datangi Posko Kesehatan terdekat untuk pemeriksaan fungsi paru berkala."
        )
        
    return wa_message, f"SUCCESS: Pesan kategori [{status_code}] berhasil dibentuk."

# ==============================================================================
# E K S E K U S I   S I M U L A S I
# ==============================================================================
formatted_message, log_status = process_bmkg_to_whatsapp(bmkg_raw_json)

print(f"[{log_status}]\n")
print("=== HASIL OUTPUT KALIMAT PESAN WHATSAPP ===")
print(formatted_message)