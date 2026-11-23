# D1.6 — Reproduksi transien inverter

## Menyiapkan mesin
Pada Windows, pengujian ini menggunakan Python 3.13 dan ngspice 47. Tambahkan folder yang berisi `ngspice_con.exe` ke PATH, lalu periksa versinya di PowerShell dengan `ngspice_con -v`. Pada Debian/Ubuntu, ngspice dapat dipasang dengan `sudo apt install ngspice` dan diperiksa dengan `ngspice -v`. Skrip `run.py` mencatat versi alat dan sistem operasi di `tools/versions.txt`.

Ekstrak ZIP dan buka terminal di folder yang memuat README.md. Buat lingkungan Python dengan `python -m venv .venv`. Aktifkan dengan `.venv\Scripts\activate.bat` (Windows CMD) atau `source .venv/bin/activate` (Linux/macOS). Jalankan:

```sh
python -m pip install -r requirements.txt
python run.py
```

## Menelusuri hasil
1. Untuk menjalankan simulasi batch secara manual dari folder ini, gunakan `ngspice_con -b inverter.cir` pada Windows atau `ngspice -b inverter.cir` pada Linux. Perintah ini menghasilkan `trace.dat` dengan tiga kolom: waktu (s), Vin (V), dan Vout (V). Terminal menampilkan tPHL dan tPLH dalam detik.
2. run.py menjalankan perintah batch yang sama untuk rangkaian awal 20 pF dan salinan dengan satu perubahan, yaitu baris Cload menjadi 100p. Model NMOS/PMOS level-1, catu 5 V, masukan dan langkah waktu dipertahankan. Run dijalankan di direktori sementara terpisah agar satu trace tidak menimpa yang lain.
3. results/trace_20pF.csv dan trace_100pF.csv menyimpan ekspor masing-masing run. Untuk membuat ulang gambar hanya dari CSV, ketik `python plot.py`. Baca selisih waktu antara persilangan 2,5 V pada input dan output untuk tepi berlawanan. Cocokkan dengan results/delays.csv (ns) dan baris tphl/tplh di results/logs (s). Beban yang lebih besar memerlukan muatan lebih banyak pada ayunan tegangan yang sama sehingga kedua tepi keluaran tertunda.
4. Uji sengaja mengganti v(out) dengan v(ouut) pada wrdata. Bandingkan results/logs/fault_node.log dengan fixed_node.log. Kembalikan nama node ke v(out), jalankan ulang dan pastikan data baru ada. Analisis transient dapat selesai meskipun ekspor gagal; periksa pesan dan berkas data, selain kode keluar.
5. Run otomatis menulis ulang hasil. Untuk uji pribadi, tiap engineer memakai ekstraksi baru, menyimpan tools/versions.txt dan results miliknya, lalu mencatat nama, mesin, dua pasang delay dan status uji salah node. Bandingkan terhadap results/logs/rerun.txt pada arsip asli. Untuk versi solver berbeda, selisih relatif 1% pada delay dapat dipakai sebagai toleransi praktikum; telusuri selisih lebih besar lewat CSV dan versi alat.

## Hasil run pribadi

- Nama engineer: [isi nama kamu]
- Tanggal pelaksanaan: [isi tanggal run]
- Lingkungan: Windows, Python 3.13, ngspice 47 versi konsol.
- Perintah yang dijalankan dari folder `Jawaban_D1_6` di PowerShell:
  `& "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe" .\run.py`

Simulasi menggunakan VDD 5 V. Delay diukur pada persilangan 2,5 V di masukan dan keluaran. Hasil berikut diambil dari `results/delays.csv` setelah run pribadi.

| Beban keluaran | tPHL (ns) | tPLH (ns) |
|---|---:|---:|
| 20 pF | 5,36195 | 5,36095 |
| 100 pF | 25,9305 | 25,7719 |

Saat beban dinaikkan dari 20 pF menjadi 100 pF, kedua delay meningkat sekitar 4,8 kali. Kapasitor yang lebih besar memerlukan lebih banyak muatan sehingga keluaran mencapai ambang 2,5 V lebih lambat.

Uji salah node juga berhasil. Saat `v(out)` diubah menjadi `v(ouut)`, ekspor waveform gagal. Setelah nama node dikembalikan ke `v(out)`, data berhasil diekspor kembali. Bukti kedua percobaan tersimpan di `results/logs/fault_node.log` dan `results/logs/fixed_node.log`.

Grafik hasil run tersimpan di `results/transient.png`. Versi alat dan sistem operasi tercatat di `tools/versions.txt`.

Sumber instalasi: [ngspice](https://ngspice.sourceforge.io/download.html) dan [Python](https://www.python.org/downloads/).
