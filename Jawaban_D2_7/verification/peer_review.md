# D2.7 | Verifikasi independen · 15.00–16.00

**Status D2.7: BELUM DIUJI.** Saya, Ahyar, menyiapkan delapan pengujian untuk domain power, GPIO, filter, dan ADC. Angka prediksi di matriks berasal dari perhitungan analitis. Hasil pengujian D2.7 akan saya isi setelah menjalankan setiap kasus dan menyimpan lognya. Verifikasi oleh reviewer independen masih menunggu.

## Rencana rotasi reviewer dan pelaksanaan mandiri

Tabel berikut menunjukkan rotasi A → B → C → D → A yang diminta YEKVO. Pada pengerjaan ini, Ahyar Muhaemin bertanggung jawab menguji keempat domain. Kuntjoro Pinardi tercatat sebagai reviewer yang ditunjuk. Pengujian independen dan keputusan reviewer masih menunggu pelaksanaan.

| Owner | Reviewer yang melakukan clone | Domain | Test yang diulang |
|---|---|---|---|
| A | B | Power/reset | T01-B dan T01-F |
| B | C | GPIO | T02-B dan T02-F |
| C | D | Filter | T03-B dan T03-F |
| D | A | ADC | T04-B dan T04-F |

| Waktu | Aktivitas dan rekaman |
|---|---|
| 15.00–15.10 | Owner menyerahkan commit, test utama, parameter, hasil mentah, dan cara run. Reviewer mengunci kriteria, satuan serta toleransi sebelum melihat hasil run sendiri. |
| 15.10–15.25 | Reviewer clone repo ke direktori baru dan ulangi minimal satu test utama milik owner. Catat nilai dan log pada baris B. |
| 15.25–15.40 | Pilih parameter yang belum divariasikan pada tes utama. Buat deliberate fault satu parameter pada salinan input, simpan diff dan output. Owner menjalankan variasi identik secara terpisah agar kedua hasil bisa dibandingkan. |
| 15.40–15.52 | Reviewer membuka issue dan melampirkan dua hasil. Owner mempersempit klaim atau memberi bukti tambahan. Reviewer mengulang pada revisi jika ada perubahan. |
| 15.52–16.00 | Team lead mencocokkan baris requirement, test, hasil dan verdict. Catat semua isu terbuka serta keputusan gate. |

## Cara reviewer membuktikan run

1. Pada terminal, ganti nilai di dalam tanda kutip dengan URL dan SHA yang diberikan owner. Contoh berikut menggunakan folder kerja baru.

   ```sh
   git clone "URL_REPO" review-d27
   cd review-d27
   git checkout --detach "SHA_OWNER"
   git rev-parse HEAD
   git status --short
   ```

2. Jalankan perintah test dari repo pada SHA tersebut. Untuk netlist dengan analisis dan pengukuran di dalamnya, contoh perintah adalah `ngspice_con -b -o T02-B-reviewer.log input_gpio.cir`. Ganti nama input sesuai repo. Simpan versi simulator, perintah persis, satuan keluaran, dan log.
3. Untuk baris F, salin input baseline dan ubah hanya parameter terpilih. Tulis di issue nama parameter, nilai sebelum/sesudah, serta test utama yang sudah diperiksa untuk memastikan variasi memang baru. Jika contoh fault sudah ada di repo, pilih parameter lain, perbarui prediksi dan toleransi **sebelum** run, lalu tautkan diff.
4. Bandingkan keluaran dengan kriteria desain untuk kolom hasil desain aktual. Untuk verdict reproduksi, bandingkan *hasil owner dengan hasil reviewer* pada commit, input, dan kondisi identik. Isi selisih absolut. Toleransi pada CSV adalah usulan latihan dan dapat diganti dengan toleransi proyek yang disepakati sebelum run.

## Empat fault dan angka pembanding

Kriteria di bawah adalah spesifikasi latihan. Gunakan spesifikasi repo yang sebenarnya untuk keputusan proyek. Baris F sengaja mendorong desain melewati batas.

| Domain | Apa yang diukur | Prediksi baseline → fault dan alasannya |
|---|---|---|
| Power | Irisan waktu antara RST HIGH, catu valid dan clock berjalan. Gunakan model waktu reset aktif-HIGH dengan target latihan 2 µs. | Clock siap pada 5 → 7 µs sementara RST turun di 8 µs. Irisan menyusut dari 3 → 1 µs. Ukuran ini menguji margin timing; keberhasilan boot perangkat memerlukan bukti terpisah. |
| GPIO | Waktu dari pelepasan pin hingga 3 V, pada pull-up 10 kΩ ke 5 V dan tegangan awal nol. | C naik dari 100 → 200 pF. Waktu naik dari 0,916 → 1,833 µs, melampaui batas 1 µs. |
| Filter | Magnitudo Vout/Vin pada 1 kHz untuk RC low-pass, dengan sumber ideal. | Penambahan beban 1 kΩ ke ground menurunkan gain DC menjadi 0,5 dan membuat resistansi efektif 500 Ω. Gain pada frekuensi uji turun dari sekitar 0,707 → 0,447 V/V, di bawah batas 0,65. |
| ADC | Kode ADC ideal pada Vin absolut 1,2 V. Gunakan pembulatan ke bawah dan batasi kode ke 0–1023. | Vref naik dari 2,4 → 2,424 V. Kode turun dari 512 → 506. Galat 6 kode melampaui anggaran 2 kode. |

## Membaca verdict dan menindaklanjuti issue

- **reproducible** jika kedua run selesai dengan revisi dan input yang cocok, selisih berada dalam toleransi, dan keduanya menghasilkan klasifikasi desain yang sama. Contoh hipotetis: dua reviewer/owner mendapatkan 1,83 µs pada fault GPIO. Keduanya melanggar batas 1 µs. Hasil desain GAGAL dan verdict reproducible.
- **not reproducible** jika pengulangan yang dicoba tidak berhasil mengikuti prosedur terdokumentasi, atau hasilnya berbeda menurut aturan di atas. Lampirkan perintah dan keluaran aktual, termasuk error. Gunakan BELUM DIUJI bila belum ada percobaan atau masih menunggu bukti pembanding.
- Baris issue berstatus DRAF hanya menyediakan tempat untuk empat fault. Jika run owner menunjukkan masalah, ubah status isu menjadi TERBUKA dan cantumkan log owner. Isi label reproduksi setelah reviewer mengulang kasus dan mencatat hasilnya. Tambahkan issue tersendiri untuk baseline yang tidak cocok. Owner mencatat revisi klaim atau bukti tambahan. Reviewer menutup issue hanya setelah memeriksa bukti dan mencatat keputusan. Pertahankan log gagal, SHA awal, serta hasil awal. Tambahkan baris matriks untuk retest pada revisi baru.

## Keputusan gate oleh team lead

| Isian akhir | Nilai saat persiapan |
|---|---|
| Test critical dengan verdict reproducible / jumlah critical | 0 / 8 terverifikasi |
| Ketidakcocokan tersisa, issue ID, owner, dan waktu tindak lanjut | Belum dinilai |
| Keputusan D2.7 dan nama pemeriksa | MENUNGGU BUKTI |

Gate D2.7 lulus jika semua test critical dapat direproduksi dan semua ketidakcocokan tersisa dicatat terbuka. Satu critical test tanpa bukti replikasi menahan gate. Fault yang gagal sesuai prediksi dapat memenuhi gate reproduksi; keputusan kelayakan desain tetap mengikuti requirement dan batas penggunaan yang dicatat owner.
