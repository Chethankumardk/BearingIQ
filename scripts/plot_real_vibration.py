# ============================================================
# BearingIQ — Real Healthy vs Damaged Vibration
# ============================================================
import numpy as np
import matplotlib.pyplot as plt
from src.bearing_utils import load_vibration, FS, PROJECT_ROOT


def main():
    # 1. Load real Paderborn vibration measurements
    healthy, _ = load_vibration("K002", recording_number=1)
    damaged, _ = load_vibration("KA04", recording_number=1)

    # 2. Display first 0.1 seconds using nominal sampling frequency
    duration = 0.1
    n_samples = int(FS * duration)
    if min(len(healthy), len(damaged)) < n_samples:
        raise ValueError("Recording is shorter than the requested time window.")
    time = np.arange(n_samples) / FS

    # 3. Compare signals using the same vertical scale
    fig, axes = plt.subplots(2, 1, figsize=(12, 7), sharex=True)
    axes[0].plot(time, healthy[:n_samples], color="tab:blue", linewidth=0.7)
    axes[0].set_title("K002 — Healthy bearing")
    axes[1].plot(time, damaged[:n_samples], color="tab:orange", linewidth=0.7)
    axes[1].set_title("KA04 — Outer-ring damaged bearing")
    axes[1].set_xlabel("Time (s, nominal)")
    max_amplitude = max(np.max(np.abs(healthy[:n_samples])),
                        np.max(np.abs(damaged[:n_samples])))
    for ax in axes:
        ax.set_ylabel("Vibration (raw recorded units)")
        ax.set_ylim(-1.1 * max_amplitude, 1.1 * max_amplitude)
        ax.grid(True, alpha=0.3)
    fig.suptitle("BearingIQ — Real Bearing Vibration Comparison", fontsize=14)
    plt.tight_layout()

    # 4. Save figure
    output_dir = PROJECT_ROOT / "results" / "figures"
    output_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_dir / "vibration_healthy_vs_damaged.png", dpi=300,
                bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    main()
