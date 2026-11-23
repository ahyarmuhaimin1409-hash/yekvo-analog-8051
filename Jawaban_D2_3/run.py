from pathlib import Path
import csv
import subprocess
import tempfile
import numpy as np

sources = {
    'fast_ramp': ('0 0 1m 5', 0.8, True),
    'slow_ramp': ('0 0 100m 5', 80.0, True),
    'short_dip': ('0 5 10m 5 10.01m 3 10.21m 3 10.22m 5', 10.215, False),
    'quick_restart': ('0 5 10m 5 10.01m 0 10.21m 0 10.22m 5', 10.218, False)
}
def last_fall(t, diff, start):
    k = np.where((diff[:-1] > 0) & (diff[1:] <= 0) & (t[1:] >= start))[0]
    if len(k)==0:
        return None
    j=k[-1]
    return t[j]-diff[j]*(t[j+1]-t[j])/(diff[j+1]-diff[j])
rows=[]
for case,(pwl, valid, cold) in sources.items():
    for cap in [1,10]:
        deck=f"""D2.3 - {case}, {cap} uF
VDD dd 0 PWL({pwl})
Cc dd x {cap}u
Rs x rst 1k
Rext rst 0 10k
Rint rst 0 100k
Dclamp 0 rst DM
.model DM D(IS=1n N=1)
.temp 27
.control
set numdgt=12
set wr_singlescale
tran 2u 380m
wrdata wave.dat v(dd) v(rst)
.endc
.end
"""
        Path("netlists").mkdir(exist_ok=True)
        Path("netlists", f"{case}_{cap}u.cir").write_text(deck)
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp); (p/'reset.cir').write_text(deck)
            subprocess.run(['ngspice','-b','reset.cir','-r','unused.raw'],cwd=p,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,check=True)
            t,v,y=np.loadtxt(p/'wave.dat').T
        t=t*1000
        start=0 if cold else 10.21
        mask=t>=start
        diff=y-.5*v
        crossed=(diff[mask]>0).any()
        assert cold==bool(crossed)
        end=last_fall(t,diff,start)
        high=last_fall(t,y-.7*v,valid)
        clock=valid+8
        overlap=max(0,(high if high is not None else clock)-clock)
        low=last_fall(t,y-(.2*v-.1),valid)
        if np.interp(valid,t,y-(.2*v-.1))<=0: low=valid
        rows.append([case,cap,cap*(1+10*100/110),start,valid,0 if cold else None,end,end if cold else 0,np.max(y[mask]),clock,high,overlap*1000,low,'memenuhi model' if overlap>=.002 else 'tidak terbukti'])
with open('reset_test_matrix.csv','w',newline='') as f:
    w=csv.writer(f);w.writerow('skenario C_uF tau_ms awal_evaluasi_ms t_VCC_valid_ms t_assert50_ms t_release50_ms pulsa50_ms RST_peak_V clock_siap_asumsi_ms akhir_HIGH_terjamin_ms overlap_HIGH_clock_us t_LOW_terjamin_ms status_2us'.split())
    for row in rows:w.writerow([round(v,6) if isinstance(v,(float,np.floating)) else v for v in row])
