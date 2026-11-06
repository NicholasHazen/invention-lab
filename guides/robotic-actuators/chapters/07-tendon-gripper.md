# Design a tendon-driven finger

A tendon lets you put a motor away from a moving finger. The finger can stay light, the transmission can bend around obstacles, and a compliant element can soften contact. The price is a less obvious relationship between motor angle and what happens at the fingertip. Cord stretch, changing routing, slack, spool layering and contact geometry all matter.

We will make that relationship explicit for **one hinged finger**, then identify what changes in a real gripper. You need moments and free-body diagrams from [Chapter 4](#chapter-04), plus the component and joint workflow used in the preceding studies. You will construct a constant-radius tendon layout, budget the hinge clearances, model the motion in Fusion, and plan a low-energy unpowered experiment. A complete gripping hand and a motor-control system come later.

[Fusion envelope model](designs/tendon-gripper-envelopes.f3d) · [STEP model](designs/tendon-gripper-envelopes.step) · [front DXF](designs/tendon-gripper-front.dxf) · [axial DXF](designs/tendon-gripper-axial.dxf) · [parameters](designs/tendon-gripper-parameters.csv) · [layout JSON](designs/tendon-gripper-layout.json)

These files describe **envelopes and pitch surfaces**. They have no final tendon groove, anchor, bushings, return spring or motor coupling, and their component positions are snapshots. The native features are editable, but they are not a finished associative assembly or fabrication release. Use the steps below to develop your own design around selected cord, pin, bearings and actuator.

![Fusion perspective of the finger hinge, separately supported spool and connected stop structure. The orange sketch marks routing/travel references; grooves, anchors, spring and motor coupling are still to be designed.](designs/tendon-gripper-fusion.png)

*Fusion perspective of the finger hinge, separately supported spool and connected stop structure. The orange sketch marks routing/travel references; grooves, anchors, spring and motor coupling are still to be designed.*

## Put a real moment arm into the drawing

The target is a 5 N fingertip force acting perpendicular to a 30 mm arm. Its hinge moment is `5 × 0.030 = 0.150 N·m`. A tendon with a **10 mm effective moment arm** needs `0.150 / 0.010 = 15 N` tension in the ideal static case. An 8 mm spool then needs `15 × 0.008 = 0.120 N·m` before friction, spring load or acceleration.

“Effective moment arm” means perpendicular distance from the hinge to the tendon's line of action. It does not mean distance from the hinge to an arbitrary attachment hole. A straight cord attached to a hole changes its moment arm as the finger moves; in some poses it can approach zero. Our study instead wraps the tendon around a circular sector concentric with the hinge. The straight segment remains tangent to the sector, keeping its ideal moment arm at 10 mm.

![Tendon layout with a constant-radius finger sector, spool, fingertip load, and a separate axial section of the supported hinge.](assets/design-tendon-layout.svg)

In the drawing, the hinge is at X = 0, Y = 0. The incoming tangent lies at Y = 10 mm. The spool centre is X = −45, Y = 18 mm, putting its lower 8 mm-radius tangent on the same line. The tendon continues around the finger sector to an anchor. For example, an anchor initially 60° below the finger's forward axis gives 150° of wrap from the upper tangent; after a 60° closing rotation, 90° of wrap remains. The groove and anchor must accommodate that entire excursion. A line ending at the tangent point would not connect the tendon to the finger.

Here the specified radii refer to the **tendon centre line**. Cord diameter shifts the required groove surface. An 8 mm-radius printed cylinder is therefore only a spool pitch envelope, not the final surface to print. Select the cord first and respect its bending and termination guidance; a sharp drilled hole is not an adequate default guide for repeated sliding.

## Check travel as well as force

With constant effective radius, tendon displacement is radius multiplied by angle in radians. A 60° finger rotation requires `10 × π/3 = 10.47 mm` of ideal tendon travel. The 8 mm spool must rotate `10.47 / 8 = 1.309 rad`, or **75°**. This relation assumes the tendon remains seated, taut and on one layer at an unchanged effective spool radius.

Suppose a second winding layer increases effective spool radius from 8 to 9 mm. The same 75° now takes up 11.78 mm, about 12.5% more cord; 15 N tension also requires 0.135 N·m instead of 0.120 N·m. A motor-angle command that was correct on the first layer is no longer correct. For this short-travel study, use a single controlled groove and sufficient anchored wrap rather than a heap of cord on a drum.

The 5 N calculation also assumes a particular contact direction. If the contact normal makes angle β with the finger, its moment is `F × 0.030 × sin(β)`. Multiple contacts introduce additional unknown forces. Tension alone does not tell you every fingertip contact force. The [Yale OpenHand project](https://www.eng.yale.edu/grablab/openhand/) is a useful next reference for seeing how practical tendon-driven hands combine mechanical design with adaptive behavior; its designs are not evidence that this new finger is validated.

## Model the hinge and routing together

![Four modeling checkpoints for the tendon radii, supported hinge, motion range and accessible tendon termination.](assets/design-tendon-steps.svg)

1. **Create the design vocabulary.** Start a new Fusion document with components `Layout`, `Base`, `Finger`, `Pin`, `Spool`, `SpoolSupport`, `OpenStop` and `ClosedStop`. Add user parameters `finger_length = 30 mm`, `tendon_radius = 10 mm`, `spool_radius = 8 mm`, `finger_thickness = 8 mm`, `pin_diameter = 4 mm`, `side_clearance = 0.3 mm`, and `finger_travel = 60 deg`. Define `clevis_gap = finger_thickness + 2 * side_clearance`. These are study values, not selected-hardware tolerances.

2. **Constrain the routing sketch.** On XY, centre the finger pitch circle at the origin and dimension its radius with `tendon_radius`. Add the spool circle at X = −45 mm, Y = 18 mm. Constrain a horizontal construction line tangent to the top of the finger circle and bottom of the spool circle. Use the actual Tangent constraints, then inspect their solutions: the wrong tangent branch can place the line on the opposite side. Mark both circles as construction geometry so they cannot be mistaken for printable groove boundaries.

3. **Sketch the finger and sector.** Activate `Finger`. Draw a 30 mm centre line and a compact outline around it. Constrain the hinge centre to the origin and dimension the tip location from that centre. Add the circular sector surrounding the hinge. Keep a substantial section between the hinge bore and tendon path; rounding the outline cannot compensate for a thin ligament. **Extrude** the joined finger profile 8 mm. Add the pin/bushing opening from the selected hardware dimensions, not by copying an assumed screw clearance.

4. **Create the clevis stack.** The finger occupies Z = 0…8 mm. Start the two 4 mm cheeks at Z = −4.3 and 8.3 mm, leaving 0.3 mm per side. Create them as stationary geometry connected to the base; a removable cheek can simplify assembly and service. Keep the metal pin separate. Use **Section Analysis** through the hinge to inspect the stack, including any washers or bushing flanges. If washers are added later, increase the gap or revise the stack rather than compressing the finger between cheeks.

5. **Give the spool its own support.** Put the tendon in the Z = 4 mm plane. Reserve bearings or bushings on both sides of the spool and connect their housings to the base. The downloaded rings and connected legs reserve those functions; they do not contain selected bearings, fits or fastening details. A motor coupling transmits spool torque. The finger's contact load travels through its hinge and base, while tendon tension loads both finger and spool supports. Do not hang the whole mechanism on a small motor shaft merely because it turns.

6. **Develop the groove and termination.** After choosing cord diameter, create a groove section on a plane through the finger hinge and use **Revolve → Cut** for a circular track, or **Sweep → Cut** along the intended sector path. Locate the seated cord centre line at the specified 10 mm radius. Leave enough sidewall to retain the cord through the excursion, with rounded entry edges and accessible cleaning. Place the anchor outside the working sliding region. Model the actual clamp, knot pocket or termination method and a tool path to reach it. Repeat for the spool at its 8 mm effective radius.

7. **Add motion and real stops.** Ground the base and use a **Revolute Joint** about the pin, initially limited to 0…60°. Drive it slowly in Fusion. Check fingertip sweep, anchor sweep, retained wrap and cheek clearance at the ends and several intermediate poses. Model open and closed contact stops against supported finger features. The download's simple stops touch its rectangular finger at the nominal endpoints; recheck their contact faces against your actual swept outline. Software joint limits do not create these physical stops.

## Treat the return spring as another load

A single tendon pulls but does not push. A return spring can reopen the finger, provided its torque exceeds hinge and routing friction over the intended range. Its load also adds to the required tendon tension during closing. If the spring contributes 0.020 N·m at one pose, that pose needs another `0.020 / 0.010 = 2 N` of tendon tension. The ideal total becomes 17 N and spool torque 0.136 N·m before friction. A spring chosen only to remove slack may not reopen a binding hinge.

Model the spring's operating envelope and its anchor access, then use its actual force/deflection data to check the full range. Preload stores energy even when the finger is open. For the first fit and motion check, leave the spring off and move the finger by hand; add a modest, documented return element only after the path is clear. Keep a caught finger or loose spring out of the experiment by using a fixture, soft test objects and a supported hand-operated tendon.

A return spring is also different from a **series elastic sensing element**. A spring deliberately placed in series with the tendon can estimate tension from measured extension: approximately `T = k × extension` within its calibrated region. For an illustrative 5 N/mm element, 15 N produces 3 mm extension. That extra 3 mm belongs in the spool-travel budget. Measuring a spring elsewhere in the mechanism, or assuming a printed flexure's stiffness, does not automatically measure tendon tension. [Chapter 9](#chapter-09) develops the distinction between motor position and output measurement.

## Print to protect the hinge and the cord

Print a hinge-fit coupon before a full finger: two cheek samples, a short finger boss, the selected pin and any bushings. Test the planned 0.3 mm side clearances, then adjust from measured results. Avoid making an ordinary threaded screw the wearing hinge surface; choose an appropriate smooth pin or shoulder and a retention method that does not clamp the moving part solid.

Lay out the finger so its principal bending load has a continuous material path from tip to hinge. Inspect perimeters around the bore and groove in the slicer. A groove that leaves a thin shell beside the pin can fail regardless of infill percentage. Add root fillets at the finger/sector transition and small bed-edge chamfers after the structural profile is settled. Smooth cord-contact edges after printing and inspect for support scars; a bevel that helps insertion is not necessarily a suitable repeated-bending surface.

Keep at least the study pin's 22 mm length clear along its withdrawal direction. Make the tendon termination reachable after the finger is installed, because retensioning and replacement are expected maintenance operations. A beautiful enclosed finger that requires cutting the cord for every adjustment teaches an expensive lesson about serviceability.

## Test the relationship before trusting a force estimate

Make a paper version first. Mark a 10 mm-radius sector, draw the upper tangent, and rotate a finger line through 60°. Measure arc length with a paper strip: the expected ideal travel is about 10.47 mm. Then draw a straight tendon from the spool to one attachment hole and repeat the rotation. Observe how its perpendicular distance to the hinge changes. This comparison explains exactly which assumption the sector buys you.

On an eventual unpowered prototype, mark the tendon near a fixed reference, pull it gently by hand, and record displacement versus finger angle without a spring or contact load. Hesitation followed by a jump suggests friction or snagging; motor/spool rotation without immediate finger motion suggests slack, stretch or termination slip. Repeat after adding the return spring, then after adding a small measured contact load. Those are separate tests, not one unexplained “grip strength” number.

**Predict:** If the tendon radius doubles while fingertip geometry stays unchanged, what happens? **Answer:** Ideal required tension halves, but tendon travel for the same angle doubles. With the same spool, its rotation doubles; ideal spool torque halves. Hinge size, cord routing and packaging change too.

**Try a variation:** Move contact from 30 to 20 mm from the hinge while keeping 5 N perpendicular force. Recalculate tension and spool torque, then explain why the same tendon tension can produce a different contact force. Finally add a second finger on a shared tendon and list the extra contact and compliance information needed before claiming that both fingertips exert the same force.
