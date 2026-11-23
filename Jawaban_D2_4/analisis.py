import csv
import numpy as np
import matplotlib.pyplot as plt
ac=np.loadtxt('ac.dat')
tr=np.loadtxt('transient.dat')
freq=ac[:,0];t=tr[:,0];mask=t>=.02
freqs=[100,10000]
def basis(t):
    cols=[np.ones(len(t))]
    for f in freqs:cols.extend([np.sin(2*np.pi*f*t),np.cos(2*np.pi*f*t)])
    return np.column_stack(cols)
X=basis(t[mask]); curves=[]; summary=[];bode=[]
fig,axes=plt.subplots(2,1,figsize=(10,7),layout='constrained')
for ax,(l,h) in zip(axes,[(20,40),(29.8,30.5)]):
    keep=(t*1000>=l)&(t*1000<=h)
    ax.plot(t[keep]*1000,tr[keep,1],color='#888',lw=1,label='Masukan')
for j,(rs,fc) in enumerate((r,f) for r in [0,10000] for f in [200,1000,5000]):
    z=ac[:,2*j+1]+1j*ac[:,2*j+2];g=np.abs(z);p=np.angle(z,deg=True)
    R=1e4;L=1e6;C=1/(2*np.pi*R*fc);S=R+rs;K=L/(L+S);tau=(L*S/(L+S))*C;fa=1/(2*np.pi*tau)
    fs=np.exp(np.interp(K/np.sqrt(2),g[::-1],np.log(freq[::-1])))
    pred=K/(1+1j*freq/fa)
    assert np.max(abs(g/abs(pred)-1))<.001 and np.max(abs(p-np.angle(pred,deg=True)))<.05 and abs(fs/fa-1)<.001
    for f,gm,pm,pr in zip(freq,g,p,pred):
        bode.append([rs,fc,f,gm,20*np.log10(gm),pm,abs(pr),np.angle(pr,deg=True),1/np.sqrt(1+(f/fc)**2)])
    y=tr[:,j+2];coef=np.linalg.lstsq(X,y[mask],rcond=None)[0]
    if rs==0:
        for ax,(l,h) in zip(axes,[(20,40),(29.8,30.5)]):
            keep=(t*1000>=l)&(t*1000<=h)
            ax.plot(t[keep]*1000,y[keep],label=f'fc {fc} Hz')
    for k,(f,ain) in enumerate(zip(freqs,[.3,.02])):
        a,b=coef[1+2*k:3+2*k];at=np.hypot(a,b);pt=np.degrees(np.arctan2(b,a));i=np.argmin(abs(freq-f));gp=abs(pred[i]);phi=np.angle(pred[i],deg=True)
        assert abs(at/(ain*gp)-1)<.002 and abs(pt-phi)<.1
        summary.append([rs,fc,C*1e9,K,fa,fs,tau*1e3,4.60517*tau*1e3,f,ain/np.sqrt(1+(f/fc)**2)*1000,ain*gp*1000,ain*g[i]*1000,at*1000,p[i],pt,100*(at/(ain*gp)-1)])
def write(name,head,rows):
    with open(name,'w',newline='') as fp:
        w=csv.writer(fp);w.writerow(head.split());w.writerows([[float(f'{v:.10g}') for v in row] for row in rows])
write('filter_bode.csv','Rs_ohm fc_target_Hz freq_Hz gain_AC_VperV gain_AC_dB phase_AC_deg gain_loaded_calc phase_loaded_calc_deg gain_ideal_unloaded',bode)
write('hasil_ukur.csv','Rs_ohm fc_target_Hz C_nF K_DC fc_calc_Hz fc_AC_Hz tau_ms t_settle_1pct_ms tone_Hz A_ideal_mVpk A_loaded_calc_mVpk A_AC_mVpk A_tran_mVpk phase_AC_deg phase_tran_deg err_tran_pct',summary)
for ax,title in zip(axes,['Dua periode sinyal sensor','Detail riak 10 kHz di sekitar persilangan sinyal sensor']):
    ax.set(title=title,xlabel='Waktu (ms)',ylabel='Tegangan (V)');ax.grid(alpha=.2);ax.legend(ncol=4,fontsize=9)
fig.suptitle('Respons terhadap stimulus dua nada • Rs = 0 Ω, beban 1 MΩ')
fig.savefig('transient_overlay.png',dpi=170)
