"""Deterministic first-order plant simulation. This does not drive hardware."""
import argparse
import csv


def simulate(kp=2.0, ki=0.0, dt=0.02, duration=20.0, antiwindup=True,
             reference=None, disturbance=0.0):
    if dt <= 0 or duration <= 0:
        raise ValueError("dt and duration must be positive")
    reference = reference or (lambda t: 0.6)
    y, integral = 0.0, 0.0
    samples = []
    for step in range(round(duration / dt)):
        time_s = step * dt
        target = reference(time_s)
        error = target - y
        proposed = integral + ki * error * dt
        proposed_command = kp * error + proposed
        # Freeze only integration that would push further into saturation.
        pushes_high = proposed_command > 1.0 and error > 0
        pushes_low = proposed_command < 0.0 and error < 0
        if not antiwindup or not (pushes_high or pushes_low):
            integral = proposed
        requested = kp * error + integral
        applied = max(0.0, min(1.0, requested))
        # Euler model: tau=1 s; normalized output and command.
        y += dt * (applied + disturbance - y)
        samples.append({"time_s": time_s + dt, "target": target, "output": y,
                        "requested": requested, "applied": applied, "integral": integral})
    return samples


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", help="Optional output path for all four runs")
    args = parser.parse_args()
    step_target = lambda t: 2.0 if t < 10.0 else 0.4
    runs = {"P": simulate(), "PI": simulate(ki=1.0),
            "PI windup": simulate(ki=1.0, duration=30, reference=step_target, antiwindup=False),
            "PI protected": simulate(ki=1.0, duration=30, reference=step_target)}
    for name in ["P", "PI"]:
        print(f"{name}: final output={runs[name][-1]['output']:.3f}, target=0.600")
    for name in ["PI windup", "PI protected"]:
        sample = runs[name][int(12 / 0.02) - 1]
        print(f"{name}: at 12 s output={sample['output']:.3f}, integral={sample['integral']:.3f}")
    if args.csv:
        with open(args.csv, "w", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=["run"] + list(runs["P"][0]))
            writer.writeheader()
            for name, samples in runs.items():
                writer.writerows({"run": name, **sample} for sample in samples)


if __name__ == "__main__":
    main()
