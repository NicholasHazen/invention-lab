# Design a belt-driven rotary joint

A small motor can turn an arm without carrying the arm on its own bearings. Put the arm on a separate steel shaft, support that shaft at two stations, and connect the shafts with a timing belt. This separates two jobs that are easy to confuse: the belt transmits torque; the shaft supports and housing carry the external loads.

This study takes the 0.25 kg payload, 100 mm arm and 3:1 reduction from [the sizing chapter](#chapter-04) into Fusion. You need that chapter's torque and speed concepts, basic sketch/extrude familiarity, and a millimetre document. By the end, you should be able to explain the load path, construct an editable layout, inspect its axial clearances, and design a small fit coupon before committing to a housing.

The downloads are **envelope studies**, not parts ready for fabrication. The native models contain separate, named components and editable sketches/extrusions. Their positions are snapshots; changing a reference parameter does not rebuild the complete assembly. The manual recipe below teaches the associations you should add to your own model. Pitch cylinders have no teeth, the motor is generic, and the purchased hardware, fasteners, fits and guards still need selection.

[Fusion envelope model](designs/belt-joint-envelopes.f3d) · [STEP model](designs/belt-joint-envelopes.step) · [front DXF](designs/belt-joint-front.dxf) · [axial DXF](designs/belt-joint-axial.dxf) · [parameter table](designs/belt-joint-parameters.csv) · [layout JSON](designs/belt-joint-layout.json)

![Fusion perspective of the separate shaft, bearing-station, pulley-pitch, arm, motor and bracket envelopes. No belt, pulley teeth, final fits or fasteners are modeled.](designs/belt-joint-fusion.png)

*Fusion perspective of the separate shaft, bearing-station, pulley-pitch, arm, motor and bracket envelopes. No belt, pulley teeth, final fits or fasteners are modeled.*

## Make the geometry agree with the transmission

For a synchronous pulley, pitch circumference is tooth count multiplied by belt pitch. Our 20-tooth and 60-tooth pulleys at 2 mm pitch therefore have pitch diameters of 12.732 mm and 38.197 mm. Those circles describe motion; they are not outside diameters or tooth-generation templates. Buy a matched belt and pulley family, then replace the circles with the manufacturer's geometry. The [Gates design manual](https://www.gates.com/content/dam/documents-library/catalogs/light-power-and-precision-manual.pdf) explains selection of pitch, width, length, installation allowance and tension; matching “2 mm” alone is insufficient to establish a compatible system.

Choose a **candidate** belt pitch length of 200 mm for this study. For an open belt with centre distance C and pitch radii R and r, its ideal length is:

`L = 2√(C² − (R − r)²) + π(R + r) + 2(R − r) asin((R − r)/C)`.

Solving gives **C = 58.61153 mm**. The downloadable [generator](designs/generate_layouts.py) solves this equation and checks the reconstructed length. We have not selected or verified a 200 mm belt SKU. Do that before converting the layout into a mounting pattern. Add a provisional 4 mm adjustment range along the centre line; the selected belt's installation and tensioning requirements determine the final slot length and nominal position.

![Front view and axial section of the belt joint, including separate bearing stations and shaft insertion access.](assets/design-belt-layout.svg)

In the front view, both bearings collapse onto one circle. The axial view resolves the arrangement: bearing centres are at z = 0 and 30 mm; their 7 mm widths occupy −3.5…3.5 and 26.5…33.5 mm. The provisional pulley occupies z = 10…20 mm. That leaves **6.5 mm on each side**, before allowing for its actual hub, inner-ring spacers and retention hardware. A purchased pulley with a projecting hub can consume that space immediately. This is why an axial sketch precedes a detailed housing.

## Follow the force before drawing the bracket

The horizontal arm's worst gravity torque is `9.81 × (0.25 × 0.1 + 0.08 × 0.05) = 0.28449 N·m`. A 90° triangular move in one second has acceleration 6.283 rad/s². The arm and payload inertia total 0.0027667 kg·m², adding approximately 0.01738 N·m during acceleration. Adding the assumed 0.010 N·m friction allowance gives a conservative output-demand envelope of **0.3119 N·m**. The gravity and acceleration maxima need not coincide; this sum is a useful preliminary bound.

At 3:1 and assumed 90% forward efficiency, this load contributes about **0.1155 N·m at the motor**. Motor rotor inertia, drive-pulley inertia and other rotating parts still add acceleration torque. In particular, rotor inertia contributes `Jmotor × 18.85 rad/s²` for this motion; it has not been set to zero. Peak output speed is 30 rpm and motor speed 90 rpm.

At the output pitch radius, `0.3119 / 0.01910 ≈ 16.3 N` is the **difference** between tight-side and slack-side belt tension. It is not the total bearing load. Installation tension can produce substantial radial force even with no output torque. The arm also produces shaft bending when its load acts away from the bearing span. Draw these forces separately. A wider bearing span helps resist a bending moment, but cannot fix a flexible base or loose bearing seats. The 608 dimensions in this exercise establish space; they do not establish a complete bearing rating or axial-retention scheme.

## Build a skeleton that you can change

![Four instructional checkpoints for locating the axes, arranging the stack, supporting the shaft, and finishing printed brackets.](assets/design-belt-steps.svg)

1. **Create the document and components.** Save a new design named `BeltJointStudy`. Create `Layout`, `Base`, `MotorMount`, `OutputShaft`, `BearingA`, `BearingB`, `OutputPulley` and `Arm` components before adding solids. A component represents a separately moving or assembled item; a body is geometry within it. Ground the base in the completed assembly, not every component. Keep the existing pivot in its own file.

2. **Name the governing dimensions.** Open **Modify → Change Parameters**. Enter `pitch = 2 mm`, `motor_teeth = 20`, `output_teeth = 60`, `center_distance = 58.61153 mm`, `bearing_spacing = 30 mm`, `bearing_width = 7 mm`, `shaft_diameter = 8 mm`, and `belt_plane = 15 mm`. Make tooth counts unitless. Define pitch diameters with `motor_teeth * pitch / PI` and `output_teeth * pitch / PI`. Named expressions preserve intent when you revise the ratio. [Autodesk's parameter reference](https://help.autodesk.com/cloudhelp/ENU/Fusion-Model/files/SLD-MODIFY-PARAMETERS.htm) describes these dependencies. Our CSV is a human-readable parameter table, not a promise of compatibility with Fusion's parameter-import schema.

3. **Constrain the front layout.** Activate `Layout`, create an XY sketch, and place the output circle at the origin. Place the motor circle to its right. Constrain its centre horizontal to the origin and dimension the centre distance. Make both pitch circles construction geometry and dimension their diameters with the expressions. Add two common external tangents as construction lines. Apply Tangent constraints and constrain each endpoint onto its circle; do not estimate the angle by eye. The motor centre should have no remaining freedom once its horizontal relation and distance are defined.

4. **Build the axial layout.** Create an XZ sketch through the output axis. Draw construction station lines at z = 0, `belt_plane`, and `bearing_spacing`. Add bearing and pulley section rectangles with their widths. Use symmetric dimensions about station lines instead of independently positioning both edges. Inspect the 6.5 mm spaces with **Inspect → Measure**. The two DXFs can provide a reference, but [Insert DXF](https://help.autodesk.com/cloudhelp/ENU/Fusion-Model/files/SLD-INSERT-TOOLS.htm) imports fixed sketch geometry; tracing the small skeleton with native constraints teaches more than fixing an entire imported drawing.

5. **Create the purchased-part envelopes.** Activate each appropriate component. Use **Construct → Offset Plane**, then **Sketch → Circle** and **Extrude** for the shaft, bearing annuli and pitch cylinders. The output shaft spans z = −15…45 mm in the study. Model bearings as separate 8 mm bore, 22 mm OD, 7 mm wide annuli. Name pitch cylinders conspicuously. Replace them with supplier CAD before designing against flanges or hubs. A plain shaft cylinder likewise omits the features needed to transmit torque and retain parts.

6. **Connect the stationary structure.** Model two bearing cartridges attached to a common base. Keep one cartridge removable so that a belt and pulley can be installed between the stations. Sketch cartridge feet and triangular root gussets before adding cosmetic details. Project only the stable skeleton geometry you need; avoid projecting every edge of a detailed purchased component. Add a slotted motor plate whose adjustment follows the axis-centre line. Include the washer diameter and a straight driver-access cylinder at each proposed fastener, not merely its hole.

7. **Represent motion and service access.** Rigidly connect the shaft, arm and output pulley, then add a **Revolute Joint** between shaft and base. The motor turns on its own supports. Drive the output joint through the intended range and inspect arm/base clearance; a motion relation can express the ideal 3:1 ratio but does not simulate belt tension. Reserve at least 60 mm beyond the shaft insertion end in this study, then check the actual assembly sequence. A housing that assembles only by bending a shaft is unfinished.

## Finish the printable parts deliberately

Start with a bearing-seat coupon instead of both cartridges. Sketch a 32 mm square with a central circular opening, extrude it 9 mm, and make three separate copies with trial openings of 22.2, 22.3 and 22.4 mm. These are exploratory dimensions for an accessible slip-fit experiment, not a bearing-fit specification. Print them in the intended material, orientation and slicer profile; measure the openings and record which accepts the actual bearing without hammering. A removable cap or properly designed retainer must supply retention rather than an arbitrary printed interference fit.

Use a small **Chamfer**, initially 0.3–0.5 mm at 45°, on bed-contact edges to reduce first-layer interference. Give an insertion mouth a short lead-in while preserving the intended cylindrical seating length. Use **Fillet** at heavily loaded bracket roots to spread the geometric transition. A rounded upper edge can create an unfavorable underside overhang; a chamfer or changed orientation may print more cleanly. Keep these finishing features late in the timeline so layout changes remain easier to diagnose.

A 0.4 mm nozzle and 0.2 mm layer height are reasonable first coupon settings on the X1 Carbon. Choose wall thickness from the actual line width and inspect the slicer's paths around seats, screw bosses and gussets. More infill does not repair a thin load path. Orient each cartridge so that its main bending load does not peel a narrow layer interface, and check whether the bearing bore needs support or finishing in that orientation. No fixed wall count establishes a load rating.

## Check the design without powering it

On paper, list the order: open the removable station; place the belt around both pulleys; insert shaft, spacers and output pulley; close the station; add retention; align pulley planes; adjust belt tension according to the selected system. In Fusion, hide each installed component in reverse order. If a part cannot leave along its intended insertion path, revise access before printing.

For an eventual unpowered bench assembly, support the arm and verify smooth hand rotation before adding a payload. A tight spot once per turn suggests runout or misalignment; binding that appears when a cartridge is tightened suggests distorted or non-coaxial seats. Belt tracking against one flange suggests plane/alignment error. Loosening everything until it turns is a diagnosis step, not a final repair. Use [the validation chapter](#chapter-10) to establish controlled loading and measurement after hardware selection.

**Predict:** If you double the bearing spacing while preserving the same bending moment, what happens to the ideal reaction-force couple? **Answer:** Its force magnitude halves because `M = F × spacing`. Shaft flexibility, housing deformation and direct radial forces remain. The model has not proven that overall deflection halves.

**Try a variation:** Replace the output pulley with an 80-tooth candidate, keep the motor pulley at 20 teeth, and find a suitable new centre distance. Update the axial envelope as well as the front sketch. Explain the change in motor speed, load torque, reflected inertia, belt clearance and installation access before choosing a new motor.
