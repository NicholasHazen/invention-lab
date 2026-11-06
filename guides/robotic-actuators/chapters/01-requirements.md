# Start at the thing you want to move

A small robot arm can be easy to move by hand and surprisingly difficult to drive well. It has to lift its load, speed up, stop without bouncing, and sometimes hold still for much longer than it moves. The motor has to do its share of that work while the shaft, bearings, frame, driver, and power supply do theirs. A large torque number on a product listing tells us very little about that whole job.

Our first design will move a 250 g payload at the end of a 100 mm arm. The arm itself weighs 80 g. We want a 90° swing in one second around a horizontal axis. That is small enough to reason about on paper, but it contains the same decisions that appear in larger robot joints: reduction ratio, support spacing, speed, feedback, heat, and what happens when power disappears.

By the end of this guide, you will be able to describe an actuator's job, estimate the demands it creates, compare drive arrangements, and model three mechanical layouts in Fusion. You will also have a measurement plan that tells you what a real prototype still needs to prove. The three studies are a belt-driven rotary joint, a screw-driven linear stage, and a tendon-driven finger. Their CAD files are dimensioned layout studies; they deliberately stop short of claiming a selected, manufactured, tested actuator.

You need basic arithmetic, a way to draw a dimensioned sketch, and a little familiarity with Fusion's sketches and components. The [handbook's mechanisms chapter](../../handbook/mechanisms/index.html) is a useful starting point if shafts, bearings, and transmissions are new. You can do the calculation activities without Fusion or any electronics. A calculator or the included Python programs is enough.

## Draw the boundary before choosing parts

An actuator turns supplied energy into controlled mechanical motion or force. In a robot project, the useful design boundary is usually bigger than the motor. Include the transmission that changes speed and torque; the bearings and housing that carry loads; the sensor that reports motion; the driver that switches electrical power; and the controller that decides what to request next.

![System diagram separating electrical energy, mechanical power, structural reactions, and feedback. The output bearing support returns load reactions to the fixed frame.](assets/system-boundary.svg)

*Follow the solid arrows to see where power travels. Follow the dashed arrows to see what is measured or commanded. The bearing support has a separate job: it closes the structural load path to the fixed frame.*

Consider the same arm driven by a small geared motor. The motor creates torque. The gearbox changes the relation between motor rotation and arm rotation. If the arm is fastened to a long unsupported shaft extension, its weight also bends that shaft and loads the gearbox's output bearing. A gearbox that can transmit enough torque may still have an unsuitable bearing arrangement. We therefore draw a supported output shaft first and decide how to drive it second.

The electronics have a similar separation. A microcontroller can request a position; it cannot deliver the motor's required power directly. A driver switches that power, subject to its own current, voltage, and thermal limits. A feedback sensor measures something at a particular place. An encoder on the motor reports motor motion. It does not directly reveal a flexible belt twisting or a loose output hub moving independently.

This boundary makes comparisons fair. A hobby servo includes several pieces inside one enclosure. A bare brushless motor leaves many of them to you. Comparing their purchase prices or masses without accounting for the missing pieces is comparing different systems.

## Write a job that a test could settle

“Strong and precise” is a direction, not a test. Replace it with a table of quantities and conditions. For our rotary study, we can already write the following. The unresolved entries are useful: they identify decisions that a product listing cannot make for us.

| Requirement | Study value or next decision | Why it changes the design |
| --- | --- | --- |
| Payload and location | 0.25 kg, 100 mm from output axis | Sets gravitational moment and contributes inertia |
| Moving arm | Uniform 0.08 kg arm, 100 mm long | Its own weight and inertia also need support and drive torque |
| Orientation | Horizontal output axis | Gravity changes joint torque as the arm rotates |
| Motion | 90° in 1.0 s, rest to rest | Sets speed and acceleration once a profile is chosen |
| Motion profile | Symmetric triangular speed profile | Provides a simple, explicit acceleration model |
| Repetition and dwell | Specify before selecting a motor | A single move and a repeated cycle create different heating |
| Position error | Define at the output, under a stated load | Separates useful performance from encoder resolution |
| Power loss | Initially support the load independently | A powered holding claim says nothing about an unpowered joint |
| Environment | Indoor bench study | Temperature, debris, moisture, and duty remain product decisions |

For a real requirement, finish the sentence: “After approaching from either direction, the output must settle within ___ degrees in ___ seconds while carrying ___.” That wording exposes backlash and settling behavior. A repeatability test approached from only one direction answers a narrower question. Record which question you actually tested.

The requirement also needs a reference frame. An arm rotating in a horizontal plane around a vertical shaft has a different gravitational torque about that shaft from an arm lifting in a vertical plane. The same mass and distance are insufficient unless the orientation is known. Draw an arrow for gravity on your first sketch.

