"""Validate a synthetic ADC log and convert counts to millimetres; no packages needed."""
import argparse
import csv
import math
from pathlib import Path


def calibrate_mm(raw):
    if not 0 <= raw <= 1023:
        raise ValueError("raw count outside 0..1023")
    # Illustrative calibration references: 100 counts at 0 mm; 900 counts at 40 mm.
    return (raw - 100) * 40.0 / (900 - 100)


def clean_rows(rows):
    accepted, rejected = [], []
    last_time = -math.inf
    for line, row in enumerate(rows, start=2):
        try:
            timestamp = float(row["time_s"])
            raw = int(row["raw_count"])
            if not math.isfinite(timestamp) or timestamp < 0:
                raise ValueError("time must be finite and nonnegative")
            if timestamp <= last_time:
                raise ValueError("time must increase")
            if row["status"] != "ok":
                raise ValueError("sensor status is not ok")
            distance = calibrate_mm(raw)
        except (ValueError, KeyError, TypeError) as error:
            rejected.append((line, str(error)))
            continue
        accepted.append({"time_s": timestamp, "raw_count": raw,
                         "distance_mm": distance})
        last_time = timestamp
    return accepted, rejected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", type=Path,
                        default=Path(__file__).with_name("sensor_fixture.csv"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    with args.input.open(newline="") as stream:
        rows, rejected = clean_rows(csv.DictReader(stream))
    print(f"accepted={len(rows)} rejected={len(rejected)}")
    for row in rows:
        print(f"t={row['time_s']:.2f} s distance={row['distance_mm']:.2f} mm")
    for line, reason in rejected:
        print(f"rejected line {line}: {reason}")
    if args.output:
        with args.output.open("w", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=["time_s", "raw_count", "distance_mm"])
            writer.writeheader()
            writer.writerows(rows)


if __name__ == "__main__":
    main()
