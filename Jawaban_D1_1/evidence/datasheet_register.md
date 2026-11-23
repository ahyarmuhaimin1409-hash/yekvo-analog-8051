# Hari 1 · D1.1 | Audit part dan pin | 08.00–09.00

## 1. Identifikasi komponen dan sumber

Dua nomor pemesanan berikut dipilih sebagai objek audit dokumen. Identitas chip pada papan fisik belum diverifikasi. Nomor halaman mengikuti angka tercetak pada PDF.

| ID | Part dan kemasan | Dokumen, revisi | URL resmi | Akses | Bukti identitas |
|---|---|---|---|---|---|
| A | AT89S52-24PU, PDIP 40 pin | Atmel AT89S52, 1919D–MICRO–6/08, Juni 2008 | https://www.microchip.com/content/dam/mchp/documents/OTH/ProductDocuments/DataSheets/doc1919.pdf | 21 November 2026 | hlm. 1, 2, 34 |
| S | C8051F330-GM, QFN 20 pin dengan pad tengah GND | Silicon Labs C8051F330/1/2/3/4/5, Rev. 1.7, Desember 2010 | https://www.silabs.com/documents/public/data-sheets/C8051F33x.pdf | 21 November 2026 | hlm. 1, 18, 35–37 |

Salinan sumber berada di direktori datasheets. Inventaris pin menggunakan orientasi tampak atas dan penomoran kemasan yang dipilih. Lihat ../pin_inventory.csv.

### Kondisi listrik

Nilai berikut adalah jaminan minimum HIGH atau maksimum LOW pada kondisi yang ditulis. Karakteristik GPIO berlaku pada −40 hingga +85 °C. Arus keluaran negatif menandakan pin menyuplai arus ke beban.

| Parameter | AT89S52-24PU | C8051F330-GM |
|---|---|---|
| Catu dan frekuensi | VCC 4,0–5,5 V untuk grade 24 MHz (A34) | VDD 2,7–3,6 V, hingga 25 MHz (S1, S18) |
| VIL maksimum | 0,2 VCC − 0,1 V kecuali EA. Untuk EA, 0,2 VCC − 0,3 V (A29) | GPIO digital 0,8 V (S134). /RST 0,3 VDD (S102) |
| VIH minimum | 0,2 VCC + 0,9 V kecuali XTAL1 dan RST. Untuk keduanya, 0,7 VCC (A29) | GPIO digital 2,0 V (S134). /RST 0,7 VDD (S102) |
| VOL maksimum | P1/P2/P3 0,45 V pada 1,6 mA. P0/ALE/PSEN 0,45 V pada 3,2 mA (A29) | Port 0,1 V pada 10 µA atau 0,6 V pada 8,5 mA (S134) |
| VOH minimum | P1/P2/P3/ALE/PSEN 2,4 V pada −60 µA dan VCC 5 V ±10%, 0,75 VCC pada −25 µA, 0,9 VCC pada −10 µA. P0 dalam mode bus eksternal memiliki batas tegangan yang sama pada −800, −300, −80 µA dengan syarat catu masing-masing yang sama (A29) | Port push-pull: VDD − 0,1 V pada −10 µA, VDD − 0,7 V pada −3 mA. Nilai pada −10 mA hanya tipikal (S134) |
| Reset eksternal | RST aktif HIGH selama minimal dua siklus mesin saat osilator berjalan (A5) | /RST aktif LOW minimal 10 µs, berbagi pin dengan C2CK (S35, S97–102) |
| Clock | Penguat osilator internal memakai kristal/resonator di XTAL1–XTAL2 atau sumber clock eksternal pada XTAL1 (A19–20) | Osilator internal HF nominal 24,5 MHz dan LF nominal 80 kHz dengan pembagi. Opsi sumber eksternal melalui fungsi XTAL sesuai mode (S1, S35, S113–120) |
| GPIO | 32 jalur. P1–P3 memakai pull-up internal, tulis 1 untuk input. P0 sebagai GPIO bersifat open-drain sehingga memerlukan pull-up bila mengandalkan level HIGH pasif (A1, A4–5) | 17 jalur digital toleran 5 V. Port mendukung push-pull atau open-drain. P0/P1 juga dapat dipakai sebagai input analog (S1, S35–37, S123–125) |

## 2. Status blok

“Built-in classic” menyatakan fungsi dasar yang dikenal pada 8051 klasik. “Built-in derivative” menyatakan tambahan atau implementasi khusus part. “External” menunjukkan komponen di luar chip untuk konfigurasi yang disebut. “Not evidenced” berarti sumber audit tidak menunjukkan blok internal tersebut. Keyakinan tinggi berarti ada pernyataan, tabel atau diagram langsung. Sedang berarti kesimpulan dari inventaris dan diagram tanpa pernyataan eksplisit tentang ketiadaan.

| Blok | AT89S52-24PU · status, bukti, keyakinan | C8051F330-GM · status, bukti, keyakinan |
|---|---|---|
| Inti/instruksi 8051 | built-in classic · A1,3 · tinggi | built-in derivative · inti CIP-51 kompatibel 8051, S1,19,71 · tinggi |
| RAM data internal | built-in classic · A1,3,10 · tinggi | built-in classic untuk fungsi RAM data, dengan tambahan XRAM internal · S1,24 · tinggi |
| Flash ISP | built-in derivative · A1,21–22 · tinggi | built-in derivative · S1,19 · tinggi |
| GPIO dan port serial UART | built-in classic · A1,3–5 · tinggi | built-in classic untuk fungsi GPIO/UART, dengan crossbar khusus turunan · S1,19,26 · tinggi |
| Timer 0/1 dan interupsi | built-in classic · A1,11–12,17–18 · tinggi | built-in classic untuk fungsi dasar · S1,19,22,27 · tinggi |
| Timer tambahan dan watchdog | built-in derivative · Timer 2 dan WDT, A1,11–12 · tinggi | built-in derivative · Timer 2/3 dan watchdog PCA, S19,27 · tinggi |
| Reset dan rangkaian clock | built-in classic · RST dan penguat osilator, A5,19–20 · tinggi | built-in derivative · monitor catu, reset dan osilator internal, S19,23,97–98 · tinggi |
| Kristal atau sumber clock dari luar | external · A19–20 · tinggi | external bila opsi clock eksternal dipilih · S35,113–120 · tinggi |
| ADC | not evidenced · A1,3,7–9 · sedang | built-in derivative · ADC0 10 bit, S18–19,41 · tinggi |
| Komparator analog | not evidenced · A1,3,7–9 · sedang | built-in derivative · Comparator0, S19,29,65 · tinggi |
| DAC | not evidenced · A1,3,7–9 · sedang | built-in derivative · DAC arus 10 bit, S18–19,57 · tinggi |

**Mengapa ADC bukan syarat CPU 8051?** Inti menjalankan instruksi. ADC adalah periferal yang mengubah tegangan menjadi kode numerik. Contoh terkontrol ada pada S18–19: F330 dan F331 sama-sama memakai CIP-51, tetapi hanya diagram F330 yang memuat ADC0. Untuk mengukur tegangan dengan AT89S52, ADC eksternal merupakan pilihan rancangan. Membaca satu bit GPIO hanya menguji level logika.

## 3. Prediksi, variasi, dan keputusan

Lihat ../five_voltage_prediction.md untuk hipotesis, hasil per tegangan, batas inklusif dan uji variasi. Tahap ini adalah audit datasheet. Tidak ada pengukuran papan maupun hasil simulasi yang diklaim.
