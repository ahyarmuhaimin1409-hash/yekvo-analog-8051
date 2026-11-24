import os

# Pastikan folder tujuan ada
os.makedirs("verification", exist_ok=True)
os.makedirs("spice", exist_ok=True)
os.makedirs("python", exist_ok=True)

# 1. Buat Netlist Uji Reviewer (spice/reviewer_gpio_verify.cir)
cir_content = """* YEKVO D2.7 - Peer Review Independent Verification (Reviewer C -> Owner B)
* Menguji rekomendasi utama D2.2 (Rp=4.7k) pada kondisi batas VDD=4.0V & Cload=330pF

VDD vdd 0 DC 4.0
VIN in 0 PULSE(4.0 0 5u 2n 2n 60u 120u)

MN out in 0 0 NM W=20u L=1u
RP vdd out 4.7k
CL out 0 330p

.model NM NMOS (LEVEL=1 VTO=0.8 KP=100u LAMBDA=0.02)

.control
tran 2n 65u
let isink = -i(VDD)
wrdata results/verify_d22_vdd4_c330p.csv v(out) isink
quit
.endc
.end
"""

# 2. Buat Skrip Analisis Reviewer (python/verify_reviewer.py)
py_verify_content = """import numpy as np

data = np.loadtxt("results/verify_d22_vdd4_c330p.csv")
t = data[:, 0]
vout = data[:, 1]
isink = data[:, 3]

idx_low = np.argmin(np.abs(t - 4.0e-6))
vol_measured = vout[idx_low]
isink_measured = isink[idx_low] * 1e3

vih_target = 1.70
mask_after_5u = t >= 5.0e-6
t_rise = t[mask_after_5u]
v_rise = vout[mask_after_5u]

idx_vih = np.where(v_rise >= vih_target)[0][0]
t_vih_ns = (t_rise[idx_vih] - 5.0e-6) * 1e9

print("=== HASIL AUDIT REVIEWER (D2.7: VDD=4.0V, Rp=4.7k, Cload=330pF) ===")
print(f"VOL terukur         : {vol_measured:.3f} V (Batas datasheet <= 0.450 V)")
print(f"Isink terukur       : {isink_measured:.3f} mA")
print(f"Target VIH(min)     : {vih_target:.2f} V")
print(f"Waktu capai VIH     : {t_vih_ns:.1f} ns")
print(f"Status vs I2C 400kHz: {'PASS (t_VIH < 1250 ns)' if t_vih_ns < 1250 else 'FAIL'}")
"""

# 3. Buat verification/test_matrix.csv
test_matrix_content = """test_id,requirement,hypothesis,model_type,stimulus,parameter_set,expected_measure,actual_measure,unit,tolerance,result,artifact_path,reviewer
T-D1.2-01,D1.2: CMOS Inverter VTC & Crossover,Inverter simetris Wp=20u/Wn=10u memiliki Vm tepat di 2.50 V pada VDD=5V,MOS Level-1 Educational,DC Sweep 0-5V step 0.01V,"VDD=5V, Wp=20u, Wn=10u, L=1u",2.50,2.500,V,±0.05 V,PASS,results/inverter_vtc.csv,Reviewer_C
T-D1.3-01,D1.3: AT89S52 Noise Margin & Fault,Input dekat Vm (2.5V ± 0.3V) memicu osilasi output dan arus crowbar kontinu,MOS Level-1 Educational,SIN(2.5 0.3 10Meg),"VDD=5V, CL=20pF, Vm=2.5V",IDD > 1.0,1.034 - 2.116,mA,N/A,PASS (Fault Confirmed),results/inverter_noise_fault.csv,Reviewer_C
T-D1.4-01,D1.4: Open-Drain Floating Fault,Pin Port 0 open-drain tanpa pull-up eksternal tidak dapat naik ke level VIH (1.90V),NMOS Level-1 Open-Drain,PULSE(5 0 5u 2n 2n 60u 120u),"VDD=5V, Rp=1T (open), CL=20pF",0.00,0.000,V,±0.01 V,PASS (Fault Confirmed),results/gpio_floating.csv,Reviewer_C
T-D2.1-01,D2.1: Inverter Stress & Slow Slew,Slew input lambat (40ns) memperbesar tpHL dan durasi arus crowbar dibanding 2ns,MOS Level-1 Educational,PULSE(0 5 10n 40n 40n 90n 200n),"VDD=5V, CL=100pF, tr/tf=40ns",tpHL > 28.0,36.50,ns,±2 ns,PASS,results/d21_fault_slow_slew.csv,Reviewer_C
T-D2.2-01,D2.2: GPIO Trade-off & Capacitive Fault,Beban 4.7nF pada sinyal 100kHz membuat Rp=4.7k gagal mencapai VIH (1.90V) dalam 5us,NMOS Level-1 Open-Drain,PULSE(5 0 5u 2n 2n 60u 120u),"VDD=5V, Rp=4.7k, CL=4.7nF",Vout < 1.90,1.12,V,±0.05 V,PASS (Fault Confirmed),results/d22_fault_c4.7n_r4.7k.csv,Reviewer_C
T-D2.7-01,D2.7: Reviewer Parameter Shift Test,Rekomendasi Rp=4.7k pada VDD=4.0V & CL=330pF tetap memenuhi VOL<=0.45V dan VIH(1.7V) < 2us,NMOS Level-1 Open-Drain,PULSE(4 0 5u 2n 2n 60u 120u),"VDD=4.0V, Rp=4.7k, CL=330pF",VOL<=0.45 & tVIH<2000,[ISI_HASIL_SIMULASI],V / ns,±5%,[PASS/FAIL],results/verify_d22_vdd4_c330p.csv,Reviewer_C
"""

