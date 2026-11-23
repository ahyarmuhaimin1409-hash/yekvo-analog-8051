# D2.8 | Berita acara keputusan desain

**Status awal: MENUNGGU BUKTI.** Belum ada peserta yang dinilai atau disahkan. Gunakan satu baris scorecard untuk setiap engineer dan satu salinan blok keputusan di bawah untuk setiap desain.

## Aturan penilaian
Gunakan bobot rubrik 100 poin YEKVO untuk rekap. Penguji memeriksa juga bukti D1–D2 yang relevan. Bukti tambahan dari sesi D2.8 dicatat pada scorecard.

| Kriteria YEKVO | Maksimum | Bukti yang diperiksa |
|---|---:|---|
| Integritas datasheet dan bukti | 20 | Varian, halaman sumber, kondisi pin dan batas model |
| Penalaran dan prediksi | 15 | Prediksi bertanggal sebelum uji dan penjelasan koreksi |
| Simulasi dan metrik terukur | 25 | Netlist, perintah, log, grafik dan angka bersatuan |
| Fault injection dan verifikasi | 20 | Empat domain D2.7, fault dan bukti pengulangan reviewer |
| Keputusan rekayasa dan pembelaan | 20 | Trade-off, counterexample, batas desain, lima jawaban dan tanya jawab aktual |

## Critical gates per engineer
Isi setiap gate dengan LULUS atau GAGAL setelah diperiksa. Tulis nama berkas atau lokasi bukti pada baris yang sama.

| Gate | Team lead memberi LULUS bila |
|---|---|
| G1 · Source trace | Engineer membuka locator untuk klaim acak dan menunjukkan bahwa varian, mode, serta kondisi berlaku cocok. |
| G2 · Run mandiri | Team lead menyaksikan engineer menjalankan perintah sendiri dan membaca hasil baru. Catat perintah, versi, input, lokasi log, metrik serta satuan. |
| G3 · Baseline | Engineer menunjukkan parameter acak dan satuannya pada input yang dijalankan serta menjelaskan kaitannya dengan grafik. |

**Individual.** Jumlahkan lima komponen rubrik. Periksa pula status critical gate D2.7 dari matriks verifikasi. LULUS jika skor ≥80/100, seluruh gate LULUS, dan bukti lengkap. Jika nilai lengkap tetapi ambang atau gate gagal, catat UJI ULANG. Jika bukti atau nilai belum lengkap, catat MENUNGGU BUKTI. CSV menggunakan isian manual agar dapat digunakan di Excel, LibreOffice, atau editor teks. Periksa penjumlahan dan keputusan sebelum paraf.

**Tim.** Cocokkan jumlah baris dengan daftar hadir. Sahkan hanya setelah setiap engineer lulus, termasuk peserta yang menjalani uji ulang. Simpan hasil awal dan tambahkan baris baru untuk percobaan berikutnya.

## Rekaman keputusan
| Isian | Catatan penguji |
|---|---|
| Tanggal, desain, revisi, serta batas penggunaan | [tanggal dan revisi saat sesi] · Pull-up P0, model RC nominal 5 V |
| Nama seluruh engineer dan team lead | Ahyar Muhaemin (engineer), [nama penguji saat sesi] |
| Kriteria desain, parameter terpilih beserta toleransinya | 3 V dalam ≤1 µs pada 200 pF, arus LOW ideal ≤1 mA. Pilihan nominal 5,1 kΩ. Pada kondisi model, rentang R sekitar 5,00–5,46 kΩ. |
| Bukti penentu, nilai aktual, margin, dan satuan | Acuan desain 0,934617 µs, margin +0,065383 µs. Run pribadi dan log yang disaksikan: [isi saat demo]. |
| Peserta lulus / jumlah peserta wajib | ___ / ___ |
| Gate terbuka, penanggung jawab, tenggat, dan kriteria uji ulang | D2.7 menunggu bukti reviewer pada arsip terakhir. Ahyar menyiapkan hasil owner. Penguji memeriksa matriks terbaru, audit sumber, baseline dan run mandiri. Tenggat: [sepakati saat sesi]. |
| Keputusan akhir dan alasan | MENUNGGU BUKTI |
| Nama/paraf team lead dan waktu keputusan | ___ |

Setelah nilai dikunci, tim mengisi judul/edisi buku Analog dan nomor bab/halaman pada sepuluh pertanyaan di reviews/final_defense.md.
