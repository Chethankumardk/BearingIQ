import numpy as np

amplitudes = np.array([1.00, 1.03, 0.98, 1.02, 0.99])

mean_amplitude = np.mean(amplitudes)

standard_deviation = np.std(amplitudes, ddof=1)

print("Sample standard deviation:", standard_deviation, "m/s²")

print("Mean amplitude:", mean_amplitude, "m/s²")


coefficient_of_variation = (standard_deviation / mean_amplitude) * 100

print("Coefficient of variation:", coefficient_of_variation, "%")