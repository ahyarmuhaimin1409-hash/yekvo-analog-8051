"""Jalankan dari direktori paket setelah menjalankan ngspice."""
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
r = Path("results")
d = np.loadtxt(r / "dc.dat")
t = np.loadtxt(r / "tran.dat")
assert d.shape == (5001, 7) and t.shape[1] == 5
for name, data, fields in [
    ("inverter_vtc", d, "Vin_V,Vout_seimbang_V,Vout_P_lemah_V,Vout_P_kuat_V,Idd_seimbang_A,Idd_P_lemah_A,Idd_P_kuat_A"),
    ("inverter_tran", t, "waktu_s,Vin_V,Vout_V,Idd_A,Inmos_ke_GND_A")
]:
    np.savetxt(r / (name + ".csv"), data, delimiter=",", header=fields, comments="", fmt="%.12g")

fig, (a,b) = plt.subplots(2,1,figsize=(8,7),sharex=True,layout="constrained")
for j, label, color in [(2,"PMOS lemah","#ac481a"),(1,"Seimbang","#12677b"),(3,"PMOS kuat","#654291")]:
    x = d[:,0]
    vm = np.interp(0,(d[:,j]-x)[::-1],x[::-1])
    a.plot(x,d[:,j],label=f"{label}   {vm:.3f} V",color=color)
    a.scatter(vm,vm,color=color)
    b.plot(x,d[:,j+3]*1e6,label=label,color=color)
a.plot(x,x,"--",color="gray",lw=1,label="Vout = Vin")
a.legend(); a.set(ylabel="Vout (V)",title="Karakteristik transfer dan titik switching")
b.set(xlabel="Vin (V)",ylabel="Arus catu DC (µA)")
for ax in (a,b): ax.grid(alpha=.2)
fig.savefig(r/"inverter_vtc.png",dpi=180)
fig, axes = plt.subplots(2,2,figsize=(9,6),layout="constrained")
for k,(start,title) in enumerate([(10,"Vin naik"),(1020,"Vin turun")]):
    ns=t[:,0]*1e9-start
    mask=(ns>=-5)&(ns<=250)
    for j,label in [(1,"Vin"),(2,"Vout")]: axes[0,k].plot(ns[mask],t[mask,j],label=label)
    for j,label in [(3,"Dari VDD"),(4,"Ke GND lewat NMOS")]: axes[1,k].plot(ns[mask],1e3*t[mask,j],label=label)
    axes[0,k].set(title=title,ylabel="Tegangan (V)")
    axes[1,k].set(xlabel="Waktu sejak awal tepi (ns)",ylabel="Arus (mA)")
for ax in axes.flat: ax.grid(alpha=.2); ax.legend(fontsize=8)
fig.savefig(r/"inverter_transien.png",dpi=180)
