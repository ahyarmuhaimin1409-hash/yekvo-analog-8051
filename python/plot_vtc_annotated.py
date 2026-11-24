import numpy as np
import matplotlib.pyplot as plt

# 1. Parameter dari Datasheet AT89S52 (Hal. 29, VCC = 5.0V) & Simulasi D1.2
VIL = 0.90   # Input Low Voltage maks (0.2*VCC - 0.1)
VIH = 1.90   # Input High Voltage min (0.2*VCC + 0.9)
VM  = 2.50   # Switching point inverter simulasi D1.2

# 2. Baca data VTC hasil ngspice
data = np.loadtxt("results/inverter_vtc.csv")
vin = data[:, 1]
vout = data[:, 3]

fig, ax = plt.subplots(figsize=(9, 5.2))

# 3. Tandai 3 Wilayah Logika
ax.axvspan(0.0, VIL, color="#d4edda", alpha=0.65, label=f"Guaranteed LOW (0,00 V – {VIL:.2f} V)")
ax.axvspan(VIL, VIH, color="#fff3cd", alpha=0.85, label=f"Undefined Region ({VIL:.2f} V – {VIH:.2f} V)")
ax.axvspan(VIH, 5.0, color="#cce5ff", alpha=0.65, label=f"Guaranteed HIGH ({VIH:.2f} V – 5,00 V)")

# 4. Plot kurva VTC, batas datasheet, dan titik switching Vm
ax.plot(vin, vout, "b-", linewidth=2.2, label="Kurva VTC Inverter (Model Level-1)")
ax.axvline(VIL, color="green", linestyle="--", linewidth=1.3, label=f"Batas Datasheet VIL = {VIL:.2f} V")
ax.axvline(VIH, color="darkorange", linestyle="--", linewidth=1.3, label=f"Batas Datasheet VIH = {VIH:.2f} V")
ax.scatter([VM], [VM], color="red", s=60, zorder=6, label=f"Switching Point Inverter Vm = {VM:.2f} V")

# Anotasi teks langsung pada grafik
ax.text(0.45, 0.5, "LOW\n(Logika 0)", ha="center", va="center", fontsize=9, fontweight="bold", color="darkgreen")
ax.text(1.40, 2.5, "UNDEFINED\n(Zona Terlarang)", ha="center", va="center", fontsize=8.5, fontweight="bold", color="#856404")
ax.text(3.60, 4.3, "HIGH\n(Logika 1)", ha="center", va="center", fontsize=9, fontweight="bold", color="navy")

ax.set_xlabel("Tegangan Input Vin (V)")
ax.set_ylabel("Tegangan Output Vout (V)")
ax.set_title("Anotasi Wilayah Logika Datasheet AT89S52 (Hal. 29) vs Switching Point Vm")
ax.set_xlim(0, 5)
ax.set_ylim(-0.2, 5.3)
ax.grid(True, linestyle=":")
ax.legend(loc="lower left", fontsize=8)

plt.tight_layout()
out_path = "results/plots/vtc_annotated.png"
plt.savefig(out_path, dpi=150)
print(f"Grafik VTC teranotasi berhasil disimpan di: {out_path}")