"""Synthetic RC and sampled-signal data. Python 3, standard library only."""

import csv
import math
from pathlib import Path

RESISTOR_OHM = 10_000.0
CAPACITOR_F = 1e-6
STEP_V = 3.3
SAMPLE_HZ = 20.0
SIGNAL_HZ = 18.0
COMPARISON_HZ = 2.0


def rc_voltage(time_s, resistor_ohm, capacitor_f, step_v):
    if resistor_ohm <= 0 or capacitor_f <= 0 or time_s < 0:
        raise ValueError("R and C must be positive; time must be non-negative")
    return step_v * (1 - math.exp(-time_s / (resistor_ohm * capacitor_f)))


def main():
    if SAMPLE_HZ <= 0:
        raise ValueError("Sample frequency must be positive")
    assert math.isclose(rc_voltage(0.01, 10_000, 1e-6, 3.3), 2.085997844, abs_tol=1e-9)
    assert rc_voltage(0, 10_000, 1e-6, 3.3) == 0
    tau = RESISTOR_OHM * CAPACITOR_F
    print("Synthetic model data (not sensor measurements)")
    print(f"Time constant: {tau * 1000:.3f} ms")
    for time_s in (0.01, 0.05):
        voltage = rc_voltage(time_s, RESISTOR_OHM, CAPACITOR_F, STEP_V)
        print(f"At {time_s * 1000:.0f} ms: {voltage:.3f} V")
    with open("rc_step.csv", "w", newline="", encoding="utf-8") as output:
        writer = csv.writer(output)
        writer.writerow(("time_ms", "voltage_v"))
        for millisecond in range(101):
            writer.writerow((millisecond, rc_voltage(millisecond / 1000,
                             RESISTOR_OHM, CAPACITOR_F, STEP_V)))
    errors = []
    with open("alias_samples.csv", "w", newline="", encoding="utf-8") as output:
        writer = csv.writer(output)
        writer.writerow(("time_s", "sampled_signal", "negative_comparison_sine"))
        for sample in range(int(SAMPLE_HZ) + 1):
            time_s = sample / SAMPLE_HZ
            signal = math.sin(2 * math.pi * SIGNAL_HZ * time_s)
            comparison = -math.sin(2 * math.pi * COMPARISON_HZ * time_s)
            errors.append(abs(signal - comparison))
            writer.writerow((time_s, signal, comparison))
    print(f"Largest difference between sampled curves: {max(errors):.3g}")
    print(f"Wrote rc_step.csv and alias_samples.csv in {Path.cwd()}")
    print("Checks passed: initial condition and one-time-constant benchmark.")


if __name__ == "__main__":
    main()
