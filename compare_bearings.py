
"""
BearingIQ — Healthy vs Damaged Bearing Comparison
================================================

Objective:
    Compare vibration measurements from two healthy bearings
    (K001, K002) and one damaged bearing (KA04).

Operating condition:
    N09_M07_F10

Analysis:
    1. Load vibration data
    2. Validate sample counts
    3. Calculate vibration features
    4. Compare bearing measurements
    5. Check measurement duration

Note:
    Physical vibration units are not yet verified.
"""

# ============================================================
# 1. IMPORT LIBRARIES
# ============================================================

import numpy as np
from scipy.io import loadmat


# ============================================================
# 2. CONFIGURATION
# ============================================================
# Keep bearing IDs and operating conditions in one place.

OPERATING_CONDITION = "N09_M07_F10"

BEARINGS = {
    "K001": "Healthy",
    "K002": "Healthy",
    "KA04": "Damaged — outer ring",
}


# ============================================================
# 3. LOAD VIBRATION DATA
# ============================================================
# WHAT: Load vibration measurements from MATLAB files.
# WHY: Apply the same loading method to every bearing.
#
# Channel identification is based on the channel name
# rather than a fixed channel position.

def load_vibration(bearing_id, recording_number=1):

    measurement_id = (
    f"{OPERATING_CONDITION}_{bearing_id}_{recording_number}"
    )

    file_path = (
        f"data/raw/{bearing_id}/{measurement_id}.mat"
    )

    data = loadmat(file_path)
    record = data[measurement_id][0, 0]

    channels = record["Y"]

    for i in range(channels.shape[1]):

        channel = channels[0, i]

        channel_name = str(
            np.asarray(channel["Name"]).squeeze().item()
        )

        if channel_name == "vibration_1":

            vibration = channel["Data"].flatten()

            # MATLAB XIndex is one-based.
            # Convert it to a Python zero-based index.
            x_index = int(
                np.asarray(channel["XIndex"]).squeeze()
            ) - 1

            time = (
                record["X"][0, x_index]["Data"].flatten()
            )

            if len(time) != len(vibration):
                raise ValueError(
                    f"Timestamp/sample mismatch: {bearing_id}"
                )

            return vibration, time

    raise ValueError(
        f"Vibration channel not found: {bearing_id}"
    )


# ============================================================
# 4. CALCULATE VIBRATION FEATURES
# ============================================================
# WHAT: Calculate statistical vibration indicators.
# WHY: Quantify and compare measured vibration behaviour.
#
# Mean:
#     Average signal value.
#
# RMS:
#     Overall vibration magnitude.
#
# Absolute peak:
#     Maximum absolute vibration value.
#
# Crest factor:
#     Ratio of absolute peak to RMS.

def calculate_features(vibration):

    if vibration.size == 0:
        raise ValueError("Vibration array is empty.")

    mean_value = np.mean(vibration)

    rms_value = np.sqrt(
        np.mean(vibration ** 2)
    )

    peak_value = np.max(
        np.abs(vibration)
    )

    crest_factor = (
        peak_value / rms_value
        if rms_value > 0
        else np.nan
    )

    return {
        "Mean": mean_value,
        "RMS": rms_value,
        "Absolute peak": peak_value,
        "Crest factor": crest_factor,
    }


# ============================================================
# 5. LOAD ALL THREE BEARINGS
# ============================================================
# WHAT: Load K001, K002 and KA04.
# WHY: Compare healthy references against a damaged bearing.

measurements = {}

for bearing_id in BEARINGS:

    vibration, time = load_vibration(bearing_id)

    measurements[bearing_id] = {
        "vibration": vibration,
        "time": time,
        "features": calculate_features(vibration),
    }

    print(
        f"{bearing_id} ({BEARINGS[bearing_id]}): "
        f"{len(vibration)} samples loaded"
    )


# ============================================================
# 6. COMPARE VIBRATION FEATURES
# ============================================================
# WHAT: Print features for all three bearings.
# WHY: Identify similarities and differences.
#
# IMPORTANT:
# A larger RMS or crest factor does not automatically
# indicate a damaged bearing.

