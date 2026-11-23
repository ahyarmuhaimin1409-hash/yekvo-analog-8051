# D1.7 — Peta AFE C8051F330
Kompatibilitas 8051 menjelaskan inti dan set instruksi. Pada C8051F330, ADC0, multiplexer, referensi, CP0 dan IDA0 dibuktikan oleh diagram blok serta definisi register. Datasheet AT89S52 mendokumentasikan periferal berbeda. Jika AT89S52 dipakai untuk membaca tegangan sebagai kode, tambahkan ADC eksternal dan ikuti register/protokol komponen itu.

## Pembacaan tegangan
Contoh ini memakai pin P0.2 untuk sinyal dan P0.3 untuk ambang CP0 eksternal. Konfigurasikan kedua pin sebagai analog dan lewati pada crossbar. Pilih P0.2 pada AMX0P dan GND pada AMX0N. Atur REFSL=1 untuk menggunakan VDD 3,3 V sebagai referensi, atur clock SAR dan waktu tracking, mulai konversi, periksa AD0INT, lalu baca ADC0H:ADC0L sesuai alignment. Comparator memilih pin melalui CPT0MX sendiri sehingga lintasan ambang dapat memicu event sebelum firmware membaca hasil ADC. IDA0 di P0.1 adalah jalur keluaran arus terpisah.

## Resolusi dan akurasi
Pada mode single-ended, 1 LSB ideal = 3,3 V / 1024 = 3,22265625 mV. Kode 512 mewakili nominal 1,65 V dan kode tertinggi 1023 mewakili 3,29678 V. Resolusi menyatakan ukuran langkah kode. Akurasi menyatakan kedekatan hasil terhadap masukan sebenarnya; offset, gain, INL, ketidakpastian VREF, dan pengisian kapasitor yang belum selesai dapat memperbesar selisih.

## Prediksi sesudah pindah kanal
Untuk langkah masukan skala penuh dan target sisa galat 0,5 LSB, model Gbr. 5.4 memberi t ≈ ln(2048) × (Rs + 5 kΩ) × 5 pF. Dengan sumber Thévenin resistif 1 kΩ diperoleh 0,229 µs; gunakan sekurangnya batas akuisisi tabel 0,300 µs. Dengan 100 kΩ diperoleh 4,00 µs. Angka 300 ns saja tidak mencukupi dalam contoh kedua. Prediksi jika kanal sebelumnya tinggi dan kanal berikutnya rendah: sampel pertama cenderung terlalu tinggi. Uji dengan menambah waktu track atau memakai buffer impedansi rendah dan bandingkan kode pertama. Ini perhitungan model resistif; bila ada kapasitor filter eksternal, evaluasi pula transfer muatan dan waktu pengisian ulang filter. Nilai komponen contoh dan ambang CP0 merupakan pilihan rangkaian, bukan spesifikasi sensor dari datasheet.