Manufacturer sizing procedures follow this output-first sequence: define the mechanism, motion, holding and positioning needs, calculate at the drive shaft, and then check the selected motor and gearhead together. The [Oriental Motor sizing reference](https://www.orientalmotor.com/products/pdfs/F_TecRef/TecMtrSiz.pdf) is a useful example of that workflow.

## Separate weight, torque, and inertia

With the arm horizontal, the payload's weight is 0.25 × 9.81 = 2.4525 N. Its torque about the joint is that force multiplied by the perpendicular 0.100 m distance: 0.24525 N·m. The uniform arm's weight acts at its midpoint, adding 0.08 × 9.81 × 0.050 = 0.03924 N·m. Together, they produce **0.28449 N·m** of gravitational torque.

That value is a static result. It says what must be balanced at the horizontal pose; it does not include acceleration, friction, or the mass of an output pulley we have not yet selected. When the arm points straight down or up, gravity has zero moment about this ideal joint even though the bearings still carry weight. A vanishing gravity torque does not mean a vanishing structural load.

Inertia describes resistance to a change in rotational speed. Mass farther from the axis matters more strongly here: a point mass contributes mass times radius squared. Our payload contributes 0.25 × 0.100² = 0.0025 kg·m². The uniform arm contributes mass times length squared divided by three, giving another 0.0002667 kg·m². The modeled load inertia is **0.0027667 kg·m²**.

Predict what happens if we move the same payload from 100 mm to 200 mm while keeping the original arm model separate. Its gravity torque doubles, but its inertia contribution becomes four times as large. This is why a longer robot link can demand a different actuator even when the payload does not change. If you also lengthen the arm, update its mass distribution instead of carrying forward the old arm inertia.

Keep units beside values in both sketches and spreadsheets. Entering 100 into a formula that expects meters makes the gravitational moment a thousand times too large and the payload inertia a million times too large. The included calculators accept labeled millimeters at their boundary and convert to meters before calculation.

## A ratio changes more than torque

Suppose a motor turns a 20-tooth pulley that drives a 60-tooth output pulley. The reduction ratio is 60/20 = 3. The motor makes three revolutions for each output revolution. In an ideal lossless transmission, the output torque is three times the motor torque and its speed is one third. Power is conserved by that exchange; a ratio is not a source of energy.

Real transmissions lose energy and store some elastic deformation. Their geometry also changes what the motor and load feel when they accelerate. Motor inertia appears larger when viewed from a reduced-speed output; the ideal reflected value scales with the square of the ratio. [Modern Robotics' actuation lesson](https://modernrobotics.northwestern.edu/nu-gm-book-resource/8-9-actuation-gearing-and-friction/) develops that relationship. We will use it when a larger reduction looks like an effortless way to solve every torque problem.

For now, draw the motor and the output as separate rotating components. Place two bearing stations on the output shaft, then sketch the belt plane. The support spacing, output overhang, and belt tension influence shaft and frame loading. They belong in the same design review as the motor's torque-speed curve.

## Make a requirements card before opening a catalog

Take a sheet of paper or copy the table above. Spend about twenty minutes completing these four steps for a mechanism you care about.

1. Draw the moving part in its most demanding likely pose. Mark the axis, gravity, mass locations, and external contact force. If several poses might dominate, keep all of them.
2. Write one motion in measurable terms: start, finish, distance or angle, and time. Add how often it repeats and how long it waits under load.
3. Identify what must be measured at the output. Choose position, speed, force, or a combination, then state the condition under which an error would matter.
4. Draw where the load goes when motion stops and when power is removed. Identify the frame, support bearings, and any independently rated holding element your application will require.

Your expected result is a page with enough information to estimate loads and enough open questions to guide measurement. It is normal for friction, required life, and thermal conditions to remain unknown. Label them “measure” or “decide,” rather than replacing them with favorable guesses.

If you cannot decide whether a load belongs in the torque calculation, ask whether its line of action has a perpendicular offset from the rotation axis. If you cannot decide whether it belongs in the bearing calculation, trace how its force reaches the frame. A load can matter to one calculation even when its contribution to the other is zero.

## Check the boundary you drew

**Prediction:** A motor encoder reports exactly the commanded angle, but the arm tip moves when you push gently on it. Does that prove the controller is faulty?

**Check:** No. The output may move through belt elasticity, gearbox backlash, a loose hub, bearing clearance, or frame flex while the motor encoder stays still. First observe which parts move relative to one another. An output sensor can reveal the error; it cannot make a mechanically loose connection stiff.

**Prediction:** The calculated horizontal holding torque is 0.28449 N·m. A listing claims a 0.30 N·m stall torque. Is the motor selected?

**Check:** No. Stall describes zero-speed operation under particular conditions, often with current and heating that cannot be sustained. We still need motion torque, speed, continuous operation limits, the driver and supply, and the support structure. Chapters 2–4 turn those missing pieces into a comparison you can actually make.

For your own variation, take one neighboring robot module as the load. Weigh it, locate its center of mass relative to the proposed joint, and make the same requirements card. Keep those measurements separate from this guide's 250 g study. The existing [45° pivot](../triangulated-pivot/index.html) gives us a useful mechanical starting point, but adding actuation will require a new load case, packaging review, and physical validation.
