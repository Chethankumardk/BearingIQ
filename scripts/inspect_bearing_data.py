# ============================================================
# BearingIQ — Experimental Bearing Vibration Inspection
# ============================================================
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
from src.bearing_utils import load_vibration, PROJECT_ROOT, FS, OPERATING_CONDITION

BEARING_ID = "K001"
RECORDING_NUMBER = 1


def main():
    # 1. Inspect original MATLAB structure and channels
    measurement_id = f"{OPERATING_CONDITION}_{BEARING_ID}_{RECORDING_NUMBER}"
    file_path = PROJECT_ROOT / "data" / "raw" / BEARING_ID / f"{measurement_id}.mat"
    data = loadmat(file_path)
    measurement = data[measurement_id]
    record = measurement[0, 0]
    print("\n========== MATLAB FILE CONTENTS ==========")
    print("Keys:", list(data.keys()))
    print("Available fields:", measurement.dtype.names)
    print("\n========== AVAILABLE CHANNELS ==========")
    for i, channel in enumerate(record["Y"].flat):
        print(f"Channel {i}: name={channel['Name']}, unit={channel['Unit']}")

    # 2. Load vibration_1 with its correct associated time axis
    vibration, time = load_vibration(BEARING_ID, RECORDING_NUMBER)
    print("\n========== VIBRATION DATA ==========")
    print("Samples:", len(vibration))
    print("First 10 samples:", vibration[:10])

    # 3. Inspect timestamp spacing (nominal 64 kHz)
    intervals = np.diff(time)
    nominal_dt = 1 / FS
    unusual = np.sum(np.abs(intervals - nominal_dt) > 0.05 * nominal_dt)
    print("\n========== SAMPLING VALIDATION ==========")
    print("Duration:", time[-1] - time[0], "s")
    print("Mean interval:", np.mean(intervals), "s")
    print("Median interval:", np.median(intervals), "s")
    print("Minimum interval:", np.min(intervals), "s")
    print("Maximum interval:", np.max(intervals), "s")
    print("Non-increasing intervals:", np.sum(intervals <= 0))
    print("Intervals outside 5%:", unusual)

    # 4. Calculate general vibration features
    mean_value = np.mean(vibration)
    rms_value = np.sqrt(np.mean(vibration ** 2))
    peak_value = np.max(np.abs(vibration))
    crest_factor = peak_value / rms_value if rms_value > 0 else np.nan
    print("\n========== VIBRATION STATISTICS ==========")
    print(f"Mean: {mean_value:.6f}")
    print(f"RMS: {rms_value:.6f}")
    print(f"Absolute peak: {peak_value:.6f}")
    print(f"Crest factor: {crest_factor:.6f}")

    # 5. Plot measured vibration against recorded timestamps
    plt.figure(figsize=(11, 4))
    plt.plot(time, vibration, linewidth=0.5)
    plt.xlabel("Recorded time (s)")
    plt.ylabel("Vibration (raw recorded units)")
    plt.title(f"Paderborn {BEARING_ID} — Healthy Bearing Vibration")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
