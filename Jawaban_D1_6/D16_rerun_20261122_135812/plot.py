from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def plot(results):
    fig, ax = plt.subplots(figsize=(8, 4.5), layout="constrained")
    for load in (20, 100):
        data = np.genfromtxt(results / f"trace_{load}pF.csv", delimiter=",", names=True)
        ns = data["time_s"] * 1e9
        if load == 20:
            ax.plot(ns, data["vin_V"], color="grey", linestyle=":", label="Masukan")
        ax.plot(ns, data["vout_V"], label=f"Keluaran {load} pF")
    ax.axhline(2.5, color="#667", lw=0.8, ls="--", label="Ambang ukur 50%")
    ax.set(xlabel="Waktu (ns)", ylabel="Tegangan (V)", title="Respons inverter saat beban kapasitif berubah")
    ax.legend()
    ax.grid(alpha=0.2)
    fig.savefig(results / "transient.png", dpi=180)
    plt.close(fig)

if __name__ == "__main__":
    plot(Path("results"))
