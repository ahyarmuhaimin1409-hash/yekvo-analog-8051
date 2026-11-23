from pathlib import Path
from tempfile import TemporaryDirectory
from itertools import product
import subprocess
import csv
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def cross(x,y,value,rising=True):
    hits=np.where(((y[:-1]<value)&(y[1:]>=value)) if rising else ((y[:-1]>value)&(y[1:]<=value)))[0]
    if len(hits)!=1: raise ValueError((value,hits))
    j=hits[0]
    return x[j]+(value-y[j])*(x[j+1]-x[j])/(y[j+1]-y[j])

def simulate(v,c,k,slew):
    deck=f"""D2.1 CMOS inverter
VDD dd 0 {v}
VIN in 0 DC 0 PULSE(0 {v} 100n {slew}n {slew}n 3u 7u)
MN out in 0 0 NM W=10u L=1u
MP out in dd dd PM W={20*k}u L=1u
.model NM NMOS(level=1 VTO=0.8 KP=100u LAMBDA=0.04)
.model PM PMOS(level=1 VTO=-0.8 KP=50u LAMBDA=0.04)
CL out 0 {c}p
.temp 27
.options reltol=1e-6
.control
set wr_singlescale
set numdgt=12
dc VIN 0 {v} {v/2000}
wrdata dc.dat v(out)
tran 0.2n 6.9u
wrdata tr.dat v(in) v(out) i(VDD)
quit
.endc
.end
"""
    with TemporaryDirectory() as folder:
        p=Path(folder);(p/'inverter.cir').write_text(deck)
        subprocess.run(['ngspice','-n','-b','inverter.cir'],cwd=p,stdout=subprocess.DEVNULL,check=True)
        x,y=np.loadtxt(p/'dc.dat').T
        t,vin,out,ineg=np.loadtxt(p/'tr.dat').T
    if (v,c,k,slew)==(5,100,1,1):Path('inverter_nominal.cir').write_text(deck)
    slope=np.gradient(y,x);mid=np.argmin(slope)
    vil=cross(x[:mid+1],slope[:mid+1],-1,False);vih=cross(x[mid:],slope[mid:],-1)
    vol=np.interp(vih,x,y);voh=np.interp(vil,x,y)
    vm=cross(x,y-x,0,False)
    ns=t*1e9;ma=-ineg*1000
    down=ns<3000;up=~down
    def outedge(f,rise):
        m=up if rise else down
        return cross(ns[m],out[m],v*f,rise)
    tf=outedge(.1,False)-outedge(.9,False);tr=outedge(.9,True)-outedge(.1,True)
    phl=outedge(.5,False)-cross(ns[down],vin[down],v*.5)
    plh=outedge(.5,True)-cross(ns[up],vin[up],v*.5,False)
    assert max(out[-1]-v,v-out[-1]) < .001*v and min(tr,tf)>0
    energy=np.trapezoid(ma*v,ns);efall=np.trapezoid(ma[down]*v,ns[down])
    row=[v,c,k,slew,vm,vil,vih,vol,voh,vil-vol,voh-vih,tr,tf,plh,phl,max(ma[down]),max(ma[up]),efall,energy,energy/7000]
    return row,(x,y,ns,vin,out,ma)

figs=[plt.subplots(1,3,figsize=(13,4),layout='constrained') for _ in range(2)]
f3,aa=plt.subplots(2,1,figsize=(8,6),sharex=True,layout='constrained')
rows=[]
for v,c,k,s in product([5,4,3.3],[10,100,500],[.5,1,2],[1,100]):
    row,(x,y,t,vin,out,ma)=simulate(v,c,k,s);rows.append(row)
    if c==100 and s==1:
        ax=figs[0][1][[5,4,3.3].index(v)];ax.plot(x,y,label=f'βp/βn = {k:g}');ax.plot(row[4],row[4],'k.',ms=4);ax.set_title(f'VDD = {v:g} V')
    if v==5 and k==1 and s==1:
        axes=figs[1][1]
        for ax,mask,ref in [(axes[0],(t>=98)&(t<500),100),(axes[1],(t>=3099)&(t<3501),3101)]:
            ax.plot(t[mask]-ref,out[mask],label=f'{c} pF')
        axes[2].plot(c,row[13],'o',color='teal');axes[2].plot(c,row[14],'x',color='darkorange')
    if v==5 and k==1 and c==100:
        mask=(t>=95)&(t<255)
        aa[0].plot(t[mask]-100,vin[mask],label=f'Vin • {s} ns');aa[1].plot(t[mask]-100,ma[mask],label=f'slew {s} ns')
head='VDD_V Cload_pF betaP_betaN input_edge_0_100_ns VM_V VIL_model_V VIH_model_V VOL_model_V VOH_model_V NML_model_V NMH_model_V tr_ns tf_ns tpLH_ns tpHL_ns Idd_peak_out_fall_mA Idd_peak_out_rise_mA E_out_fall_pJ E_cycle_pJ P_at_period7us_mW'.split()
with open('inverter_stress.csv','w',newline='') as f:
    w=csv.writer(f);w.writerow(head);w.writerows([[float(f'{v:.9g}') for v in r] for r in rows])
for ax in figs[0][1]:
    ax.set(xlabel='Vin (V)',ylabel='Vout (V)');ax.legend(fontsize=8)
for i,ax in enumerate(figs[1][1][:2]):
    ax.set(title=['Keluaran turun','Keluaran naik'][i],xlabel='Waktu sejak tepi input mulai (ns)',ylabel='Vout (V)');ax.legend()
ax=figs[1][1][2];ax.plot([],[],'o',color='teal',label='tpLH');ax.plot([],[],'x',color='darkorange',label='tpHL');ax.legend();ax.set(xlabel='Cload (pF)',ylabel='Delay (ns)',title='Delay di 50% VDD')
aa[0].set_ylabel('Vin (V)');aa[1].set(xlabel='Waktu sejak input mulai naik (ns)',ylabel='Arus dari VDD (mA)')
for ax in aa:ax.legend()
for fig,axes,title,name in [(*figs[0],'VTC untuk tiga kekuatan PMOS • titik hitam: Vin = Vout','01_vtc'),(*figs[1],'Pengaruh beban • 5 V, βp/βn = 1, slew 1 ns','02_beban'),(f3,aa,'Arus catu ketika keluaran turun • 5 V, 100 pF, βp/βn = 1','03_arus_slew')]:
    for ax in axes:ax.grid(alpha=.18)
    fig.suptitle(title);fig.savefig(name+'.png',dpi=160);plt.close(fig)
