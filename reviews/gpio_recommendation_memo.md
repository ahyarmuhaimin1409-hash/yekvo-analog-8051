# Engineering Recommendation Memo — D2.2: GPIO Drive, Fanout & Interface Limits

**Proyek:** `yekvo-analog-8051` (AT89S52 GPIO Interface)  
**Bukti Simulasi & Data:** `spice/gpio_d22.cir`, `results/gpio_tradeoff.csv`, `results/plots/d22_capacitive_fault.png`

---

## 1. Prediksi Awal & Jawaban Intuisi
* **Jawaban Intuisi:** Meskipun firmware telah menulis bit logika `1` atau `0` dengan benar ke register port, pin GPIO dapat mengalami kegagalan pembacaan bit maupun kerusakan kelistrikan apabila konstanta waktu pengisian $RC$ ($\tau = R_{\text{pullup}} \cdot C_{\text{load}}$) lebih lambat daripada waktu *sampling* sinyal, atau arus *sink* saat output LOW ($I_{\text{sink}}$) melampaui batas maksimum port pada datasheet AT89S52.
* **Prediksi Awal (Terbukti):** Resistor *pull-up* tercepat ($1\text{ k}\Omega$) memberikan *bandwidth* paling tinggi, tetapi belum tentu paling aman karena menarik arus *sink* sebesar $4,440\text{ mA}$ yang mendorong $V_{OL}$ naik di atas batas datasheet $0,45\text{ V}$. Sementara itu, beban kapasitif berlebih ($4,7\text{ nF}$) menahan tegangan di bawah ambang $V_{IH(\min)} = 1,90\text{ V}$ sehingga *sampling* sinyal gagal.

---

## 2. Tabel Hasil Pengukuran & Bandwidth Praktis (`results/gpio_tradeoff.csv`)
* **Rumus Perhitungan:**
  * Arus *sink* kondisi LOW:
    $$I_{\text{sink}} = \frac{V_{DD} - V_{OL}}{R_{\text{pullup}}}$$
  * Estimasi waktu mencapai $70\%\,V_{DD}$ ($3,50\text{ V}$):
    $$t_{70\%(\text{est})} = R_{\text{pullup}} \cdot C_{\text{load}} \cdot \ln\left(\frac{V_{DD} - V_{OL}}{V_{DD} - 3,50\text{ V}}\right)$$
  * Bandwidth *cutoff* $-3\text{ dB}$ dan frekuensi pulsa maksimum praktis (*duty cycle* $50\%$):
    $$BW_{-3\text{dB}} = \frac{1}{2\pi \cdot R_{\text{pullup}} \cdot C_{\text{load}}}, \qquad f_{\max,\text{praktis}} = \frac{1}{2 \cdot t_{70\%(\text{sim})}}$$

