# ============================================================
# BearingIQ — Theoretical Outer-Ring Fault Frequency
# ============================================================
import numpy as np


def main():
    # 1. Bearing geometry for KA04
    rolling_elements = 8
    ball_diameter = 6.75       # mm
    pitch_diameter = 28.55     # mm
    contact_angle = 0          # degrees

    # 2. Operating condition: 900 rpm
    speed_rpm = 900
    shaft_frequency = speed_rpm / 60

    # 3. Calculate theoretical BPFO
    bpfo = (
        (rolling_elements / 2) * shaft_frequency
        * (1 - (ball_diameter / pitch_diameter)
           * np.cos(np.deg2rad(contact_angle)))
    )

    print(f"Shaft frequency: {shaft_frequency:.2f} Hz")
    print(f"Outer-ring BPFO: {bpfo:.2f} Hz")
    for harmonic in range(1, 7):
        print(f"{harmonic} × BPFO: {harmonic * bpfo:.2f} Hz")


if __name__ == "__main__":
    main()
