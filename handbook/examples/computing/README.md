# Computing labs

These programs are small, deterministic teaching experiments. They use Python's standard library, open no network connections, and drive no physical hardware. They do not establish that a physical sensor, controller, or robot is validated.

Download these files into one folder:

- [sensor_log.py](sensor_log.py) and its [sensor_fixture.csv](sensor_fixture.csv)
- [control_lab.py](control_lab.py)
- [robot_arm.py](robot_arm.py)
- [vision_baseline.py](vision_baseline.py)
- [message_lab.py](message_lab.py)
- [test_labs.py](test_labs.py)

Use Python 3.10 or newer. Check `python3 --version`, open a terminal in the downloaded folder, then run:

```sh
python3 sensor_log.py
python3 control_lab.py
python3 robot_arm.py
python3 vision_baseline.py
python3 message_lab.py
python3 -m unittest -v test_labs.py
```

On Windows, a Python installation may expose `py` instead of `python3`; use the available Python 3 command consistently. No `pip install` step is required.

The logger reports four accepted and four rejected records. The controller reports P output 0.400 and PI output 0.600 for a target of 0.600; its windup comparison reports outputs 1.000 and 0.292 at 12 seconds. The arm endpoint is (155.885, 10.000) mm. The vision experiment reports TP=3, FP=2, TN=2, FN=1. The message receiver rejects duplicate, old, and expired commands and ends off. The test suite contains nine tests and should report `OK`.

Optional outputs, written in the current folder:

```sh
python3 sensor_log.py --output clean.csv
python3 control_lab.py --csv control-results.csv
python3 vision_baseline.py --images vision-images
```

The CSV files can be opened in a spreadsheet. The vision images are deliberately tiny plain-text PGM files: inspect their pixel values in a text editor if your image viewer does not support PGM. The source fixture is synthetic. Change copies of the examples, record each prediction, then compare the observed output.

Tests cover independent calibration references, invalid observations, control equilibrium and saturation, kinematic checks and reach limits, held-out confusion counts, and message replay/timeout behavior. They check specified software behavior, not general physical safety or production accuracy.
