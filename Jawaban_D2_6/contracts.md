# D2.6 | Kontrak antarmuka mini-8051 AFE

**Hasil integrasi.** Dari 40 slot per skenario, 35 menghasilkan data valid dan 5 diblokir saat catu turun atau sistem masih dalam reset. Keputusan nominal sesuai tegangan node filter pada 35/35 sampel valid. Namun empat sampel pada tepi langkah melampaui sasaran galat analog ½ LSB. Jalur digital bisa mengambil keputusan yang benar walau akurasi analog sesaat belum memenuhi target.

## Perangkat dan skenario
Model mengacu pada keberadaan ADC0 SAR 10 bit, AMUX0 dan Comparator0 pada **Silicon Labs C8051F330**. Datasheet keluarga F33x Rev. 1.7 menempatkan ADC0 pada F330/F332/F334 (bab 5); lihat Gbr. 1.1, Tabel 5.1, bab 7 dan Gbr. 8.1. AT89S52 klasik tidak menyediakan ADC0 dan CP0 tersebut. Nilai RC, histeresis, supervisor, waktu konversi serta aturan keputusan berikut adalah pilihan eksperimen behavioral. Reset dimodelkan sebagai kondisi logis aktif, terlepas dari polaritas pin fisik.

Simulasi Python berjalan 4 ms dengan langkah 0,1 µs. Masukan naik dari 0,5 ke 2,8 V pada 1 ms sambil menerima sinus 20 mV puncak pada 10 kHz. Catu turun dari 3,2 ke 2,9 V selama 2,40–2,70 ms. Supervisor hipotetis trip di bawah 3,0 V dan menahan reset 0,20 ms setelah pemulihan. Penurunan ini menguji kebijakan supervisor eksternal yang dipilih. Filter tetap bertenaga dan pin tidak melampaui catu pada profil ini.

## Kontrak blok
| Blok dan domain | Input / range | Waktu dan keluaran | Asumsi serta metrik lulus/gagal |
|---|---|---|---|
| Sensor eksternal, analog | Langkah dan noise di atas | Vin 0,48–2,82 V, direkam di akhir track | Lulus bila berada pada 0…VDD setiap saat. Impedansi dan proteksi sensor fisik perlu diverifikasi. |
| Filter eksternal, analog | Vin sensor | Low-pass orde satu, fc=1 kHz, τ≈159,15 µs; keluaran filter_V | Model buffered, gain DC 1; lulus rentang bila 0…VDD. Untuk kasus ini, keluaran setelah 1 ms dari langkah harus dalam ±5 mV dari 2,8 V (riak teoritis sekitar 1,99 mV). |
| MUX dan S/H, analog | Kanal lama 0,5 V; kanal baru adalah node filter yang terus berubah | Sumber efektif total 100 kΩ, Cs=10 pF, τ=1 µs; track 10 µs atau fault 1 µs, keluaran hold_V | Kanal lama kembali ke 0,5 V sebelum tiap slot. Buffer memisahkan filter dari beban switching. Lulus per sampel jika abs(Vhold−Vfilter saat hold) ≤½ LSB = 1,5625 mV pada 3,2 V. Galat mencakup settling dan ketertinggalan terhadap input bergerak. |
| Supply/reset dan validasi | VDD normal 3,2 V, dip 2,9 V | Reset instan dan hold-off; valid mencakup seluruh interval track sampai baca | Lulus jika slot tidak valid tidak menerbitkan kode, keputusan baru, atau event. Latch CP0 disinkronkan dengan level saat re-arm agar tidak menciptakan tepi palsu. Hasil model: lima slot INHIBIT per skenario. |
| Referensi dan ADC0, analog ke digital | 0…Vref aktual; Vref=VDD | q=clip(floor(1024 Vhold/Vref),0,1023); satu slot per 100 µs; kode siap 4 µs sesudah hold | Konversi ideal; lulus jika kode sama dengan kuantisasi tegangan yang benar-benar ditahan. ideal_code_at_filter menjadi pembanding independen untuk mengungkap salah akuisisi. |
| Firmware, digital | Kode valid dan Vref firmware | Vlapor=q·Vref_fw/1024. LOW jika <2,70 V; HIGH jika >2,85 V; sisanya IN_RANGE. INHIBIT untuk slot tidak valid. | Lulus jika keputusan cocok dengan klasifikasi filter_V pada saat hold. Dengan Vref nominal cocok: 0/35 salah; track pendek: 20/35 salah; Vref firmware salah: 19/35 salah. |
| Comparator CP0 dan event | Node filter bercabang sebelum MUX, 0…VDD | Naik pada ≥1,55 V, turun pada ≤1,45 V, selainnya tetap. Tepi 0→1 ketika aktif menghasilkan event. | Band histeresis ideal untuk eksperimen; ambang bukan setelan histeresis bawaan F330. Lulus bila tepat satu event untuk langkah naik, nol selama reset dan saat re-arm. Event naik t=1,0972 ms, Vfilter≈1,5500 V. |

