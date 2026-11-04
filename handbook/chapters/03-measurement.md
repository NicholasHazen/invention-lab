# Measure, experiment and debug

Your printed shaft hole looks round and your caliper displays 8.12 mm. The shaft still will not enter. Which claim failed: the drawing, the manufacturing process, the measurement or the assumption that a single diameter describes the fit? You cannot answer by adding more decimal places. You need to define what you are measuring and how the assembly uses that feature.

In this chapter you will distinguish resolution, repeatability and bias; make a small experimental comparison; and record enough context for another person to interpret the result. Use [units and arithmetic from Chapter 2](../math-physics/). Bring a ruler or caliper if you have one, a rigid object with accessible faces and a notebook. A ruler-based placement experiment works without buying a precision instrument.

## Define the question before choosing the instrument

“Measure the hole” can mean diameter at its entrance, diameter farther down, roundness, taper or whether a particular shaft slides through. These are related but different questions. A chamfer can make the entrance larger than the cylindrical region that controls fit. Caliper jaws can contact two high points and miss a local restriction. A functional gauge or the intended mating part may answer the assembly question more directly, provided you do not force it into the part.

Write a measurement statement such as: “Measure the outside width between these two marked faces, at the centre of the part, after it has cooled to room conditions.” Name the instrument, reference surfaces, contact method and temperature when relevant. Photograph or sketch the location. This definition makes later comparisons meaningful.

Resolution is the smallest displayed or distinguishable increment. Accuracy concerns closeness to a reference value. Repeatability concerns agreement when the measurement is repeated under specified conditions. A display reading to 0.01 mm does not establish ±0.01 mm accuracy. A zero check is useful, but does not by itself calibrate the instrument over its whole range.

## Repetition exposes variation, not every error

Consider five invented readings of the same width, in millimetres:

| Reading | Width |
|---|---:|
| 1 | 20.04 |
| 2 | 20.02 |
| 3 | 20.03 |
| 4 | 20.05 |
| 5 | 20.01 |

Their mean is 20.03 mm. Their range is 0.04 mm. The sample standard deviation is approximately 0.0158 mm. The range is an easy description of the observed spread, but depends strongly on how many samples you took. Standard deviation summarizes deviations from the mean; it is not the largest possible error.

If these readings are independent observations under stable conditions, the estimated standard uncertainty of their mean from this repeatability contribution is `s/√n ≈ 0.0071 mm`. That reduction applies to the estimate of the mean. It does not say each individual part or future reading varies by only 0.0071 mm. It also says nothing about an instrument offset shared by all five readings.

Suppose a suitable reference check reveals a +0.08 mm offset under the relevant conditions. Subtracting the estimated offset changes the corrected mean to 19.95 mm. The correction itself has uncertainty. Taking fifty readings without checking the reference could produce a very consistent answer to the wrong value.

