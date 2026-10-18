# ============================================================
# BearingIQ — Rms Practice
# Learning exercise (synthetic data, not bearing measurements)
# ============================================================

import numpy as np

acceleration = np.array([2, -3, 4, -2, 3])

print("Acceleration samples:", acceleration)
print("Number of samples:", len(acceleration))

squared_acceleration = acceleration ** 2

print("Squared acceleration:", squared_acceleration)

mean_squared = np.mean(squared_acceleration)

rms_acceleration = np.sqrt(mean_squared)

print("Mean squared acceleration:", mean_squared)
print("RMS acceleration:", rms_acceleration, "m/s²")
