# ============================================================
# BearingIQ — FFT Comparison: Healthy K002 vs Damaged KA04
# ============================================================
import numpy as np
import matplotlib.pyplot as plt
from src.bearing_utils import load_vibration, calculate_fft, FS, BPFO, PROJECT_ROOT


def main():
    # 1. Load real bearing measurements
    healthy, _ = load_vibration("K002", recording_number=1)
    damaged, _ = load_vibration("KA04", recording_number=1)

    # 2. Calculate Hann-windowed FFT spectra
    freq_healthy, amp_healthy = calculate_fft(healthy, FS)
    freq_damaged, amp_damaged = calculate_fft(damaged, FS)

    # 3. Compare spectra and theoretical BPFO harmonics
    plt.figure(figsize=(12, 6))
    plt.plot(freq_healthy, amp_healthy, label="K002 — Healthy", alpha=0.8)
    plt.plot(freq_damaged, amp_damaged, label="KA04 — Outer-ring damage", alpha=0.8)
    for harmonic in range(1, 7):
        plt.axvline(
            harmonic * BPFO, color="red", linestyle="--", linewidth=1,
            alpha=0.6, label="Theoretical BPFO harmonics" if harmonic == 1 else None
        )
    plt.xlim(0, 500)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("FFT amplitude (raw recorded units)")
    plt.title("BearingIQ — Raw Vibration FFT Comparison")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    output_dir = PROJECT_ROOT / "results" / "figures"
    output_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_dir / "fft_healthy_vs_damaged.png", dpi=300, bbox_inches="tight")
    print("FFT comparison figure saved successfully.")
    plt.show()

    # 4. Verify theoretical harmonics in the damaged recording
    search_width = 2.0
    print("\n========== BPFO HARMONIC VERIFICATION ==========")
    print(f"{'Harmonic':<12}{'Expected Hz':>14}{'Measured Hz':>14}{'Amplitude':>14}")
    for harmonic in range(1, 7):
        expected = harmonic * BPFO
        mask = np.abs(freq_damaged - expected) <= search_width
        if not np.any(mask):
            raise ValueError(f"No FFT bins around harmonic {harmonic}.")
        index = np.argmax(amp_damaged[mask])
        print(f"{harmonic:<12}{expected:>14.2f}"
              f"{freq_damaged[mask][index]:>14.2f}"
              f"{amp_damaged[mask][index]:>14.6f}")

    # 5. Compare healthy and damaged harmonic amplitudes
    print("\n========== HEALTHY VS DAMAGED BPFO ==========")
    print(f"{'Harmonic':<12}{'K002 amplitude':>18}{'KA04 amplitude':>18}{'Ratio':>12}")
    for harmonic in range(1, 7):
        expected = harmonic * BPFO
        healthy_mask = np.abs(freq_healthy - expected) <= search_width
        damaged_mask = np.abs(freq_damaged - expected) <= search_width
        healthy_amplitude = np.max(amp_healthy[healthy_mask])
        damaged_amplitude = np.max(amp_damaged[damaged_mask])
        ratio = damaged_amplitude / healthy_amplitude if healthy_amplitude > 0 else np.nan
        print(f"{harmonic:<12}{healthy_amplitude:>18.6f}"
              f"{damaged_amplitude:>18.6f}{ratio:>12.2f}")


if __name__ == "__main__":
    main()
