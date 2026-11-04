# Work like an inventor

A sensor needs to stay pointed at a moving target. You can imagine a printed bracket, a motorized mount, a camera that follows the target, or a robot that carries the sensor. All four are plausible projects. They are very different first experiments.

Start by asking what you need to learn next. If the sensor's location is still uncertain, a cardboard mount can answer more than a beautifully modeled enclosure. If the location is known but the bracket droops, a load and deflection test is useful. If the bracket is stable but the readings jump, another mechanical redesign may be irrelevant. Inventing becomes less mysterious when each build is a way to resolve a particular uncertainty.

This chapter assumes no specialist tools. By the end, you should be able to turn a broad idea into a small test, distinguish a requirement from a solution, and explain what evidence would justify the next version. You will need paper, a ruler, tape, and an ordinary object you would like to position or hold. A cardboard substitute is enough.

## Begin with the job, then define the boundary

“The device should be better” gives you no way to decide when to stop. “The sensor should return to the same position after I remove and reinstall it” is more useful, but still needs a context. How close is close enough? Who installs it? With which tools? In what environment?

Write a sentence with a person, an action and a situation. For example: “At my indoor workbench, I want to remove a small sensor to change its cable and reinstall it without re-aiming it from scratch.” You have described a job. A dovetail, a magnet and two locating pins are possible solutions. Keeping these separate makes it easier to change the mechanism without forgetting why it exists.

The **system boundary** separates what you are designing from what you accept as given. For the first bracket, the bench, sensor and cable may be outside the boundary. Their mounting dimensions and loads still cross it. Draw a box around your design and arrows for every crossing: forces, electrical power, data, heat and human actions. An ordinary cable can cross three boundaries at once: it carries signals, consumes connector space and pulls on the mount.

This is also where you decide what this version will not attempt. A bench fixture need not survive rain unless outdoor use is part of its actual job. It does need enough cable access to be assembled. A useful scope boundary removes irrelevant work while retaining conditions that can make the intended use fail.

## Requirements describe observations

A requirement is a statement you can check. It is not automatically a scientifically justified threshold. Your first numbers may be provisional; mark them as such and explain how you chose them.

| Vague wish | Testable first requirement | Why it matters |
| --- | --- | --- |
| Easy to remove | A user can remove and replace the sensor using one specified tool | Tests the service sequence rather than the appearance |
| Accurate | After five reinstallations, a marked point remains within a provisional 1 mm target region | Makes repositioning visible; the threshold still needs application evidence |
| Strong | Holds a stated test object in a defined orientation without slipping during a supervised bench check | Identifies load, pose and failure; does not establish an unrestricted load rating |
| Compact | Fits inside a measured envelope while leaving the connector removable | Includes the space used during maintenance |

A constraint is a boundary you must respect: a mounting-hole position, available supply voltage, fabrication process or budget. An objective is something you would like to improve within those constraints: mass, cost, noise or assembly time. If you combine every objective into “best,” the tradeoffs disappear from the conversation but remain in the object.

Stanford's [Design Thinking Bootleg](https://dschool.stanford.edu/tools/design-thinking-bootleg) offers practical methods for understanding a situation, generating options and testing them. Use one method to investigate a real decision. Collecting an entire vocabulary of design methods is less useful than observing one person struggle with an actual connector.

## Three representations of the same idea

Keep three views beside one another:

1. **A description:** what the device should accomplish and for whom.
2. **A model:** a sketch, equation, circuit or program that predicts something about it.
3. **An experiment:** an action that can reveal whether the prediction is useful.

Suppose a thin plastic strip supports the sensor. Your description says the sensor must keep its aim. Your model says a longer unsupported span bends more. Your experiment compares two spans under the same small load. These are connected, but they are not interchangeable. A CAD image is a geometric model; it is not evidence that a particular printed material will hold its position for a week.

Every model leaves things out. A simple beam equation may ignore a flexible clamp. A circuit calculation may treat the supply as an ideal voltage source. A robot simulation may assume perfect friction. Write down the omission when it could change your decision. You do not need a complete model of the universe to make a bracket; you need a model whose limits you can recognize.

## Choose the next experiment by information gained

Imagine you have four hours available. Printing a full enclosure takes three, and testing it takes another. A paper connector template takes ten minutes and can reveal that the cable cannot bend into the available space. When that uncertainty is unresolved, the template has a better learning return.

A simple planning table helps. Use ordinal scores as a conversation aid, not a mathematically precise forecast.

| Uncertainty | Consequence if wrong | Cheap test | Decision changed by the result |
| --- | --- | --- | --- |
| Connector can be serviced | Assembly may be unusable | Full-size cardboard envelope and real cable | Move the connector or enlarge the opening |
| Printed hole fits the chosen fastener | Part may need reprinting | Small fit coupon | Adjust one clearance parameter |
| Sensor gives useful readings | Entire concept may be unsuitable | Bench readings from the actual sensor | Change sensor or measurement method |
| Surface texture is attractive | Cosmetic preference | Small finish sample | Change finish after function is established |

