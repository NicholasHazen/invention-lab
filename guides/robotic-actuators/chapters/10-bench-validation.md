# Turn a promising layout into measured evidence

The first useful actuator test may involve no motor at all. If an unpowered output shaft binds once per revolution, a controller can hide the symptom by drawing more current. If a printed mount slowly bends under a steady load, a successful one-second move tells you little about its ability to hold position. A test sequence should reveal those mechanisms separately before combining them.

You need the sizing sheet, the feedback sketch from [the previous chapter](#chapter-09), a securely mounted mechanism, and an independent way to observe position or deflection. A ruler or dial indicator can start the process if its uncertainty suits the question. A force gauge and temperature instruments become useful later. By the end, you will have a bounded test plan and a record that distinguishes measured behavior, instrument limits, and untested assumptions.

No physical actuator was printed, powered, or load-qualified for this chapter. The downloadable calculation and analysis programs were executed; the physical procedures below are a plan to apply to your selected parts. The earlier pivot remains an unpowered, separate project.

## Write the stopping conditions first

Download the [bench record](worksheets/bench-record.csv). Before a run, identify the model revision, material, print orientation, fasteners, fixture, instrument uncertainty, and planned load. Record limits for travel, force, current, temperature, and deflection that come from the actual components and your experiment. An empty limit is an unresolved prerequisite, not an invitation to discover the breaking point.

For an early printed mechanism, the question is usually whether it moves repeatably within a small intended working range. It is not its ultimate strength. Stop at cracking, whitening, loose hardware, increasing drag, unexpected motion, or an unexplained change in the load-deflection slope. Support any attached mass so a failed part cannot drop it onto a hand or pull the fixture from the bench. Keep the motor disabled while rearranging the fixture or instruments.

## First establish an unpowered baseline

Clamp the base using a fixture that does not distort bearing seats. Support the arm against gravity and remove stored spring or tendon energy using the assembly's intended release procedure. With electrical power disconnected and the manufacturer's discharge wait completed, inspect shaft retention, belt alignment, fastener access, wiring clearance, and the complete swept volume.

Move the mechanism slowly by hand only where the transmission is intended to be backdriven. Do not force a screw or high-reduction gearbox that resists backdriving; decouple and check its moving elements separately according to its assembly instructions. For the belt joint, check the output supports before connecting the belt. Then add the belt and compare drag. A new periodic tight spot points toward alignment, pulley eccentricity, or belt tension rather than software.

Record where resistance changes. Bearing seats that look concentric in CAD can shift when a printed housing is tightened. If loosening a mounting fastener changes drag, inspect alignment and clamping distortion before reducing its final torque. The resolution is a corrected assembly or fit, not leaving a structural fastener casually loose.

## Separate lost motion from elasticity

Mount a pointer or indicator at a known radius and immobilize the input through a suitable fixture, with the drive unpowered. Apply small, bounded tangential forces in each direction; select the force range only after the fixture and parts have been reviewed. Read displacement from the same reference every time. The fixture's compliance is part of the measurement unless you independently characterize it.

Two things can happen on reversal. Clearance can be taken up before a load-bearing surface engages, creating lost motion. Once engaged, the assembly can deflect elastically. A single positive-to-negative displacement measurement includes both. To distinguish them, record several force levels on each seated branch and fit the approximately linear portions. Do not keep increasing force merely to obtain a straighter graph.

![Synthetic positive and negative load branches. Their slopes measure compliance and their extrapolated zero-force intercepts estimate a lost-motion gap.](assets/sizing-compliance.svg)

The following numbers are **invented teaching data**, not a print test. At a 100 mm radius, positive forces of 0.10 and 0.20 N produce deflections of +0.60 and +1.00 mm. Negative forces produce −0.60 and −1.00 mm. Each branch has slope 4 mm/N. Extrapolating the positive branch to zero force gives +0.20 mm; the negative branch gives −0.20 mm. Their separation is 0.40 mm.

For small angles, angle ≈ tip deflection/radius. The apparent lost motion is therefore 0.40/100 = 0.004 rad = **0.229183°**. Rotational stiffness is torque/angle. Using the slope rather than the total displacement gives r²/(displacement-per-force) = 0.100²/0.004 = **2.5 N·m/rad**. Friction, fixture movement, and material hysteresis can also separate the branches, so label the result “apparent lost motion” until those effects are investigated.

Download [bench_analysis.py](examples/bench_analysis.py), [its tests](examples/test_bench_analysis.py), and [synthetic-compliance.csv](worksheets/synthetic-compliance.csv). With the program and CSV in your working folder:

```sh
python3 bench_analysis.py synthetic-compliance.csv --arm-mm 100
python3 -m unittest -v test_bench_analysis
```

The executed run returned 0.400000000 mm branch separation, 0.229183118° apparent lost motion, and 2.500000000 N·m/rad stiffness on both branches. Five behavioral tests passed. They check that a pure spring has no gap, a sensor zero offset does not create one, radius conversion works, and invalid data is rejected. Two points per branch make a line but cannot demonstrate linearity; use repeated measurements and more force levels for an actual experiment.

Predict the result if both slopes stay the same but both intercepts become zero. Stiffness stays at 2.5 N·m/rad and the estimated gap vanishes. That is why a flexible mechanism can have little backlash, while a stiff mechanism can still have a loose coupling.

## Look for slow changes while power is still absent

Apply a previously reviewed, supported static load and record immediate deflection, then deflection at fixed times such as 10, 30, and 60 seconds. Unload and record recovery at the same intervals. These times are observation points, not a validated endurance protocol. If the load creeps toward the stopping limit, remove it using the support arrangement and investigate the geometry or material.

Printed parts may exhibit time-dependent deflection, and clamps can settle or slip. Compare witness marks and unloaded residual position to separate those possibilities. Repeat only after identifying any unexpected change. Record ambient temperature and the print's orientation; a result from one orientation, wall structure, or material cannot silently qualify another.

## Gate the first electrical experiment on actual datasheets

Before enabling a drive, identify the exact motor, controller, encoder, supply, and firmware. Record permissible supply voltage, current conventions and limits, thermal limits, expected calibration motion, and the handling of returned energy. Use a compatible low-voltage, current-limited bench arrangement with the manufacturer's required protection. A lower voltage is not automatically supported by every drive, and a supply current limit does not replace a winding-current limit.

Begin with the motor secured and mechanically unloaded where the manufacturer's calibration procedure requires it. Remove loose shaft hardware and contain the potential motion. Calibration can itself energize and rotate a motor: ODrive's [motor calibration documentation](https://docs.odriverobotics.com/v/latest/articles/motor-parameters.html) describes separate resistance, inductance, and lock-in behavior. Use the actual product's procedure and selected limits; do not copy the illustrative currents from this guide into a drive.

With motor torque disabled, verify sensor readings while turning only components intended to move manually. Confirm positive direction, units, reference position, and signal continuity before closing a position loop. Then follow the drive's documented commissioning sequence at the lowest useful, approved motion and current limits. Incorrect direction feedback can turn a small requested move into increasing error, so keep the first motion unloaded, bounded, and physically contained.

Couple the mechanism only after that baseline is understood. Start without the study payload, with gravity support and a restricted travel window. Stop between changes; increase one variable at a time. The next step is justified by recorded behavior inside limits, not simply by the absence of smoke or a fault message.

## Measure motion and heat against the same timeline

Log requested and independently measured position, direction of approach, speed, motor current with its convention, DC bus voltage/current, and temperatures at identified locations. Synchronize readings well enough for the question. A slow dashboard cannot reveal a brief current spike or bus transient; use suitable recorded telemetry or instruments before concluding those events are absent.

For a position exercise, command the same unloaded target repeatedly from one side, then the other, within the approved travel window. Suppose five **illustrative** readings at a 45° target are 44.8, 44.9, 44.8, 44.9, and 44.8°. Their mean is **44.84°**, bias **−0.16°**, and range **0.10°**. Good repeatability has not eliminated the systematic error. An instrument that only resolves 0.1° cannot justify quoting a few thousandths of a degree as demonstrated accuracy.

Only after successful low-energy motion should you introduce incrementally reviewed load and repetition. Track winding-sensor, driver, and adjacent plastic temperatures where available; housing surface temperature is not winding temperature. Stop below the selected limits and account for sensor uncertainty and thermal lag. Driver thermal protection may reduce torque or disable it; [ODrive's thermal regulation documentation](https://docs.odriverobotics.com/v/latest/manual/hardware-config.html#temperature-regulation) illustrates why a hot mechanism can lose holding capability rather than merely become warm.

## Finish by proving how the run ends

First perform a commanded stop into a mechanically supported rest position. Verify zero motion, disable torque through the documented interface, and observe that the support carries the load. Disconnect power only through the intended supply procedure, wait the specified discharge time, and verify the state before touching wiring. Do not unplug phase or sensor connectors while energized.

A later loss-of-command test should use a documented watchdog/test mechanism, with the load caught and travel contained. Record whether it stops, coasts, or disables. A controlled-stop success does not prove safe behavior under total power loss; validate that separate case only with an arrangement that remains physically safe without active torque. Do not deliberately short wiring, jam the mechanism, or overheat a component to test protection.

Your next revision should answer the clearest remaining question. If elastic slope dominates error, change the load path or stiffness and repeat the same unpowered measurement. If the branches separate, inspect clearances and attachments. If motion tracks until current saturates, revisit sizing. The useful outcome is a comparison that tells you which design decision changed the behavior, with the rest of the experiment held steady.
