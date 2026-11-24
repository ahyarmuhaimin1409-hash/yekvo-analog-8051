import numpy as np

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
