
"""
BearingIQ — Experimental Bearing Vibration Inspection
=====================================================

Dataset:
    Paderborn University Bearing DataCenter

Measurement:
    K001 — Healthy bearing
    N09_M07_F10_K001_1.mat

Objective:
    Load and inspect experimental bearing data, identify the vibration
    channel, validate timestamp information, calculate basic vibration
    indicators, and visualize the measured signal.

Important assumptions:
    - Channel 'vibration_1' is the vibration measurement of interest.
    - Physical vibration units have not yet been verified.
    - The timestamps may contain irregularities.
    - No bearing fault diagnosis is performed in this script.
"""

# ============================================================
# 1. IMPORT LIBRARIES
# ============================================================
# NumPy: numerical calculations and array operations.
# SciPy: loading MATLAB measurement files.
# Matplotlib: engineering plots.

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat


# ============================================================
# 2. CONFIGURATION
# ============================================================
# Keep measurement-specific information in one place.
# This makes it easier to analyze other bearing recordings.

BEARING_ID = "K001"
MEASUREMENT_ID = "N09_M07_F10_K001_1"

FILE_PATH = f"data/raw/{BEARING_ID}/{MEASUREMENT_ID}.mat"

# Nominal reference frequency for investigating timestamps.
# This is not yet a validated FFT sampling frequency.
NOMINAL_SAMPLING_FREQUENCY = 64000  # Hz


# ============================================================
# 3. LOAD MATLAB MEASUREMENT
# ============================================================
# WHAT: Read the experimental measurement.
# WHY: Access the original recorded data without modifying it.

data = loadmat(FILE_PATH)

print("\n========== MATLAB FILE CONTENTS ==========")

for key in data.keys():
    print(key)

# Extract the measurement structure using its identifier.
measurement = data[MEASUREMENT_ID]

print("\nMeasurement type:", type(measurement))
print("Measurement shape:", measurement.shape)
print("Available fields:", measurement.dtype.names)

# The measurement is stored as a (1, 1) structured array.
record = measurement[0, 0]


# ============================================================
# 4. INSPECT MEASUREMENT STRUCTURE
# ============================================================
# WHAT: Examine the available fields and measurement channels.
# WHY: Avoid accidentally analyzing the wrong physical quantity.

print("\n========== MEASUREMENT STRUCTURE ==========")

for field in measurement.dtype.names:
    value = record[field]

    print(f"\nField: {field}")
    print("Shape:", value.shape)
    print("Data type:", value.dtype)


# The Y field contains the measurement channels.
channels = record["Y"]

print("\n========== AVAILABLE CHANNELS ==========")

for i in range(channels.shape[1]):
    channel = channels[0, i]

    print(f"\nChannel {i}")
    print("Name:", channel["Name"])
    print("Unit:", channel["Unit"])


# ============================================================
# 5. EXTRACT VIBRATION SIGNAL
# ============================================================
# WHAT: Retrieve vibration samples from channel 6.
# WHY: Prepare a one-dimensional array for signal analysis.
#
# IMPORTANT:
# Channel 6 was identified as 'vibration_1' by inspecting
# the original file. The index must be verified for other files.

VIBRATION_CHANNEL_INDEX = 6

vibration_channel = channels[0, VIBRATION_CHANNEL_INDEX]

raw_vibration = vibration_channel["Data"]

# Convert from shape (1, N) to shape (N,).
vibration = raw_vibration.flatten()

print("\n========== VIBRATION DATA ==========")

print("Original shape:", raw_vibration.shape)
print("Sample count:", len(vibration))
print("Data type:", vibration.dtype)
print("First 10 samples:", vibration[:10])
print("Channel raster:", vibration_channel["Raster"])
print("Channel XIndex:", vibration_channel["XIndex"])


# ============================================================
# 6. INSPECT TIME AXES
# ============================================================
# WHAT: Inspect available timestamp arrays.
# WHY: A correct time axis is necessary for time-domain plots
#      and later frequency-domain analysis.

