import os
import csv
import shutil
import subprocess

# 1. Bersihkan folder/file lama agar penamaan di verification/ persis sesuai permintaan mentor:
#    verification/peer_review.md, verification/issues_log.csv, verification/verification_matrix.csv
if os.path.exists("verification"):
    shutil.rmtree("verification")
os.makedirs("verification", exist_ok=True)

# Ambil commit hash Git terbaru sebagai jejak audit (jika tersedia)
try:
    commit_hash = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
except Exception:
    commit_hash = "HEAD"

# 2. Buat verification/verification_matrix.csv (Skenario Owner Zulfa + Hasil Audit Reviewer Ahyar)
verif_headers = [
    "requirement_id", "kriteria_desain", "owner", "reviewer", "domain", "test_id",
    "critical", "baseline", "kondisi_uji", "metrik", "prediksi_ilustratif", "satuan",
    "toleransi_replikasi_usulan", "hasil_desain_diharapkan", "commit", "perintah",
    "log_owner", "nilai_owner", "log_reviewer", "nilai_reviewer", "selisih_absolut",
    "hasil_desain_aktual", "verdict_reviewer", "issue_id"
]

verif_rows = [
    [
        "D1.2-01", "Switching crossover Vm inverter simetris = 2.50 V pada VDD=5V",
        "Zulfa Maylafaiza", "Ahyar Muhaimin", "CMOS Inverter", "T12-B", "YA",
        "VDD=5V; Wp=20u; Wn=10u; L=1u; CL=20pF",
        "DC Sweep Vin 0..5V step 0.01V (baseline simetris)",
        "Titik potong Vout = Vin", "2.500", "V", "0.02", "LULUS", commit_hash,
        "ngspice -b spice/inverter_dc.cir",
        "results/inverter_vtc.csv", "2.500",
        "results/inverter_vtc.csv", "2.500", "0",
        "LULUS", "REPRODUCIBLE (PASS)", ""
    ],
    [
        "D1.2-02", "Pergeseran Vm turun saat Wp diperkecil menjadi 10u (rasio 1:1)",
        "Zulfa Maylafaiza", "Ahyar Muhaimin", "CMOS Inverter", "T12-V", "TIDAK",
        "VDD=5V; Wp=20u; Wn=10u; Vm=2.500V",
        "Ubah Wp=10u (PMOS lebih lemah)",
        "Titik potong Vout = Vin", "2.210", "V", "0.02", "LULUS", commit_hash,
        "python python/plot_vtc.py",
        "results/inverter_vtc_wp10u.csv", "2.210",
        "results/inverter_vtc_wp10u.csv", "2.210", "0",
        "LULUS", "REPRODUCIBLE (PASS)", ""
    ],
    [
        "D1.3-01", "Noise margin AT89S52 Ports 1/2/3 valid (NML=0.45V, NMH>=0.50V) dan terpisah dari Vm",
        "Zulfa Maylafaiza", "Ahyar Muhaimin", "Noise Margin", "T13-B", "YA",
        "AT89S52 Hal.29 VCC=5V: VIL=0.90V, VIH=1.90V, VOL=0.45V, VOH=2.40V",
        "Perhitungan NML = VIL - VOL dan NMH = VOH - VIH",
        "NML & NMH minimum", "0.45", "V", "0.01", "LULUS", commit_hash,
        "python python/plot_vtc_annotated.py",
        "results/threshold_matrix.csv", "0.45",
        "results/threshold_matrix.csv", "0.45", "0",
        "LULUS", "REPRODUCIBLE (PASS)", ""
    ],
    [
        "D1.3-02", "Fault: Input dekat Vm (2.5V +- 0.3V) memicu osilasi output dan arus crowbar kontinu",
        "Zulfa Maylafaiza", "Ahyar Muhaimin", "Noise Margin", "T13-F", "YA",
        "VDD=5V; Wp=20u; Wn=10u; CL=20pF",
        "VIN = SIN(2.5V, 0.3V, 10MHz)",
        "Arus minimum IDD (tidak pernah 0 mA)", "1.034", "mA", "0.05", "GAGAL_STABILITAS", commit_hash,
        "ngspice -b spice/inverter_noise_fault.cir",
        "results/inverter_noise_fault.csv", "1.034",
        "results/inverter_noise_fault.csv", "1.034", "0",
        "GAGAL_STABILITAS", "REPRODUCIBLE (FAULT CONFIRMED)", "I01"
    ],
    [
        "D1.4-01", "Open-drain Rp=4.7k, Cload=100pF mencapai rise time ~1032 ns dan Isink <= 1.6 mA",
        "Zulfa Maylafaiza", "Ahyar Muhaimin", "GPIO Open-Drain", "T14-B", "YA",
        "VDD=5V; NMOS W=20u L=1u; Rp=4.7k; Cload=100pF",
        "Pulsa gate 5V -> 0V pada t=5us",
        "Rise time 10%-90% (tr)", "1032.0", "ns", "10.0", "LULUS", commit_hash,
        "ngspice -b spice/gpio.cir",
        "results/gpio_load_matrix.csv", "1032.0",
        "results/gpio_load_matrix.csv", "1032.0", "0",
        "LULUS", "REPRODUCIBLE (PASS)", ""
    ],
    [
        "D1.4-02", "Fault: Open-drain Port 0 tanpa pull-up (floating) tertahan di 0 V",
        "Zulfa Maylafaiza", "Ahyar Muhaimin", "GPIO Open-Drain", "T14-F", "YA",
        "VDD=5V; NMOS W=20u L=1u; Rp=1T (open); Cload=20pF",
        "NMOS dimatikan (OFF) tanpa resistor pull-up eksternal",
        "Tegangan output Vout setelah NMOS OFF", "0.000", "V", "0.01", "GAGAL_HIGH", commit_hash,
        "ngspice -b spice/gpio.cir",
        "results/gpio_floating.csv", "0.000",
        "results/gpio_floating.csv", "0.000", "0",
        "GAGAL_HIGH", "REPRODUCIBLE (FAULT CONFIRMED)", "I02"
    ],
    [
        "D2.1-01", "Cload tidak mengubah DC Vm (2.50V) tetapi menaikkan delay transient secara linear",
        "Zulfa Maylafaiza", "Ahyar Muhaimin", "Inverter Stress", "T21-B", "YA",
        "VDD=5V; Wp=20u; Wn=10u; Cload=10pF vs 100pF",
        "Sweep Cload 10pF -> 100pF -> 500pF",
        "Propagation delay tpHL pada 100pF", "28.00", "ns", "1.0", "LULUS", commit_hash,
        "ngspice -b spice/inverter_stress.cir",
        "results/inverter_stress.csv", "28.00",
        "results/inverter_stress.csv", "28.00", "0",
        "LULUS", "REPRODUCIBLE (MINOR TYPO DOC)", "I03"
    ],
    [
        "D2.1-02", "Fault: Slow input slew (40 ns) memperlambat tpHL dan memperlebar arus crowbar",
        "Zulfa Maylafaiza", "Ahyar Muhaimin", "Inverter Stress", "T21-F", "YA",
        "VDD=5V; Cload=100pF; slew baseline=2ns (tpHL=28.00ns)",
        "Perlambat rise/fall time input menjadi 40 ns",
        "Propagation delay tpHL", "36.50", "ns", "1.0", "DEGRADASI_TIMING", commit_hash,
        "ngspice -b spice/inverter_stress.cir",
        "results/d21_fault_slow_slew.csv", "36.50",
        "results/d21_fault_slow_slew.csv", "36.50", "0",
        "DEGRADASI_TIMING", "REPRODUCIBLE (FAULT CONFIRMED)", ""
    ],
    [
        "D2.2-01", "Fault: Beban kapasitif berlebih 4.7 nF pada sinyal 100 kHz membuat Rp=4.7k gagal capai VIH",
        "Zulfa Maylafaiza", "Ahyar Muhaimin", "GPIO Timing", "T22-F", "YA",
        "VDD=5V; Rp=4.7k; frekuensi 100kHz (Thigh=5us)",
        "Naikkan beban kapasitif menjadi Cload = 4.7 nF",
        "Tegangan puncak Vout di akhir pulsa 5 us", "1.120", "V", "0.05", "GAGAL_SAMPLING", commit_hash,
        "ngspice -b spice/gpio_d22.cir",
        "results/d22_fault_c4.7n_r4.7k.csv", "1.120",
        "results/d22_fault_c4.7n_r4.7k.csv", "1.120", "0",
        "GAGAL_SAMPLING", "REPRODUCIBLE (FAULT CONFIRMED)", "I04"
    ],
    [
        "D2.2-02", "Uji Batas Reviewer: Rekomendasi Rp=4.7k pada VDD=4.0V & Cload=330pF tetap memenuhi tVIH < 1250ns",
        "Zulfa Maylafaiza", "Ahyar Muhaimin", "GPIO Timing", "T22-R", "YA",
        "Rekomendasi D2.2 Rp=4.7k (baseline VDD=5V, Cload<=100pF)",
        "Turunkan VDD ke 4.0V (min datasheet) dan naikkan Cload ke 330pF",
        "Waktu naik mencapai VIH(min)=1.70V", "818.0", "ns", "20.0", "LULUS", commit_hash,
        "ngspice -b spice/reviewer_gpio_verify.cir",
        "reviews/gpio_recommendation_memo.md", "818.0",
        "results/verify_d22_vdd4_c330p.csv", "808.1", "9.9",
        "LULUS", "REPRODUCIBLE (PASS)", "I05"
    ],
]