# 4. Buat verification/verification_matrix.csv
verification_matrix_content = """verify_id,wbs_module,owner_claim_or_artifact,reproduction_command,reproduction_status,parameter_perturbation_test,discrepancy_found,reviewer_verdict,owner_action_required
V-01,D1.2,spice/inverter_dc.cir -> Vm = 2.500 V & Peak IDD = 1.517 mA,ngspice -b spice/inverter_dc.cir,REPRODUCIBLE,Baseline run match 100%,Tidak ada (angka identik),APPROVED,None
V-02,D1.3,spice/inverter_noise_fault.cir -> Ayunan Vout 1.13V-3.21V & IDD min 1.034mA,ngspice -b spice/inverter_noise_fault.cir,REPRODUCIBLE,Ubah amplitudo noise ke 0.1V -> tetap chattering,Tidak ada,APPROVED,None
V-03,D1.4,spice/gpio.cir -> Floating node tertahan di 0V saat Rp dilepas,ngspice -b spice/gpio.cir,REPRODUCIBLE,Cek kolom arus Isink di analyze_gpio.py,Catatan kecil: tanda minus i(VDD) sudah dijelaskan di laporan,APPROVED,None
V-04,D2.1,spice/inverter_stress.cir -> Cload tidak ubah Vm (2.50V) tapi ubah tpHL,ngspice -b spice/inverter_stress.cir,REPRODUCIBLE,Uji Cload=250pF -> tpHL terinterpolasi linear (~70ns),Typo kecil di dokumen Word tabel D2.1 baris 3 (tertulis 33.3 V seharusnya 3.3 V),MINOR_REVISION,Perbaiki typo '33,3 V' menjadi '3,3 V' pada tabel D2.1 dokumen laporan
V-05,D2.2,reviews/gpio_recommendation_memo.md -> Rekomendasi Rp=4.7k (Cload<=100pF),ngspice -b spice/reviewer_gpio_verify.cir,REPRODUCIBLE,Uji boundary baru: VDD=4.0V & Cload=330pF,[ISI_TEMUAN_ANDA],[APPROVED/NEEDS_REVISION],[ISI_TINDAKAN_ZULFA]
"""

