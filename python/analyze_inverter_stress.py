import csv
import numpy as np
import matplotlib.pyplot as plt

def get_vm(dc_file):
    data = np.loadtxt(dc_file)
    vin = data[:, 1]
    vout = data[:, 3]
    idd = data[:, 5] * 1e3
    idx = np.argmin(np.abs(vout - vin))
    return vin[idx], np.max(idd), vin, vout, idd

def measure_tran(tran_file, vdd):
    data = np.loadtxt(tran_file)
    t = data[:, 0] * 1e9   # detik ke ns
    vin = data[:, 1]
    vout = data[:, 3]
    idd = data[:, 5] * 1e3 # A ke mA

    v10 = 0.1 * vdd
    v50 = 0.5 * vdd
    v90 = 0.9 * vdd

    # 1. Transisi Input NAIK (t ~ 20 ns) -> Output TURUN (tpHL & Fall Time 90%-10%)
    m1 = (t >= 15.0) & (t <= 515.0)
    t1, vin1, vout1 = t[m1], vin[m1], vout[m1]
    tin_50_rise = t1[np.where(vin1 >= v50)[0][0]]
    tout_50_fall = t1[np.where(vout1 <= v50)[0][0]]
    tphl = tout_50_fall - tin_50_rise

    t_out90 = t1[np.where(vout1 <= v90)[0][0]]
    t_out10 = t1[np.where(vout1 <= v10)[0][0]]
    t_fall = t_out10 - t_out90

    # 2. Transisi Input TURUN (t ~ 522 ns) -> Output NAIK (tpLH & Rise Time 10%-90%)
    m2 = (t >= 518.0) & (t <= 1095.0)
    t2, vin2, vout2 = t[m2], vin[m2], vout[m2]
    tin_50_fall = t2[np.where(vin2 <= v50)[0][0]]
    tout_50_rise = t2[np.where(vout2 >= v50)[0][0]]
    tplh = tout_50_rise - tin_50_fall

    t_in10 = t2[np.where(vout2 >= v10)[0][0]]
    t_in90 = t2[np.where(vout2 >= v90)[0][0]]
    t_rise = t_in90 - t_in10

    return tphl, tplh, t_fall, t_rise, np.max(idd), t, vin, vout, idd

rows = []
print("=== HASIL PENGUKURAN D2.1: INVERTER STRESS & SENSITIVITY ===")
print(f"{'Skenario':<24} | {'VDD':<4} | {'Cload':<5} | {'Vm(V)':<6} | {'tpHL(ns)':<8} | {'tpLH(ns)':<8} | {'tfall(ns)':<9} | {'trise(ns)':<9} | {'IDD_pk(mA)':<10}")
print("-" * 104)

# A. Sweep VDD (5V, 4V, 3.3V) pada Cload=100pF, Wp=20u/Wn=10u
for v_str, v_val in [("5", 5.0), ("4", 4.0), ("3.3", 3.3)]:
    vm, _, _, _, _ = get_vm(f"results/d21_dc_vdd{v_str}.csv")
    tphl, tplh, tf, tr, idd_pk, _, _, _, _ = measure_tran(f"results/d21_tran_vdd{v_str}_c100p.csv", v_val)
    label = f"VDD={v_str}V (Wp=20u/10u)"
    print(f"{label:<24} | {v_val:<4.1f} | {'100p':<5} | {vm:<6.2f} | {tphl:<8.2f} | {tplh:<8.2f} | {tf:<9.2f} | {tr:<9.2f} | {idd_pk:<10.2f}")
    rows.append([label, v_val, "100p", "20u/10u", f"{vm:.2f}", f"{tphl:.2f}", f"{tplh:.2f}", f"{tf:.2f}", f"{tr:.2f}", f"{idd_pk:.2f}"])

