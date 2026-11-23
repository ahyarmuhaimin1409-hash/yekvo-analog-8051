# D2.1 — Inverter stress & sensitivity

## Keputusan desain
Untuk beban 100 pF dan target tepi naik/turun seimbang, rasio βp/βn = 1 menghasilkan waktu tepi hampir sama. Pada 5 V keduanya sekitar 64 ns. Menurunkan catu ke 3,3 V menghemat sekitar 56% energi per siklus tetapi hampir menggandakan delay propagasi. Untuk jalur yang terutama membutuhkan tepi naik cepat, menggandakan kekuatan PMOS memangkas tpLH sekitar separuh dengan konsekuensi berkurangnya margin HIGH model.

## Eksperimen dan satuan
Ada 54 run: VDD 5/4/3,3 V × Cload 10/100/500 pF × βp/βn 0,5/1/2 × slew input 1/100 ns. Semua memakai ngspice 44.2, 27 °C, MOS level-1, |VTO|=0,8 V, KPn/KPp=100/50 µA/V², λ=0,04 V⁻¹. Panjang kanal 1 µm, Wn=10 µm dan Wp=10/20/40 µm. β = KP × W/L. Slew di sini adalah durasi ramp linier 0–100% untuk kedua tepi. CSV menyimpan satu baris untuk setiap run.

| Besaran | Cara ukur |
|---|---|
| VM | Sweep DC 0→VDD (2.000 interval), interpolasi akar Vout−Vin=0. |
| tr dan tf | Selang waktu keluaran 0,1→0,9 VDD dan 0,9→0,1 VDD. |
| tpLH dan tpHL | Waktu persilangan keluaran 50% VDD dikurangi waktu persilangan input 50% VDD pada tepi pemicu yang berlawanan. |
| VIL dan VIH model | Dua titik kemiringan dVout/dVin=−1 pada VTC. Dengan pasangan inverter identik, VOH=Vout(VIL), VOL=Vout(VIH); NML=VIL−VOL, NMH=VOH−VIH. |
| Arus, energi, daya | Idd=−i(VDD). Dua puncak dicatat terpisah menurut arah transisi keluaran. E=∫VDD·Idd dt selama satu pengosongan dan satu pengisian; simulasi sampai 6,9 µs. Daya rata-rata E/7 µs menganggap konsumsi sisa interval diam dapat diabaikan. Energi driver input di luar pengukuran. |

## Hasil nominal • 100 pF, rasio 1, slew 1 ns
| VDD (V) | VM (V) | tr (ns) | tf (ns) | tpLH (ns) | tpHL (ns) | Energi/siklus (nJ) | NML / NMH (V) |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 5,0 | 2,50 | 64,02 | 64,02 | 25,93 | 25,92 | 2,500 | 1,58 / 1,58 |
| 4,0 | 2,00 | 86,83 | 86,83 | 36,23 | 36,22 | 1,600 | 1,36 / 1,36 |
| 3,3 | 1,65 | 114,84 | 114,84 | 49,36 | 49,35 | 1,089 | 1,20 / 1,20 |

**Beban dan VTC.** Untuk catu dan rasio tetap, ketiga Cload memberikan VM yang sama sampai presisi CSV. Pada DC kapasitor ideal telah selesai diisi. Selama transien, Q=CΔV harus dipindahkan oleh arus kanal. Pada 5 V dan rasio 1, kenaikan beban 10→100→500 pF menghasilkan tr 6,40→64,02→320,09 ns. Catu lebih rendah juga mengurangi overdrive transistor sehingga pengisian/pengosongan melambat. Energi dinamis dari catu mendekati Cload·VDD² per siklus penuh untuk input cepat.

**Rasio dan margin.** Pada 5 V, 100 pF dan slew 1 ns, rasio 0,5→1→2 menggeser VM sebesar 2,217→2,500→2,783 V. PMOS lebih kuat membutuhkan Vin lebih tinggi untuk menyeimbangkan kedua arus. tpLH turun dari 51,64 ke 25,93 lalu 13,08 ns; tpHL tetap sekitar 25,92 ns karena ukuran NMOS tetap. NML naik dari 1,16 ke 2,06 V, sedangkan NMH turun dari 2,06 ke 1,16 V. Ini margin statis dua inverter model identik.

**Slew dan arus.** Pada 5 V, 100 pF dan rasio 1, tepi input diperpanjang dari 1 menjadi 100 ns. Ketika keluaran turun, puncak arus catu naik dari 0,00582 menjadi 0,376 mA, dan energi yang ditarik pada setengah siklus ini naik dari 0,0103 menjadi 54,11 pJ. Kapasitor melepaskan muatan ke ground pada tepi ini; arus dari catu terutama menandai konduksi bersamaan PMOS–NMOS. Pada tepi keluaran naik, puncak arus justru turun dari 10,57 ke 7,90 mA karena pengisian beban lebih tersebar dalam waktu. Energi total naik dari 2,500 ke 2,608 nJ per siklus. Jadi puncak arus satu tepi saja tidak menentukan konsumsi energi.

## Batas interpretasi
Model level-1 ini memakai parameter nominal dan beban kapasitif terpusat. Parasitik layout dan interkoneksi, beban gate tahap berikut, variasi proses/suhu, leakage nyata, serta dinamika catu dan driver input belum dikalibrasi. Memperlebar PMOS pada silikon juga menambah beban gate dan difusi. Gunakan angka untuk membandingkan mekanisme pada model yang sama; validasi spesifikasi pin chip dengan datasheet atau pengukuran.

## Ulangi
Ekstrak ZIP dan buka terminal pada folder ekstraksi. Dengan ngspice pada PATH, Python 3, NumPy ≥2 dan Matplotlib terpasang, jalankan `python sweep.py` untuk membangun ulang CSV, tiga PNG dan netlist nominal. Satu kasus dapat dijalankan dengan `ngspice -b inverter_nominal.cir`; file dc.dat berisi Vin dan Vout, sedangkan tr.dat memuat waktu, Vin, Vout dan i(VDD).