print("\n========== AVAILABLE TIME AXES ==========")

for i in range(record["X"].shape[1]):
    axis = record["X"][0, i]

    print(f"\nAxis {i}")
    print("Name:", axis["Name"])
    print("Type:", axis["Type"])
    print("Unit:", axis["Unit"])
    print("Raster:", axis["Raster"])
    print("Sample count:", axis["Data"].size)
    print("First 5 values:", axis["Data"].flatten()[:5])


# The HostService axis was identified as the matching time
# array for this vibration channel.
TIME_AXIS_INDEX = 1

time = record["X"][0, TIME_AXIS_INDEX]["Data"].flatten()

# Check that every vibration sample has a timestamp.
if len(time) != len(vibration):
    raise ValueError(
        "Time and vibration arrays have different lengths."
    )


# ============================================================
# 7. VALIDATE SAMPLING INFORMATION
# ============================================================
# WHAT: Calculate time differences between adjacent samples.
# WHY: Standard FFT methods assume uniformly sampled data.

time_intervals = np.diff(time)

mean_dt = np.mean(time_intervals)
median_dt = np.median(time_intervals)

estimated_sampling_frequency = 1 / mean_dt

recording_duration = time[-1] - time[0]

nominal_dt = 1 / NOMINAL_SAMPLING_FREQUENCY

relative_error = (
    np.abs(time_intervals - nominal_dt) / nominal_dt
)

unusual_intervals = np.sum(relative_error > 0.05)

print("\n========== SAMPLING VALIDATION ==========")

print("Time samples:", len(time))
print("Mean interval:", mean_dt, "s")
print("Median interval:", median_dt, "s")
print("Estimated frequency:", estimated_sampling_frequency, "Hz")
print("Minimum interval:", np.min(time_intervals), "s")
print("Maximum interval:", np.max(time_intervals), "s")
print("Recording duration:", recording_duration, "s")
print("Intervals deviating more than 5%:", unusual_intervals)
print("Total intervals:", len(time_intervals))

# NOTE:
# The estimated frequency is based on mean timestamp spacing.
# We must not automatically treat it as the correct FFT
# sampling frequency without further validation.


# ============================================================
# 8. CALCULATE VIBRATION FEATURES
# ============================================================
# WHAT: Quantify basic characteristics of the vibration.
# WHY: These indicators provide a reference for later
#      healthy-versus-damaged bearing comparisons.

# Mean: average recorded vibration level.
mean_vibration = np.mean(vibration)

# RMS: overall magnitude of the measured vibration.
rms_vibration = np.sqrt(np.mean(vibration ** 2))

# Absolute peak: largest vibration magnitude.
peak_vibration = np.max(np.abs(vibration))

# Crest factor: peak relative to RMS.
# A high value indicates large peaks relative to the
# overall signal magnitude, but does not prove damage.
crest_factor = peak_vibration / rms_vibration

print("\n========== VIBRATION STATISTICS ==========")

print("Bearing:", BEARING_ID)
print("Mean:", mean_vibration)
print("RMS:", rms_vibration)
print("Absolute peak:", peak_vibration)
print("Crest factor:", crest_factor)

# Units remain unverified and are treated as raw recorded units.


# ============================================================
# 9. VISUALIZE VIBRATION
# ============================================================
# WHAT: Plot the original measured vibration against time.
# WHY: Inspect amplitude variation, transients and possible
#      measurement-quality issues before further analysis.

plt.figure(figsize=(11, 4))

plt.plot(time, vibration, linewidth=0.5)

plt.xlabel("Time (s)")
plt.ylabel("Vibration (raw recorded units)")

plt.title(
    f"Paderborn {BEARING_ID} — Healthy Bearing Vibration"
)

plt.grid(True)
plt.tight_layout()

plt.show()