# B. Sweep Cload (10p, 100p, 500p) pada VDD=5V, Wp=20u/Wn=10u
vm_5v, _, _, _, _ = get_vm("results/d21_dc_vdd5.csv")
for c_str in ["10p", "100p", "500p"]:
    tphl, tplh, tf, tr, idd_pk, _, _, _, _ = measure_tran(f"results/d21_tran_c{c_str}.csv", 5.0)
    label = f"Cload={c_str}F (VDD=5V)"
    print(f"{label:<24} | {5.0:<4.1f} | {c_str:<5} | {vm_5v:<6.2f} | {tphl:<8.2f} | {tplh:<8.2f} | {tf:<9.2f} | {tr:<9.2f} | {idd_pk:<10.2f}")
    rows.append([label, 5.0, c_str, "20u/10u", f"{vm_5v:.2f}", f"{tphl:.2f}", f"{tplh:.2f}", f"{tf:.2f}", f"{tr:.2f}", f"{idd_pk:.2f}"])

# C. Sweep 3 Rasio Kekuatan (Wp=10u/10u, 20u/10u, 40u/10u) pada VDD=5V, Cload=100pF
ratios = [
    ("Rasio 1:1 (Wp=10u/10u)", "results/d21_dc_wp10u.csv", "results/d21_tran_wp10u.csv", "10u/10u"),
    ("Rasio 2:1 (Wp=20u/10u)", "results/d21_dc_vdd5.csv", "results/d21_tran_c100p.csv", "20u/10u"),
    ("Rasio 4:1 (Wp=40u/10u)", "results/d21_dc_wp40u.csv", "results/d21_tran_wp40u.csv", "40u/10u"),
]
for label, f_dc, f_tr, r_txt in ratios:
    vm, _, _, _, _ = get_vm(f_dc)
    tphl, tplh, tf, tr, idd_pk, _, _, _, _ = measure_tran(f_tr, 5.0)
    print(f"{label:<24} | {5.0:<4.1f} | {'100p':<5} | {vm:<6.2f} | {tphl:<8.2f} | {tplh:<8.2f} | {tf:<9.2f} | {tr:<9.2f} | {idd_pk:<10.2f}")
    rows.append([label, 5.0, "100p", r_txt, f"{vm:.2f}", f"{tphl:.2f}", f"{tplh:.2f}", f"{tf:.2f}", f"{tr:.2f}", f"{idd_pk:.2f}"])

# D. Fault Test: Slow Slew (tr=tf=40ns) pada VDD=5V, Cload=100pF
tphl_s, tplh_s, tf_s, tr_s, idd_pk_s, t_sl, vin_sl, vout_sl, idd_sl = measure_tran("results/d21_fault_slow_slew.csv", 5.0)
print(f"{'Fault: Slow Slew 40ns':<24} | {5.0:<4.1f} | {'100p':<5} | {vm_5v:<6.2f} | {tphl_s:<8.2f} | {tplh_s:<8.2f} | {tf_s:<9.2f} | {tr_s:<9.2f} | {idd_pk_s:<10.2f}")
rows.append(["Fault: Slow Slew 40ns", 5.0, "100p", "20u/10u", f"{vm_5v:.2f}", f"{tphl_s:.2f}", f"{tplh_s:.2f}", f"{tf_s:.2f}", f"{tr_s:.2f}", f"{idd_pk_s:.2f}"])

with open("results/inverter_stress.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Scenario", "VDD_V", "Cload", "Wp_Wn", "Vm_V", "tpHL_ns", "tpLH_ns", "tfall_90_10_ns", "trise_10_90_ns", "IDD_peak_mA"])
    writer.writerows(rows)

