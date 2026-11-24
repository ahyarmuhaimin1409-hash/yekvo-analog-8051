import os
import numpy as np
import matplotlib.pyplot as plt

def baca_vtc(path):
    data = np.loadtxt(path)
    vin = data[:, 1]
    vout = data[:, 3]
    idd = data[:, 5] * 1e3 if data.shape[1] >= 6 else None
    idx_vm = np.argmin(np.abs(vout - vin))
    vm = vin[idx_vm]
    return vin, vout, idd, vm

# 1. Baca data baseline (Wp = 20u)
vin1, vout1, idd1, vm1 = baca_vtc("results/inverter_vtc.csv")
print("=== HASIL D1.2: CMOS INVERTER VTC ===")
print(f"[Baseline Wp=20u] Switching Vm = {vm1:.3f} V | Peak IDD = {np.max(idd1):.3f} mA")

# 2. Cek apakah file variasi (Wp = 10u) ada
has_var = os.path.exists("results/inverter_vtc_wp10u.csv")
if has_var:
    vin2, vout2, idd2, vm2 = baca_vtc("results/inverter_vtc_wp10u.csv")
    print(f"[Variasi  Wp=10u] Switching Vm = {vm2:.3f} V | Peak IDD = {np.max(idd2):.3f} mA")

# 3. Buat grafik VTC + perbandingan
fig, ax1 = plt.subplots(figsize=(8, 5))
ax1.plot(vin1, vout1, "b-", linewidth=2, label=f"VTC Baseline Wp=20u (Vm={vm1:.2f}V)")
ax1.scatter([vm1], [vm1], color="blue", zorder=5)

if has_var:
    ax1.plot(vin2, vout2, "g-", linewidth=2, label=f"VTC Variasi Wp=10u (Vm={vm2:.2f}V)")
    ax1.scatter([vm2], [vm2], color="green", zorder=5)

ax1.plot(vin1, vin1, "k--", alpha=0.5, label="Garis Vout = Vin")
ax1.set_xlabel("Vin (V)")
ax1.set_ylabel("Vout (V)", color="b")
ax1.set_xlim(0, 5)
ax1.set_ylim(-0.2, 5.2)
ax1.grid(True, linestyle=":")

ax2 = ax1.twinx()
ax2.plot(vin1, idd1, "r:", alpha=0.8, label="Arus IDD Wp=20u (mA)")
if has_var:
    ax2.plot(vin2, idd2, "m:", alpha=0.8, label="Arus IDD Wp=10u (mA)")
ax2.set_ylabel("IDD (mA)", color="r")

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="center left", fontsize=8.5)

plt.title("CMOS Inverter VTC & Pergeseran Switching Point (Model Level-1)")
fig.tight_layout()
plt.savefig("results/plots/inverter_vtc.png", dpi=150)
print("Grafik tersimpan di: results/plots/inverter_vtc.png")