# ============================================================
# BearingIQ — Fourth-BPFO-Harmonic Repeatability Plot
# ============================================================
import pandas as pd
import matplotlib.pyplot as plt
from src.bearing_utils import PROJECT_ROOT


def main():
    # 1. Load measured features from CSV
    data = pd.read_csv(PROJECT_ROOT / "results" / "diagnostic_features.csv")
    fig, ax = plt.subplots(figsize=(9, 5))

    # 2. Separate calibration and held-out recordings
    for bearing_id, color in [("K002", "tab:blue"), ("KA04", "tab:orange")]:
        subset = data[data["bearing_id"] == bearing_id]
        calibration = subset[subset["dataset_split"] == "calibration"]
        held_out = subset[subset["dataset_split"] == "held_out"]
        ax.scatter(calibration["recording"], calibration["amplitude_4x_bpfo"],
                   color=color, s=70, label=f"{bearing_id} — Calibration")
        ax.scatter(held_out["recording"], held_out["amplitude_4x_bpfo"],
                   color=color, marker="D", edgecolors="black", s=85,
                   label=f"{bearing_id} — Held-out")

    # 3. Save engineering figure
    ax.set_xlabel("Recording number")
    ax.set_ylabel("4× BPFO amplitude (raw recorded units)")
    ax.set_title("BearingIQ — Fourth-BPFO-Harmonic Repeatability")
    ax.set_xticks([1, 3, 4, 5, 6])
    ax.grid(True, alpha=0.3)
    ax.legend()
    plt.tight_layout()
    output_dir = PROJECT_ROOT / "results" / "figures"
    output_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_dir / "bpfo_repeatability.png", dpi=300, bbox_inches="tight")
    plt.show()


if __name__ == "__main__":
    main()
