# D1.1 · Prediksi lima tegangan

**Hipotesis awal untuk diuji.** Pada input digital yang diberi catu normal, dugaan awal untuk 0, 1, 2, 3 dan 5 V berturut-turut ialah LOW, LOW, ragu, HIGH dan HIGH. Ini contoh prediksi awal untuk latihan, bukan data ukur. Pemeriksaan berikut memakai tegangan ideal di kaki pin, ground bersama, GPIO dalam mode input digital dan catu stabil.

| VIN | AT GPIO P1.2, VCC 5,0 V | AT RST, VCC 5,0 V | F330 GPIO P1.2, VDD 3,3 V | F330 /RST, VDD 3,3 V |
|---:|---|---|---|---|
| 0 V | LOW | LOW | LOW | LOW |
| 1 V | undefined | undefined | undefined | undefined |
| 2 V | HIGH | undefined | HIGH | undefined |
| 3 V | HIGH | undefined | HIGH | HIGH |
| 5 V | HIGH | HIGH | HIGH | HIGH¹ |

**Aturan penilaian.** Dalam rentang tegangan masukan yang diizinkan, VIN ≤ VIL(max) dijamin LOW dan VIN ≥ VIH(min) dijamin HIGH. Interval terbuka di antaranya tidak dijamin (undefined). Nilai di luar rating harus dinilai tersendiri. LOW/HIGH pada kolom reset menyatakan level listrik. Reset aktif HIGH pada AT dan aktif LOW pada F330, dengan syarat durasi masing-masing (A5, S35).

| Pin dan catu | VIL(max) | VIH(min) | Interval undefined | Bukti |
|---|---:|---:|---|---|
| AT P1.2, 5,0 V | 0,90 V | 1,90 V | 0,90 < VIN < 1,90 V | A29 §27 |
| AT RST atau XTAL1, 5,0 V | 0,90 V | 3,50 V | 0,90 < VIN < 3,50 V | A29 §27 |
| AT EA, 5,0 V | 0,70 V | 1,90 V | 0,70 < VIN < 1,90 V | A29 §27 |
| F330 P1.2, 3,3 V | 0,80 V | 2,00 V | 0,80 < VIN < 2,00 V | S134 tab. 14.1 |
| F330 /RST, 3,3 V | 0,99 V | 2,31 V | 0,99 < VIN < 2,31 V | S102 tab. 10.1 |

¹ Untuk /RST, S102 menetapkan VIH minimum dan S31 mencantumkan maksimum absolut 5,8 V pada port atau RST. Hasil pada 5 V hanya menilai level pada pin yang dilepas sebagai input. Karena /RST juga keluaran open-drain, jangan memaksanya HIGH dengan penggerak push-pull ketika MCU dapat menariknya LOW (S35). Toleransi 5 V untuk GPIO digital dinyatakan pada S1. Batas digital ini tidak menetapkan rentang konversi ADC (S41–46).

**Jawaban intuisi.** Pada satu pembacaan, CPU memperoleh satu bit. Di antara batas yang dijamin, datasheet tidak menentukan apakah bit itu 0 atau 1. Nilai dapat berbeda antarperangkat atau antarbacaan. Tepat 2,00 V dijamin HIGH pada kedua GPIO dalam tabel. Pada F330 nilainya tepat di ambang spesifikasi sehingga tidak ada margin terhadap penurunan tegangan sekecil apa pun.

**Fault test di atas kertas — ubah hanya catu.** Naikkan VCC AT89S52-24PU dari 5,0 ke 5,5 V, keduanya dalam rentang A34. Untuk P1.2, VIL(max) berubah menjadi 1,00 V dan VIH(min) menjadi 2,00 V (A29). Karena batasnya inklusif, 1,00 V berubah dari undefined menjadi LOW. Pada VIN 1,95 V hasil justru berubah dari HIGH menjadi undefined. Jika yang diganti hanya pinnya pada VCC 5,0 V, 2 V yang dijamin HIGH pada P1.2 masuk daerah undefined pada RST. Tidak ada satu angka ambang yang berlaku untuk semua pin dan catu.

**Pemeriksaan hipotesis.** Dugaan LOW pada 1 V gagal untuk semua kolom pada catu awal. Keraguan pada 2 V terjawab untuk GPIO, tetapi tetap berlaku pada kedua pin reset. Prediksi HIGH pada 3 V juga gagal sebagai jaminan untuk RST AT. Label undefined sengaja dipertahankan di setiap sel tersebut.

Kode sumber A dan S merujuk ke evidence/datasheet_register.md.
