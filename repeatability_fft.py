import numpy as np

from bearing_utils import load_vibration, calculate_fft

# ============================================================
# CONFIGURATION
# ============================================================

fs = 64000
bpfo = 45.81

target_frequency = 4 * bpfo
search_width = 2.0

recording_numbers = [1, 3, 4, 5]


# ============================================================
# EXTRACT HARMONIC AMPLITUDE
# ============================================================

def get_harmonic_amplitude(vibration):

    frequencies, amplitudes = calculate_fft(
        vibration, fs
    )

    mask = (
        (frequencies >= target_frequency - search_width)
        & (frequencies <= target_frequency + search_width)
    )

    return np.max(amplitudes[mask])


# ============================================================
# COMPARE REPEATED RECORDINGS
# ============================================================

print("\n========== BPFO REPEATABILITY ==========")

for bearing_id in ["K002", "KA04"]:

    harmonic_amplitudes = []

    print(f"\nBearing: {bearing_id}")

    for recording_number in recording_numbers:

        vibration, time = load_vibration(
            bearing_id, recording_number
        )

        amplitude = get_harmonic_amplitude(vibration)

        harmonic_amplitudes.append(amplitude)

        print(
            f"Recording {recording_number}: "
            f"{amplitude:.6f}"
        )

    mean_amplitude = np.mean(harmonic_amplitudes)
    std_amplitude = np.std(
        harmonic_amplitudes, ddof=1
    )

    cv = (
        100 * std_amplitude / mean_amplitude
        if mean_amplitude > 0
        else np.nan
    )

    print(f"Mean amplitude: {mean_amplitude:.6f}")
    print(f"Standard deviation: {std_amplitude:.6f}")
    print(f"CV: {cv:.2f}%")

# ============================================================
# 4. EXPLORATORY DIAGNOSTIC THRESHOLD
# ============================================================

healthy_amplitudes = np.array([
    0.001386, 0.001075, 0.001085, 0.001364
])

damaged_amplitudes = np.array([
    0.039767, 0.039132, 0.038519, 0.038597
])

threshold = (
    np.max(healthy_amplitudes)
    + np.min(damaged_amplitudes)
) / 2

print("\n========== EXPLORATORY THRESHOLD ==========")
print(f"Threshold: {threshold:.6f}")

for amplitude in healthy_amplitudes:
    prediction = "Inspect" if amplitude > threshold else "Normal"
    print(f"K002: {amplitude:.6f} -> {prediction}")

for amplitude in damaged_amplitudes:
    prediction = "Inspect" if amplitude > threshold else "Normal"
    print(f"KA04: {amplitude:.6f} -> {prediction}")