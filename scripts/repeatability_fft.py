# ============================================================
# BearingIQ — Fourth-BPFO-Harmonic Repeatability
# ============================================================
import csv
import numpy as np
from src.bearing_utils import load_vibration, get_harmonic_amplitude, PROJECT_ROOT

CALIBRATION_RECORDINGS = [1, 3, 4, 5]
HELD_OUT_RECORDING = 6
BEARINGS = {"K002": "healthy", "KA04": "outer_ring_damage"}


def calculate_results():
    """Calculate features and threshold without using held-out data."""
    rows = []
    calibration = {}
    print("\n========== BPFO REPEATABILITY ==========")
    for bearing_id, condition in BEARINGS.items():
        amplitudes = []
        print(f"\nBearing: {bearing_id}")
        for recording_number in CALIBRATION_RECORDINGS:
            vibration, _ = load_vibration(bearing_id, recording_number)
            amplitude = get_harmonic_amplitude(vibration)
            amplitudes.append(amplitude)
            rows.append([bearing_id, condition, recording_number, amplitude, "calibration"])
            print(f"Recording {recording_number}: {amplitude:.6f}")
        calibration[bearing_id] = np.asarray(amplitudes)
        mean_amplitude = np.mean(amplitudes)
        std_amplitude = np.std(amplitudes, ddof=1)
        cv = 100 * std_amplitude / mean_amplitude if mean_amplitude > 0 else np.nan
        print(f"Mean amplitude: {mean_amplitude:.6f}")
        print(f"Standard deviation: {std_amplitude:.6f}")
        print(f"CV: {cv:.2f}%")

    # Threshold selected only from calibration recordings
    threshold = (np.max(calibration["K002"]) + np.min(calibration["KA04"])) / 2
    print("\n========== EXPLORATORY THRESHOLD ==========")
    print(f"Threshold: {threshold:.6f}")
    for bearing_id, amplitudes in calibration.items():
        for amplitude in amplitudes:
            prediction = "Inspect" if amplitude > threshold else "Normal"
            print(f"{bearing_id}: {amplitude:.6f} -> {prediction}")

    # Held-out features are calculated after threshold selection
    for bearing_id, condition in BEARINGS.items():
        vibration, _ = load_vibration(bearing_id, HELD_OUT_RECORDING)
        amplitude = get_harmonic_amplitude(vibration)
        rows.append([bearing_id, condition, HELD_OUT_RECORDING, amplitude, "held_out"])

    return rows, threshold


def main():
    rows, threshold = calculate_results()
    output_path = PROJECT_ROOT / "results" / "diagnostic_features.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["bearing_id", "condition", "recording",
                         "amplitude_4x_bpfo", "dataset_split"])
        for bearing_id, condition, recording_number, amplitude, split in rows:
            writer.writerow([bearing_id, condition, recording_number,
                             f"{amplitude:.6f}", split])
    # Save the full-precision threshold for validation and plots.
    threshold_path = PROJECT_ROOT / "results" / "calibration_threshold.txt"
    threshold_path.write_text(f"{threshold:.17g}\n", encoding="utf-8")
    print(f"\nThreshold saved: {threshold_path}")
    print(f"Feature table saved: {output_path}")
    print("Note: threshold was calibrated on recordings 1, 3, 4 and 5 only.")


if __name__ == "__main__":
    main()