NIST distinguishes uncertainty evaluated through statistical analysis of observations, called Type A, from uncertainty evaluated using other information, called Type B. These are methods of evaluation, not alternative names for random and systematic error. Its [Technical Note 1297](https://www.nist.gov/pml/nist-technical-note-1297) is a useful deeper reference once you need a defensible uncertainty budget.

## A useful uncertainty budget starts with causes

For a fit experiment, list plausible influences before calculating a single combined number:

- Instrument resolution and its applicable specification or calibration information.
- Jaw placement, tilt and contact force, especially on a flexible printed wall.
- Surface texture, seam, burrs, taper and the location being measured.
- Temperature, moisture and time after manufacturing where they affect the material.
- Variation between repeated readings, between features and between separately manufactured parts.

Those last three variations are not interchangeable. Measuring one part ten times explores measurement repeatability. Measuring ten parts once explores a mixture of part variation and measurement variation. Neither design alone completely separates the two.

A formal combined standard uncertainty commonly uses a measurement model and combines contributions with appropriate sensitivities and correlations. A beginner can still make a disciplined decision without claiming a formal confidence interval. State the observed range, the instrument limitations and the unmeasured influences. If a decision depends on a 0.02 mm difference and your method cannot reliably distinguish it, improve the method or redesign the interface to be less sensitive.

Avoid reporting `±` without saying what it means. “Mean 20.03 mm; five readings ranged from 20.01 to 20.05 mm” is clearer than “20.03 ±0.02 mm” with no definition. For a critical acceptance decision, uncertainty and the acceptance rule need explicit treatment; a displayed number barely inside a limit is weak evidence.

## Design a comparison that can answer its question

Imagine testing whether a cardboard stop improves the repeatability of placing a sensor mockup. The response is the measured position of the sensor's reference edge. The deliberate change is presence or absence of the stop. Keep the object, surface, reference line, measurement method and operator procedure constant enough to interpret the comparison.

Write predictions before taking data: “The stop will reduce the spread of placement positions” is different from “The stop will move the average position toward 40 mm.” A device can become more repeatable while becoming consistently wrong. Measure both centre and spread.

These invented results illustrate the distinction:

| Condition | Five placement positions, mm | Mean, mm | Range, mm |
|---|---|---:|---:|
| Free placement | 38, 42, 40, 41, 39 | 40.0 | 4.0 |
| Against stop | 40.5, 40.7, 40.6, 40.5, 40.7 | 40.6 | 0.2 |

The stop reduces the observed range from 4.0 to 0.2 mm but shifts the mean 0.6 mm above the target. Adjusting the stop's location may correct the centre. More trials are needed to characterize reliability across days, users and wear. These five values demonstrate arithmetic, not a measured result from an actual fixture.

If all free trials occur first, practice or fatigue may confound the comparison. Alternate or randomize the order where practical, and record it. Randomization does not remove every influence; it reduces the chance that a time-related influence always coincides with one condition. Repeating a whole experiment on another day tests something different from repeatedly reading the same placement.

## One variable at a time has limits

Changing one factor while keeping others fixed is a good first diagnostic. It lets you connect a changed response to a deliberate intervention more easily. But factors can interact. A print temperature that improves bonding in one orientation may not provide the same practical benefit in another geometry. A flexible sensor mount may behave differently only when a cable is attached.

A small two-factor comparison can reveal that interaction. Test both configurations with and without the cable, using the same loading and measurement procedure. Compare the cable's effect within each configuration. If the effect changes substantially, the factors interact over the tested conditions. Do not average away the difference and declare one setting universally best.

More advanced design of experiments formalizes factor selection, replication, randomization and response models. The [NIST/SEMATECH handbook's experimental-design section](https://www.itl.nist.gov/div898/handbook/pri/section3/pri3.htm) is a deeper route. At the bench, your first responsibility is simpler: preserve what changed, what stayed fixed and what was actually observed.

## Debug by separating possible causes

A failure such as “the sensor reading jumps” is a symptom, not a diagnosis. Draw the path: physical stimulus → sensor → wiring → conversion → software → display. Then find a measurement that separates explanations.

If a known constant input produces stable raw readings but an unstable displayed value, the later software path deserves attention. If touching the cable changes raw readings, inspect the physical connection and electrical reference. If the problem appears only when a motor starts, power, grounding, electromagnetic coupling and mechanical motion become competing hypotheses. Several may contribute at once.

Use a short hypothesis table. For each explanation, write what observation would support it, what would contradict it and the cheapest safe test. Change one relevant thing, retain the previous working state and record the outcome. Randomly replacing five components can remove the symptom while leaving you unable to explain or reproduce the repair.

Negative evidence is useful only when the test could have detected the effect. “I did not see deflection” means little if the ruler could not resolve it or the camera moved with the fixture. Establish the measurement's reference and sensitivity.

## Bench lab: separate placement from reading

Download the [experiment log](../worksheets/experiment-log.csv). Use a ruler, a small rigid block or folded card sensor mockup, tape and a flat table. Use a removable card stop; no sharp tool or powered equipment is necessary.

1. Mark a reference line and a target position suitable for your ruler, perhaps 40 mm. Define which edge of the mockup is measured.
2. Place the mockup once and read its position five times without moving it. Look away between readings. Record every result. This mainly probes your reading method, though the object may drift.
3. Remove and replace it five times, measuring once after each placement. This adds placement variation.
4. Add the stop and repeat five replacements. Alternate conditions if the stop can be removed reproducibly; otherwise note the order as a limitation.
5. Calculate the mean and range for each set. Describe any shift in the mean separately from the change in spread.
6. Ask another person to repeat the method using only your written instructions, or repeat it later without referring to your earlier values.

Expected outcome: repeated placements may vary more than repeated readings of an unmoved object, and a stable stop may reduce placement variation. Your apparatus may behave differently. If all readings are identical, check whether the ruler is simply too coarse to reveal the differences. If the stop performs worse, inspect tape movement, flexible edges and inconsistent contact pressure. Keep the result; the experiment is allowed to reject your prediction.

## Check your understanding

**Will averaging remove a constant zero offset?** No. It can reduce an independent repeatability contribution to uncertainty in the mean; a shared offset remains until addressed through a suitable correction or method.

**Do twenty measurements of one printed hole establish production consistency?** No. They mainly describe repeated measurement of that feature. You need separately manufactured parts to study part-to-part variation.

**The improved fixture is more repeatable but misses the target. Is it a failure?** It has solved one problem and exposed another. Decide whether the offset can be corrected without losing repeatability, then test the revised configuration.

**Must every experiment use a formal statistical test?** No. Early exploratory work often needs transparent raw data and a large, reproducible practical effect. A formal test cannot rescue a poorly defined measurement or confounded comparison.

For independent practice, choose one disputed fit, sensor behavior or placement in your project. Write two competing explanations and design a measurement that distinguishes them. Use a provisional acceptance rule before seeing the result. In [Chapter 4](../product-design/), you will connect such evidence to a user's actual task, where a technically measurable improvement may still be the wrong thing to optimize.