| $R_{\text{pullup}}$ | $C_{\text{load}}$ | $V_{OL}$ | $I_{\text{sink}}$ (LOW) | $t_{70\%}$ Teori | $t_{70\%}$ Simulasi | $BW_{-3\text{dB}}$ | $f_{\max}$ Praktis | Evaluasi Datasheet AT89S52 (Hal. 29) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| $1\text{ k}\Omega$ | $20\text{ pF}$ | $0,560\text{ V}$ | $4,440\text{ mA}$ | $21,7\text{ ns}$ | $22,0\text{ ns}$ | $7957,7\text{ kHz}$ | $22727,3\text{ kHz}$ | Melampaui uji Port 0 ($I_{\text{sink}} > 3,2\text{ mA}$, $V_{OL} > 0,45\text{ V}$) |
| $1\text{ k}\Omega$ | $100\text{ pF}$ | $0,560\text{ V}$ | $4,440\text{ mA}$ | $108,5\text{ ns}$ | $108,6\text{ ns}$ | $1591,5\text{ kHz}$ | $4604,0\text{ kHz}$ | Melampaui uji Port 0 ($I_{\text{sink}} > 3,2\text{ mA}$, $V_{OL} > 0,45\text{ V}$) |
| $1\text{ k}\Omega$ | $1\text{ nF}$ | $0,560\text{ V}$ | $4,440\text{ mA}$ | $1085,2\text{ ns}$ | $1086,0\text{ ns}$ | $159,2\text{ kHz}$ | $460,4\text{ kHz}$ | Melampaui uji Port 0 ($I_{\text{sink}} > 3,2\text{ mA}$, $V_{OL} > 0,45\text{ V}$) |
| $4,7\text{ k}\Omega$ | $20\text{ pF}$ | $0,125\text{ V}$ | $1,037\text{ mA}$ | $110,8\text{ ns}$ | $112,1\text{ ns}$ | $1693,1\text{ kHz}$ | $4460,3\text{ kHz}$ | Aman & Kompatibel ($V_{OL} \le 0,45\text{ V}$, $I_{\text{sink}} \le 1,6\text{ mA}$) |
| $4,7\text{ k}\Omega$ | $100\text{ pF}$ | $0,125\text{ V}$ | $1,037\text{ mA}$ | $554,0\text{ ns}$ | $556,1\text{ ns}$ | $338,6\text{ kHz}$ | $899,1\text{ kHz}$ | Aman & Kompatibel (ideal untuk bus $\text{I}^2\text{C}$ $100\text{–}400\text{ kHz}$) |
| $4,7\text{ k}\Omega$ | $1\text{ nF}$ | $0,125\text{ V}$ | $1,037\text{ mA}$ | $5539,6\text{ ns}$ | $5542,1\text{ ns}$ | $33,9\text{ kHz}$ | $90,2\text{ kHz}$ | Aman arus, namun kecepatan terbatas ($\le 90\text{ kHz}$) |
| $10\text{ k}\Omega$ | $20\text{ pF}$ | $0,059\text{ V}$ | $0,494\text{ mA}$ | $238,4\text{ ns}$ | $240,1\text{ ns}$ | $795,8\text{ kHz}$ | $2082,5\text{ kHz}$ | Aman & Kompatibel (paling hemat daya) |
| $10\text{ k}\Omega$ | $100\text{ pF}$ | $0,059\text{ V}$ | $0,494\text{ mA}$ | $1192,1\text{ ns}$ | $1194,1\text{ ns}$ | $159,2\text{ kHz}$ | $418,7\text{ kHz}$ | Aman & Kompatibel (aman untuk sinyal $\le 100\text{ kHz}$) |
| $10\text{ k}\Omega$ | $1\text{ nF}$ | $0,059\text{ V}$ | $0,494\text{ mA}$ | $11920,7\text{ ns}$ | $11922,1\text{ ns}$ | $15,9\text{ kHz}$ | $41,9\text{ kHz}$ | Sangat lambat — hanya untuk sinyal $\le 40\text{ kHz}$ |

---

## 3. Perbandingan Terhadap Level Tegangan & Batas Arus Datasheet AT89S52 (Hal. 29)
1. **Perbandingan Tegangan ($V_{OL}$ vs $V_{IL} = 0,90\text{ V}$ & $V_{OH}$ vs $V_{IH} = 1,90\text{ V}$):**
   * $R_{\text{pullup}} = 1\text{ k}\Omega$ menghasilkan $V_{OL} = 0,560\text{ V}$ (melanggar jaminan datasheet $V_{OL(\max)} = 0,45\text{ V}$ dan menyisakan $NM_L = 0,340\text{ V}$).
   * $R_{\text{pullup}} = 4,7\text{ k}\Omega$ ($V_{OL} = 0,125\text{ V}$, $NM_L = 0,775\text{ V}$) dan $10\text{ k}\Omega$ ($V_{OL} = 0,059\text{ V}$, $NM_L = 0,841\text{ V}$) memenuhi spesifikasi $V_{OL} \le 0,45\text{ V}$ dengan margin *noise* yang lebar.
   * Pada sisi HIGH, saat sinyal mencapai $70\%\,V_{DD}$ ($3,50\text{ V}$), ketiganya memberikan margin $NM_H = 3,50\text{ V} - 1,90\text{ V} = 1,60\text{ V}$ di atas ambang penerima $V_{IH(\min)} = 1,90\text{ V}$.
2. **Perbandingan Batas Arus (*Current Limits*) & *Fanout*:**
   * Datasheet AT89S52 membatasi arus uji $V_{OL} \le 0,45\text{ V}$ pada **$3,2\text{ mA}$** (Port 0) dan **$1,6\text{ mA}$** (Ports 1–3), serta batas maksimum mutlak **$10\text{ mA/pin}$**, **$26\text{ mA}$ total 8-bit Port 0**, dan **$15\text{ mA}$ total 8-bit Ports 1–3**.
   * Konfigurasi $1\text{ k}\Omega$ ($4,440\text{ mA/pin}$) gagal memenuhi arus uji Port 0 dan mencapai **$35,52\text{ mA}$** jika 8 pin LOW bersamaan ($> 26\text{ mA}$). Sebaliknya, $4,7\text{ k}\Omega$ ($8,30\text{ mA}$ untuk 8 pin) dan $10\text{ k}\Omega$ ($3,95\text{ mA}$ untuk 8 pin) aman di seluruh kondisi.
   * Karena arus bocor input penerima sangat kecil ($I_{IL} = -50\,\mu\text{A}$ pada Ports 1–3, $I_{LI} = \pm 10\,\mu\text{A}$ pada Port 0), batas *fanout* praktis ditentukan oleh akumulasi kapasitansi pin ($C_{IO} = 10\text{ pF/pin}$) dan jalur PCB, bukan arus DC.

