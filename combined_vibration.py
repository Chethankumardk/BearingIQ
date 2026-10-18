import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import rfft, rfftfreq

sampling_frequency = 1000
duration = 1

time = np.arange(0, duration, 1 / sampling_frequency)

# First vibration component
vibration_1 = 2 * np.sin(2 * np.pi * 10 * time)

# Second vibration component
vibration_2 = 1 * np.sin(2 * np.pi * 30 * time)

# Combined acceleration
combined_vibration = vibration_1 + vibration_2

rng = np.random.default_rng(42)

noise = rng.normal(
    loc=0,
    scale=2.0,
    size=len(combined_vibration)
)

noisy_vibration = combined_vibration + noise

signal_rms = np.sqrt(np.mean(combined_vibration ** 2))

noise_rms = np.sqrt(np.mean(noise ** 2))

print("Signal RMS:", signal_rms, "m/s²")
print("Noise RMS:", noise_rms, "m/s²")

snr_db = 20 * np.log10(signal_rms / noise_rms)

print("Calculated SNR:", snr_db, "dB")


# To Calculate FFT
number_of_samples = len(combined_vibration)

fft_values = rfft(combined_vibration)

fft_frequencies = rfftfreq(
    number_of_samples,
    d=1 / sampling_frequency
)


noisy_fft_values = rfft(noisy_vibration)

noisy_fft_amplitude = (
    2 * np.abs(noisy_fft_values) / number_of_samples
)

print("Number of FFT frequency bins:", len(fft_frequencies))
print("First 5 frequencies:", fft_frequencies[:5])

fft_amplitude = 2 * np.abs(fft_values) / number_of_samples

print("Clean 10 Hz amplitude:", fft_amplitude[10])
print("Noisy 10 Hz amplitude:", noisy_fft_amplitude[10])

print("Clean 30 Hz amplitude:", fft_amplitude[30])
print("Noisy 30 Hz amplitude:", noisy_fft_amplitude[30])

print("Amplitude at 10 Hz:", fft_amplitude[10])
print("Amplitude at 30 Hz:", fft_amplitude[30])

plt.figure()

plt.plot(
    fft_frequencies,
    fft_amplitude,
    label="Clean signal"
)

plt.plot(
    fft_frequencies,
    noisy_fft_amplitude,
    label="Noisy signal",
    alpha=0.7
)

plt.xlabel("Frequency (Hz)")
plt.ylabel("Amplitude (m/s²)")
plt.title("Clean vs Noisy FFT Spectrum")
plt.xlim(0, 50)
plt.legend()
plt.grid(True)
plt.show()