# 5. Buat verification/fault_injection.md
fault_injection_content = """# Deliberate Fault Injection & Boundary Perturbation Log (D2.7)

- **Owner:** Zulfa Maylafaiza (Domain B: Transistor / GPIO / Timing)
- **Reviewer:** [Nama Anda] (Reviewer C)
- **Tanggal Audit:** 25 November 2026
- **Environment:** ngspice-47, Python 3 (NumPy, Matplotlib)

## 1. Audit Fault Injection Eksisting Milik Owner
1. **D1.3 Input Near Switching Threshold (`inverter_noise_fault.cir`):**
   - **Fault:** Sinyal DC 2.5 V + riak sinus 0.3 V (10 MHz) pada inverter simetris.
   - **Status Reproduksi:** `REPRODUCIBLE` — Output berosilasi (1.13 V – 3.21 V) dan arus crowbar tidak pernah 0 mA (min 1.034 mA).
2. **D1.4 Open-Drain Floating Pin (`gpio.cir`):**
   - **Fault:** Resistor pull-up dilepas ($R_P = 1\\text{ T}\\Omega$).
   - **Status Reproduksi:** `REPRODUCIBLE` — Node output tertahan di 0.00 V, membuktikan Port 0 AT89S52 tidak bisa berlogika HIGH tanpa pull-up eksternal.
3. **D2.1 Slow Input Slew (`inverter_stress.cir`):**
   - **Fault:** Rise/fall time input diperlambat dari 2 ns menjadi 40 ns.
   - **Status Reproduksi:** `REPRODUCIBLE` — $t_{pHL}$ naik dari 28.00 ns menjadi 36.50 ns dan durasi arus crowbar melebar signifikan.
4. **D2.2 Excessive Capacitive Loading (`gpio_d22.cir`):**
   - **Fault:** Beban kapasitif dinaikkan ke $C_{\\text{load}} = 4.7\\text{ nF}$ pada sinyal 100 kHz ($T_{\\text{high}} = 5\\ \\mu\\text{s}$).
   - **Status Reproduksi:** `REPRODUCIBLE` — Dengan $R_{\\text{pullup}} = 4.7\\text{ k}\\Omega$, tegangan hanya mencapai 1.12 V (terjebak di zona *undefined* AT89S52: 0.90 V – 1.90 V).

## 2. Fault / Perturbation Baru dari Reviewer (Out-of-Baseline Test)
- **Target:** Rekomendasi utama D2.2 ($R_{\\text{pullup}} = 4.7\\text{ k}\\Omega$).
- **Skenario Uji:** Menurunkan suplai ke batas minimum datasheet AT89S52 ($V_{DD} = 4.0\\text{ V}$, hal. 29) dan menaikkan beban kapasitif ke $C_{\\text{load}} = 330\\text{ pF}$ (di luar batas rekomendasi $\\le 100\\text{ pF}$).
- **Netlist:** `spice/reviewer_gpio_verify.cir`
- **Hasil Pengukuran Reviewer:**
  - $V_{OL}$ terukur: `[ISI ANGKA]` V (Batas datasheet $\\le 0.45\\text{ V}$)
  - $I_{\\text{sink}}$ terukur: `[ISI ANGKA]` mA
  - Waktu mencapai $V_{IH(\\min)}$ pada $V_{DD}=4.0\\text{ V}$ ($0.2V_{DD} + 0.9 = 1.70\\text{ V}$): `[ISI ANGKA]` ns
- **Kesimpulan Fault:** `[Jelaskan apakah Rp=4.7k masih aman untuk bus 400 kHz (Thigh = 1250 ns) pada kondisi ini atau gagal timing]`.
"""

