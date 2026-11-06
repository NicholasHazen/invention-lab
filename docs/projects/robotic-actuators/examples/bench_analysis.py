#!/usr/bin/env python3
"""Fit two quasi-static load branches; never controls hardware.

Input CSV: force_N,tip_deflection_mm. Force and displacement signs must share
one convention. The signed force is tangent to a known arm radius. Branches
must be selected from a seated, linear region; this program cannot verify that.
"""
import argparse
import csv
import math
from statistics import mean


def line_fit(points):
    if len(points) < 2:
        raise ValueError('each branch needs at least two points')
    if any(not math.isfinite(v) for p in points for v in p):
        raise ValueError('all samples must be finite')
    xbar, ybar = mean(p[0] for p in points), mean(p[1] for p in points)
    denominator = sum((x-xbar)**2 for x, _ in points)
    if denominator == 0:
        raise ValueError('each branch needs different forces')
    slope = sum((x-xbar)*(y-ybar) for x, y in points)/denominator
    if slope <= 0:
        raise ValueError('nonpositive compliance: inspect signs or branch selection')
    return slope, ybar-slope*xbar


def analyze(points, arm_mm=100.0):
    if not math.isfinite(arm_mm) or arm_mm <= 0:
        raise ValueError('arm_mm must be finite and positive')
    if any(not math.isfinite(v) for p in points for v in p):
        raise ValueError('all samples must be finite')
    positive = [(f, d) for f, d in points if f > 0]
    negative = [(f, d) for f, d in points if f < 0]
    sp, bp = line_fit(positive)
    sn, bn = line_fit(negative)
    width_mm = abs(bp-bn)
    r = arm_mm/1000
    return dict(positive_compliance_mm_N=sp, negative_compliance_mm_N=sn,
                positive_intercept_mm=bp, negative_intercept_mm=bn,
                branch_gap_mm=width_mm,
                apparent_lost_motion_deg=math.degrees(width_mm/arm_mm),
                positive_stiffness_Nm_rad=r*r/(sp/1000),
                negative_stiffness_Nm_rad=r*r/(sn/1000))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('csv_path')
    parser.add_argument('--arm-mm', type=float, default=100)
    args = parser.parse_args()
    try:
        with open(args.csv_path, newline='') as f:
            rows = list(csv.DictReader(f))
        result = analyze([(float(r['force_N']), float(r['tip_deflection_mm'])) for r in rows], args.arm_mm)
    except (ValueError, KeyError, OSError) as exc:
        parser.error(str(exc))
    print('INPUT DATA ONLY: fit does not establish load rating or isolate every source of hysteresis.')
    for k, v in result.items():
        print(f'{k}: {v:.9f}')


if __name__ == '__main__':
    main()
