import numpy as np
import matplotlib.pyplot as plt


sampling_frequency = 1000
duration = 1
frequency = 10
amplitude = 4

time = np.arange(0, duration, 1 / sampling_frequency)

acceleration = amplitude * np.sin(2 * np.pi * frequency * time)

print("Number of samples:", len(time))
print("First 5 time values:", time[:5])
print("First 5 acceleration values:", acceleration[:5])

rms_acceleration = np.sqrt(np.mean(acceleration ** 2))

print("Calculated RMS:", rms_acceleration, "m/s²")

plt.plot(time, acceleration)
plt.xlabel("Time (s)")
plt.ylabel("Acceleration (m/s²)")
plt.title("Simulated Vibration Signal — 10 Hz")
plt.grid(True)
plt.show()