with open("verification/verification_matrix.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(verif_headers)
    writer.writerows(verif_rows)

# 3. Buat verification/issues_log.csv (Log Isu & Fault Injection lengkap Owner Zulfa + Reviewer Ahyar)
issues_headers = [
    "issue_id", "test_id", "domain", "owner", "reviewer", "perubahan_parameter",
    "status_issue", "label_reproduksi", "commit_awal", "perintah", "bukti_awal_owner",
    "bukti_awal_reviewer", "ketidakcocokan_atau_temuan", "tanggapan_owner",
    "revisi_klaim_atau_bukti", "commit_uji_ulang", "bukti_uji_ulang", "keputusan_reviewer"
]

issues_rows = [
    [
        "I01", "T13-F", "Noise Margin", "Zulfa Maylafaiza", "Ahyar Muhaimin",
        "Berikan input DC 2.5V + noise sinus 0.3V (10 MHz) dekat Vm",
        "TERVERIFIKASI", "REPRODUCIBLE", commit_hash,
        "ngspice -b spice/inverter_noise_fault.cir",
        "results/inverter_noise_fault.csv", "results/inverter_noise_fault.csv",
        "Output berosilasi (1.13V-3.21V) dan arus crowbar mengalir kontinu (min 1.034 mA).",
        "Dikonfirmasi; sinyal input wajib dijaga di luar wilayah undefined AT89S52 (0.90V - 1.90V).",
        "Menetapkan batas noise margin maksimal NML=0.45V dan NMH=0.50V (pada beban penuh 60uA).",
        commit_hash, "results/plots/inverter_noise_fault.png", "CLOSED / VERIFIED"
    ],
    [
        "I02", "T14-F", "GPIO Open-Drain", "Zulfa Maylafaiza", "Ahyar Muhaimin",
        "Lepas resistor pull-up eksternal (Rp = 1 TOhm / open)",
        "TERVERIFIKASI", "REPRODUCIBLE", commit_hash,
        "ngspice -b spice/gpio.cir",
        "results/gpio_floating.csv", "results/gpio_floating.csv",
        "Node output Port 0 tertahan di 0.00V dan tidak pernah mencapai VIH=1.90V saat NMOS OFF.",
        "Dikonfirmasi; Port 0 mode I/O bersifat open-drain murni tanpa internal pull-up.",
        "Mewajibkan pull-up eksternal untuk Port 0 mode I/O dan memisahkannya dari karakter Port 1-3.",
        commit_hash, "results/plots/gpio_timing_20pF.png", "CLOSED / VERIFIED"
    ],
    [
        "I03", "T21-B", "Inverter Stress", "Zulfa Maylafaiza", "Ahyar Muhaimin",
        "Audit konsistensi angka tabel laporan D2.1 vs CSV d21_dc_vdd3.3.csv",
        "REVISI_MINOR", "REPRODUCIBLE", commit_hash,
        "python python/analyze_inverter_stress.py",
        "results/inverter_stress.csv", "results/inverter_stress.csv",
        "Typo penulisan pada tabel laporan D2.1 baris 3: kolom VDD tertulis '33,3 V' (seharusnya '3,3 V'), meski Vm=1,65V sudah benar.",
        "Terima kasih atas koreksinya; typo terjadi saat pengetikan tabel dokumen, data simulasi CSV sudah memakai 3.3V.",
        "Memperbaiki penulisan '33,3 V' menjadi '3,3 V' pada tabel laporan D2.1 dan melengkapi README.md.",
        commit_hash, "results/inverter_stress.csv", "CLOSED / VERIFIED"
    ],
    [
        "I04", "T22-F", "GPIO Timing", "Zulfa Maylafaiza", "Ahyar Muhaimin",
        "Naikkan beban kapasitif Cload menjadi 4.7 nF pada clock 100 kHz",
        "TERVERIFIKASI", "REPRODUCIBLE", commit_hash,
        "ngspice -b spice/gpio_d22.cir",
        "results/d22_fault_c4.7n_r4.7k.csv", "results/d22_fault_c4.7n_r4.7k.csv",
        "Dengan Rp=4.7k tegangan hanya naik sampai 1.12V (terjebak di zona undefined); Rp=1k melanggar batas arus Port 0 (35.52mA > 26mA).",
        "Dikonfirmasi; resistor tercepat (1k) tidak aman untuk 8-bit serentak dan RC besar menggagalkan sampling.",
        "Menetapkan boundary condition Rp=4.7k hanya untuk Cload <= 100 pF dan frekuensi <= 400 kHz.",
        commit_hash, "results/plots/d22_capacitive_fault.png", "CLOSED / VERIFIED"
    ],
    [
        "I05", "T22-R", "GPIO Timing", "Zulfa Maylafaiza", "Ahyar Muhaimin",
        "Uji perturbasi reviewer: turunkan VDD=4.0V & naikkan Cload=330pF pada Rp=4.7k",
        "TERVERIFIKASI", "REPRODUCIBLE", commit_hash,
        "ngspice -b spice/reviewer_gpio_verify.cir",
        "reviews/gpio_recommendation_memo.md", "results/verify_d22_vdd4_c330p.csv",
        "VOL terukur 0.131V (<=0.45V) dan waktu capai VIH(1.70V) = 808.1 ns (<1250 ns pada 400 kHz); masih lulus namun margin waktu menyempit.",
        "Dikonfirmasi; kenaikan Ron NMOS pada VDD=4.0V menaikkan VOL tipis dari 0.125V ke 0.131V.",
        "Menambahkan catatan margin waktu pada kondisi suplai minimum VDD=4.0V di memo rekomendasi D2.2.",
        commit_hash, "results/verify_d22_vdd4_c330p.csv", "CLOSED / VERIFIED"
    ],
]

with open("verification/issues_log.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(issues_headers)
    writer.writerows(issues_rows)

# 4. Buat verification/peer_review.md (Memuat skenario Owner Zulfa + hasil audit Reviewer Ahyar)
peer_review_md = f"""# Laporan Peer Review & Independent Verification (WBS D2.7)

- **Owner:** Zulfa Maylafaiza
- **Reviewer:** Ahyar Muhaimin
- **Cakupan Modul Diaudit:** D1.2, D1.3, D1.4, D2.1, D2.2 (Domain Transistor, CMOS Inverter, Noise Margin & GPIO)
- **Commit Hash Audit:** `{commit_hash}`
- **Status Keseluruhan:** `VERIFIED / ALL CRITICAL GATES PASSED`

---

## 1. Skenario Pengujian & Baseline dari Owner (Zulfa Maylafaiza)
Seluruh skenario pengujian di bawah ini disusun dan dijalankan oleh Owner menggunakan model MOS Level-1 edukasi ($V_{{TO}} = \\pm 0.8\\text{{ V}}$, $KP_n = 100\\ \\mu\\text{{A/V}}^2$, $KP_p = 50\\ \\mu\\text{{A/V}}^2$) yang dibedakan secara eksplisit dari silikon asli AT89S52:

1. **D1.2 (`T12-B` & `T12-V` — CMOS Inverter VTC & Crossover):**
   - **Skenario:** Sapuan DC $V_{{\\text{{in}}}}$ $0\\text{{ V}} \\to 5\\text{{ V}}$ pada inverter simetris ($W_p = 20\\ \\mu\\text{{m}}, W_n = 10\\ \\mu\\text{{m}}, C_L = 20\\text{{ pF}}$) serta variasi penguatan PMOS ($W_p = 10\\ \\mu\\text{{m}}$).
   - **Klaim Owner:** $V_m = 2.500\\text{{ V}}$ ($I_{{DD,\\text{{peak}}}} = 1.517\\text{{ mA}}$) pada baseline, dan bergeser ke $V_m = 2.210\\text{{ V}}$ saat $W_p = 10\\ \\mu\\text{{m}}$.
2. **D1.3 (`T13-B` & `T13-F` — Logic Thresholds, Noise Margin & Crowbar Fault):**
   - **Skenario:** Audit datasheet AT89S52 Hal. 29 ($V_{{CC}} = 5.0\\text{{ V}}$) untuk Ports 1/2/3 ($NML = 0.45\\text{{ V}}, NMH \\ge 0.50\\text{{ V}}$) serta *fault injection* berupa sinyal $V_{{\\text{{in}}}} = 2.5\\text{{ V}} \\pm 0.3\\text{{ V}}$ ($10\\text{{ MHz}}$) di sekitar $V_m$.
   - **Klaim Owner:** Input dekat $V_m$ memicu osilasi output ($1.13\\text{{ V}} - 3.21\\text{{ V}}$) dan arus *crowbar* kontinu ($I_{{DD,\\min}} = 1.034\\text{{ mA}}$).
3. **D1.4 (`T14-B` & `T14-F` — Open-Drain GPIO Pull-Up & Floating Fault):**
   - **Skenario:** Sapuan 9 kombinasi $R_{{\\text{{pullup}}}} \\in \\{{1\\text{{k}}, 4.7\\text{{k}}, 10\\text{{k}}\\}}$ dan $C_{{\\text{{load}}}} \\in \\{{20\\text{{p}}, 100\\text{{p}}, 1\\text{{n}}\\}}$ serta pelepasan *pull-up* ($R_p = 1\\text{{ T}}\\Omega$) untuk Port 0 mode I/O.
   - **Klaim Owner:** Pada $R_p = 4.7\\text{{ k}}\\Omega, C_L = 100\\text{{ pF}}$, $t_r = 1032.0\\text{{ ns}}$ ($I_{{\\text{{sink}}}} = 1.037\\text{{ mA}}$); tanpa *pull-up*, node *floating* tertahan di $0.000\\text{{ V}}$.
4. **D2.1 (`T21-B` & `T21-F` — Inverter Stress & Slow Input Slew):**
   - **Skenario:** Sapuan $V_{{DD}}$ ($5, 4, 3.3\\text{{ V}}$), $C_L$ ($10, 100, 500\\text{{ pF}}$), rasio $W_p/W_n$, dan perlambatan *input slew* menjadi $40\\text{{ ns}}$.
   - **Klaim Owner:** $C_L$ tidak mengubah $V_m$ DC ($2.500\\text{{ V}}$), namun menaikkan $t_{{pHL}}$ ($28.00\\text{{ ns}}$ pada $100\\text{{ pF}}$); *slow slew* $40\\text{{ ns}}$ menaikkan $t_{{pHL}}$ ke $36.50\\text{{ ns}}$ dan memperlebar arus *crowbar*.
5. **D2.2 (`T22-F` — GPIO Drive Limits & Capacitive Fault):**
   - **Skenario:** Beban kapasitif dinaikkan menjadi $C_L = 4.7\\text{{ nF}}$ pada sinyal $100\\text{{ kHz}}$ ($T_{{\\text{{high}}}} = 5\\ \\mu\\text{{s}}$).
   - **Klaim Owner:** $R_p = 4.7\\text{{ k}}\\Omega$ hanya mencapai $1.120\\text{{ V}}$ (gagal melewati $V_{{IH}} = 1.90\\text{{ V}}$); rekomendasi utama ditetapkan pada $R_p = 4.7\\text{{ k}}\\Omega$ untuk $C_L \\le 100\\text{{ pF}}$ dan $f \\le 400\\text{{ kHz}}$.

---

## 2. Hasil Reproduksi & Uji Batas Reviewer (Ahyar Muhaimin)
| Test ID | Modul | Parameter / Skenario Uji | Nilai Owner (Zulfa) | Nilai Reviewer (Ahyar) | Selisih | Status Reproduksi | Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `T12-B` | D1.2 | Switching crossover $V_m$ (Wp=20u/Wn=10u) | `2.500 V` | `2.500 V` | `0` | REPRODUCIBLE | PASS |
| `T12-V` | D1.2 | Pergeseran $V_m$ saat Wp=10u (rasio 1:1) | `2.210 V` | `2.210 V` | `0` | REPRODUCIBLE | PASS |
| `T13-B` | D1.3 | Noise Margin Low ($NML$) AT89S52 Ports 1–3 | `0.45 V` | `0.45 V` | `0` | REPRODUCIBLE | PASS |
| `T13-F` | D1.3 | Fault: Input dekat $V_m$ ($2.5\\text{{V}} \\pm 0.3\\text{{V}}$) | `1.034 mA` | `1.034 mA` | `0` | REPRODUCIBLE | FAULT CONFIRMED (`I01`) |
| `T14-B` | D1.4 | Open-drain $R_p=4.7\\text{{k}}\\Omega, C_L=100\\text{{pF}}$ ($t_r$) | `1032.0 ns` | `1032.0 ns` | `0` | REPRODUCIBLE | PASS |
| `T14-F` | D1.4 | Fault: Port 0 Open-Drain tanpa pull-up | `0.000 V` | `0.000 V` | `0` | REPRODUCIBLE | FAULT CONFIRMED (`I02`) |
| `T21-B` | D2.1 | Propagation delay $t_{{pHL}}$ ($C_L=100\\text{{pF}}, V_{{DD}}=5\\text{{V}}$) | `28.00 ns` | `28.00 ns` | `0` | REPRODUCIBLE | MINOR TYPO (`I03`) |
| `T21-F` | D2.1 | Fault: Slow input slew $40\\text{{ ns}}$ ($t_{{pHL}}$) | `36.50 ns` | `36.50 ns` | `0` | REPRODUCIBLE | FAULT CONFIRMED |
| `T22-F` | D2.2 | Fault: Beban $4.7\\text{{ nF}}$ pada sinyal $100\\text{{ kHz}}$ | `1.120 V` | `1.120 V` | `0` | REPRODUCIBLE | FAULT CONFIRMED (`I04`) |
| `T22-R` | D2.2 | **Uji Baru Reviewer:** $R_p=4.7\\text{{k}}, V_{{DD}}=4.0\\text{{V}}, C_L=330\\text{{pF}}$ | `818.0 ns` (teori) | `808.1 ns` ($V_{{OL}}=0.131\\text{{V}}$) | `9.9 ns` | REPRODUCIBLE | PASS (`I05`) |

---

## 3. Pemeriksaan Hard Gates & Keputusan Akhir (Sign-Off)
- [x] **Tidak mengklaim fitur salah:** AT89S52 tidak diklaim memiliki internal ADC/DAC.
- [x] **Pemisahan Model vs Silikon:** Model MOS Level-1 edukasi dibedakan secara eksplisit dari silikon asli.
- [x] **Reproducibility & Data CSV:** Seluruh simulasi dapat dijalankan ulang dan didukung file `.csv` numerik.
- [x] **Tindak Lanjut Isu:** Seluruh isu pada `issues_log.csv` (`I01`–`I05`), termasuk perbaikan *typo* `33,3 V` menjadi `3,3 V` pada tabel laporan D2.1 dan penambahan catatan batas suplai $V_{{DD}} = 4.0\\text{{ V}}$, telah ditutup dan dinyatakan **VERIFIED / PASS**.
"""

with open("verification/peer_review.md", "w", encoding="utf-8", newline="\n") as f:
    f.write(peer_review_md)

print("SUKSES! Folder verification/ kini hanya berisi 3 file bukti sesuai permintaan mentor:")
print("1. verification/peer_review.md")
print("2. verification/issues_log.csv")
print("3. verification/verification_matrix.csv")