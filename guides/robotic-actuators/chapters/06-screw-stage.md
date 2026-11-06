# Design a screw-driven linear stage

A screw is good at turning rotation into axial motion. It is a poor substitute for the rest of a linear stage. If you bolt a platform to a nut and leave the platform unsupported, a sideways force can bend the screw, twist the nut and change friction along the travel. Give the platform a guide, give the screw a defined thrust reaction, and connect them so each does its intended job.

Here we design a **horizontal stage with 50 mm useful travel**, moving at 20 mm/s against 10 N axial resistance. You need the rotary-to-linear relations from [Chapter 4](#chapter-04) and the component/sketch workflow from [the belt joint](#chapter-05). The outcome is a dimensioned motion envelope and a Fusion model whose useful travel, support locations and assembly route agree. This is a layout exercise, not a qualified machine axis.

[Fusion envelope model](designs/screw-stage-envelopes.f3d) · [STEP model](designs/screw-stage-envelopes.step) · [plan DXF](designs/screw-stage-plan.dxf) · [end-view DXF](designs/screw-stage-end.dxf) · [parameters](designs/screw-stage-parameters.csv) · [layout JSON](designs/screw-stage-layout.json)

The downloaded screw is a plain 8 mm cylinder and the nut is an envelope. Neither contains thread geometry. The native assembly has editable component features but fixed layout positions, rather than the completed parametric motion relationships taught below. Its fixed-support and guide blocks reserve space for hardware that still needs selection.

![Fusion perspective with the base below the stage: separate screw, nut carrier, guide, axial-support, coupling and motor-mount envelopes. Threads, final bearing selection and fasteners are absent.](designs/screw-stage-fusion.png)

*Fusion perspective with the base below the stage: separate screw, nut carrier, guide, axial-support, coupling and motor-mount envelopes. Threads, final bearing selection and fasteners are absent.*

## Turn a travel requirement into a complete length budget

Use X along the screw, Y across the base, and Z upward. Put the screw axis at Y = 0, Z = 20 mm. The useful **carriage-centre** range is X = 40…90 mm. A 20 mm nut therefore occupies X = 30…50 at one end and 80…100 at the other. A candidate threaded region from X = 25…105 leaves 5 mm of thread beyond the nut at either useful endpoint.

The guide block is longer: 30 mm. Its two extreme envelopes are X = 25…55 and 75…105. The guide spans X = 20…110. Again, the preliminary end allowance is 5 mm. These are geometric margins; the chosen guide's insertion, engagement and end-clearance requirements can demand more. Never choose rail length from useful travel alone.

![Plan and end views showing the nut, separate linear guide, fixed and floating screw supports, and the full travel budget.](assets/design-screw-layout.svg)

The illustrative screw spans X = −10…130 mm, including 10 mm inside the coupling. We reserve X = 0…15 for the fixed support and 115…130 for a floating radial support; transitions to the working thread lie between those zones and the threaded region. The actual shaft machining, retaining nuts, shoulders and bearing arrangement will change these envelopes. The coupling occupies X = −20…0; the generic motor shaft ends at −11, leaving 1 mm between shaft ends. Its bore sizes and engagement lengths require a selected coupling. It must not become the stage's thrust bearing by accident.

The end stops contact the **guide block**, not the delicate nut flange. Contact planes at X = 20 and 110 place block-centre stops at 35 and 95. The useful endpoints at 40 and 90 consequently have 5 mm before mechanical contact. A home/limit sensor must trigger with enough remaining distance for detection, stopping and uncertainty. Five millimetres is only a study allowance; it has not been verified against a real controller or stopping distance.

## Check speed, torque and the support load

The screw lead is 2 mm/revolution. At 20 mm/s it turns at `20 / 2 = 10 rev/s`, or **600 rpm**. For a 10 N axial resistance and assumed 35% forward efficiency:

`torque = force × lead / (2π × efficiency)`

`= 10 × 0.002 / (2π × 0.35) = 0.00909 N·m`.

Useful linear power is `10 × 0.020 = 0.20 W`; the corresponding steady screw input is approximately 0.571 W. The torque looks small because the screw trades considerable rotation for little travel. It excludes acceleration, guide and nut preload, seals, coupling losses and motor inertia. A motor must supply the required torque **at 600 rpm**, not merely have an impressive zero-speed holding torque.

The 0.35 efficiency is an explicit teaching assumption. Actual screw efficiency depends on geometry and friction; lubrication, duty and nut design matter. Thomson discusses those dependencies in its [lead-screw and ball-screw comparison](https://www.thomsonlinear.com/en/support/20150128-uk). Use the chosen product's data rather than treating our calculated value as a specification.

The nut pushes the carriage with 10 N and pushes the screw oppositely. That reaction travels through a properly retained axial-bearing arrangement into the base. The far support locates the screw radially while permitting the intended axial accommodation. “Fixed” and “floating” describe support functions, not just whether a block is bolted down. A pair of generic printed blocks containing 608 bearings does not automatically provide controlled thrust support. Appropriate bearings, fits, shoulders, retaining hardware and alignment must complete the load path. Thomson's [screw selection resources](https://www.thomsonlinear.com/en/products/ball-screws) also treat support configuration, critical speed and compression as selection inputs; our 140 mm envelope establishes none of those ratings.

## Model the carriage's freedom, then remove the unwanted freedoms

![Four Fusion modeling checkpoints: travel envelopes, separate guide, thrust path, and assembly order.](assets/design-screw-steps.svg)

1. **Create components and parameters.** Start a new document with `Layout`, `Base`, `Screw`, `Nut`, `GuideRail`, `GuideBlock`, `Carriage`, `FixedSupport`, `FloatingSupport` and two `EndStop` components. Enter `travel = 50 mm`, `lead = 2 mm`, `nut_length = 20 mm`, `block_length = 30 mm`, `travel_start = 40 mm`, and `travel_end = travel_start + travel`. Use expressions for block and nut endpoints. Do not scatter “90” through unrelated sketches.

2. **Sketch both limiting positions.** On the XY plane, draw a construction screw-axis line. Add centre points at `travel_start` and `travel_end`, constrained horizontal to the origin and dimensioned along X. Draw centre rectangles for the nut and guide block at each point; use construction geometry for these swept envelopes. The guide centre line is offset 25 mm in Y. Equal constraints keep paired endpoint envelopes the same size. Both positions must be visible before you choose the base outline.

3. **Set the height in an end-view sketch.** On the YZ plane, dimension the screw centre 20 mm above the base datum. Draw a guide envelope at Y = 25, a block above it and a bridge connecting block to nut. Use **Project/Include → Project** selectively to reference the stable layout axes. Inspect the bridge underside and screw/nut clearance. The downloaded end view makes this distinction visible; a plan view alone can hide a bridge passing through a screw.

4. **Extrude the envelopes in their own components.** Sketch the 8 mm screw section on a YZ plane and **Extrude** along X. Create the 20 mm nut around it as an annulus, explicitly named `Nut envelope — no thread`. Create the rail and block with rectangular sketches and extrusions. Do not add decorative helical grooves: they would look authoritative without representing the selected screw. Supplier CAD and an exact screw/nut designation belong here once chosen.

5. **Assemble one permitted carriage motion.** Ground the base; rigidly attach the rail and support housings. Rigidly connect guide block, carriage and nut. Use a **Slider Joint** along X between carriage and base and set its useful travel to 50 mm. Give the screw a **Revolute Joint** about X. A motion relation of 360° rotation per 2 mm translation can demonstrate the ideal kinematics. Joint limits are an animation aid; they neither create an end stop nor model friction, compliance or a controller.

6. **Locate and make removable the end stops.** Project the endpoint block envelope into each stop sketch. Put stop contact faces 5 mm beyond the useful positions, as above. A stop should transfer load to the base through a substantial shoulder or supported face; a tiny screw suspended in a thin printed tab is a poor default. Keep one stop removable so the block can slide onto the rail. Reserve at least 30 mm beyond that open end for insertion of this study's block, then update the allowance from the actual guide and assembly instructions.

7. **Add hardware and tool envelopes.** Replace the fixed-support placeholder with the selected assembly before cutting its mounting holes. Include the coupling's clamping screws and their driver direction. Place rail screws where the carriage can uncover them, or provide a documented assembly order. A useful check is to model a cylinder as wide as your hex-driver handle and move it along each screw axis. Hide it before export; keep the sketch as a service-access reference.

## Give printed parts jobs they can perform predictably

Print the base, carriage adapter, guards and sensor brackets; buy the screw/nut, guide and support hardware. A printed threaded nut may be an interesting separate friction experiment, but it changes this study's precision, wear and efficiency assumptions. A plastic base also changes alignment with clamping and temperature, so it should not be treated as a metrology surface.

Use **Fillet** at carriage-bridge roots and bracket transitions, while preserving flat hardware seating faces. Put a small 45° **Chamfer** on bed-contact perimeter edges and accessible insertion mouths. Keep screw-head counterbores and nut pockets open to a tool. Avoid a broad unsupported ceiling above a captive nut; use an insertion slot, a separately attached cover, or an orientation that prints the pocket cleanly. [Prusa's modeling guidance](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135) illustrates why print orientation changes the usefulness of fillets and chamfers.

Make a small coupon containing the chosen screw clearance hole, washer recess, and nut or insert pocket before printing the base. The exact pocket comes from the actual hardware. Measure the coupon after cooling; check seating, insertion and removal, not merely whether a fastener can be forced into it. Fastener clearance and bearing fit are different design requirements and should have different parameters.

In the slicer, inspect continuous perimeters around the carriage attachment and stop roots. Place ribs beneath the bridge where they shorten its bending span. Orient the main load-bearing sections to avoid relying on a narrow bond between layers, and ensure a screw cannot split a layer stack when tightened. The layout models intentionally omit those final details: apply them to a selected-hardware design, then repeat interference and service-access checks.

## A bench exercise that distinguishes alignment from backlash

First do the exercise in Fusion. Move the carriage centre to X = 40, 65 and 90. At each position inspect nut engagement, block engagement, cable space and screw clearances. The expected result is 5 mm preliminary margin at both useful extremes and no bridge/screw overlap. If the margin exists at only one end, check whether a centre dimension was confused with an edge dimension.

When hardware is selected and assembled, disconnect motor power and turn the screw slowly by hand. Move the guide block alone before connecting it to the nut. If each subsystem moves freely separately but binds when connected, suspect parallelism, height error or an overconstrained attachment. More motor current is not a correction for misalignment. With the screw stationary, gently reverse a small axial force and measure carriage displacement: that motion may combine thread backlash, axial-support clearance and structural flex. Measuring only motor angle cannot separate them.

**Predict:** Does a 2 mm lead guarantee that the stage stays still without power? **Answer:** No. Backdrivability depends on the selected screw, friction, load and vibration; our horizontal study establishes no vertical holding function. A vertical version requires a deliberate power-loss restraint strategy and new load analysis.

**Try a variation:** Increase useful travel to 100 mm while retaining the 20 mm nut and 30 mm block. Extend the thread and guide envelopes from the centre-position extremes; then revisit screw critical speed, bending, base stiffness and insertion access. Simply lengthening the base leaves several of those dependencies unchanged when they need to change.
