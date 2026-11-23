# Discovery review | Hari 1, 16.00–17.00

## Pertanyaan pembuka
Jika pin akhirnya mencapai 5 V, apakah input sudah terbaca HIGH saat firmware membacanya? Uji GPIO menunjukkan bahwa waktu mencapai VIH dan rise time 10–90% menjawab dua pertanyaan berbeda. Pada 4,7 kΩ dan 100 pF, pin mencapai VIH 1,90 V sekitar 222 ns setelah dilepas; perpindahan 0,5 ke 4,5 V sendiri memakan 1.033 ns (sekitar 1,03 µs).

## Rencana sesi dan contoh hipotesis
Saya menyiapkan lima topik untuk review hari pertama: logika, GPIO, power/reset, simulasi, dan AFE. Tabel berikut berisi contoh hipotesis dan bukti untuk bahan diskusi. Alokasi YEKVO untuk setiap peserta adalah 6 menit demo dan 4 menit tanya jawab. Pemeriksaan mandiri yang sudah saya lakukan dicatat pada bagian Hasil review mandiri. Demo dan tanya jawab dengan reviewer masih menunggu pelaksanaan.

| Topik review | Prediksi yang diuji | Bukti dan akar masalah | Pembetulan / pertanyaan reviewer |
|---|---|---|---|
| 16.00–16.10 · Logika | HIGH dari F330 tetap punya cadangan positif saat pengirim 2,7 V dan penerima AT89S52 5,5 V. | threshold_matrix.csv: VOH minimum dan VIH minimum sama-sama 2,00 V. VIH penerima berubah dengan catu. | Hitung margin per kondisi beban dan catu. Berapa cadangan jika VCC penerima kembali ke 5,0 V? |
| 16.10–16.20 · GPIO | Pull-up 1 kΩ selalu pilihan terbaik karena paling cepat. | Pada 100 pF, 1 kΩ memberi rise time 220 ns, tetapi arus LOW 4,88 mA dan disipasi resistor 23,78 mW. Jaminan VOL P0 sebesar 0,45 V diberikan pada arus uji 3,2 mA. | Pilih R dari tenggat baca, anggaran daya, dan spesifikasi LOW. Bisakah reviewer memperoleh ulang angka untuk 4,7 kΩ? |
| 16.20–16.30 · Power/reset | Ramp yang akhirnya mencapai 5 V selalu menghasilkan reset startup yang cukup. | Pada ramp 100 ms, RST melewati ambang model ke bawah sekitar 13,33 ms; VCC baru mencapai 4 V pada 80 ms. RC merespons perubahan catu dan kapasitor terisi selama ramp. | Tumpangtindihkan RST HIGH terjamin dengan clock yang berjalan. Bagaimana mengukur startup clock pada papan? |
| 16.30–16.40 · Simulasi | Exit code 0 membuktikan ekspor waveform berhasil. | fault_node.log: salah ketik v(ouut) membuat ekspor gagal meski ngspice selesai dengan kode 0. | Pulihkan v(out), periksa data baru, panjang vektor dan waktu monoton. Bagaimana mendeteksi CSV lama? |
| 16.40–16.50 · AFE | Waktu akuisisi 300 ns cukup untuk semua impedansi sumber. | Model input F330, langkah skala penuh, Rs 100 kΩ, RMUX 5 kΩ dan Csample 5 pF memberi sekitar 4,00 µs untuk galat 0,5 LSB. Muatan kanal sebelumnya masih tersisa. | Tambah waktu track atau turunkan impedansi sumber. Apa pengaruh kapasitor filter eksternal? |
| 16.50–17.00 · Rencana penutupan | Penutupan | Pilih satu angka untuk rerun langsung; periksa satuan dan kondisi. | Isi signoff, tetapkan nama untuk peran dan pilih urutan uji hari kedua. |

## Hasil acuan inverter dan GPIO
Dari folder bukti, jalankan perintah berikut (ngspice CLI harus tersedia pada PATH):

~~~sh
ngspice_con -b gpio.cir > gpio_pribadi.log 2>&1
ngspice_con -b inverter.cir > inverter_pribadi.log 2>&1
~~~

Buka gpio_load_matrix.csv. Pilih R_ohm=4700 dan Cload_pF=100, kolom tr_sim_ns = 1032,695011 ns. Di gpio_rerun.log, pengukuran rise_r4700c100 menghasilkan 1,032695 × 10⁻⁶ s = 1032,695 ns. Estimasi ln(9) × 4700 Ω × 100 pF = 1032,695551 ns. Perhatikan titik desimal pada data mesin. Angka-angka cocok sampai pembulatan log; hasil berlaku untuk tepi naik dari 0,5 ke 4,5 V pada catu 5 V. Model NMOS generik dan beban lumped belum memasukkan kabel, probe, atau variasi silikon.

Pada bukti/delays.csv dari paket acuan, uji inverter 20 pF menghasilkan tPHL = 5,361313 ns dan tPLH = 5,361391 ns. Cocokkan dengan delays.csv. Saat sesi langsung, reviewer bebas mengganti baris GPIO dan menulis hasilnya di signoff_d1.md.

## Hasil review mandiri

Saya memeriksa pengaruh perubahan beban pada inverter model MOS level-1 dengan catu 5 V. Delay diukur pada persilangan 2,5 V di masukan dan keluaran.

| Beban | tPHL (ns) | tPLH (ns) |
|---|---:|---:|
| 20 pF | 5,36195 | 5,36095 |
| 100 pF | 25,9305 | 25,7719 |

Ketika beban dinaikkan dari 20 pF menjadi 100 pF, kedua delay meningkat sekitar 4,8 kali. Saya mengulang simulasi dari folder bersih pada laptop yang sama. Keempat nilai delay cocok dengan run pertama hingga presisi CSV.

## Prediksi awal dan pembetulan

Sebelum simulasi D1.5, saya memperkirakan bahwa reset akan cukup lama selama VCC akhirnya mencapai 5 V. Pada ramp 100 ms, RST sudah turun melewati ambang model pada 13,329 ms, sedangkan VCC baru mencapai 4 V pada 80 ms. Prediksi saya meleset karena saya hanya memperhatikan tegangan akhir dan mengabaikan waktu pengisian kapasitor selama catu naik perlahan.

Setelah melihat hasil tersebut, saya menilai reset dari lamanya RST bertahan HIGH ketika catu sudah valid dan clock sudah berjalan.

[Bukti run pribadi](../bukti/delays_pribadi.csv) · [Perbandingan kedua run](../bukti/bukti_perbandingan.txt)
