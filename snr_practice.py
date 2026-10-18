import numpy as np

signal_rms = 2.0

noise_rms_A = 0.2
noise_rms_B = 2.0

snr_A = 20 * np.log10(signal_rms / noise_rms_A)
snr_B = 20 * np.log10(signal_rms / noise_rms_B)

print("Measurement A SNR:", snr_A, "dB")
print("Measurement B SNR:", snr_B, "dB")