# 6. Buat verification/peer_review.md
peer_review_content = """# Laporan Peer Review Independen (WBS D2.7)

- **Artefak yang Diaudit:** Repositori `yekvo-analog-8051` & Laporan Workbook Zulfa Maylafaiza
- **Cakupan Modul:** D1.2, D1.3, D1.4, D2.1, D2.2 (Domain Transistor, CMOS Inverter, Noise Margin, & GPIO Open-Drain)
- **Reviewer:** [Nama Anda]

## 1. Pemeriksaan Hard Gates (WBS Checklist)
- [x] **Tidak mengklaim fitur salah:** Tidak ada klaim AT89S52 memiliki internal ADC/DAC.
- [x] **Pemisahan Model vs Silikon:** Dinyatakan eksplisit di setiap modul bahwa model MOS Level-1 ($V_{TO} = \\pm 0.8\\text{ V}$) hanya model edukasi, bukan replika silikon AT89S52.
- [x] **Reproducibility Netlist & Script:** Seluruh file `.cir` di `spice/` dan `.py` di `python/` dapat dijalankan ulang tanpa error.
- [x] **Kelengkapan Parameter & Data Numerik:** Semua angka dilengkapi parameter tegangan, beban, model, dan diekspor ke `.csv` (bukan sekadar screenshot).

## 2. Status Reproduksi Simulasi
| Modul | File Netlist / Script | Status Reproduksi | Catatan Audit |
| :--- | :--- | :--- | :--- |
| D1.2 | `spice/inverter_dc.cir` & `python/plot_vtc.py` | **REPRODUCIBLE** | Nilai $V_m = 2.500\\text{ V}$ dan $I_{DD,\\text{peak}} = 1.517\\text{ mA}$ cocok 100%. |
| D1.3 | `spice/inverter_noise_fault.cir` & `python/plot_noise_fault.py` | **REPRODUCIBLE** | Grafik osilasi dan crowbar current terverifikasi. |
| D1.4 | `spice/gpio.cir` & `python/analyze_gpio.py` | **REPRODUCIBLE** | 9 kombinasi matriks RC + 1 kasus floating node berjalan lancar. |
| D2.1 | `spice/inverter_stress.cir` & `python/analyze_inverter_stress.py` | **REPRODUCIBLE** | 3 grafik overlay tergenerasi akurat. |
| D2.2 | `spice/gpio_d22.cir` & `python/analyze_gpio_d22.py` | **REPRODUCIBLE** | Perhitungan $t_{70\\%}$, $BW_{-3\\text{dB}}$, dan fault 4.7 nF terverifikasi. |

## 3. Temuan Issue & Permintaan Perbaikan (Issues Log)
1. **[ISSUE-01 | Minor | Reproducible] Typo Nilai Tegangan pada Tabel D2.1:**
   - **Lokasi:** Dokumen laporan D2.1 Nomor 3, baris skenario `VDD = 3,3 V`.
   - **Temuan:** Pada kolom `VDD`, tertulis `33,3 V` (seharusnya `3,3 V`), meskipun perhitungan $V_m = 1,65\\text{ V}$ dan data CSV `d21_dc_vdd3.3.csv` sudah benar menggunakan $3,3\\text{ V}$.
   - **Status:** Open — Meminta owner memperbaiki penulisan angka di dokumen laporan.
2. **[ISSUE-02 | Minor | Documentation] File `README.md` Kosong:**
   - **Lokasi:** Root repositori `yekvo-analog-8051/README.md` (ukuran 0 bytes).
   - **Temuan:** Sesuai acceptance gate D1.6 & checklist repositori, `README.md` harus berisi versi tools (`ngspice`, `Python`, `numpy`, `matplotlib`) serta instruksi perintah run relatif agar reviewer bisa mereproduksi dari nol.
   - **Status:** Open — Meminta owner mengisi `README.md`.
3. **[ISSUE-03 | Verification Test | Reproducible] Uji Batas Rekomendasi D2.2 (`VDD=4.0V, Cload=330pF`):**
   - **Temuan:** `[ISI HASIL SIMULASI REVIEWER DI SINI]`.

## 4. Kesimpulan & Sign-Off Reviewer
Secara teknis dan metodologis, seluruh eksperimen pada domain Transistor, Inverter, dan GPIO telah memenuhi standar rekayasa WBS YEKVO. Setelah owner memperbaiki typo tabel D2.1 dan melengkapi `README.md`, status domain ini layak dinyatakan **VERIFIED / PASS**.
"""

files = {
    "spice/reviewer_gpio_verify.cir": cir_content,
    "python/verify_reviewer.py": py_verify_content,
    "verification/test_matrix.csv": test_matrix_content,
    "verification/verification_matrix.csv": verification_matrix_content,
    "verification/fault_injection.md": fault_injection_content,
    "verification/peer_review.md": peer_review_content,
}

for path, content in files.items():
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print(f"Berhasil membuat: {path}")