You can quantify part of this choice without pretending to know failure probabilities. If a fit coupon uses 8 g of filament and a full part uses 160 g, the full part consumes the material of **20 coupons**. That does not prove the coupon predicts every behavior of the full part. It explains why local fit is worth checking locally while reserving full-size tests for span, warping and structural behavior that depend on scale.

**Predict:** would a half-size bracket establish the strength of the full-size bracket? **Check:** no. Geometry, load, layer arrangement and failure mechanisms do not all scale in the same way. A small specimen can answer a defined local question; it cannot silently stand in for every property of the final design.

## A notebook that supports decisions

Give every experiment an identifier. Record the question, the design revision, the test setup, the raw result and the conclusion separately. “Hole too small” loses useful information. “Coupon F03, modeled 8.1 mm, PLA, mouth upward, sleeve enters by hand after loose debris removal” preserves the conditions of the observation.

Keep the raw readings even when they look inconvenient. A transcription error can be corrected with a note; silently replacing a surprising value makes it impossible to distinguish a measurement problem from a real event. Photographs should include a scale or identifiable reference when size matters. A file named `final-final-real.stl` is a warning that your revision system has become interpretive art.

A practical directory can be small:

```text
sensor-mount/
  brief.md
  design/                 editable CAD and drawings
  fabrication/            named exports and process settings
  experiments/            raw readings, photographs, notes
  software/               code and configuration, if any
  releases/               a frozen set someone else could reproduce
```

Keep the editable source and the manufactured output together by revision. Changing a Fusion parameter does not update an STL already sent to a printer. The [software and data chapter](../software-data/) extends this habit to code, configuration and test inputs.

## Bench lab: make a reversible positioning fixture

Choose an object light enough that a fall onto the table will not damage it; use a cardboard dummy if uncertain. Keep it away from people, fragile equipment and table edges. The lab investigates repeatable placement, not load capacity.

1. Trace the object's outline on paper. Mark the location of a cable or access door if it has one.
2. Make a crude holder with folded card and tape. Add two visible reference marks, one on the holder and one on the object.
3. Write a test before performing it: remove the object, replace it, and measure the reference-mark displacement five times. Specify the ruler direction and what counts as the same location.
4. Perform the sequence. Record every reading and note whether the object rocks, the card flexes or the tape slides.
5. Change one feature: add a locating stop, a wider base or a second contact. Repeat the same sequence.
6. Compare the ranges and the assembly experience. Decide which uncertainty to investigate next.

**Expected observation:** a physical stop often makes placement less dependent on visual alignment, but a flexible stop may move with the object. A smaller spread after the change supports an improvement under this test. It does not establish performance in other orientations or after repeated wear.

**If the readings are indistinguishable:** your ruler or marking method may be too coarse to see the difference, or both concepts may already be adequate for the chosen requirement. Improve the measurement or stop optimizing that property. A test that cannot discriminate between designs should not be turned into a confident ranking.

**If the holder shifts on the table:** first separate movement of the holder from movement within the holder. Otherwise you may redesign a locating feature to compensate for an unrelated attachment problem.

## Use a makerspace as a learning system

A shared shop offers more than expensive machines. It provides examples, experienced operators and feedback on your setup. Bring a drawing and a question: “How would you hold this stock while leaving these two faces accessible?” invites a more useful conversation than “Can this machine make my part?”

Learn the local authorization and cleanup rules before operating a machine. For the immediate lab, the relevant hazards are modest. As projects grow, identify the energy involved: a hot nozzle, rotating tool, stored spring, charged capacitor or moving actuator each changes the test setup. Choose a way to stop and de-energize the experiment before increasing that energy. Machine-specific instruction belongs beside the actual machine and its trained operator; reading a general chapter is not a substitute.

## Leave with one decision, not a shopping spree

Fill in the [project brief](../worksheets/project-brief.md). Your first independent task is to name one uncertain interface and make the cheapest prototype that can resolve it. An interface is where two things meet: a bolt and hole, hand and handle, sensor and software, or message and receiver.

Before moving on, answer these questions in your notebook:

- **What would count as a failed experiment?** A result you dislike can still be informative. A setup that cannot answer the stated question is the more fundamental failure.
- **Which part of the result is measured, and which part is inferred?** Five stable placements are measured evidence. A prediction about a thousand placements requires an additional argument or test.
- **What will the next version change?** Name one cause you intend to address and the observation that will tell you whether it helped.

The bracket is only the beginning. The same cycle applies when your object becomes a circuit, a program or a robot: define the job, expose the assumptions, run a discriminating experiment, and keep enough evidence to make the next decision intelligible.
