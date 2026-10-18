
# ============================================================
# BearingIQ - Reusable Engineering Functions
# File: bearing_utils.py
# ============================================================

import numpy as np
from pathlib import Path
from scipy.io import loadmat


# ============================================================
# 1. CONFIGURATION
# ============================================================

OPERATING_CONDITION = "N09_M07_F10"

DATA_DIRECTORY = Path(__file__).resolve().parent / "data" / "raw"


# ============================================================
# 2. LOAD VIBRATION DATA
# ============================================================

def load_vibration(bearing_id, recording_number=1):
    """
    Load vibration_1 data and its corresponding time array
    from a Paderborn bearing MATLAB recording.

    Parameters
    ----------
    bearing_id : str
        Example: "K002" or "KA04"

    recording_number : int
        Recording number, default = 1

    Returns
    -------
    vibration : numpy.ndarray
        Raw vibration measurements

    time : numpy.ndarray
        Corresponding timestamps
    """

    # Construct the measurement identifier
    measurement_id = (
        f"{OPERATING_CONDITION}_{bearing_id}_{recording_number}"
    )

    # Construct the MATLAB file path
    file_path = (
        DATA_DIRECTORY
        / bearing_id
        / f"{measurement_id}.mat"
    )

    # Check that the file exists
    if not file_path.exists():
        raise FileNotFoundError(
            f"MATLAB recording not found: {file_path}"
        )

    # Load MATLAB file
    data = loadmat(file_path)

    # Access the measurement record
    record = data[measurement_id][0, 0]

    # Access measurement channels
    channels = record["Y"]

    # Search for vibration_1
    for i in range(channels.shape[1]):

        channel = channels[0, i]

        channel_name = str(
            np.asarray(channel["Name"]).squeeze().item()
        )

        if channel_name == "vibration_1":

            # Extract vibration measurements
            vibration = np.asarray(
                channel["Data"]
            ).flatten()

            # Identify corresponding time channel
            x_index = int(
                np.asarray(channel["XIndex"]).squeeze()
            ) - 1

            # Extract timestamps
            time = np.asarray(
                record["X"][0, x_index]["Data"]
            ).flatten()

            # Validate sample count
            if len(vibration) != len(time):
                raise ValueError(
                    "Vibration and time arrays have different lengths."
                )

            return vibration, time

    raise ValueError(
        f"vibration_1 channel not found in {file_path}"
    )


# ============================================================
# 3. CALCULATE ONE-SIDED FFT AMPLITUDE SPECTRUM
# ============================================================

def calculate_fft(signal, fs):
    """
    Calculate a one-sided FFT amplitude spectrum.

    Processing:
    1. Remove signal mean
    2. Apply Hann window
    3. Compute real FFT
    4. Correct amplitude for window coherent gain

    Parameters
    ----------
    signal : numpy.ndarray
        Vibration signal

    fs : float
        Nominal sampling frequency in Hz

    Returns
    -------
    frequencies : numpy.ndarray
        FFT frequency bins in Hz

    amplitudes : numpy.ndarray
        One-sided FFT amplitudes in raw recorded units
    """

    signal = np.asarray(signal, dtype=float).flatten()

    if len(signal) < 2:
        raise ValueError(
            "Signal must contain at least two samples."
        )

    if fs <= 0:
        raise ValueError(
            "Sampling frequency must be positive."
        )

    # Remove DC offset
    signal_centered = signal - np.mean(signal)

    # Apply Hann window to reduce spectral leakage
    window = np.hanning(len(signal_centered))

    windowed_signal = signal_centered * window

    # Compute one-sided FFT
    spectrum = np.fft.rfft(windowed_signal)

    # Calculate frequency bins
    frequencies = np.fft.rfftfreq(
        len(signal_centered),
        d=1 / fs
    )

    # Amplitude correction for Hann window
    amplitudes = (
        2 * np.abs(spectrum) / np.sum(window)
    )

    # DC component should not be doubled
    amplitudes[0] /= 2

    # Nyquist component should not be doubled
    # when the original signal length is even
    if len(signal_centered) % 2 == 0:
        amplitudes[-1] /= 2

    return frequencies, amplitudes
