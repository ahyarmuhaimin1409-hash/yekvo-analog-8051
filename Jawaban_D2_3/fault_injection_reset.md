# D2.3 | Reset setelah catu terganggu

**Keputusan.** RC 10× memperpanjang reset pada startup dingin dengan ramp cepat. Pada restart setelah jeda mati 0,20 ms, perubahan yang sama justru menurunkan puncak RST pemulihan dari 0,781 V ke 0,086 V. Kapasitor yang masih bermuatan membuat kondisi awal penyalaan kedua berbeda dari penyalaan pertama.

## Kriteria penilaian
AT89S52 memakai RST aktif HIGH selama dua siklus mesin ketika osilator berjalan. Pada clock 12 MHz, satu siklus mesin = 12 periode dan reset minimum = 24/12 MHz = 2 µs. Dalam rentang catu 4,0–5,5 V, HIGH terjamin bila RST ≥ 0,7 VCC; LOW terjamin bila RST ≤ 0,2 VCC − 0,1 V. Pada 5 V batasnya 3,50 V dan 0,90 V. Untuk pemulihan power-down, datasheet juga meminta cukup waktu agar osilator mulai kembali dan stabil.

Simulasi memakai rangkaian VCC → kapasitor → 1 kΩ → RST, pull-down 10 kΩ paralel dengan asumsi resistor internal 100 kΩ, dan dioda penjepit bawah ilustratif. Kapasitor 1 dan 10 µF memberi τ sekitar 10,09 dan 100,91 ms saat dioda padam. Nilai resistor internal yang dicantumkan datasheet adalah 50–300 kΩ. Asumsi clock siap 8 ms setelah VCC mencapai 4 V dipakai sebagai skenario pembanding, termasuk setelah pemulihan dip. Clock pada papan dapat tetap berjalan saat dip atau perlu mulai kembali.

**Cara membaca CSV.** Semua waktu crossing adalah waktu absolut dari awal run. Ambang detektor hipotetis 0,5 VCC dipakai untuk mengukur pulsa, termasuk saat catu belum valid. Pada ramp dingin, interval dimulai pada 0⁺ saat ramp mulai dan RST berada di atas ambang relatif. Pada dip/restart, interval yang dicari adalah pulsa baru sejak tepi pemulihan. Sel kosong berarti tidak ada crossing yang relevan; durasi 0 berarti tidak muncul pulsa. Kolom overlap menghitung waktu HIGH terjamin yang berimpit dengan catu valid dan clock siap. Waktu LOW terjamin menunjukkan kapan pin telah mencapai VIL setelah catu valid. Crossing dihitung lewat interpolasi sampel transien.

## Mode kegagalan dan bukti
| Skenario | Hasil 1 µF → 10 µF | Dampak dan tindakan |
|---|---|---|
| Ramp 0→5 V dalam 1 ms; kapasitor kosong | Lebar pulsa model 6,446 → 59,914 ms. HIGH terjamin berakhir pada 3,050 → 25,961 ms. | Dengan clock siap pada 8,800 ms, overlap 0 → 17,161 ms. Kapasitor besar memenuhi syarat waktu dalam model ini, tetapi RST baru dijamin LOW pada 163,007 ms. Periksa tenggat startup aplikasi. |
| Ramp 0→5 V dalam 100 ms; kapasitor kosong | Lebar pulsa model 13,329 → 113,510 ms. Pada 10 µF puncaknya 2,858 V; selama VCC ≥ 4 V, RST tetap di bawah 0,7 VCC. | Walau crossing 50% terjadi setelah clock siap pada 88 ms, overlap HIGH terjamin tetap nol. Gunakan pengawas tegangan dengan karakteristik ramp lambat yang sesuai. |
| Dip 5→3→5 V, datar 0,20 ms, tiap tepi 0,01 ms | RST pemulihan maksimum 0,276 → 0,030 V. Tidak ada pulsa baru pada kedua RC. | VCC keluar dari rentang operasi. Perilaku CPU selama dip belum diketahui. Uji apakah supervisor mendeteksi kedalaman dan durasi dip tersebut. |
| Restart 5→0→5 V, waktu mati 0,20 ms, tiap tepi 0,01 ms | RST pemulihan maksimum 0,781 → 0,086 V. Keduanya di bawah VIL(max) 0,90 V saat catu kembali ke 5 V. | Muatan belum sempat terlepas. Konstanta waktu lebih panjang memperburuk pemulihan siklus pendek. Ulangi untuk rentang waktu mati dan periksa jalur pengosongan aktual. |

## Mitigasi dan verifikasi papan
Pilih supervisor dengan keluaran kompatibel RST aktif-HIGH atau BOD yang keberadaan dan perilakunya terverifikasi untuk perangkat yang dipakai. Pada AT89S52 ini, rancangan dapat memakai supervisor eksternal. Periksa seluruh toleransi ambang trip terhadap batas operasi 4 V dan catu normal minimum. Pilih histeresis untuk menghindari reset berulang dan periksa waktu deteksi minimum terhadap dip 200 µs. Setelah tegangan pulih, penundaan pelepasan harus mencakup startup clock terburuk terukur, dua siklus mesin, dan margin. Periksa interaksi keluaran supervisor dengan fungsi keluaran watchdog pada pin RST.

Untuk uji papan, program GPIO agar berubah segera setelah vektor reset dan mengeluarkan heartbeat berikutnya. Rekam VCC, RST, clock dengan probe berkapasitansi rendah dan penanda GPIO pada satu pemicu. Jalankan keempat profil, lalu sweep waktu mati di sekitar 0,20 ms, laju ramp, suhu, dan toleransi C. Catat HIGH kontinu setelah clock stabil, waktu LOW, kemunculan penanda boot baru dan heartbeat. Terima setiap uji pemulihan yang mensyaratkan reboot bila reset memenuhi ≥24 periode clock sesudah clock stabil pada catu valid, lalu program mulai kembali dalam tenggat aplikasi. CPU, osilator, kebocoran papan serta kondisi register selama brown-out belum dimodelkan; status pada CSV hanya menilai syarat waktu model.

## Mengulang
Ekstrak ZIP. Di terminal dengan Python, NumPy dan ngspice pada PATH, jalankan python run.py dari folder ekstraksi. Untuk membuka satu kasus di jendela ngspice, gunakan source netlists/quick_restart_10u.cir lalu plot v(dd) v(rst). Netlist menulis wave.dat di direktori kerja. Pembesaran sekitar 10–12 ms memperlihatkan tepi pemulihan.

[Sumber: Microchip AT89S52 doc1919, §4.7 RST, §9 siklus mesin, §16 power-down dan §27 karakteristik DC](https://www.microchip.com/content/dam/mchp/documents/OTH/ProductDocuments/DataSheets/doc1919.pdf)
