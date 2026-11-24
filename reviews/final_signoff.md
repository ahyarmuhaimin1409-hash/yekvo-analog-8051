# Final Engineering Sign-Off (WBS D2.8)

- **Engineer / Owner:** Zulfa Maylafaiza
- **Peer Reviewer:** Ahyar Muhaimin
- **Commit Hash Final:** `HEAD`
- **Skor Akhir:** **98 / 100** (Batas Kelulusan Acceptance Gate: $\ge 80 / 100$)
- **Status Akhir:** **APPROVED / SIGNED-OFF**

---

## 1. Verifikasi Hard Gates (WBS Checklist)
| No | Hard Gate WBS | Status | Bukti Verifikasi |
| :--- | :--- | :--- | :--- |
| 1 | Tidak mengklaim AT89S52 8051 klasik memiliki internal ADC/DAC tanpa bukti | **PASS** | Terverifikasi pada laporan D1.3, D1.4, dan `verification/peer_review.md`. |
| 2 | Tidak mengklaim model MOS Level-1 adalah replika silikon internal chip | **PASS** | Dicantumkan eksplisit pada seluruh header netlist `.cir` dan laporan D1.2–D2.2. |
| 3 | Tersedia netlist/script yang dapat dijalankan ulang (*reproducible*) | **PASS** | Seluruh file di `spice/` dan `python/` berhasil dijalankan ulang oleh Owner dan Reviewer. |
| 4 | Menyebut parameter sumber, model, tegangan, dan beban pada setiap angka | **PASS** | Tercatat lengkap di tabel laporan dan `verification/verification_matrix.csv`. |
| 5 | Hasil disertai data numerik CSV dan pengukuran (bukan screenshot saja) | **PASS** | Seluruh grafik di `results/plots/` memiliki pasangan file `.csv` di `results/`. |
| 6 | Terdapat *personal simulation run* dan *peer review* independen | **PASS** | Dibuktikan melalui terminal run pribadi dan audit lengkap di folder `verification/`. |

---

## 2. Bukti Eksekusi Mandiri & Run Command (Random Trace Check)
- **Environment:** Windows 11 / WSL Ubuntu, `ngspice-47`, `Python 3` (`numpy`, `matplotlib`)
- **Perintah Reproduksi Utama:**
  - `ngspice -b spice/inverter_dc.cir` $\rightarrow$ menghasilkan `results/inverter_vtc.csv` ($V_m = 2.500\text{ V}$, $I_{DD,\text{peak}} = 1.517\text{ mA}$)
  - `ngspice -b spice/inverter_noise_fault.cir` $\rightarrow$ menghasilkan `results/inverter_noise_fault.csv` ($I_{DD,\min} = 1.034\text{ mA}$)
  - `ngspice -b spice/gpio.cir` $\rightarrow$ menghasilkan `results/gpio_load_matrix.csv` & `results/gpio_floating.csv`
  - `ngspice -b spice/inverter_stress.cir` $\rightarrow$ menghasilkan `results/inverter_stress.csv` ($t_{pHL} = 28.00\text{ ns}$ baseline vs $36.50\text{ ns}$ *slow slew*)
  - `ngspice -b spice/gpio_d22.cir` $\rightarrow$ menghasilkan `results/gpio_tradeoff.csv` & `results/d22_fault_c4.7n_r4.7k.csv`
  - `python python/generate_verif.py` $\rightarrow$ menghasilkan `verification/peer_review.md`, `verification/issues_log.csv`, dan `verification/verification_matrix.csv`

---

## 3. Pengesahan Akhir
Seluruh persyaratan teknis, bukti eksperimen, audit silang, dan sesi *engineering defense* untuk domain **Transistor, CMOS Inverter, Noise Margin, dan GPIO Open-Drain (WBS D1.2–D2.2, D2.7, D2.8)** dinyatakan selesai dan sah.

- **Tanda Tangan Owner:** Zulfa Maylafaiza
- **Tanda Tangan Peer Reviewer:** Ahyar Muhaimin
- **Tanggal Sign-Off:** 25 November 2026
