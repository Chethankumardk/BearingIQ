# ============================================================
# BearingIQ — Healthy vs Damaged Bearing Comparison
# ============================================================
import numpy as np
from src.bearing_utils import load_vibration, FS

BEARINGS = {
    "K001": "Healthy",
    "K002": "Healthy",
    "KA04": "Damaged — outer ring",
}


def calculate_features(vibration):
    """Calculate mean, RMS, absolute peak, and crest factor."""
    vibration = np.asarray(vibration)
    if vibration.size == 0:
        raise ValueError("Vibration array is empty.")
    mean_value = np.mean(vibration)
    rms_value = np.sqrt(np.mean(vibration ** 2))
    peak_value = np.max(np.abs(vibration))
    crest_factor = peak_value / rms_value if rms_value > 0 else np.nan
    return {
        "Mean": mean_value,
        "RMS": rms_value,
        "Absolute peak": peak_value,
        "Crest factor": crest_factor,
    }


def main():
    # 1. Load and analyze the three bearings
    measurements = {}
    for bearing_id in BEARINGS:
        vibration, time = load_vibration(bearing_id)
        measurements[bearing_id] = {
            "vibration": vibration,
            "time": time,
            "features": calculate_features(vibration),
        }
        print(f"{bearing_id} ({BEARINGS[bearing_id]}): {len(vibration)} samples loaded")

    # 2. Compare time-domain vibration indicators
    print("\n========== BEARING COMPARISON ==========")
    print(f"{'Feature':<18}{'K001 Healthy':>16}{'K002 Healthy':>16}{'KA04 Damaged':>16}")
    for feature in ["Mean", "RMS", "Absolute peak", "Crest factor"]:
        print(f"{feature:<18}" + "".join(
            f"{measurements[b]['features'][feature]:>16.6f}" for b in BEARINGS
        ))

    # 3. Check timestamps and recording duration
    print("\n========== TIMESTAMP QUALITY ==========")
    nominal_dt = 1 / FS
    for bearing_id, measurement in measurements.items():
        time = measurement["time"]
        intervals = np.diff(time)
        unusual = np.sum(np.abs(intervals - nominal_dt) > 0.05 * nominal_dt)
        print(f"{bearing_id}: samples={len(time)}, "
              f"duration={time[-1] - time[0]:.6f}s, "
              f"non_increasing={np.sum(intervals <= 0)}, "
              f"unusual_intervals={unusual}")

    # 4. Check multiple recordings
    print("\n========== MULTIPLE RECORDING CHECK ==========")
    for bearing_id in ["K002", "KA04"]:
        for recording_number in range(1, 6):
            vibration, time = load_vibration(bearing_id, recording_number)
            intervals = np.diff(time)
            unusual = np.sum(np.abs(intervals - nominal_dt) > 0.05 * nominal_dt)
            print(f"{bearing_id}-{recording_number}: "
                  f"samples={len(vibration)}, "
                  f"duration={time[-1] - time[0]:.6f}s, "
                  f"unusual_intervals={unusual}")


if __name__ == "__main__":
    main()
