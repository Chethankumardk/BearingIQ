# ============================================================
# BearingIQ — Held-Out Threshold Evaluation
# ============================================================
import numpy as np
from src.bearing_utils import load_vibration, get_harmonic_amplitude, FS, PROJECT_ROOT

# Use the full-precision threshold saved from calibration recordings.
THRESHOLD_FILE = PROJECT_ROOT / "results" / "calibration_threshold.txt"
RECORDING_NUMBER = 6


def main():
    if not THRESHOLD_FILE.is_file():
        raise FileNotFoundError("Run python -m scripts.repeatability_fft first.")
    threshold = float(THRESHOLD_FILE.read_text(encoding="utf-8").strip())
    print("\n========== HELD-OUT VALIDATION ==========")
    for bearing_id in ["K002", "KA04"]:
        # 1. Load held-out recording
        vibration, time = load_vibration(bearing_id, RECORDING_NUMBER)

        # 2. Check measurement quality
        intervals = np.diff(time)
        nominal_dt = 1 / FS
        unusual = np.sum(np.abs(intervals - nominal_dt) > 0.05 * nominal_dt)

        # 3. Extract fourth-BPFO-harmonic amplitude
        feature = get_harmonic_amplitude(vibration)

        # 4. Apply the fixed calibration threshold
        prediction = "Inspect" if feature > threshold else "Normal"
        expected = "Normal" if bearing_id == "K002" else "Inspect"
        result = "MATCH" if prediction == expected else "MISMATCH"
        print(f"\nBearing: {bearing_id}")
        print(f"Samples: {len(vibration)}")
        print(f"Duration: {time[-1] - time[0]:.6f} s")
        print(f"Unusual timestamp intervals: {unusual}")
        print(f"4x BPFO amplitude: {feature:.6f}")
        print(f"Fixed threshold: {threshold:.6f}")
        print(f"Expected condition: {expected}")
        print(f"Predicted decision: {prediction}")
        print(f"Result: {result}")


if __name__ == "__main__":
    main()
