import numpy as np
import matplotlib.pyplot as plt

recordings = np.array([1, 3, 4, 5, 6])

healthy = np.array([
    0.001386, 0.001075, 0.001085,
    0.001364, 0.000921
])

damaged = np.array([
    0.039767, 0.039132, 0.038519,
    0.038597, 0.037792
])

threshold = 0.019952

plt.figure(figsize=(9, 5))

plt.plot(recordings, healthy, "o-", label="K002 — Healthy")
plt.plot(recordings, damaged, "s-", label="KA04 — Outer-ring damaged")

plt.axhline(
    threshold,
    color="red",
    linestyle="--",
    label="Exploratory threshold"
)

plt.axvline(
    5.5,
    color="gray",
    linestyle=":",
    label="Calibration / held-out boundary"
)

plt.xlabel("Recording number")
plt.ylabel("Fourth BPFO harmonic FFT amplitude (raw units)")
plt.title("BearingIQ — Physics-Informed Bearing Condition Monitoring")

plt.xticks(recordings)
plt.legend(loc="upper left")
plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig(
    "results/figures/bpfo_diagnostic_comparison.png",
    dpi=300
)

plt.show()