# Actuator calculation labs

These original programs use Python's standard library. They do not access a motor, serial port, network, or hardware driver. Python 3.10+ is sufficient; the reference run used Python 3.11.5.

From this `examples` folder:

```sh
python3 actuator_sizing.py --rotor-inertia 0.00001 --csv cycle.csv
python3 bench_analysis.py ../worksheets/synthetic-compliance.csv --arm-mm 100
python3 -m unittest -v
```

If downloading files individually, keep each test beside its matching program. Put `synthetic-compliance.csv` in the same folder and replace the second command's path with `synthetic-compliance.csv`.

`actuator_sizing.py` separates a forward-efficiency positive torque envelope from an ideal reversible-transmission cycle. The required rotor inertia is an explicit input in kg·m². `0.00001` is a hypothetical teaching value, not a selected motor. The CSV records midpoint samples with their duration so the RMS calculation is reproducible. A complete cycle raises, holds at the upper angle, lowers, and holds horizontal. The moving-friction allowance has a sign; holds get no friction credit. The model omits pulley inertia, motor friction, losses in the cycle, stiction, thermal response, and controller dynamics.

`bench_analysis.py` fits the positive and negative force branches of a force/deflection CSV. It expects a known tangential force radius, small angular deflections, and approximately linear seated branches. It cannot verify those conditions, subtract fixture compliance, distinguish all friction/hysteresis sources, or establish a safe load. The included CSV is synthetic teaching data.

The 19 tests check conservation of energy, trajectory scaling, reduction/inertia relationships, screw/tendon work balance, required inputs, sign conventions, branch fitting, and invalid data. Their success validates those mathematical behaviors, not a physical assembly.

`render_sizing_diagrams.py` regenerates the three original SVG teaching figures in `../assets`. It also uses only the standard library; run it from the unzipped guide with the folder structure preserved.
