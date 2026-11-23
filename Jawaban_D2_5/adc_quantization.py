"""Jalankan dari folder ekstraksi: python adc_quantization.py"""
import csv
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

N = 1024
VIN = 1.5
VREF = 3.3
LSB = VREF/N

def code(v, ref):
    return np.clip(np.floor(np.asarray(v)*N/ref), 0, N-1).astype(int)

def write(name, header, rows):
    with open(name, 'w', newline='', encoding='utf-8') as f:
        w=csv.writer(f)
        w.writerow(header.split())
        w.writerows(rows)

def save(fig, name):
    fig.tight_layout()
    fig.savefig(name, dpi=170)
    plt.close(fig)

def comparator(dt):
    t=np.arange(round(.020/dt)+1)*dt
    ramp=1.3+20*t
    vin=ramp+.03*np.sin(2*np.pi*2000*t)
    plain=(vin>=1.5).astype(int)
    schmitt=np.zeros_like(plain)
    for j in range(1,len(t)):
        if vin[j]>=1.55:
            schmitt[j]=1
        elif vin[j]<=1.45:
            schmitt[j]=0
        else:
            schmitt[j]=schmitt[j-1]
    return t,ramp,vin,plain,schmitt

def run():
    t,ramp,vin,plain,schmitt=comparator(1e-6)
    write('compare_hysteresis.csv','time_s ramp_V noise_V vin_V comparator_bit schmitt_bit',zip(t,ramp,vin-ramp,vin,plain,schmitt))
    edges=[np.count_nonzero(np.diff(y)) for y in [plain,schmitt]]
    fine=comparator(.5e-6)
    assert edges==[np.count_nonzero(np.diff(y)) for y in fine[-2:]]
    print('Transisi total dan tambahan:',edges,[n-1 for n in edges])
    fig,(a,b)=plt.subplots(2,1,figsize=(9,5.7),sharex=True)
    a.plot(t*1000,vin,label='Ramp + gangguan');a.plot(t*1000,ramp,':',label='Ramp bersih')
    for level in [1.45,1.5,1.55]:a.axhline(level,lw=.8,color='gray',ls='--')
    a.set(ylabel='Vin (V)',title='Mengapa satu lintasan ambang memicu beberapa tepi?');a.legend()
    b.step(t*1000,plain,where='post',label='Ambang 1,50 V');b.step(t*1000,schmitt,where='post',ls='--',label='Histeresis 1,45/1,55 V');b.legend();b.set(xlim=(7,14),xlabel='Waktu (ms)',ylabel='Keluaran',yticks=[0,1])
    save(fig,'01_comparator.png')
    assert list(code([-.1,0,1.5,3.3,3.4],3.3))==[0,0,465,1023,1023]
    fig,(a,b)=plt.subplots(1,2,figsize=(10,4))
    for ax,lo,hi in [(a,-.3,3.6),(b,1.485,1.515)]:
        v=np.linspace(lo,hi,5001);ax.step(v,code(v,VREF),where='post');ax.set(xlabel='Vin (V)',ylabel='Kode ADC');ax.grid(alpha=.2)
    a.set_title('Rentang penuh dan clipping');b.set_title('Detail sekitar 1,500 V');b.plot(VIN,465,'ro')
    save(fig,'02_adc.png')
    rows=[]
    for actual in [3.2,3.3]:
        for firmware in [3.2,3.3]:
            raw=int(code(VIN,actual));vhat=raw*firmware/N
            rows.append([VIN,actual,firmware,actual/N,raw,vhat,1000*(vhat-VIN)])
    write('vref_error.csv','vin_V vref_actual_V vref_firmware_V lsb_actual_V raw_code voltage_firmware_V error_mV',rows)
    fig,a=plt.subplots(figsize=(8,4));labels=[f"{r[1]:.2f} / {r[2]:.2f}" for r in rows];bars=a.bar(labels,[r[-1] for r in rows],color=['#378174','#d47647','#d47647','#378174'])
    a.bar_label(bars,labels=[f"{r[-1]:+.2f}" for r in rows],padding=3);a.axhline(0,color='gray',lw=.7);a.set(ylabel='Galat tegangan (mV)',xlabel='Vref aktual / Vref firmware (V)',title='Masukan tetap 1,500 V',ylim=(-57,57));save(fig,'03_vref.png')
    rows=[];fig,a=plt.subplots(figsize=(8,4.5))
    for r in [1000,10000,100000]:
        tau=r*10e-12;tmin=tau*np.log(2.3/(LSB/2))
        us=np.unique(np.r_[np.logspace(-3,1.2,201),.1,.3,1,2,5,10,tmin*1e6])
        err=2.3*np.exp(-us*1e-6/tau);vh=2.8-err
        for ti,e,h in zip(us,err,vh):
            rows.append([r,10,tau*1e6,ti,h,1000*e,e/LSB,int(code(h,VREF)),tmin*1e6,int(ti>=tmin*1e6)])
        a.plot(us,np.where(err/LSB>1e-3,err/LSB,np.nan),label=f'{r/1000:g} kΩ');a.scatter(tmin*1e6,.5,s=24)
    write('mux_settling.csv','Rsrc_ohm Cs_pF tau_us tacq_us Vhold_V error_mV error_LSB code_held tmin_half_LSB_us pass_half_LSB',rows)
    a.axhline(.5,color='#555',ls='--',label='½ LSB');a.set(xscale='log',yscale='log',xlabel='Waktu akuisisi (µs)',ylabel='Galat settling (LSB)',title='Perpindahan kanal 0,5 → 2,8 V, Cs = 10 pF');a.legend();a.grid(which='major',alpha=.2);save(fig,'04_mux.png')

if __name__=='__main__':
    run()
