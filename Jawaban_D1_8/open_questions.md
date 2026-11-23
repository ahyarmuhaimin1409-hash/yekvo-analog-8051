# Sepuluh pertanyaan terbuka untuk hari kedua

Ahyar bertanggung jawab menjalankan eksperimen dan menyimpan bukti hasilnya. Reviewer independen belum ditetapkan. Daftar berikut memuat sepuluh pertanyaan yang akan diuji pada hari kedua.

| ID | Pertanyaan yang dapat diuji | Eksperimen dan bukti yang disimpan | Ahyar Muhaemin / Kuntjoro Pinardi | Risiko kelengkapan model |
|---|---|---|---|---|
| Q01 | Pada catu berapa margin HIGH F330→AT89S52 habis untuk beban yang dipilih? | Sweep pasangan catu dalam rentang spesifikasi, hitung VOH(min)−VIH(min), simpan matriks dan titik nol. | Logika / GPIO | Beban total dan toleransi regulator belum diukur. |
| Q02 | Bagaimana Cload memengaruhi tPHL dan tPLH ketika tepi input diperlambat? | Ulangi 20/100 pF dengan dua slew input; simpan jejak dan persilangan 50%. | Simulasi / Logika | MOS level-1 belum dikalibrasi terhadap silikon. |
| Q03 | Pull-up mana yang memenuhi tenggat baca 1 µs pada ketiga Cload? | Bandingkan t(VIH=1,90 V) sejak pelepasan dengan tenggat uji 1 µs; catat ILOW. | GPIO / Logika | Tenggat adalah skenario; parasitik papan dapat menambah C. |
| Q04 | Seberapa besar kapasitansi probe menggeser rise time GPIO? | Ukur atau modelkan C probe, bandingkan tr sebelum/sesudah probe pada beban 20 pF. | GPIO / Simulasi | Kapasitansi input probe dan fixture perlu diketahui. |
| Q05 | Kapan clock papan benar-benar stabil untuk ramp 1 dan 100 ms? | Rekam VCC, RST, indikator clock, dan transisi GPIO pertama; hitung interval HIGH sesudah clock siap. | Power/reset / Simulasi | Probe kristal dapat membebani osilator. |
| Q06 | Durasi power-off minimum berapa yang mengembalikan pulsa reset startup? | Sweep jeda mati; simpan puncak RST dan waktu di atas VIH setelah catu valid. | Power/reset / GPIO | Jalur discharge dan penjepit internal belum terkarakterisasi. |
| Q07 | Dip sedalam dan selama apa yang menghasilkan hilangnya tanda eksekusi tanpa reset baru? | Sweep amplitudo/durasi dip; log VCC, RST, dan penanda firmware pada papan. | Power/reset / Logika | Model RC tidak memodelkan state CPU. |
| Q08 | Berapa waktu track untuk galat sampel pertama ≤0,5 LSB sesudah MUX berpindah? | Uji langkah skala penuh dengan Rs 1 dan 100 kΩ; bandingkan kode sampel pertama terhadap hasil tunak. | AFE / Simulasi | RMUX dan Csample adalah model pendekatan; VREF juga berderau. |
| Q09 | Apakah histeresis CP0 mengurangi event ganda pada sinyal lambat yang berderau? | Suntik gelombang dengan noise terukur; hitung event naik/turun untuk dua konfigurasi histeresis. | AFE / Logika | Offset, bandwidth dan latensi ISR dapat mengubah hitungan. |
| Q10 | Apakah dua komputer menghasilkan waktu tPHL yang konsisten dalam toleransi praktikum 1%? | Jalankan D1.6 pada komputer kedua, simpan versi alat, log, dan CSV, lalu bandingkan tPHL dengan hasil komputer pertama. | Ahyar / belum ditetapkan | Versi solver, opsi integrasi, dan pembulatan ekspor dapat berbeda. |

**Status Q10 — masih terbuka.** Pengulangan mandiri dari folder bersih pada laptop yang sama menghasilkan empat nilai delay yang identik. Pengujian pada komputer kedua belum dilakukan.
