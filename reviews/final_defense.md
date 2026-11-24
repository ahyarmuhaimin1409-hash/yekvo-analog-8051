# Engineering Defense & Cross-Examination (WBS D2.8)

- **Engineer / Owner:** Zulfa Maylafaiza
- **Peer Reviewer:** Ahyar Muhaimin
- **Cakupan Domain:** Transistor, CMOS Inverter, Noise Margin & GPIO Open-Drain (D1.2, D1.3, D1.4, D2.1, D2.2)
- **Target Referensi:** Microchip/Atmel AT89S52 (`doc1919.pdf`, Hal. 29) & Model Edukasi MOS Level-1

---

## 1. Materi Presentasi 6 Menit (4 Pilar Wajib)

### A. Satu Grafik Utama (`results/plots/d22_capacitive_fault.png` & `results/plots/d21_overlay3_slow_slew.png`)
- **Grafik:** Respons transien *open-drain* GPIO pada beban kapasitif berat ($C_{\text{load}} = 4.7\text{ nF}$, sinyal $100\text{ kHz}$, $T_{\text{high}} = 5\ \mu\text{s}$) dibandingkan dengan kurva *pull-up* $1\text{ k}\Omega$, $4.7\text{ k}\Omega$, dan $10\text{ k}\Omega$[cite: 2].
- **Penjelasan Fisika:** Logika 1 pada *open-drain* tidak digerakkan secara aktif ke $V_{DD}$, melainkan diisi secara eksponensial melalui konstanta waktu $\tau = R_{\text{pullup}} \cdot C_{\text{load}}$[cite: 2]. Ketika $\tau$ terlalu besar ($4.7\text{ k}\Omega \times 4.7\text{ nF} = 22.09\ \mu\text{s}$), tegangan pin tertahan di $1.12\text{ V}$ (zona *undefined* AT89S52: $0.90\text{ V} - 1.90\text{ V}$) saat jendela *sampling* berakhir[cite: 2].

### B. Satu Prediksi Awal yang Meleset & Koreksinya
- **Prediksi Awal:** Resistor *pull-up* terkecil ($R_{\text{pullup}} = 1\text{ k}\Omega$) dianggap selalu menjadi pilihan terbaik karena menghasilkan *rise time* paling cepat ($45.0\text{ ns}$ pada $20\text{ pF}$, mendekati kurva *push-pull* ideal)[cite: 2].
- **Root Cause & Koreksi:** Data simulasi membuktikan $R_{\text{pullup}} = 1\text{ k}\Omega$ menarik arus *sink* $I_{\text{sink}} = 4.440\text{ mA}$ saat kondisi LOW, yang mendorong $V_{OL}$ naik ke $0.560\text{ V}$—melanggar batas jaminan datasheet AT89S52 ($V_{OL(\max)} = 0.45\text{ V}$ pada $I_{OL} = 3.2\text{ mA}$ untuk Port 0, Hal. 29) dan memangkas $NML$ dari $0.45\text{ V}$ menjadi $0.340\text{ V}$[cite: 2].

### C. Satu Counterexample yang Merusak Asumsi Desain
- **Counterexample:** Jika seluruh 8 pin pada satu port (Port 0 atau Ports 1–3) menarik logika LOW secara bersamaan menggunakan $R_{\text{pullup}} = 1\text{ k}\Omega$, total arus *sink* mencapai $8 \times 4.440\text{ mA} = 35.52\text{ mA}$[cite: 2].
- **Dampak Fisika:** Angka ini melanggar batas maksimum mutlak datasheet AT89S52 (Notes 1, Hal. 29) sebesar $26\text{ mA}$ total per 8-bit Port 0 (dan $15\text{ mA}$ untuk Ports 1–3), yang berisiko merusak *driver* NMOS internal maupun memicu *ground bounce*[cite: 2].