---

## 4. Rekomendasi Eksplisit Resistor Pull-Up (Suplai $V_{DD} = 5,0\text{ V}$)

| Profil Aplikasi | Rekomendasi $R_{\text{pullup}}$ | Batas Beban ($C_{\text{load}}$) | Batas Frekuensi ($f_{\max}$) | Batas Arus & Jumlah Pin LOW Bersamaan |
| :--- | :--- | :--- | :--- | :--- |
| **Bus Standar & Antarmuka Umum ($\text{I}^2\text{C}$ $100\text{–}400\text{ kHz}$)** | **$4,7\text{ k}\Omega$** *(Utama)* | $\le 100\text{ pF}$ | $\le 400\text{ kHz}$ | $I_{\text{sink}} = 1,037\text{ mA/pin}$; aman hingga **8 pin LOW bersamaan** ($8,30\text{ mA} \le 26\text{ mA}$). |
| **Sinyal Lambat & Hemat Daya (Tombol, Sensor Statik)** | **$10\text{ k}\Omega$** | $\le 100\text{ pF}$ (menengah) / $\le 1\text{ nF}$ (lambat) | $\le 100\text{ kHz}$ ($100\text{ pF}$) / $\le 40\text{ kHz}$ ($1\text{ nF}$) | $I_{\text{sink}} = 0,494\text{ mA/pin}$; aman hingga **8 pin LOW bersamaan** ($3,95\text{ mA}$). |
| **Jalur Cepat / Beban Kapasitif Menengah ($100\text{–}500\text{ pF}$)** | **$1,5\text{ k}\Omega \text{–} 2,2\text{ k}\Omega$** *(Hindari $\le 1\text{ k}\Omega$)* | $\le 500\text{ pF}$ | $\le 500\text{ kHz} \text{–} 1\text{ MHz}$ | Wajib menjaga $I_{\text{sink}} \le 3,2\text{ mA/pin}$ (Port 0) atau $\le 1,6\text{ mA/pin}$ (Ports 1–3); maks **4–8 pin LOW** pada Port 0. |

---

## 5. Bukti Fault Test & Residual Risk (Acceptance Gate)
1. **Bukti Kegagalan Beban Kapasitif (`results/plots/d22_capacitive_fault.png`):** Saat jalur sinyal $100\text{ kHz}$ (pulsa HIGH $5\,\mu\text{s}$) dibebani $C_{\text{load}} = 4,7\text{ nF}$, tegangan $10\text{ k}\Omega$ hanya mencapai **$\approx 0,55\text{ V}$** dan $4,7\text{ k}\Omega$ hanya mencapai **$\approx 1,12\text{ V}$** — keduanya gagal melewati $V_{IH(\min)} = 1,90\text{ V}$ sehingga *sampling* bit oleh penerima gagal total.
2. **Kondisi Batas (*Boundary Conditions*):** Rekomendasi $4,7\text{ k}\Omega$ hanya valid pada $V_{CC} = 5,0\text{ V} \pm 10\%$, total kapasitansi jalur $C_{\text{load}} \le 100\text{ pF}$, frekuensi $\le 400\text{ kHz}$, dan total arus *sink* port tidak melampaui batas datasheet ($26\text{ mA}$ Port 0 / $15\text{ mA}$ Ports 1–3).
3. **Residual Risk:**
   * Nilai $V_{OL}$ dan waktu transisi diperoleh dari model edukasi NMOS Level-1 ($W = 20\,\mu\text{m}, L = 1\,\mu\text{m}$), bukan transistor silikon asli AT89S52; pada temperatur tinggi ($+85^\circ\text{C}$), resistansi kanal nyata dapat meningkat sehingga $V_{OL}$ aktual berpotensi lebih tinggi.
   * Simulasi hanya memodelkan beban kapasitif murni tanpa induktansi jalur PCB (*trace inductance*), *crosstalk*, maupun *ground bounce* saat banyak pin beralih bersamaan.