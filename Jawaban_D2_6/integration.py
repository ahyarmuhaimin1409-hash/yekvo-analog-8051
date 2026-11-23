from pathlib import Path
import csv
import numpy as np
from matplotlib import pyplot as plt

dt=.1e-6
t=np.arange(40001)*dt
sensor=np.where(np.arange(len(t))>=10000,2.8,.5)+.020*np.sin(2*np.pi*10000*t)
# Tegangan filter dipertahankan selama reset digital.
tau_f=1/(2*np.pi*1000)
y=np.empty_like(t);y[0]=.5
for i in range(1,len(t)):
    y[i]=sensor[i]+(y[i-1]-sensor[i])*np.exp(-dt/tau_f)
idx=np.arange(len(t))
dip=(idx>=24000)&(idx<27000)
vdd=np.where(dip,2.9,3.2)
reset=(idx>=24000)&(idx<29000)
cp=np.zeros(len(t),int);ev=np.zeros(len(t),int)
for i in range(1,len(t)):
    if reset[i]:continue
    if y[i]>=1.55:cp[i]=1
    elif y[i]<=1.45:cp[i]=0
    else:cp[i]=cp[i-1]
    if not reset[i-1]:ev[i]=int(cp[i]>cp[i-1])
def q(v,ref):return int(np.clip(np.floor(1024*v/ref),0,1023))
def decision(v):return 'LOW' if v<2.70 else 'HIGH' if v>2.85 else 'IN_RANGE'
rows=[]
for mode,track,fw in [('nominal',10,3.2),('short_acq',1,3.2),('wrong_vref',10,3.3)]:
    for i in range(500,40000,1000):
        # Sampling (akhir track) identik antar kasus.
        steps=int(round(track*1e-6/dt))
        valid=not reset[i-steps:i+41].any()
        h=.5 # kanal pendahulu digerakkan oleh sumber 0,5 V berimpedansi rendah
        for k in range(i-steps+1,i+1):
            h=y[k]+(h-y[k])*np.exp(-dt/1e-6)
        raw=q(h,vdd[i]) if valid else None
        measured=raw*fw/1024 if valid else None
        expected=decision(y[i])
        rows.append([mode,t[i]*1e3,t[i+40]*1e3,sensor[i],y[i],vdd[i],int(reset[i]),int(valid),track,.5,h if valid else None,(h-y[i])*1000 if valid else None,vdd[i],fw,q(y[i],vdd[i]) if valid else None,raw,measured,decision(measured) if valid else 'INHIBIT',expected if valid else 'INHIBIT',int(cp[i]) if valid else None,int(ev[max(0,i-999):i+1].sum())])
head='mode t_hold_ms t_read_ms sensor_V filter_V VDD_V reset_active valid t_acq_us prev_channel_V hold_V settling_error_mV Vref_actual_V Vref_fw_V ideal_code_at_filter raw_code fw_V decision expected_decision cp0_bit cp0_rises_since_prev'.split()
with open('integration_results.csv','w',newline='') as f:
    w=csv.writer(f);w.writerow(head);w.writerows(rows)
with open('events.csv','w',newline='') as f:
    w=csv.writer(f);w.writerow(['time_ms','filter_V','event'])
    for i in np.flatnonzero(ev):w.writerow([t[i]*1000,y[i],'CP0_rising'])
fig,ax=plt.subplots(3,1,figsize=(10,8),sharex=True,layout='constrained')
ax[0].plot(t*1000,sensor,label='Sensor',alpha=.65);ax[0].plot(t*1000,y,label='Filter');ax[0].legend();ax[0].set_ylabel('Tegangan (V)')
for mode in ['nominal','short_acq','wrong_vref']:
    subset=[r for r in rows if r[0]==mode];ax[1].plot([r[1] for r in subset],[r[16] if r[7] else np.nan for r in subset],'.-',label=mode)
ax[1].axhspan(2.70,2.85,color='green',alpha=.12);ax[1].legend(fontsize=8);ax[1].set_ylabel('Laporan ADC (V)')
ax[2].step(t*1000,cp,where='post',label='CP0');ax[2].step(t*1000,reset.astype(float),where='post',ls='--',label='Reset aktif');ax[2].scatter(t[ev==1]*1000,cp[ev==1],color='red',label='Event naik');ax[2].legend();ax[2].set(xlabel='Waktu (ms)',ylabel='Bit')
for a in ax:a.axvspan(2.4,2.9,color='gray',alpha=.12);a.grid(alpha=.2)
fig.savefig('trace.png',dpi=165)
assert sum(ev)==1
assert all((r[15] is None and r[17]=='INHIBIT') for r in rows if not r[7])
for r in rows:
    if abs(r[1]-2.15)<1e-7:print(r)
assert all(r[17]==r[18] for r in rows if r[0]=='nominal')
