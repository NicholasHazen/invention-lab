"""Ideal DC divider calculations. Run with Python 3; no packages required."""

SUPPLY_V = 3.0
R1_OHM = 10_000.0
R2_OHM = 10_000.0
LOAD_OHM = 10_000.0


def divider(supply_v, r1_ohm, r2_ohm, load_ohm=None):
    if r1_ohm <= 0 or r2_ohm <= 0:
        raise ValueError("Resistances must be positive")
    if load_ohm is not None and load_ohm <= 0:
        raise ValueError("Load resistance must be positive")
    lower = r2_ohm if load_ohm is None else 1 / (1 / r2_ohm + 1 / load_ohm)
    source_a = supply_v / (r1_ohm + lower)
    mid_v = source_a * lower
    r2_a = mid_v / r2_ohm
    load_a = 0.0 if load_ohm is None else mid_v / load_ohm
    return mid_v, source_a, r2_a, load_a


def main():
    from math import isclose

    # Independent benchmark cases; these remain valid while editing the lab values.
    assert isclose(divider(3, 10_000, 10_000)[0], 1.5)
    assert isclose(divider(3, 10_000, 10_000, 10_000)[0], 1.0)
    print("Ideal divider model (not hardware measurements)")
    for label, load in (("Unloaded", None), ("Loaded", LOAD_OHM)):
        mid, source, lower, load_a = divider(SUPPLY_V, R1_OHM, R2_OHM, load)
        assert isclose(source, lower + load_a, rel_tol=1e-12, abs_tol=1e-12)
        source_w = SUPPLY_V * source
        dissipated_w = source**2 * R1_OHM + lower**2 * R2_OHM
        if load is not None:
            dissipated_w += load_a**2 * load
        assert isclose(source_w, dissipated_w, rel_tol=1e-12, abs_tol=1e-12)
        print(f"{label}: MID={mid:.3f} V; source={source * 1e6:.1f} uA; "
              f"R2={lower * 1e6:.1f} uA; load={load_a * 1e6:.1f} uA")
        print(f"  source power={source_w * 1e3:.3f} mW; "
              f"R1 power={source**2 * R1_OHM * 1e3:.3f} mW")
    print("Checks passed: voltage benchmarks, node currents, power balance.")


if __name__ == "__main__":
    main()
