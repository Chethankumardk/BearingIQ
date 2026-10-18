
# ============================================================
# BearingIQ - Held-Out Threshold Evaluation
# File: validate_threshold.py
# ============================================================

import numpy as np
from bearing_utils import load_vibration, calculate_fft


# ============================================================
# 1. CONFIGURATION
# ============================================================

FS = 64000
BPFO = 45.81

TARGET_FREQUENCY = 4 * BPFO
SEARCH_WIDTH = 2.0

# Threshold selected using recordings 1, 3, 4 and 5
THRESHOLD = 0.019952

# Recording 6 was not used to select the threshold
RECORDING_NUMBER = 6


# ============================================================
# 2. CALCULATE THE DIAGNOSTIC FEATURE
# ============================================================

def extract_fault_feature(vibration):

    frequencies, amplitudes = calculate_fft(
        vibration, FS
    )

    mask = (
        (frequencies >= TARGET_FREQUENCY - SEARCH_WIDTH)
        & (frequencies <= TARGET_FREQUENCY + SEARCH_WIDTH)
    )

    return np.max(amplitudes[mask])


# ============================================================
# 3. EVALUATE HELD-OUT RECORDINGS
# ============================================================

print("\n========== HELD-OUT VALIDATION ==========")

for bearing_id in ["K002", "KA04"]:

    vibration, time = load_vibration(
        bearing_id,
        RECORDING_NUMBER
    )

    # Measurement quality checks
    sample_count = len(vibration)
    duration = time[-1] - time[0]

    dt = np.diff(time)
    nominal_dt = 1 / FS

    unusual_intervals = np.sum(
        np.abs(dt - nominal_dt) > 0.05 * nominal_dt
    )

    # Extract fourth BPFO harmonic amplitude
    feature = extract_fault_feature(vibration)

    # Apply the previously selected threshold
    prediction = (
        "Inspect" if feature > THRESHOLD else "Normal"
    )

    expected = (
        "Normal" if bearing_id == "K002" else "Inspect"
    )

    result = (
        "MATCH" if prediction == expected else "MISMATCH"
    )

    print(f"\nBearing: {bearing_id}")
    print(f"Samples: {sample_count}")
    print(f"Duration: {duration:.6f} s")
    print(f"Unusual timestamp intervals: {unusual_intervals}")
    print(f"4x BPFO amplitude: {feature:.6f}")
    print(f"Fixed threshold: {THRESHOLD:.6f}")
    print(f"Expected condition: {expected}")
    print(f"Predicted decision: {prediction}")
    print(f"Result: {result}")
