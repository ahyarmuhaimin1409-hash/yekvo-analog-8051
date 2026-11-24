import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt("results/inverter_noise_fault.csv")
t = data[:, 0] * 1e9      # kolom 0: waktu (detik ke ns)
vin = data[:, 1]          # kolom 1: v(in)
vout = data[:, 3]         # kolom 3: v(out)
idd = data[:, 5] * 1e3    # kolom 5: idd (A ke mA)

print("=== HASIL FAULT TEST D1.3 (INPUT DI SEKITAR Vm = 2.5V) ===")
print(f"Rentang Vin (noise)  : {np.min(vin):.2f} V s.d. {np.max(vin):.2f} V")
print(f"Ayunan Vout          : {np.min(vout):.2f} V s.d. {np.max(vout):.2f} V")
print(f"Arus IDD minimum     : {np.min(idd):.3f} mA (tidak pernah 0 mA!)")
print(f"Arus IDD maksimum    : {np.max(idd):.3f} mA")

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8.5, 5.5), sharex=True)
ax1.plot(t, vin, "k--", label="Vin (2.5V ± 0.3V Noise)")
ax1.plot(t, vout, "b-", linewidth=1.8, label="Vout (Osilasi / Chattering)")
ax1.set_ylabel("Tegangan (V)")
ax1.set_title("Konsekuensi Analog Input di Dekat Switching Threshold (Vm = 2.5V)")
ax1.grid(True, linestyle=":")
ax1.legend(loc="upper right")

ax2.plot(t, idd, "r-", linewidth=1.5, label="Arus Crowbar IDD (mA)")
ax2.set_xlabel("Waktu (ns)")
ax2.set_ylabel("IDD (mA)")
ax2.grid(True, linestyle=":")
ax2.legend(loc="upper right")

plt.tight_layout()
plt.savefig("results/plots/inverter_noise_fault.png", dpi=150)
print("Grafik tersimpan di  : results/plots/inverter_noise_fault.png")