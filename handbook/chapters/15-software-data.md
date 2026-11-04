# 15. Software and data: make the measurement explain itself

A sensor logger can produce thousands of numbers without producing one trustworthy measurement. Suppose a distance trace jumps from 20 to 40. Did the part move 20 millimetres, did the sensor restart, or did the program read a voltage as a distance? Software becomes an engineering tool when the recorded evidence lets another person distinguish those explanations.

This chapter takes the bench sensor from the electronics chapters and gives its data a reproducible path from raw counts to reported distance. You will read a small Python program, verify its calibration, reject malformed observations, and preserve a change in version control. You need arithmetic, a text editor, a terminal, and Python 3. No sensor or purchased software is required. If programming is entirely new, allow time to work through variables, loops, and functions in [CS50's free Python course](https://cs50.harvard.edu/python/) alongside this chapter; completing the lab is a starting point rather than a substitute for that practice.

## A program is a sequence of changes to state

An instruction runs with some current state: values in memory, an open file, a clock reading, perhaps a motor command. It reads some of that state and changes some of it. A variable is a name you use to refer to a value. An expression calculates a value; an assignment associates it with a name. In `distance_mm = (raw_count - 100) * 0.05`, the right side is evaluated before `distance_mm` refers to the result.

A conditional selects a path. A loop repeats a path for several observations. A function groups a transformation with a named interface. Our `calibrate_mm(raw)` function accepts one count and returns one distance; it does not open files, update a graph, or command a mechanism. That narrow responsibility makes it possible to test the arithmetic without a connected sensor.

Keep a distinction between a value and its representation. The text `"500"` read from a CSV file is a sequence of characters. Converting it with `int()` produces the integer 500. The text `"five hundred"` cannot be converted this way. That failure is an exception: the normal computation stops and control passes to an appropriate handler. Catch expected failures at the boundary where outside data enters; do not silence every exception, because an unrelated programming error would then masquerade as a missing measurement. The [Python tutorial](https://docs.python.org/3/tutorial/) provides the language reference path once these ideas are familiar.

State also explains a common debugging surprise. If two names refer to the same mutable list, changing the list through either name changes the one object. Saving an earlier result requires an intentional copy or a new immutable value. Start with simple numbers and short records so that you can trace every change on paper before introducing shared, long-lived objects.

## Python on the laptop, C near the pins

Python is convenient for parsing files, drawing conclusions, and experimenting. A typical desktop program runs under an operating system, which allocates memory and schedules it alongside other applications. A requested pause of 10 milliseconds does not promise that the next instruction will run exactly 10 milliseconds later. This matters when a control loop depends on precise timing.

Microcontroller firmware often uses C or C++. The compiled program operates close to registers, buffers, timers, and fixed memory limits. A GPIO peripheral can change a pin because software writes a particular hardware register; a hardware timer can keep time while other instructions execute. This does not automatically make every firmware loop punctual. Blocking serial output, long interrupt handlers, and unbounded work can still delay it.

The numerical rules deserve attention when translating an algorithm. In Python, `3 / 2` produces 1.5, while `3 // 2` produces 1. For positive integer operands in C, `3 / 2` produces the integer 1. Declaring a fractional result later cannot restore a fraction already discarded. Fixed-width integer types also have limited ranges. An eight-bit unsigned count can represent 0 through 255; it cannot hold the number of samples in a long experiment. Signed overflow in C is not a reliable wraparound mechanism.

Choose data types and units together. Use a clearly named elapsed-time value and understand how its clock behaves at rollover. Use a wide enough accumulator when summing samples. Keep raw integer counts until conversion, then use a suitable floating-point representation for engineering values. You do not need to master two languages at once: establish a tested transformation on the laptop, then examine the target language's representation and timing before moving it into firmware.

## Work one calibration all the way through

Imagine a deliberately simple linear displacement sensor. A reference at 0 mm produces 100 counts; a reference at 40 mm produces 900 counts. The change is 800 counts over 40 mm, so the scale is:

`scale = (40 − 0) mm / (900 − 100) counts = 0.05 mm/count`

The zero offset is not zero counts. Subtract it before applying the scale:

`distance_mm = (raw_count − 100) × 0.05`

At 500 counts, the result is `(500 − 100) × 0.05 = 20 mm`. At 300 counts, it is 10 mm. A program that instead multiplies the raw count by 0.05 reports 25 mm at the midpoint: a constant 5 mm offset across the range. That recognizable pattern helps identify a missing zero correction.

Two points determine a straight line; they do not demonstrate that the physical sensor is linear. Check additional positions, approaching them from both directions. A repeatable curved error suggests the line is an inadequate model. A difference between forward and reverse travel suggests hysteresis, backlash, or mounting movement. Random scatter needs a repeatability estimate. Store the raw values so that you can apply a better calibration later without pretending to have repeated the physical experiment.

Our synthetic converter accepts the nominal 10-bit range, 0–1023. Counts outside the calibrated interval 100–900 are mathematically extrapolated. That is a separate issue from being outside the converter's possible range. A real instrument should flag extrapolation according to its intended use; silently clipping every reported distance to 0–40 mm would hide evidence of a fault or an out-of-range part.

## Run the logger without building hardware

Download [sensor_log.py](../examples/computing/sensor_log.py) and [sensor_fixture.csv](../examples/computing/sensor_fixture.csv) into the same folder. Install Python 3 if it is not already available, open a terminal in that folder, and check `python3 --version`. On a system that exposes Python as `python`, use that command consistently. The example uses the standard library and requires no package installation.

Open the CSV in a text editor. Its header declares `time_s,raw_count,status`. Before running anything, calculate the distance for each valid row and mark suspicious records. Then run:

```sh
python3 sensor_log.py
python3 sensor_log.py --output clean.csv
```

The first command reports four accepted and four rejected records. Accepted distances are 0, 10, 20, and 40 mm at 0.00, 0.10, 0.20, and 0.50 seconds. The rejected records contain a repeated timestamp, an impossible count of 2048, a timeout status, and `nan` as time. The second command additionally writes a clean CSV; it leaves the original fixture intact.

Notice the gap between 0.20 and 0.50 seconds. Removing bad records does not make the sensor run at a constant sampling interval. A later velocity calculation must use the actual elapsed time: `(40 − 20) / (0.50 − 0.20) = 66.7 mm/s`. Assuming the usual 0.10-second interval would report 200 mm/s. A tidy table can still contain an important discontinuity.

The validator only advances its last accepted timestamp after accepting a record. This is a stated policy: a record rejected for an impossible count cannot advance the clock even if it carries a far-future timestamp. A plausible count with an incorrect future time would still need an additional clock-plausibility check. An alternative system might preserve all records with quality flags rather than remove them. Choose according to the question you need the record to answer, and keep the raw input in either case.

Change one fixture field at a time. Replace the repeated timestamp with 0.25 and predict the accepted count. Change a raw value to a word and observe a conversion error. Restore the fixture afterward. These are controlled fault injections, not random edits: each one tests a different boundary.

## Debug by narrowing the explanation

When a program fails, start with the smallest input that reproduces the failure. Write the expected result beside the actual one. Then locate the first stage where they differ: text input, numeric conversion, calibration, ordering, or output formatting. A temporary print or breakpoint is useful when it answers a question about that stage. Printing everything indefinitely makes the evidence harder to read.

Keep a run record with the software revision, calibration identifier, units, sensor identity, start time, and any known change in setup. For elapsed intervals use a monotonic clock; for matching an experiment to a notebook use a wall-clock timestamp with its time zone. A computer's civil time can be adjusted. A sequence number helps distinguish a lost record from a legitimate period of slow sampling.

Tests turn discovered mistakes into repeatable checks. Download the [complete computing examples](../examples/computing/README.md), keeping all Python files together, and run:

```sh
python3 -m unittest -v test_labs.py
```

The logger tests check the two calibration references, their midpoint, and rejection of impossible or repeated measurements. The suite also exercises the later chapters' labs. These tests have been executed for the published examples. They establish software behavior for their specified inputs; they do not calibrate a physical sensor or certify its wiring.

An especially useful new test comes from a failure you did not anticipate. If a unit change caused a thousand-fold position error, capture that conversion explicitly. Avoid writing a test that merely repeats the same formula with different variable names: a mistaken formula can then agree with itself. Independently known reference positions make stronger checks.

## Preserve decisions with small commits

Version control records deliberate snapshots of source files. In a new practice folder, initialize a Git repository, add the logger and fixture, and commit the working baseline. Change the calibration in one place, inspect the difference, run the relevant tests, then commit with a sentence explaining why the references changed. [Pro Git](https://git-scm.com/book/en/v2) teaches this local workflow before introducing remote collaboration.

A commit is most useful when it represents one understandable change. Keep credentials and large generated logs out of the repository. Record how to reproduce a result and archive important raw measurements separately with stable names. Git can preserve a binary CAD file, but a text diff cannot explain its geometric changes; save revision notes and a representative export or image alongside meaningful model revisions.

Do this first in a disposable practice repository, where restoring a file cannot discard unique work. A hosted repository adds collaboration and an off-machine copy. It does not replace a considered backup policy for experiments, CAD history, and files that were never committed.

## Check your reasoning, then extend the instrument

**Predict:** A stationary reference always reads 5 mm high after conversion. What should you inspect first? **Answer:** The zero offset and calibration references. Constant bias is different from random noise; averaging more samples will preserve the bias.

**Predict:** Why is `nan` not an acceptable timestamp even though it can be parsed as a floating-point value? **Answer:** It is not a finite measurement of time and ordinary ordering comparisons cannot establish the intended increasing sequence. Parsing establishes representation, not validity.

**Predict:** A program passes its tests but reports the wrong unit on a new sensor. What failed? **Answer:** The tested assumptions no longer match the input contract. Add a unit or sensor-type identifier at the boundary, then test the conversion against an independent reference.

For an independent project, make the logger report distance, elapsed time, and a quality flag without deleting rejected rows. Give each input record a stable sequence number. Write a short specification for duplicate times, missing values, and extrapolation, then implement it. Your completion evidence is a fixture containing each case, expected results calculated by hand, and tests that fail when you deliberately remove one validation rule.

For more practice, [Automate the Boring Stuff with Python](https://automatetheboringstuff.com/) offers approachable file-processing projects; [MIT's Missing Semester](https://missing.csail.mit.edu/) develops the command-line, debugging, and version-control habits around the language. Choose the next exercise that removes friction from an actual bench task: organizing measurements is an excellent reason to learn software.
