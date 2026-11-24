import csv
import numpy as np
import matplotlib.pyplot as plt

VDD = 5.0
V70 = 0.70 * VDD   # 3.50 V (70% VDD)
VIH_MIN = 1.90     # AT89S52 Hal. 29 (VCC = 5V)
VOL_MAX = 0.45     # AT89S52 Hal. 29

r_list = [("1k", 1e3), ("4.7k", 4.7e3), ("10k", 10e3)]
c_list = [("20p", 20e-12), ("100p", 100e-12), ("1n", 1e-9)]

rows = []
print("=== HASIL ANALISIS D2.2: GPIO DRIVE, 70% VDD & BANDWIDTH PRAKTIS ===")
print(f"{'R_pullup':<8} | {'Cload':<6} | {'VOL(V)':<6} | {'Isink(mA)':<9} | {'t70_sim(ns)':<11} | {'t70_est(ns)':<11} | {'BW_3dB(kHz)':<11} | {'f_max_praktis(kHz)':<18}")
print("-" * 105)

for r_str, r_val in r_list:
    for c_str, c_val in c_list:
        data = np.loadtxt(f"results/d22_r{r_str}_c{c_str}.csv")
        t = data[:, 0]
        vout = data[:, 1]
        isink = data[:, 3]

        # Kondisi LOW sebelum t = 5 us
        idx_low = np.argmin(np.abs(t - 4.5e-6))
        vol = vout[idx_low]
        isink_ma = isink[idx_low] * 1e3

        # Waktu mencapai 70% VDD (3.50 V) setelah t = 5 us
        mask = t >= 5.0e-6
        t_r = t[mask] - 5.0e-6
        v_r = vout[mask]

        t70_sim_ns = t_r[np.where(v_r >= V70)[0][0]] * 1e9
        t70_est_ns = (r_val * c_val * np.log((VDD - vol) / (VDD - V70))) * 1e9

        # Bandwidth -3dB RC & Frekuensi pulsa praktis (periode min = 2 * t70 untuk duty cycle 50%)
        bw_3db_khz = (1.0 / (2.0 * np.pi * r_val * c_val)) / 1e3
        f_max_khz = (1.0 / (2.0 * (t70_sim_ns * 1e-9))) / 1e3

        # Evaluasi batas datasheet Port 0 AT89S52 (IOL_test=3.2mA, VOL<=0.45V, max 10mA/pin, 26mA/port)
        if vol > VOL_MAX or isink_ma > 3.2:
            status = "PERINGATAN: Melebihi arus uji Port 0 (3.2mA) & VOL > 0.45V"
        elif t70_sim_ns > 2500:
            status = "LAMBAT: Hanya aman untuk sinyal < 100 kHz"
        else:
            status = "AMAN & KOMPATIBEL"

        print(f"{r_str:<8} | {c_str:<6} | {vol:<6.3f} | {isink_ma:<9.3f} | {t70_sim_ns:<11.1f} | {t70_est_ns:<11.1f} | {bw_3db_khz:<11.1f} | {f_max_khz:<18.1f}")
        rows.append([
            r_str, c_str, f"{vol:.3f}", f"{isink_ma:.3f}",
            f"{t70_sim_ns:.1f}", f"{t70_est_ns:.1f}",
            f"{bw_3db_khz:.1f}", f"{f_max_khz:.1f}", status
        ])

# Simpan ke results/gpio_tradeoff.csv
with open("results/gpio_tradeoff.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "R_pullup", "Cload", "VOL_V", "Isink_mA",
        "t_70pct_sim_ns", "t_70pct_est_ns",
        "BW_3dB_kHz", "f_praktis_max_kHz", "Evaluasi_Datasheet"
    ])
    writer.writerows(rows)

# === PLOT FAULT TEST: BEBAN KAPASITIF BERLEBIH (4.7nF pada sinyal 100kHz) ===
fig, ax = plt.subplots(figsize=(9, 4.8))
for r_str, col in [("1k", "blue"), ("4.7k", "orange"), ("10k", "red")]:
    df = np.loadtxt(f"results/d22_fault_c4.7n_r{r_str}.csv")
    tf = df[:, 0] * 1e6
    vf = df[:, 3]
    ax.plot(tf, vf, color=col, linewidth=2, label=f"Vout (Cload=4.7nF, R={r_str})")

ax.axhline(V70, color="purple", linestyle="--", linewidth=1.2, label="70% VDD (3.50 V)")
ax.axhline(VIH_MIN, color="green", linestyle="-.", linewidth=1.3, label="VIH Min AT89S52 (1.90 V)")
ax.set_xlim(0, 22)
ax.set_ylim(-0.2, 5.4)
ax.set_xlabel("Waktu (µs)")
ax.set_ylabel("Tegangan Output Vout (V)")
ax.set_title("Fault Test D2.2: Kegagalan Sampling pada Beban Kapasitif 4,7 nF (Sinyal 100 kHz)")
ax.grid(True, linestyle=":")
ax.legend(loc="upper right", fontsize=8.5)
fig.tight_layout()
fig.savefig("results/plots/d22_capacitive_fault.png", dpi=150)

print("\nBerhasil membuat:")
print("1. results/gpio_tradeoff.csv")
print("2. results/plots/d22_capacitive_fault.png")