print("\n========== BEARING COMPARISON ==========")

print(
    f"{'Feature':<18}"
    f"{'K001 Healthy':>16}"
    f"{'K002 Healthy':>16}"
    f"{'KA04 Damaged':>16}"
)

print("-" * 66)

feature_names = [
    "Mean",
    "RMS",
    "Absolute peak",
    "Crest factor",
]

for feature in feature_names:

    values = [
        measurements[bearing_id]["features"][feature]
        for bearing_id in BEARINGS
    ]

    print(
        f"{feature:<18}"
        + "".join(
            f"{value:>16.6f}" for value in values
        )
    )


# ============================================================
# 7. CHECK MEASUREMENT DURATION
# ============================================================
# WHAT: Check sample counts and recording durations.
# WHY: Identify possible differences in data acquisition.
#
# The documented nominal vibration sampling rate is 64 kHz.
# Recorded timestamps still require quality validation.

print("\n========== MEASUREMENT DURATION ==========")

for bearing_id, measurement in measurements.items():

    time = measurement["time"]
    vibration = measurement["vibration"]

    duration = time[-1] - time[0]

    print(
        f"{bearing_id}: "
        f"{len(vibration)} samples, "
        f"{duration:.6f} seconds"
    )


# ============================================================
# 8. BASIC TIMESTAMP QUALITY CHECK
# ============================================================
# WHAT: Detect non-increasing timestamps.
# WHY: A conventional FFT requires uniform sampling.
#
# This is only an initial check, not full validation.

print("\n========== TIMESTAMP QUALITY ==========")

for bearing_id, measurement in measurements.items():

    time = measurement["time"]

    intervals = np.diff(time)

    non_increasing = np.sum(intervals <= 0)

    print(
        f"{bearing_id}: "
        f"{non_increasing} non-increasing intervals"
    )


# ============================================================
# 9. TIMESTAMP SPACING VALIDATION
# ============================================================

nominal_dt = 1 / 64000

print("\n========== TIMESTAMP SPACING ==========")

for bearing_id in ["K002", "KA04"]:

    time = measurements[bearing_id]["time"]

    dt = np.diff(time)

    mean_dt = np.mean(dt)
    median_dt = np.median(dt)
    min_dt = np.min(dt)
    max_dt = np.max(dt)

    # Count intervals differing by more than 5%
    # from the nominal sampling interval.
    unusual_intervals = np.sum(
        np.abs(dt - nominal_dt) > 0.05 * nominal_dt
    )

    print(f"\nBearing: {bearing_id}")
    print(f"Mean interval:   {mean_dt * 1e6:.6f} us")
    print(f"Median interval: {median_dt * 1e6:.6f} us")
    print(f"Minimum interval:{min_dt * 1e6:.6f} us")
    print(f"Maximum interval:{max_dt * 1e6:.6f} us")
    print(f"Intervals outside 5%: {unusual_intervals}")


# ============================================================
# 10. TEST MULTIPLE RECORDING LOADING
# ============================================================

print("\n========== MULTIPLE RECORDING TEST ==========")

for bearing_id in ["K002", "KA04"]:

    for recording_number in range(1, 6):

        vibration, time = load_vibration(
            bearing_id,
            recording_number
        )

        print(
            f"{bearing_id} recording {recording_number}: "
            f"{len(vibration)} samples"
        )

# ============================================================
# 11. MULTIPLE RECORDING TIMING VALIDATION
# ============================================================

print("\n========== RECORDING TIMING VALIDATION ==========")

fs = 64000
nominal_dt = 1 / fs

for bearing_id in ["K002", "KA04"]:

    for recording_number in range(1, 6):

        vibration, time = load_vibration(
            bearing_id,
            recording_number
        )

        dt = np.diff(time)

        duration = time[-1] - time[0]

        unusual_intervals = np.sum(
            np.abs(dt - nominal_dt) > 0.05 * nominal_dt
        )

        print(
            f"{bearing_id}-{recording_number}: "
            f"samples={len(vibration)}, "
            f"duration={duration:.6f}s, "
            f"unusual_intervals={unusual_intervals}"
        )