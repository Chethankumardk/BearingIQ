import numpy as np

# KA04 bearing geometry
rolling_elements = 8
ball_diameter = 6.75       # mm
pitch_diameter = 28.55     # mm
contact_angle = 0          # degrees

# Operating condition N09 = 900 rpm
speed_rpm = 900

shaft_frequency = speed_rpm / 60

bpfo = (
    (rolling_elements / 2)
    * shaft_frequency
    * (
        1
        - (ball_diameter / pitch_diameter)
        * np.cos(np.deg2rad(contact_angle))
    )
)

print(f"Shaft frequency: {shaft_frequency:.2f} Hz")
print(f"Outer-ring BPFO: {bpfo:.2f} Hz")

for harmonic in [1, 2, 3]:
    print(f"{harmonic} × BPFO: {harmonic * bpfo:.2f} Hz")