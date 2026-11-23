# D2.5 | Keputusan comparator dan angka ADC

## 1. Comparator dengan memori
Stimulus uji adalah Vin(t) = 1,30 + 20t + 0,030 sin(2π·2000t) volt, dengan t dalam detik dari 0 hingga 0,020. Ramp bersih melewati 1,50 V sekali. Comparator biasa memakai y = 1 jika Vin ≥ 1,50 V, selain itu y = 0. Untuk comparator dengan histeresis, tetapkan y = 1 pada Vin ≥ 1,55 V, y = 0 pada Vin ≤ 1,45 V, dan pertahankan keadaan sebelumnya di antara kedua ambang. Keadaan awal LOW.

Hitungan tepi N = Σ|y[k]−y[k−1]|. Prediksi ramp bersih adalah satu transisi naik; transisi palsu di sini berarti jumlah tepi tambahan terhadap satu transisi yang dibutuhkan. Comparator biasa memberi 7 tepi naik dan 6 turun (13 total, 12 tambahan). Dengan histeresis diperoleh 1 naik dan 0 turun (0 tambahan). Jika firmware hanya menghitung rising edge, kesalahan hitung adalah 6 versus 0. Histeresis menunda keputusan naik sampai ambang atas. Setelah itu, gangguan 60 mV puncak-ke-puncak pada ramp naik tidak cukup untuk kembali melintasi ambang bawah yang berjarak 100 mV. Jumlah tepi diperiksa pada langkah 1 µs dan 0,5 µs.

## 2. Kuantisasi dan clipping
Untuk input single-ended, Δ = Vref/2¹⁰. Kode q = min(1023, max(0, floor(Vin/Δ))). Pada 3,30 V, Δ = 3,22265625 mV dan 1,5/Δ = 465,4545… sehingga q = 465. Pada −0,10 V keluar kode 0; pada 3,30 V dan 3,40 V keluar kode 1023. Di dalam rentang, firmware di sini melaporkan tepi bawah bin dengan Vlapor = q × Vref_fw/1024. Ketika referensi cocok, galat rekonstruksi berada antara −1 LSB dan 0 untuk 0 ≤ Vin < Vref. Tepat pada Vref, clipping membuat selisih sebesar satu LSB.

## 3. Galat referensi
Vin tetap 1,500 V. Pada Vref aktual 3,20 V, kode mentahnya selalu 480, baik firmware memakai 3,20 maupun 3,30 V. Hasil konversi firmware masing-masing 1,500000 dan 1,546875 V. Pada Vref aktual 3,30 V, kode 465 memberi 1,498535 V jika firmware juga memakai 3,30 V. Dengan skala firmware 3,20 V, hasilnya 1,453125 V. Selisih +46,875 mV pada kasus pertama yang salah skala setara 15 LSB aktual 3,20 V. Jumlah kode digital tetap 1024 dalam seluruh kasus.

## 4. MUX dan kapasitor sampel
Saat kanal berpindah dari 0,5 V ke 2,8 V, τ = Rsrc Cs, Vhold(t) = 2,8 − 2,3 exp(−t/τ), dan galat settling E = 2,8 − Vhold. Agar E ≤ Δ/2 dengan Vref=3,30 V, dibutuhkan t ≥ τ ln[2,3/(Δ/2)] = 7,2636τ. Kriteria ½ LSB ini khusus untuk settling analog sebelum kuantisasi.

| Rsrc | τ dengan Cs 10 pF | Waktu minimum untuk E ≤ 1,61133 mV |
|---:|---:|---:|
| 1 kΩ | 0,010 µs | 0,07264 µs |
| 10 kΩ | 0,100 µs | 0,72636 µs |
| 100 kΩ | 1,000 µs | 7,26361 µs |

Contoh kegagalan: pada 100 kΩ dan akuisisi 1 µs, kapasitor baru mencapai 1,95388 V. ADC melaporkan kode 606, sedangkan 2,8 V yang sudah tunak memberi kode 868. Kurangi impedansi sumber atau perpanjang waktu track untuk mengurangi pengaruh kanal sebelumnya.

## Batas model dan reproduksi
Comparator ideal memakai satu gangguan sinus deterministik; jumlah tepi bergantung pada bentuk gelombang, amplitudo, frekuensi, dan laju ramp. Offset, propagation delay dan noise acak belum dimasukkan. ADC memakai kuantisasi seragam, tanpa INL, DNL, jitter maupun drift selain variasi referensi yang ditentukan. Pada model MUX, sakelar ideal, sumber Thévenin konstan, Cs mula-mula tepat 0,5 V. Resistansi sakelar, charge injection dan kebocoran pada silikon dapat mengubah hasil. Cs dan ambang histeresis dipilih untuk eksperimen ini.

Ekstrak ZIP. Dengan Python 3, NumPy dan Matplotlib tersedia, jalankan python adc_quantization.py dari folder ekstraksi. Skrip membangun kembali tiga CSV dan empat gambar. compare_hysteresis.csv memuat data sepanjang 20 ms; grafik comparator memperbesar jendela lintasan ambang.
