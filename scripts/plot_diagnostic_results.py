# ============================================================
# BearingIQ — Diagnostic Feature Comparison
# ============================================================
import pandas as pd
import matplotlib.pyplot as plt
from src.bearing_utils import PROJECT_ROOT

THRESHOLD_FILE = PROJECT_ROOT / "results" / "calibration_threshold.txt"


def main():
    # 1. Read the full-precision calibration threshold
    if not THRESHOLD_FILE.is_file():
        raise FileNotFoundError("Run python -m scripts.repeatability_fft first.")
    threshold = float(THRESHOLD_FILE.read_text(encoding="utf-8").strip())

    # 2. Read the measured feature table
    file_path = PROJECT_ROOT / "results" / "diagnostic_features.csv"
    data = pd.read_csv(file_path)
    output_dir = PROJECT_ROOT / "results" / "figures"
    output_dir.mkdir(parents=True, exist_ok=True)

    # 2. Plot each bearing without implying a degradation trend
    fig, ax = plt.subplots(figsize=(9, 5))
    for bearing_id, marker in [("K002", "o"), ("KA04", "s")]:
        bearing_data = data[data["bearing_id"] == bearing_id]
        ax.scatter(bearing_data["recording"], bearing_data["amplitude_4x_bpfo"],
                   marker=marker, s=70, label=f"{bearing_id} — "
                   + ("Healthy" if bearing_id == "K002" else "Outer-ring damage"))

    # 3. Show exploratory threshold and held-out boundary
    ax.axhline(threshold, color="red", linestyle="--", label="Exploratory threshold")
    ax.axvline(5.5, color="gray", linestyle=":", label="Calibration / held-out boundary")
    ax.set_xlabel("Recording number")
    ax.set_ylabel("Fourth BPFO harmonic FFT amplitude (raw recorded units)")
    ax.set_title("BearingIQ — Physics-Informed Bearing Condition Monitoring")
    ax.set_xticks([1, 3, 4, 5, 6])
    ax.legend(loc="upper left")
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / "bpfo_diagnostic_comparison.png", dpi=300, bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    main()
