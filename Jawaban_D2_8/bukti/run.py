"""Jalankan tiga kasus ngspice dan simpan bukti pada direktori baru."""
import csv
import platform
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent
CASES = [("pullup", 10, 100), ("beban", 10, 200), ("desain", 5.1, 200)]

def summarize(folder):
    rows = []
    fig, ax = plt.subplots(figsize=(8.5, 4.8), layout="constrained")
    for (name, r, c), color in zip(CASES, ["#2765a8", "#b64c16", "#11745e"]):
        log = (folder / f"{name}.log").read_text(errors="replace")
        match = re.search(r"(?m)^(?:stdout )?\s*t3\s*=\s*([\d.eE+-]+)", log)
        if not match:
            raise ValueError(f"Pengukuran t3 belum tersedia dalam {name}.log")
        t3 = float(match[1]) * 1e6
        time, volts = np.loadtxt(folder / f"{name}.dat", unpack=True)
        if not (np.isfinite([time, volts]).all() and np.all(np.diff(time) > 0)
                and volts[0] < 3 < volts[-1]):
            raise ValueError(f"Periksa waktu dan tegangan dalam {name}.dat")
        crossing = np.flatnonzero(volts >= 3)[0]
        window = slice(crossing - 1, crossing + 1)
        trace_t3 = np.interp(3, volts[window], time[window]) * 1e6
        if abs(trace_t3 - t3) > 0.001:
            raise ValueError(f"Persilangan kurva berbeda dari log {name}")
        rows.append([name, r, c, f"{t3:.7f}", f"{1-t3:.7f}", f"{5/r:.5f}"])
        ax.plot(time*1e6, volts, label=f"{r:g} kΩ · {c} pF", color=color)
        ax.plot(t3, 3, "o", color=color)
    ax.axhline(3, color="#555555", ls="--", label="Ambang 3 V")
    ax.axvline(1, color="#555555", ls=":", label="Tenggat 1 µs")
    ax.set(xlabel="Waktu sejak pin dilepas (µs)", ylabel="Tegangan pin (V)",
           title="Pengisian pin GPIO setelah dilepas", xlim=(0, 3), ylim=(0, 5.1))
    ax.legend(loc="lower right")
    ax.grid(alpha=.16)
    fig.savefig(folder / "grafik_pullup.png", dpi=170)
    plt.close(fig)
    with (folder / "hasil.csv").open("w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["kasus", "R_kohm", "C_pF", "t3_log_us", "margin_us", "I_LOW_ideal_hitung_mA"])
        writer.writerows(rows)

def main():
    windows_exe = Path.home() / "Downloads/ngspice-47_64/Spice64/bin/ngspice_con.exe"
    exe = shutil.which("ngspice_con") or (str(windows_exe) if windows_exe.is_file() else shutil.which("ngspice"))
    if not exe:
        sys.exit("Tambahkan folder program ngspice ke PATH, lalu ulangi.")
    folder = Path(tempfile.mkdtemp(prefix="run_pribadi_", dir=ROOT))
    print("Folder bukti:", folder, flush=True)
    with (folder / "lingkungan.txt").open("w", encoding="utf-8") as record:
        record.write(f"Python {platform.python_version()}, numpy {np.__version__}, matplotlib {matplotlib.__version__}\n")
        version = subprocess.run([exe, "-v"], capture_output=True, text=True, errors="replace", check=True)
        record.write(version.stdout + version.stderr)
        for name, _, _ in CASES:
            shutil.copy2(ROOT / f"{name}.cir", folder)
            cmd = [exe, "-b", "-o", f"{name}.log", f"{name}.cir"]
            record.write("\n" + subprocess.list2cmdline(cmd) + "\n")
            subprocess.run(cmd, cwd=folder, check=True)
    summarize(folder)
    print((folder / "hasil.csv").read_text())
    print("Grafik, log, hasil.csv dan lingkungan.txt tersimpan di", folder)

if __name__ == "__main__":
    main()
