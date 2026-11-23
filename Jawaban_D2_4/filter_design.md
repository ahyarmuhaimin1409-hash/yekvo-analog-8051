# D2.4 | Filter untuk sensor 100 Hz

**Pilihan awal: 1 kHz** bila target praktikum adalah mempertahankan sedikitnya 98% amplitudo sensor dan menyisakan paling banyak 2 mV puncak pada 10 kHz. Dengan sumber ideal dan beban 1 MΩ, hasilnya 295,58 mV dari 300 mV serta 1,990 mV dari 20 mV. Batas ini merupakan contoh keputusan desain; selisih terhadap target riak hanya sekitar 0,010 mV. Periksa toleransi komponen sebelum menerapkan pilihan ini pada papan.

## Stimulus dan model
Vin(t) = 1,5 + 0,3 sin(2π·100t) + 0,02 sin(2π·10000t) volt; t dalam detik. Dua sumber sinus seri membentuk stimulus transien. Dalam analisis AC, eksitasi dinormalisasi ke 1 V. Pada tiap cabang, sumber Thévenin dengan Rs = 0 Ω atau 10 kΩ menggerakkan Rfilter = 10 kΩ seri; C dan RL = 1 MΩ terhubung paralel dari output ke ground. Model menggunakan nilai C ideal tanpa pembulatan ke seri komersial; RL memodelkan input resistif kontinu.

| fc nominal | C | fc terukur, Rs=0 / 10 kΩ | t settling 1%, Rs=0 / 10 kΩ |
|---:|---:|---:|---:|
| 200 Hz | 79,5775 nF | 202 / 102 Hz | 3,628 / 7,186 ms |
| 1 kHz | 15,9155 nF | 1010 / 510 Hz | 0,726 / 1,437 ms |
| 5 kHz | 3,1831 nF | 5050 / 2550 Hz | 0,145 / 0,287 ms |

## Prediksi yang dibandingkan
Tanpa pembebanan dan dengan Rs nol, |H|=1/√(1+(f/fc)²), fc=1/(2πRfilter C). Untuk beban nyata di model, definisikan S=Rs+Rfilter, K=RL/(S+RL), τ=(S || RL)C. Maka H=K/(1+j2πfτ), fc aktual=1/(2πτ) dan fase=−atan(f/fc aktual). Pengukuran cutoff mencari |H|=K/√2 relatif terhadap gain DC. Offset keluaran menjadi 1,5K volt. Waktu settling dihitung untuk respons langkah menuju sisa selisih 1% dari perubahan akhir, t=ln(100)τ.

## Amplitudo puncak (mV), Rs = 0 Ω
| fc nominal | 100 Hz ideal / hitung berbeban / transien | 10 kHz ideal / hitung berbeban / transien | Fase AC 100 Hz / 10 kHz |
|---|---:|---:|---:|
| 200 Hz | 268,328 / 266,196 / 266,196 | 0,39992 / 0,39992 / 0,39989 | −26,34° / −88,84° |
| 1 kHz | 298,511 / 295,584 / 295,584 | 1,99007 / 1,98988 / 1,98971 | −5,65° / −84,23° |
| 5 kHz | 299,940 / 296,971 / 296,971 | 8,94427 / 8,92635 / 8,92576 | −1,13° / −63,21° |

Pada 200 Hz, hanya 2,00% amplitudo gangguan lolos. Amplitudo sinyal sensor juga berkurang 11,27%, dan keterlambatan fase sinus 100 Hz setara 26,34°/(360° × 100 Hz) = 0,732 ms. Angka itu khusus untuk sinus 100 Hz. Ketika masukan berubah mendadak, kapasitor yang lebih besar memerlukan waktu pengisian lebih lama; waktu settling langkah adalah 3,628 ms. Pada cutoff 5 kHz, pembacaan lebih cepat, tetapi riak tersisa 8,926 mV.

**Uji impedansi sumber.** Untuk desain 1 kHz, tambahan Rs=10 kΩ menggeser cutoff 1010→510 Hz dan menurunkan amplitudo sensor 295,584→288,622 mV. Fase 100 Hz berubah dari −5,65° ke −11,09°. Dengan sumber ini syarat contoh 98% tidak tercapai. Ukur impedansi keluaran sensor atau gunakan buffer sebelum menetapkan RC.

## Bukti dan toleransi numerik
Sweep AC dari 1 Hz sampai 1 MHz, 300 interval/dekade. Transien sepanjang 50 ms dengan langkah maksimum 0,5 µs. Kedua amplitudo dan fase diekstrak serentak dengan regresi DC + pasangan sinus/kosinus pada 20–50 ms (tiga periode 100 Hz). Amplitudo AC pada setiap nada adalah |H| dikali amplitudo masukan nada itu. Untuk enam cabang, batas pemeriksaan terhadap prediksi berbeban: galat gain AC dan cutoff <0,1%, fase AC <0,05°, galat amplitudo transien <0,2%, fase transien <0,1°. Semua pemeriksaan lolos; galat amplitudo transien terbesar sekitar 0,00823%. Toleransi ini menguji analisis numerik. R/C fisik, ESR, variasi impedansi sensor dan arus sampling ADC memerlukan evaluasi tersendiri.

## Menjalankan kembali
Ekstrak ZIP. Dari terminal folder tersebut jalankan ngspice -b rc_filter.cir -r run.raw lalu python analisis.py (NumPy dan Matplotlib). Skrip membaca ac.dat dan transient.dat, menguji toleransi serta membangun ulang CSV dan gambar. Di jendela ngspice bisa langsung menggunakan source rc_filter.cir lalu plot v(vin) v(f200s0) v(f1000s0) v(f5000s0). Node f1000s10000 menunjukkan target 1 kHz dengan Rs=10 kΩ.