### D. Satu Keputusan Desain Final (8 Komponen Lampiran C)
- **Konfigurasi Pilihan:** Menggunakan $R_{\text{pullup}} = 4.7\text{ k}\Omega$ sebagai standar antarmuka *open-drain* AT89S52 ($V_{CC} = 5.0\text{ V}$)[cite: 2].
- **Trade-Off & Boundary Condition:** Memberikan kompromi optimal dengan $I_{\text{sink}} = 1.037\text{ mA/pin}$ ($8.30\text{ mA}$ untuk 8 pin serentak, aman di bawah $15\text{ mA}$ dan $26\text{ mA}$), $V_{OL} = 0.125\text{ V}$ ($NML = 0.775\text{ V}$), dan $t_{70\%} = 556.1\text{ ns}$ pada $C_{\text{load}} \le 100\text{ pF}$ (mendukung hingga $400\text{ kHz}$)[cite: 2]. Hasil audit reviewer (`T22-R`) membuktikan konfigurasi ini tetap lulus bahkan pada batas minimum $V_{DD} = 4.0\text{ V}$ dan $C_{\text{load}} = 330\text{ pF}$ ($V_{OL} = 0.131\text{ V}$, $t_{VIH} = 808.1\text{ ns} < 1250\text{ ns}$).
- **Residual Risk:** Model MOS Level-1 ($V_{TO} = \pm 0.8\text{ V}$) tidak memodelkan kenaikan resistansi kanal ($R_{\text{on}}$) pada suhu $+85^\circ\text{C}$ maupun induktansi jalur PCB (*simultaneous switching noise*)[cite: 2].

---

## 2. Jawaban 5 Pertanyaan Wajib Cross-Examination (4 Menit)

1. **ADC 10-bit vs Accuracy:**
   - **Jawaban:** Resolusi 10-bit hanya menentukan kehalusan langkah kuantisasi ($2^{10} = 1024$ kode, sehingga $\text{LSB} = 3.3\text{ V} / 1024 = 3.22\text{ mV}$), **bukan** akurasi pengukuran. Pengukuran 10-bit tetap tidak akurat apabila waktu akuisisi ($t_{\text{acq}}$) terlalu singkat dibanding konstanta waktu $R_{\text{src}} \cdot C_s$ (*incomplete settling*), jika tegangan referensi $V_{\text{ref}}$ bergeser, atau akibat *offset/gain error* dan *nonlinearity* (INL/DNL)[cite: 1]. (Catatan: AT89S52 tidak memiliki ADC internal; fitur ini milik derivatif seperti C8051F330[cite: 1]).
2. **Slow Ramp Reset:**
   - **Jawaban:** Pada rangkaian reset RC pasif tanpa *voltage supervisor* (BOD), kenaikan $V_{DD}$ yang lambat (*slow ramp*) menyebabkan pin `RST` melewati ambang logika reset sebelum osilator kristal mencapai amplitudo dan frekuensi yang stabil[cite: 1]. Akibatnya, CPU mulai mengeksekusi instruksi saat clock belum valid atau tegangan masih di zona *brown-out*, memicu eksekusi instruksi acak (*corrupt state*)[cite: 1].
3. **Pull-Up Current vs Speed:**
   - **Jawaban:** Memperkecil $R_{\text{pullup}}$ mempercepat pengisian kapasitor beban ($t_r \approx 2.2 R_{\text{pullup}} C_{\text{load}}$) karena arus pengisian ke $V_{DD}$ lebih besar[cite: 2]. Namun, saat transistor bawah (NMOS) menyala untuk menarik output ke LOW, resistor kecil memaksa NMOS menyedot arus statik yang jauh lebih besar ($I_{\text{sink}} = (V_{DD}-V_{OL})/R_{\text{pullup}}$), meningkatkan disipasi daya, menaikkan $V_{OL}$, dan mengancam batas arus maksimum port IC[cite: 2].
4. **Hysteresis vs False Trigger:**
   - **Jawaban:** Komparator tanpa histeresis hanya memiliki satu titik ambang tunggal ($V_{\text{th}}$)[cite: 1]. Jika sinyal input bergerak lambat dan mengandung *noise* di sekitar $V_{\text{th}}$, output akan berosilasi bolak-balik (*chattering / false trigger*)[cite: 1, 2]. Histeresis memisahkan ambang naik ($V_{TH+}$) dan ambang turun ($V_{TH-}$) sebesar pita mati ($\Delta V_{\text{hyst}} = V_{TH+} - V_{TH-}$) sehingga riak *noise* di dalam pita tersebut tidak memicu transisi palsu[cite: 1].
