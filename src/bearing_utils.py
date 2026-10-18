"""Shared loading and FFT calculations for Paderborn bearing data."""

from pathlib import Path
import numpy as np
from scipy.io import loadmat

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OPERATING_CONDITION = "N09_M07_F10"
FS = 64000  # Documented nominal sampling frequency (Hz)
BPFO = 45.81  # Approximate theoretical outer-ring fault frequency (Hz)


def load_vibration(bearing_id, recording_number=1):
    """Return vibration_1 samples and their associated MATLAB timestamps."""
    measurement_id = f"{OPERATING_CONDITION}_{bearing_id}_{recording_number}"
    file_path = PROJECT_ROOT / "data" / "raw" / bearing_id / f"{measurement_id}.mat"
    if not file_path.is_file():
        raise FileNotFoundError(f"Missing Paderborn recording: {file_path}")

    data = loadmat(file_path)
    record = data[measurement_id][0, 0]
    channels = record["Y"]

    for channel in channels.flat:
        channel_name = str(np.asarray(channel["Name"]).squeeze().item())
        if channel_name == "vibration_1":
            vibration = np.asarray(channel["Data"]).flatten()
            # MATLAB XIndex is one-based; Python indices start at zero.
            x_index = int(np.asarray(channel["XIndex"]).squeeze()) - 1
            time = np.asarray(record["X"][0, x_index]["Data"]).flatten()
            if len(vibration) != len(time):
                raise ValueError(f"Timestamp/sample mismatch: {measurement_id}")
            return vibration, time

    raise ValueError(f"vibration_1 channel not found: {measurement_id}")


def calculate_fft(signal, fs=FS):
    """Calculate Hann-windowed, coherent-gain-corrected one-sided FFT amplitude."""
    signal = np.asarray(signal, dtype=float).flatten()
    if signal.size < 2:
        raise ValueError("At least two vibration samples are required.")
    if fs <= 0:
        raise ValueError("Sampling frequency must be positive.")

    signal = signal - np.mean(signal)
    window = np.hanning(len(signal))
    spectrum = np.fft.rfft(signal * window)
    frequencies = np.fft.rfftfreq(len(signal), d=1 / fs)
    amplitude = 2 * np.abs(spectrum) / np.sum(window)
    amplitude[0] /= 2
    if len(signal) % 2 == 0:
        amplitude[-1] /= 2
    return frequencies, amplitude


def get_harmonic_amplitude(vibration, harmonic=4, search_width=2.0):
    """Maximum FFT amplitude within ±search_width Hz of a BPFO harmonic."""
    frequencies, amplitudes = calculate_fft(vibration)
    target = harmonic * BPFO
    mask = np.abs(frequencies - target) <= search_width
    if not np.any(mask):
        raise ValueError("No FFT frequency bins inside the requested search window.")
    return float(np.max(amplitudes[mask]))
