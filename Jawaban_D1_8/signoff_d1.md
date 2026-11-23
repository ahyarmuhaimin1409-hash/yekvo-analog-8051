# Signoff hari pertama

**Status hari pertama.** Peta datasheet dan hasil simulasi awal inverter serta GPIO tersedia. Saya telah mengulang simulasi inverter D1.6 secara mandiri dari folder bersih pada laptop yang sama. Keempat nilai delay cocok dengan run pertama. Demo, tanya jawab, dan pemeriksaan oleh reviewer masih menunggu pelaksanaan.

| Gate | Bukti di folder bukti | Hasil pemeriksaan |
|---|---|---|
| Peta datasheet lengkap untuk blok yang diminta | afe_inventory.csv, evidence_register.csv, annotated_signal_chain.pdf, threshold_matrix.csv | 11 blok/fungsi dan 12 entri bukti. Sensor/filter eksternal, blok internal, pengganti behavioral, batas analog/digital dan risiko dicatat. C8051F330 dan AT89S52 diidentifikasi terpisah. |
| Simulasi awal inverter berjalan | `inverter.cir`, `inverter_rerun.log`, `delays.csv`, `delays_pribadi.csv` | Pada beban 20 pF, tPHL acuan = 5,361313 ns. Run pribadi dan pengulangan mandiri masing-masing menghasilkan 5,36195 ns. |
| Simulasi awal GPIO berjalan | gpio.cir, gpio_rerun.log, gpio_load_matrix.csv | R=4,7 kΩ, C=100 pF, tr=1,032695 µs; sesuai matriks. |
| Review manusia dan penanggung jawab hari kedua | reviews/day1.md, open_questions.md | Agenda dan penugasan peran tersedia. Nama, kehadiran dan keputusan aktual diisi saat sesi. |

## Rekam review aktual

| Pelaksana | Tanggal | Pemeriksaan | Hasil |
|---|---|---|---|
| [Ahyar Muhaemin] | [22/11/2026] | Menjalankan ulang inverter D1.6 dari folder bersih pada laptop yang sama dan membandingkan kedua file delays.csv. | Keempat nilai delay cocok hingga presisi CSV. Pada beban 100 pF, tPHL run pertama dan run ulang sama-sama 25,9305 ns. Selisih 0 ns. |

**Bukti pengulangan mandiri:** [Hasil pengukuran pribadi](bukti/delays_pribadi.csv) dan [perbandingan kedua run](bukti/bukti_perbandingan.txt).

**Review saat demo:** Menunggu reviewer memilih satu angka untuk diuji ulang dan mencatat hasil serta sesi tanya jawab.

**Keputusan tim:** Menunggu review.

**Keputusan tim:** ☐ diterima   ☐ diterima dengan tindak lanjut   ☐ perlu uji ulang. Penanggung jawab dan tenggat tindak lanjut ______ .
