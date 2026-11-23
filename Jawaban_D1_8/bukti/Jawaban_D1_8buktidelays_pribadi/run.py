from pathlib import Path
import csv
import platform
import re
import subprocess
import sys
import tempfile
import numpy as np
import matplotlib
from plot import plot

root = Path(__file__).resolve().parent
results = root / "results"
logs = results / "logs"
logs.mkdir(parents=True, exist_ok=True)
(root / "tools").mkdir(exist_ok=True)
spice = "ngspice_con" if sys.platform == "win32" else "ngspice"
commands = [
    (f"{spice} -v", [spice, "-v"]),
    ("python --version", [sys.executable, "--version"]),
    ("python -c (versi paket dan OS)", [sys.executable, "-c",
     "import numpy,matplotlib,platform; print('numpy',numpy.__version__); print('matplotlib',matplotlib.__version__); print(platform.platform()); print(platform.freedesktop_os_release()['PRETTY_NAME'] if platform.system()=='Linux' else platform.system())"])
]
versions = []
for label, command in commands:
    versions.append("$ " + ("python -c \"" + command[-1] + "\"" if label.startswith("python -c") else label))
    versions.append(subprocess.check_output(command, text=True).strip())
(root / "tools" / "versions.txt").write_text("\n".join(versions) + "\n", encoding="utf-8")

base = (root / "inverter.cir").read_text()
def batch(folder, circuit, logname):
    (folder / "inverter.cir").write_text(circuit)
    proc = subprocess.run([spice, "-b", "inverter.cir"], cwd=folder,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    (logs / logname).write_text("$ ngspice -b inverter.cir\n" + proc.stdout + f"\nexit_code={proc.returncode}\n", encoding="utf-8")
    return proc

summary = []
for load in (20, 100):
    with tempfile.TemporaryDirectory() as work:
        folder = Path(work)
        circuit = base.replace("Cload out 0 20p", f"Cload out 0 {load}p")
        proc = batch(folder, circuit, f"batch_{load}pF.log")
        proc.check_returncode()
        trace = np.loadtxt(folder / "trace.dat")
        assert trace.shape[1] == 3 and np.isfinite(trace).all() and np.all(np.diff(trace[:,0]) > 0)
        np.savetxt(results / f"trace_{load}pF.csv", trace, delimiter=",", header="time_s,vin_V,vout_V", comments="", fmt="%.12e")
        delays = [float(re.search(rf"(?m)^{name}\s*=\s*([\d.eE+\-]+)", proc.stdout)[1])*1e9 for name in ("tphl", "tplh")]
        summary.append([load, *delays])
assert all(summary[1][i] > summary[0][i] > 0 for i in (1, 2))
with (results / "delays.csv").open("w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Cload_pF", "tPHL_ns", "tPLH_ns"])
    writer.writerows(summary)
with tempfile.TemporaryDirectory() as work:
    folder = Path(work)
    bad = base.replace("wrdata trace.dat v(in) v(out)", "wrdata trace.dat v(in) v(ouut)")
    proc = batch(folder, bad, "fault_node.log")
    assert "ouut" in proc.stdout.lower() and not (folder / "trace.dat").exists()
    fixed = batch(folder, base, "fixed_node.log")
    fixed.check_returncode()
    assert np.array_equal(np.loadtxt(folder / "trace.dat"), np.loadtxt(results / "trace_20pF.csv", delimiter=",", skiprows=1))
plot(results)
print("OK: 2 simulasi, CSV, plot dan pengujian salah node.")
