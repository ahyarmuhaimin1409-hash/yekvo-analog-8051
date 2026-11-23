import csv
from math import floor
from pathlib import Path

folder = Path(__file__).resolve().parent / "logs"
folder.mkdir(exist_ok=True)

with (folder / "adc_owner.csv").open("w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["test_id", "Vin_V", "Vref_V", "kode_adc", "galat_kode", "hasil_desain"])

    vin = 1.2
    for test_id, vref in [("T04-B", 2.4), ("T04-F", 2.424)]:
        kode = max(0, min(1023, floor(1024 * vin / vref)))
        galat = abs(kode - 512)
        hasil = "LULUS" if galat <= 2 else "GAGAL"
        writer.writerow([test_id, vin, vref, kode, galat, hasil])
        print(f"{test_id}: kode ADC = {kode}, galat = {galat} kode -> {hasil}")