## Telusuri satu keputusan
Pada t_hold=2,150 ms dan t_read=2,154 ms, Vin=2,800000 V, Vfilter=2,800307 V, CP0=1, reset=0. Kode ideal node filter = 896. Event CP0 sudah terjadi sebelumnya; level HIGH pada slot ini tidak menghasilkan event baru.

| Skenario | t_track | Vhold | Vref aktual / firmware | Kode | Vlapor | Keputusan / harapan |
|---|---:|---:|---:|---:|---:|---|
| Nominal | 10 µs | 2,800197 V | 3,2 / 3,2 V | 896 | 2,8000 V | IN_RANGE / IN_RANGE |
| Akuisisi pendek | 1 µs | 1,954071 V | 3,2 / 3,2 V | 625 | 1,9531 V | LOW / IN_RANGE |
| Salah Vref | 10 µs | 2,800197 V | 3,2 / 3,3 V | 896 | 2,8875 V | HIGH / IN_RANGE |

**Diagnosis.** Pada fault akuisisi, satu τ menyisakan sekitar 37% selisih dari kanal sebelumnya. Kesalahan muncul di node hold sebelum ADC dan menghilangkan 271 hitungan. Untuk input tunak, waktu ke ½ LSB dari langkah 2,3 V sekitar 7,3 µs. Pada input yang bergerak cepat, penambahan waktu track saja tidak menghilangkan lag RC; turunkan impedansi efektif atau ubah jadwal sampling. Pada fault Vref, hold dan kode tetap seperti nominal. Galat +87,5 mV terhadap laporan nominal baru muncul saat kode diskalakan firmware. Ukur atau kalibrasi referensi yang sebenarnya.

**Trace dip.** Pada slot 2,45 ms, VDD=2,9 V; pada 2,75 ms VDD sudah 3,2 V tetapi hold-off masih aktif. Kedua slot memiliki valid=0, kode dan volt laporan kosong, keputusan INHIBIT. Pada 2,95 ms sampling dilanjutkan. Tidak ada sampel lama yang dipakai ulang sebagai hasil baru.

## Reproduksi dan batas penggunaan
Jalankan python integration.py dari folder ekstraksi dengan NumPy dan Matplotlib. Buka integration_results.csv, pilih mode dan t_hold_ms; kolom boolean 1 berarti aktif. events.csv menyimpan timestamp tepi aktual; kolom cp0_rises_since_prev menghitung event sejak slot sebelumnya. trace.png merangkum transien dan system/block_diagram.png menunjukkan cabang serta dependensi.

Noise dan sampling sama-sama 10 kHz sehingga tiap slot melihat fase gangguan yang sama. Coba variasi fase/laju saat menguji aliasing pada papan. Model tidak mencakup leakage, kickback ke filter, offset komparator, INL ADC, startup clock, dan perilaku internal selama brown-out. Lulus kontrak keputusan pada stimulus ini belum mengesahkan perangkat fisik.

[Silicon Labs C8051F33x, Rev. 1.7](https://www.silabs.com/documents/public/data-sheets/C8051F33x.pdf) · [Microchip AT89S52, doc1919](https://www.microchip.com/content/dam/mchp/documents/OTH/ProductDocuments/DataSheets/doc1919.pdf)
