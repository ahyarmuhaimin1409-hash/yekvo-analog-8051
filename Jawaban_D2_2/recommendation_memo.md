# D2.2 | Pemilihan pull-up GPIO AT89S52

**Keputusan.** Pada catu 5,0 V, pilih 10 kΩ untuk jalur sampai 100 pF pada 100 kHz. Bila beban mencapai 1 nF, pilih 4,7 kΩ dan batasi frekuensi ke 50 kHz untuk jadwal sampling di bawah. Pada 1 kΩ, sink LOW model mencapai 4,88 mA, melampaui kondisi uji VOL Port 0.

## Anggaran antarmuka
Contoh memakai satu P0.0 AT89S52 sebagai pengirim open-drain dalam mode GPIO dan satu P0.0 chip AT89S52 lain sebagai input (latch 1); keduanya aktif, ground bersama. HIGH berasal dari pull-up. Pada 5 V, VIH(min) input = 1,90 V dan VIL(max) = 0,90 V. Target desain 70% VDD = 3,50 V memberi cadangan 1,60 V di atas VIH. Pada logika LOW, batas VOL = 0,45 V pada arus uji 3,2 mA memberi NML ≥0,45 V pada kondisi kompatibel. Dalam model tanpa kebocoran, VOH tunak ≈5 V dan NMH ≈3,10 V. CSV membedakan margin tunak dari margin pada waktu sampling.

Dipilih sinyal periodik duty 50%. Sampling efektif pada 80% interval HIGH, yaitu 0,4/f setelah pin dilepas; sisa 20% interval HIGH disisihkan. Batas frekuensi praktis dari sisi tepi naik adalah f_max = 0,4/t70. Angka ini mengasumsikan pelepasan dari LOW tunak. Kapasitas transfer aktual juga bergantung pada tepi turun, setup/hold dan latensi firmware. Pada 100 kHz, keputusan HIGH diuji di 4 µs.

## Pilihan dengan batas operasi eksplisit
| R | C total maksimum / frekuensi maksimum yang disarankan | Waktu tersedia / t70 nominal pada batas beban | Batas arus LOW per jalur | Risiko tersisa dan pemeriksaan |
|---|---|---|---|---|
| 10 kΩ | 100 pF / 100 kHz | 4,00 / 1,20 µs | ≤0,50 mA dari resistor ideal; ≤0,54 mA dengan R ±5% dan anggaran kebocoran 10 µA | Fanout dan kabel menambah C, dan kebocoran menurunkan HIGH. Ukur kapasitas total termasuk probe. |
| 4,7 kΩ | 100 pF / 500 kHz | 0,80 / 0,563 µs | ≤1,064 mA ideal; ≤1,13 mA dengan toleransi dan kebocoran yang sama | Jitter, kapasitansi konektor, atau tambahan receiver mengurangi sisa 0,237 µs. Verifikasi waktu sampling aktual. |
| 4,7 kΩ | 1 nF / 50 kHz | 8,00 / 5,634 µs | ≤1,064 mA ideal; ≤1,13 mA dengan toleransi dan kebocoran yang sama | C kabel dan gangguan ground mengurangi cadangan. Periksa tegangan di pin terjauh sebelum tenggat. |

Batas di atas berlaku pada 5,0 V; satu anggaran arus parasit 10 µA ditambahkan sebagai asumsi desain pada LOW. Saat menambah receiver, hitung ulang arus, C, dan suhu. Estimasi konservatif untuk timing dengan R +5%, total C tepat pada batas, VOL awal 0 V, dan kebocoran jalur 10 µA ke ground: Vakhir = 5 − 10 µA × Rmax; t70 = −Rmax C ln(1 − 3,5/Vakhir). Hasilnya sekitar 1,32 / 0,61 / 6,06 µs untuk tiga baris di atas, masih di bawah waktu sampling masing-masing. Kebocoran driver, papan, dan input tambahan perlu masuk anggaran aktual.

## Hasil simulasi dan batas datasheet
Untuk R 1 / 4,7 / 10 kΩ, VOL model masing-masing sekitar 0,124 / 0,0265 / 0,0125 V dan arus sink sekitar 4,876 / 1,058 / 0,499 mA. Disipasi resistor selama LOW sekitar 23,78 / 5,26 / 2,49 mW. Muatan C tidak mengubah arus tunak. Datasheet membatasi sink tunak secara eksternal ke 10 mA per pin, 26 mA total Port 0, dan 71 mA seluruh pin keluaran. Melebihi arus uji 3,2 mA menghilangkan jaminan VOL terkait, bahkan sebelum mencapai batas 10 mA. Delapan jalur 1 kΩ LOW bersamaan diperkirakan menarik 39,0 mA pada model, melebihi batas Port 0. Angka absolute maximum 15 mA adalah rating stres.

**Fanout.** Untuk N receiver, gunakan Ctotal = Cjalur + Cprobe + jumlah Cin, dan estimasikan VOH tunak dari 5 − R × jumlah kebocoran ke ground. Contoh asumsi: jalur/probe 40 pF dan tiap receiver 10 pF memberi maksimal enam receiver dalam anggaran 100 pF. Dengan enam receiver masing-masing 10 µA dan R=10 kΩ, estimasi HIGH = 4,40 V sebelum menambahkan kebocoran driver/papan. Nilai Cin dan kebocoran perlu diverifikasi sesuai kondisi datasheet serta konfigurasi aktual. Menggandakan jumlah pin pengirim aktif LOW juga mengubah anggaran arus port secara terpisah.

## Fault test pada satu jadwal sampling
Pada 4,7 kΩ dan 100 kHz, dengan 100 pF didapat 4,999 V pada 4 µs. Dengan 1 nF didapat 2,877 V, masih memenuhi VIH tetapi gagal target 3,50 V. Dengan 4,7 nF, pin baru mencapai 0,850 V, di dalam wilayah LOW meskipun firmware sudah melepas pin. Dengan 10 kΩ / 1 nF, sampel 1,657 V berada di wilayah tak terjamin. Keempat hasil diukur dari satu pelepasan setelah LOW tunak.

## Metode dan sumber
Model konseptual NMOS level-1, 27 °C, VTO=1 V, KP=0,01 A/V², W/L=1, C total terkumpul. Netlist mengukur arus LOW pada 0,5 µs, tegangan akhir pada 299 µs, dan crossing sejak gate melewati 2,5 V ke bawah. Nilai hitung I_sink=(5−VOL)/R; t70=RC ln[(5−VOL)/(5−3,50)]. Dengan VOL≈0, t70≈1,204RC. Perbedaan estimasi RC dan hasil simulasi diperiksa untuk seluruh kasus. Arus LOW yang diukur adalah arus tunak. Arus puncak pelepasan muatan ketika NMOS mulai menghantar memerlukan model driver dan interkoneksi aktual.

Ekstrak arsip. Di terminal folder ekstraksi, jalankan ngspice -b gpio_tradeoff.cir. Di jendela ngspice, jalankan source gpio_tradeoff.cir dari folder yang sama, lalu plot v(r4700c100) v(r4700c1000) v(r4700c4700). Nama node memuat R dalam ohm dan C dalam pF. CSV memuat sembilan kombinasi utama serta kasus beban tambahan.

[Sumber: Microchip AT89S52 doc1919, §4.3 dan §26–27, hlm. 4 dan 29; perhatikan catatan 1 untuk arus port](https://www.microchip.com/content/dam/mchp/documents/OTH/ProductDocuments/DataSheets/doc1919.pdf)