# === BUAT 3 OVERLAY FIGURES ===
fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))
for v_str, col in [("5", "blue"), ("4", "orange"), ("3.3", "green")]:
    vm, _, vin, vout, _ = get_vm(f"results/d21_dc_vdd{v_str}.csv")
    ax1.plot(vin, vout, color=col, linewidth=2, label=f"VDD={v_str}V (Vm={vm:.2f}V)")
    _, _, _, _, _, t, _, vout_t, _ = measure_tran(f"results/d21_tran_vdd{v_str}_c100p.csv", float(v_str))
    ax2.plot(t, vout_t, color=col, linewidth=2, label=f"VDD={v_str}V")
ax1.set_title("Overlay 1A: VTC DC pada Variasi VDD")
ax1.set_xlabel("Vin (V)"); ax1.set_ylabel("Vout (V)"); ax1.grid(True, linestyle=":"); ax1.legend()
ax2.set_title("Overlay 1B: Transient (Cload=100pF) Variasi VDD")
ax2.set_xlabel("Waktu (ns)"); ax2.set_ylabel("Vout (V)"); ax2.set_xlim(0, 750); ax2.grid(True, linestyle=":"); ax2.legend()
fig1.tight_layout()
fig1.savefig("results/plots/d21_overlay1_vdd.png", dpi=150)

fig2, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))
for c_str, col in [("10p", "blue"), ("100p", "orange"), ("500p", "red")]:
    _, _, _, _, _, t, _, vout_t, _ = measure_tran(f"results/d21_tran_c{c_str}.csv", 5.0)
    ax1.plot(t, vout_t, color=col, linewidth=2, label=f"Cload={c_str}F")
ax1.set_title("Overlay 2A: Dampak Cload pada Delay (VDD=5V)")
ax1.set_xlabel("Waktu (ns)"); ax1.set_ylabel("Vout (V)"); ax1.set_xlim(0, 1050); ax1.grid(True, linestyle=":"); ax1.legend()

for label, _, f_tr, _ in ratios:
    _, _, _, _, _, t, _, vout_t, _ = measure_tran(f_tr, 5.0)
    ax2.plot(t, vout_t, linewidth=2, label=label)
ax2.set_title("Overlay 2B: Dampak Rasio Wp/Wn (Cload=100pF)")
ax2.set_xlabel("Waktu (ns)"); ax2.set_ylabel("Vout (V)"); ax2.set_xlim(0, 750); ax2.grid(True, linestyle=":"); ax2.legend()
fig2.tight_layout()
fig2.savefig("results/plots/d21_overlay2_cload_ratio.png", dpi=150)

_, _, _, _, _, t_fs, vin_fs, vout_fs, idd_fs = measure_tran("results/d21_tran_c100p.csv", 5.0)
fig3, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 5.5), sharex=True)
ax1.plot(t_fs, vout_fs, "b-", linewidth=1.8, label="Vout (Fast Slew 2ns)")
ax1.plot(t_sl, vout_sl, "r--", linewidth=1.8, label="Vout (Slow Slew 40ns)")
ax1.set_ylabel("Tegangan Vout (V)")
ax1.set_title("Overlay 3: Dampak Input Slew Lambat (40ns) vs Cepat (2ns) pada Cload=100pF")
ax1.grid(True, linestyle=":"); ax1.legend()

ax2.plot(t_fs, idd_fs, "b-", linewidth=1.6, label="IDD Fast Slew 2ns")
ax2.plot(t_sl, idd_sl, "r-", linewidth=1.8, label="IDD Slow Slew 40ns (Crowbar Lebih Lama)")
ax2.set_xlabel("Waktu (ns)"); ax2.set_ylabel("Arus IDD (mA)")
ax2.set_xlim(0, 700); ax2.grid(True, linestyle=":"); ax2.legend()
fig3.tight_layout()
fig3.savefig("results/plots/d21_overlay3_slow_slew.png", dpi=150)

print("\nBerhasil membuat:")
print("1. results/inverter_stress.csv")
print("2. results/plots/d21_overlay1_vdd.png")
print("3. results/plots/d21_overlay2_cload_ratio.png")
print("4. results/plots/d21_overlay3_slow_slew.png")