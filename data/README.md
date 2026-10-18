# BearingIQ — Dataset Information

This project uses vibration measurements from the Paderborn University Bearing Data Center.

The original MATLAB measurement files are not included in this repository. They must be downloaded separately from the dataset provider.

## Bearings Used

| Bearing ID | Condition |
|---|---|
| K001 | Healthy reference |
| K002 | Healthy reference |
| KA04 | Real outer-ring fatigue damage |

## Operating Conditions

- Shaft speed: 900 rpm
- Load torque: 0.7 Nm
- Radial force: 1,000 N
- Nominal sampling frequency: 64 kHz
- Recording duration: approximately 4 seconds

## Local Data Folder Structure

Place the downloaded `.mat` files in the following folders:

```text
data/
├── README.md
└── raw/
    ├── K001/
    │   └── N09_M07_F10_K001_1.mat
    ├── K002/
    │   ├── N09_M07_F10_K002_1.mat
    │   └── ...
    └── KA04/
        ├── N09_M07_F10_KA04_1.mat
        └── ...
```

The main diagnostic analysis uses recordings 1, 3, 4, 5 and 6 from K002 and KA04. Recording 2 was excluded from the calibration and held-out evaluation pending further investigation of measurement consistency.

The Python scripts load the measurements from these local folders.

## Data Availability

**Source:** Paderborn University Bearing Data Center

**Dataset website:** https://mb.uni-paderborn.de/kat/forschung/datacenter/bearing-datacenter

The `data/raw/` directory is excluded from Git using `.gitignore`.

Only the analysis code, extracted diagnostic results and generated engineering figures are published in this repository.
