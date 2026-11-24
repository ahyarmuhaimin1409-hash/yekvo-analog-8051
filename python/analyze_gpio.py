import csv
import numpy as np
import matplotlib.pyplot as plt

VIH_AT89S52 = 1.90  # Batas VIH min AT89S52 Hal. 29 (VCC = 5.0V)
r_list = [("1k", 1e3), ("4.7k", 4.7e3), ("10k", 10e3)]
c_list = [("20p", 20e-12), ("100p", 100e-12), ("1n", 1e-9)]

rows = []
print("=== HASIL PENGUKURAN D1.4 NOMOR 3: LOW CURRENT & RISE-TIME ===")
print(f"{'R_pullup':<8} | {'Cload':<6} | {'VOL (V)':<7} | {'Isink (mA)':<10} | {'tr_sim (ns)':<11}")
print("-" * 55)

for c_str, c_val in c_list:
    fig, ax = plt.subplots(figsize=(8.5, 4.8))

    for r_str, r_val in r_list:
        data = np.loadtxt(f"results/gpio_r{r_str}_c{c_str}.csv")
        t = data[:, 0]
        vout = data[:, 1]
        isink = data[:, 3]
        vout_pp = data[:, 5]

        # 1. Ukur kondisi LOW saat t = 4.5 us (sebelum NMOS dimatikan di t = 5 us)
        idx_low = np.argmin(np.abs(t - 4.5e-6))
        vol = vout[idx_low]
        isink_ma = isink[idx_low] * 1e3  # konversi ke mA

        # 2. Ukur Rise Time (10% - 90%) setelah t = 5 us
        mask_rise = t >= 5.0e-6
        t_r = t[mask_rise] - 5.0e-6
        v_r = vout[mask_rise]

        v10 = vol + 0.1 * (5.0 - vol)
        v90 = vol + 0.9 * (5.0 - vol)

        t10 = t_r[np.where(v_r >= v10)[0][0]]
        t90 = t_r[np.where(v_r >= v90)[0][0]]
        tr_sim_ns = (t90 - t10) * 1e9

        # Simpan juga data pendukung untuk Nomor 4 (RC teori, daya, dan waktu capai VIH)
        p_low_mw = 5.0 * isink_ma
        tr_rc_ns = 2.2 * r_val * c_val * 1e9
        t_vih_ns = t_r[np.where(v_r >= VIH_AT89S52)[0][0]] * 1e9

        print(f"{r_str:<8} | {c_str:<6} | {vol:<7.3f} | {isink_ma:<10.3f} | {tr_sim_ns:<11.1f}")
        rows.append([
            r_str, c_str, f"{vol:.3f}", f"{isink_ma:.3f}",
            f"{p_low_mw:.2f}", f"{tr_sim_ns:.1f}", f"{tr_rc_ns:.1f}", f"{t_vih_ns:.1f}"
        ])

        ax.plot(t_r * 1e6, v_r, linewidth=2, label=f"Open-Drain R={r_str} (tr={tr_sim_ns:.0f} ns)")

    # Tambahkan pembanding Push-Pull Ideal & Floating Node
    ax.plot(t_r * 1e6, vout_pp[mask_rise], "k--", linewidth=1.5, label="Push-Pull Ideal (Pembanding)")

    data_flt = np.loadtxt("results/gpio_floating.csv")
    v_flt = data_flt[:, 1][mask_rise]
    ax.plot(t_r * 1e6, v_flt, "r:", linewidth=1.8, label="Tanpa Pull-Up (Floating)")
    ax.axhline(VIH_AT89S52, color="green", linestyle="-.", linewidth=1.2, label="VIH Min AT89S52 (1.90 V)")

    xlim_us = 0.25 if c_str == "20p" else (1.2 if c_str == "100p" else 12.0)
    ax.set_xlim(0, xlim_us)
    ax.set_ylim(-0.2, 5.4)
    ax.set_xlabel("Waktu setelah NMOS OFF (µs)")
    ax.set_ylabel("Tegangan Output Vout (V)")
    ax.set_title(f"Timing Transisi Open-Drain GPIO pada Beban Cload = {c_str}F")
    ax.grid(True, linestyle=":")
    ax.legend(loc="lower right", fontsize=8)
    fig.tight_layout()
    plt.savefig(f"results/plots/gpio_timing_{c_str}F.png", dpi=150)

# Simpan matriks hasil ke results/gpio_load_matrix.csv
with open("results/gpio_load_matrix.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "R_pullup", "Cload", "VOL_V", "Isink_mA",
        "Power_Low_mW", "tr_sim_ns", "tr_RC_est_ns", "t_reach_VIH_ns"
    ])
    writer.writerows(rows)

print("\nBerhasil membuat:")
print("1. results/gpio_load_matrix.csv")
print("2. results/plots/gpio_timing_20pF.png")
print("3. results/plots/gpio_timing_100pF.png")
print("4. results/plots/gpio_timing_1nF.png")