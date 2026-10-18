# ============================================================
# BearingIQ — FFT Comparison
# Healthy K002 vs Damaged KA04
# ============================================================

import numpy as np
import matplotlib.pyplot as plt

from scipy.signal import find_peaks
from compare_bearings import load_vibration

# 1. Measurement configuration
fs = 64000  # Hz, documented nominal sampling frequency

# 2. Load the vibration signals
healthy, _ = load_vibration("K002")
damaged, _ = load_vibration("KA04")

# 3. Calculate FFT magnitude spectrum
def calculate_fft(signal, fs):

    # Remove the mean (DC offset)
    signal = signal - np.mean(signal)

    # Apply Hann window to reduce spectral leakage
    window = np.hanning(len(signal))
    windowed_signal = signal * window

    # Calculate real-valued FFT
    spectrum = np.fft.rfft(windowed_signal)

    # Calculate frequency axis
    frequencies = np.fft.rfftfreq(
        len(signal), d=1/fs
    )

    # Window-corrected, one-sided amplitude spectrum
    amplitude = (
        2 * np.abs(spectrum) / np.sum(window)
    )

    # DC and Nyquist bins are not doubled
    amplitude[0] /= 2

    if len(signal) % 2 == 0:
        amplitude[-1] /= 2

    return frequencies, amplitude


# 4. Calculate spectra
freq_healthy, amp_healthy = calculate_fft(healthy, fs)
freq_damaged, amp_damaged = calculate_fft(damaged, fs)


# 5. Plot the frequency spectra
plt.figure(figsize=(12, 6))

plt.plot(
    freq_healthy,
    amp_healthy,
    label="K002 — Healthy",
    alpha=0.8
)

plt.plot(
    freq_damaged,
    amp_damaged,
    label="KA04 — Outer-ring damage",
    alpha=0.8
)

plt.xlim(0, 500)
plt.xlabel("Frequency (Hz)")
plt.ylabel("Amplitude (raw recorded units)")
plt.title("BearingIQ — Raw Vibration FFT Comparison")
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()


# ============================================================
# 6. VERIFY THEORETICAL BPFO HARMONICS
# ============================================================

bpfo = 45.81  # Hz
search_width = 2.0  # Hz

print("\n========== BPFO HARMONIC VERIFICATION ==========")

print(
    f"{'Harmonic':<12}"
    f"{'Expected Hz':>14}"
    f"{'Measured Hz':>14}"
    f"{'Amplitude':>14}"
)

for harmonic in range(1, 7):

    expected_frequency = harmonic * bpfo

    # Search near each theoretical harmonic.
    mask = (
        (freq_damaged >= expected_frequency - search_width)
        & (freq_damaged <= expected_frequency + search_width)
    )

    local_frequencies = freq_damaged[mask]
    local_amplitudes = amp_damaged[mask]

    peak_index = np.argmax(local_amplitudes)

    measured_frequency = local_frequencies[peak_index]
    measured_amplitude = local_amplitudes[peak_index]

    print(
        f"{harmonic:<12}"
        f"{expected_frequency:>14.2f}"
        f"{measured_frequency:>14.2f}"
        f"{measured_amplitude:>14.6f}"
    )

# ============================================================
# 7. HEALTHY VS DAMAGED BPFO AMPLITUDE COMPARISON
# ============================================================

print("\n========== HEALTHY VS DAMAGED BPFO ==========")

print(
    f"{'Harmonic':<12}"
    f"{'K002 amplitude':>18}"
    f"{'KA04 amplitude':>18}"
    f"{'Ratio':>12}"
)

for harmonic in range(1, 7):

    expected_frequency = harmonic * bpfo

    healthy_mask = (
        (freq_healthy >= expected_frequency - search_width)
        & (freq_healthy <= expected_frequency + search_width)
    )

    damaged_mask = (
        (freq_damaged >= expected_frequency - search_width)
        & (freq_damaged <= expected_frequency + search_width)
    )

    healthy_amplitude = np.max(amp_healthy[healthy_mask])
    damaged_amplitude = np.max(amp_damaged[damaged_mask])

    ratio = (
        damaged_amplitude / healthy_amplitude
        if healthy_amplitude > 0
        else np.nan
    )

    print(
        f"{harmonic:<12}"
        f"{healthy_amplitude:>18.6f}"
        f"{damaged_amplitude:>18.6f}"
        f"{ratio:>12.2f}"
    )