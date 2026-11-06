# Transmissions: exchange motion without losing the load path

Our arm needs slow rotation and appreciable holding torque. A small motor often prefers to turn faster. A transmission can make those requirements compatible, but it also changes the feel of an external push, the forces in the bearings, and the angle error after a reversal. Choosing only a reduction ratio leaves most of the mechanism undesigned.

Bring torque, angular speed, and the distinction between motor and output from [chapter 2](#chapter-02). You will compare transmission families, calculate the effects of reduction, and sketch where the resulting forces enter a printed frame. The exercises need a calculator and paper. The geometry remains a design study until actual purchased parts and their limits are selected.

## Define the ratio before using it

Define reduction as `N = motor speed / output speed`. A 20-tooth motor pulley driving a 60-tooth output pulley therefore gives `N = 60/20 = 3`. The motor turns three revolutions while the output turns once. For forward power transmission with efficiency η:

`ωmotor = N × ωoutput`

`τoutput ≈ η × N × τmotor`

The ratio trades speed for torque. It does not create power: multiplying these relationships gives output mechanical power approximately η times input mechanical power. Efficiency represents losses under specified operating conditions. At rest, where mechanical power is zero, use a static torque/friction model and thermal limits rather than pretending a power efficiency determines holding behavior.

Our shared arm's moving-load bound is approximately 0.312 N·m and its peak output speed is 30 rpm. With `N = 3` and assumed `η = 0.90`, the preliminary motor-shaft targets are about 0.116 N·m and 90 rpm. These are conservative sizing coordinates, not a claim that maximum load torque occurs at exactly the maximum-speed instant. They also exclude the motor's own inertia and unidentified transmission losses.

## Belts make the arrangement visible

A toothed belt can separate the motor axis from the output axis. That helps place motor mass closer to the robot's base and leaves the joint center available for a shaft or cable passage. Tooth engagement determines the nominal ratio; belt stretch, tooth clearance, pulley alignment, and mounting flexibility still affect loaded positioning. A toothed belt should not be described as perfectly rigid or automatically free of reversal error.

The **pitch circle** follows the belt's nominal pitch line. For tooth count `z` and pitch `p`, its diameter is `d = zp/π`. Our 2 mm pitch, 20T and 60T layout therefore uses pitch diameters 12.73 mm and 38.20 mm. Those circles locate motion; they are not pulley outside diameters or manufacture-ready tooth profiles. Select a matching belt and pulley tooth system before importing supplier CAD or preparing production geometry.

Torque comes from a difference between tight-side and slack-side belt tensions. At the output pulley, `ΔT = τ/r`. A 0.312 N·m torque on a 19.10 mm pitch radius requires a tension difference near 16.3 N. The shaft also experiences the vector sum of both span tensions. Pretension can make that bearing load much larger than the torque-producing difference. Gates' [precision-drive manual](https://www.gates.com/content/dam/documents-library/catalogs/light-power-and-precision-manual.pdf) provides separate selection, tension, and force relationships; using the tension difference alone as a bearing load misses part of the problem.

In Fusion, model the belt plane, pulley faces, flange envelopes, bearing stations, and tension-adjustment travel before decorating the housing. Keep a path for sliding the belt into place and reaching the mounting screws. A motor plate that bends under pretension changes alignment even when the motor has ample torque. [Chapter 5](#chapter-05) develops this layout into the guide's first rotary study.

## Gears concentrate the ratio

An external spur-gear pair turns opposite ways, with speed ratio set by tooth count. Several pairs multiply their ratios, while their losses and clearances accumulate. Gears keep the drive compact but create tooth forces that push shafts apart. For a chosen gear geometry, tangential force transmits torque and the pressure angle determines an additional separating component. Shaft locations and housing stiffness therefore belong in the gear design.

A planetary stage puts planet gears between a central sun and an outer ring. With the ring fixed, sun input, and carrier output, the ideal reduction is `N = 1 + Zring/Zsun`. A 60-tooth ring and 20-tooth sun give 4:1; the moving carrier changes the kinematics. Jönköping University's [planetary-gear lesson](https://mechanics.ju.se/MachineElements/planetary-gears.html) derives the relationships for different fixed members. Load sharing also depends on geometry, support, and tolerances; multiplying one tooth's strength by the number of planets is not a complete rating method.

Printed spur or planetary gears can teach assembly and motion at low loads. Start with a valid tooth profile, adequate tooth thickness, retained shafts, and measured center-distance clearance. Layer direction, tooth-root stress, surface finish, temperature, and wear then become experimental variables. A printed housing around purchased gears often separates useful fabrication practice from the harder task of making durable precision teeth.

## Cycloidal and strain-wave drives use small geometric differences

A cycloidal reducer uses an eccentric input to move a lobed disc around a surrounding ring of pins or rollers. The difference between disc lobes and ring features produces a large reduction; output pins or another mechanism extract the disc's slow rotation while accommodating its orbit. Nabtesco's [RV mechanism explanation](https://www.nabtescoprecision.com/engineering/) shows a commercial two-stage arrangement with paired discs and deliberate bearing support. Its shock and precision claims describe that engineered product, not every printed cycloidal shape.

A strain-wave drive uses a wave generator to deform a flexible toothed member into engagement with a rigid outer member. In a common arrangement, the flexible member has two fewer teeth. A 200-tooth flexspline inside a fixed 202-tooth circular spline retreats two teeth per wave-generator revolution, yielding 100:1 reduction with reversed direction. Harmonic Drive Systems' [operating-principle animation](https://www.hds.co.jp/english/products/hd_theory/) makes those moving engagement regions visible.

Both mechanisms offer compact high reduction, but compactness does not eliminate elasticity, friction, fatigue, or assembly tolerances. A strain-wave flexspline bends repeatedly; a printed demonstration must be evaluated for cyclic material behavior rather than assigned the life of a metal commercial unit. “Zero backlash” also does not mean zero torsional deflection under load. Keep those as separate quantities in a comparison table.

A worm drive uses a screw-like input meshing with a wheel, often turning the output through a right angle. Its sliding contact makes friction and lubrication consequential. Some combinations resist backdriving, but that behavior depends on geometry and condition. Bodine's [gearmotor FAQ](https://bodine-electric.com/faqs/) explicitly warns against relying on self-locking gearing to prevent movement. If power loss must not drop the arm, design an appropriate holding device and supported failure state; a difficult-to-turn gearbox is not sufficient evidence.

## Reduction changes inertia in both directions

Imagine accelerating the output by hand. The motor must accelerate N times as fast. Since rotational kinetic energy is `½Jω²`, substituting `ωmotor = Nωoutput` makes the motor's energy look like an output-side inertia `Jmotor × N²`. Looking from the motor in the opposite direction, the load appears as `Jload/N²`. These describe the same mechanism from different reference shafts.

![Increasing reduction lowers load inertia seen by the motor but increases rotor inertia felt at the output. Both directions are shown with an explicit 3:1 example.](assets/families-inertia.svg)

For our payload and uniform arm, `Jload = 0.25×0.1² + 0.08×0.1²/3 = 0.002767 kg·m²`. To expose the trade, temporarily assume an illustrative motor inertia of `0.000020 kg·m²`; this is a sensitivity input, not the inertia of a selected motor. Ignore transmission inertia and losses for this energy comparison.

| Reduction N | Motor speed at 30 rpm output | Load inertia seen at motor, kg·m² | Motor inertia seen at output, kg·m² |
| --- | ---: | ---: | ---: |
| 1 | 30 rpm | 0.002767 | 0.000020 |
| 3 | 90 rpm | 0.0003074 | 0.000180 |
| 10 | 300 rpm | 0.00002767 | 0.002000 |
| 30 | 900 rpm | 0.000003074 | 0.018000 |

More reduction makes the load easier for the motor to accelerate, but makes the motor harder for the output to accelerate. At 30:1, this illustrative rotor contributes over six times the arm's own inertia when viewed at the output. This matters for impacts, hand guidance, and force response. Add gearbox and pulley inertia at their actual shaft speeds; do not multiply every component by the same ratio.

Direct drive sets `N = 1`, removing the reduction stage while demanding the full joint torque from the motor. A modest-ratio quasi-direct drive retains some torque multiplication with a smaller inertia penalty. Neither term guarantees backdrivability: cogging, seals, friction, active control, and electrical braking also affect an external push. A power-off test condition must specify whether motor terminals are open, shorted, or connected to a live drive.

## Carry bending around the transmission

The arm's load creates both a torque about the rotation axis and forces perpendicular to it. A motor torque rating addresses only the first. Support the output shaft through a bearing arrangement whose radial, axial, moment, speed, and fit limits suit the complete load. Our two 608-size bearing envelopes, 30 mm apart, illustrate a support layout; their dimensions alone provide no assembled load rating.

As a simple moment check, a 0.300 N·m bending moment reacted by two stations 0.030 m apart requires a force couple of `M/L = 10 N`. Doubling spacing halves that couple. Actual bearing reactions must also include net arm weight, belt forces, overhang, and axial loads; the 10 N is not the complete reaction. Move the pulley into a well-supported region where packaging permits, and make the bearing seats part of a continuous load path into the frame.

For printed parts, broad load paths, accessible through-bolts, and metal shaft interfaces are useful starting choices. Radius a structural inside corner to reduce a sharp stress concentration; chamfer an insertion edge to help assembly. Neither feature compensates for thin material splitting across layers. Inspect the print orientation together with the free-body diagram.

## Compare ratios without hiding the costs

Predict: if N doubles with the same motor, does motor inertia felt at the output double or quadruple? Does doubling bearing spacing reduce the arm's weight?

1. Recreate the four-row inertia table in a spreadsheet or calculator, retaining units in column headings.
2. Change the illustrative motor inertia to `0.000040 kg·m²`. Identify which columns change.
3. Sketch the 3:1 belt drive in side view. Mark both bearing centers, both pulley centers, the belt plane, and the arm's load line. Add an assembly direction and a wrench-access arrow.
4. On a second sketch, shorten the bearing spacing from 30 mm to 15 mm while keeping the illustrative bending moment at 0.300 N·m. Recalculate the moment couple.

**Check:** reflected motor inertia quadruples when N doubles. Doubling motor inertia doubles only the final table column. The closer stations require a 20 N moment couple, while net weight stays unchanged. If your bearing calculation gives smaller couple forces at smaller spacing, the lever arm has been inverted. If your gear ratio appears to create power, check that torque and speed refer to the same shaft.

For an independent design, compare a 3:1 belt and a 30:1 gearbox for a joint a person must reposition by hand with drive power removed. Make a decision using torque–speed capability, inertia, friction, encoder location, and the behavior after release. The strongest explanation will identify the measurements still needed rather than declare a winner from ratio alone.
