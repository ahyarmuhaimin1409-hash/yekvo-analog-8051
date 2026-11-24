# Design Review D2.1 — CMOS Inverter Stress & Sensitivity

## 1. Tujuan & Prediksi Awal (Hipotesis)
* **Tujuan:** Menguji sensitivitas kinerja DC dan transient CMOS inverter (model edukasi Level-1) terhadap variasi tegangan suplai ($V_{DD} \in \{5\text{ V}, 4\text{ V}, 3,3\text{ V}\}$), kapasitas beban ($C_{load} \in \{10\text{ pF}, 100\text{ pF}, 500\text{ pF}\}$), rasio kekuatan transistor ($W_p/W_n$), serta gangguan *input slew* lambat ($40\text{ ns}$).
* **Prediksi Awal:** Penurunan $V_{DD}$ akan menggeser titik *switching* $V_m$ turun mendekati $0,5\,V_{DD}$ dan memperbesar *propagation delay* ($t_{pHL}, t_{pLH}$). Sebaliknya, variasi $C_{load}$ tidak akan memengaruhi kurva VTC DC karena kapasitor bersifat rangkaian terbuka pada kondisi DC tunak.

## 2. Tabel Hasil Pengukuran (`results/inverter_stress.csv`)
* **Definisi Threshold:** $V_m$ diukur pada perpotongan $V_{out} = V_{in}$; $t_{pHL}$ & $t_{pLH}$ diukur antar titik $50\%\,V_{DD}$; $t_{fall}$ & $t_{rise}$ diukur antar level $10\%$ dan $90\%\,V_{DD}$.

| Skenario Pengujian | VDD | Cload | Rasio Wp/Wn | Vm | tpHL | tpLH | tfall (90%-10%) | trise (10%-90%) | IDD Peak |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| VDD = 5,0 V (Baseline) | 5,0 V | 100 pF | 20u / 10u | 2,50 V | 28,00 ns | 27,99 ns | 66,50 ns | 66,50 ns | 9,69 mA |
| VDD = 4,0 V | 4,0 V | 100 pF | 20u / 10u | 2,00 V | 38,50 ns | 38,51 ns | 89,50 ns | 89,50 ns | 5,53 mA |
| VDD = 3,3 V | 3,3 V | 100 pF | 20u / 10u | 1,65 V | 52,00 ns | 52,10 ns | 117,50 ns | 117,50 ns | 3,33 mA |
| Cload = 10 pF | 5,0 V | 10 pF | 20u / 10u | 2,50 V | 3,00 ns | 2,99 ns | 6,75 ns | 6,75 ns | 9,61 mA |
| Cload = 100 pF | 5,0 V | 100 pF | 20u / 10u | 2,50 V | 28,00 ns | 27,99 ns | 66,50 ns | 66,50 ns | 9,69 mA |
| Cload = 500 pF | 5,0 V | 500 pF | 20u / 10u | 2,50 V | 138,00 ns | 130,00 ns | 332,00 ns | 332,00 ns | 9,67 mA |
| Rasio 1:1 (PMOS Lemah) | 5,0 V | 100 pF | 10u / 10u | 2,21 V | 28,00 ns | 55,49 ns | 66,50 ns | 132,50 ns | 4,85 mA |
| Rasio 2:1 (Simetris) | 5,0 V | 100 pF | 20u / 10u | 2,50 V | 28,00 ns | 27,99 ns | 66,50 ns | 66,50 ns | 9,69 mA |
| Rasio 4:1 (PMOS Kuat) | 5,0 V | 100 pF | 40u / 10u | 2,79 V | 28,00 ns | 13,93 ns | 66,50 ns | 33,00 ns | 19,37 mA |
| Fault: Slow Slew 40 ns | 5,0 V | 100 pF | 20u / 10u | 2,50 V | 36,50 ns | 36,50 ns | 68,00 ns | 68,00 ns | 9,48 mA |

## 3. Interpretasi Mekanisme Fisika & Trade-Off
1. **Sensitivitas Tegangan Suplai ($V_{DD}$):** Penurunan $V_{DD}$ ($5\text{ V} \rightarrow 3,3\text{ V}$) menurunkan tegangan *gate-source overdrive* ($V_{GS} - V_{TO}$), sehingga arus pengisian/pengosongan kapasitor menyusut dan *delay* naik hampir $2\times$ lipat ($28,00\text{ ns} \rightarrow 52,00\text{ ns}$). *Noise margin* ikut menyempit ($V_m: 2,50\text{ V} \rightarrow 1,65\text{ V}$), namun konsumsi daya dinamis ($P \propto V_{DD}^2$) turun signifikan.
2. **Dampak Kapasitansi Beban ($C_{load}$):** Waktu transisi berbanding lurus dengan kapasitas beban ($t_p \propto C_{load}$, naik dari $3,00\text{ ns}$ pada $10\text{ pF}$ menjadi $138,00\text{ ns}$ pada $500\text{ pF}$), sedangkan kurva VTC DC tetap identik ($V_m = 2,50\text{ V}$) karena kapasitor bersifat *open-circuit* pada kondisi DC.
3. **Rasio Kekuatan Transistor ($W_p/W_n$):** Memperbesar lebar PMOS ($W_p = 40\,\mu\text{m}$) menurunkan resistansi kanal sehingga mempercepat transisi naik ($t_{pLH}$ turun menjadi $13,93\text{ ns}$), dengan kompromi lonjakan arus puncak $I_{DD}$ ($19,37\text{ mA}$), area silikon lebih besar, dan pergeseran $V_m$ ke $2,79\text{ V}$.
4. **Fault Test — Slow Input Slew ($40\text{ ns}$):** Sinyal input yang melandai lambat memperlambat *delay* ($28,00\text{ ns} \rightarrow 36,50\text{ ns}$) dan menahan PMOS serta NMOS aktif bersamaan lebih lama di wilayah transisi, memperbesar energi arus hubung singkat (*crowbar current*).

## 4. Batasan Model (Acceptance Gate)
* Seluruh simulasi menggunakan model MOS Level-1 edukasi ($V_{TO} = \pm 0,8\text{ V}$) dan bukan replika silikon internal IC AT89S52; efek kanal pendek, kebocoran *subthreshold*, dan variasi temperatur tidak dimodelkan di sini.