5. **Vref Drift:**
   - **Jawaban:** Pada ADC ideal, kode digital berbanding terbalik dengan tegangan referensi ($\text{Code} = \lfloor V_{\text{in}} / V_{\text{ref}} \times 2^N \rfloor$)[cite: 1]. Jika $V_{\text{ref}}$ mengalami *drift* (misal turun dari $3.30\text{ V}$ ke $3.20\text{ V}$ atau naik $+1\%$), setiap volt input yang sama akan dipetakan ke kode digital yang berbeda (*gain error* sistematis), sehingga nilai tegangan hasil konversi *firmware* menyimpang dari tegangan fisik sebenarnya[cite: 1].

---

## 3. 10 Pertanyaan Pembuka Buku Analog (Hari ke-3) & Mapping Bab

| No | Pertanyaan dari Hasil Kegagalan / Pengukuran Simulasi | Modul Asal | Mapping Bab Buku Analog (Sedra/Smith / Razavi / Art of Electronics) |
| :--- | :--- | :--- | :--- |
| 1 | Mengapa kurva arus $I_{DD}$ pada transisi CMOS inverter membentuk puncak segitiga (*crowbar current*) dan bagaimana menghitung energi disipasi hubung singkat per siklus secara analitik? | D1.2 / D2.1 | CMOS Digital Logic Circuits — Dynamic Power & Short-Circuit Dissipation |
| 2 | Bagaimana menurunkan persamaan analitik titik switching $V_m$ inverter CMOS ketika mobilitas elektron dan hole ($\mu_n C_{ox}$ vs $\mu_p C_{ox}$) tidak simetris serta adanya *channel-length modulation* ($\lambda$)? | D1.2 / D2.1 | MOSFET Inverters — Voltage Transfer Characteristic (VTC) & Noise Margins |
| 3 | Mengapa batas input datasheet AT89S52 ($V_{IL}=0.9\text{ V}, V_{IH}=1.9\text{ V}$) bersifat asimetris (TTL-compatible) dibandingkan gerbang CMOS murni yang simetris di $0.5 V_{DD}$? | D1.3 | Logic Family Interfacing — TTL vs CMOS Voltage Levels & Level Shifting |
| 4 | Bagaimana struktur internal rangkaian *quasi-bidirectional* Port 1–3 pada 8051 klasik yang menggunakan kombinasi *weak pull-up* dan *strong pull-up* sesaat (*edge accelerator*)? | D1.4 / D2.2 | Digital I/O Pad Design — Open-Drain, Push-Pull & Quasi-Bidirectional Drivers |
| 5 | Bagaimana menghitung pengaruh induktansi jalur PCB ($L_{\text{trace}}$) dan kapasitansi parasitik terhadap fenomena *ground bounce* saat 8 pin GPIO berpindah dari HIGH ke LOW serentak? | D2.2 | Signal Integrity & High-Speed Digital Design — Ground Bounce & SSN |
| 6 | Mengapa model MOSFET Level-1 (persamaan kuadratik Shichman-Hodges) menyimpang dari silikon modern akibat *velocity saturation* dan *subthreshold conduction*? | D2.1 | Deep-Submicron MOSFET Modeling — Short-Channel Effects |
| 7 | Bagaimana merancang rangkaian *Schmitt Trigger* berbasis umpan balik positif untuk menggantikan inverter biasa pada jalur input yang memiliki *slow slew rate* ($40\text{ ns}$)? | D1.3 / D2.1 | Regenerative Circuits — Schmitt Trigger & Hysteresis Design |
| 8 | Bagaimana menentukan ukuran kapasitor *decoupling* ($C_{\text{dec}}$) dan tata letaknya agar lonjakan arus transien $I_{DD}$ tidak menyebabkan *voltage droop* pada rel $V_{DD}$? | D1.3 / D1.5 | Power Supply Integrity — Decoupling Capacitors & ESR/ESL Effects |
| 9 | Bagaimana memodelkan resistansi kanal sakelar analog ($R_{\text{on}}$) pada *transmission gate* MUX yang berubah secara non-linear terhadap tegangan sinyal input ($V_{\text{in}}$)? | D2.5 / D2.6 | Analog Switches & Sample-and-Hold Circuits — Charge Injection & On-Resistance |
| 10 | Bagaimana menghitung *thermal noise* ($kT/C$) pada kapasitor *sampling* $C_s = 10\text{ pF}$ dan menentukan batas *source impedance* maksimum agar tidak merusak akurasi SAR ADC 10-bit? | D2.4 / D2.5 | Data Converters (SAR ADC) — Sampling Noise, Settling Time & Reference Buffering |
