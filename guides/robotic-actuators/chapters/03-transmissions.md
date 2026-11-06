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

## Chains and capstans: other ways to span two axes

A **roller chain and sprockets** can transmit motion between separated shafts with an average ratio set by tooth count. It is useful for robust power transmission, but joint wear lengthens the chain, slack affects reversals, and lubrication and alignment remain maintenance tasks. A chain bends at discrete joints, so its path around a sprocket is a polygon. This **chordal action** produces cyclic speed variation, especially with small sprockets. [Tsubaki's chain guide](https://catalog.ustsubaki.com/view/303981549/1/) explains that geometry; [Renold's wear guide](https://www.renold.com/media/1269222/Chain-wear-guide-instructions.pdf) shows how elongation is inspected. Those effects can matter much more in precise joint reversals than in a continuously rotating wheel drive.

A **cable capstan** transmits effort through a cable wrapped around a drum, using friction and initial tension to maintain traction. This can provide a light transmission with little tooth-clearance backlash, but slip, cable stretch, terminations, and drum accuracy become the design problems. More wrap and preload can increase traction; preload also loads the shafts. [MIT's transmission notes](https://fab.cba.mit.edu/classes/865.21/topics/mechanical_design/transmissions/) explain the wrap and termination constraints. A tendon wound onto an anchored spool is related but does not rely solely on frictional capstan traction: [chapter 7](#chapter-07) uses an attached tendon and a return spring. In both, the cable pulls; reverse actuation needs an opposed tensioned path or a return mechanism.

## Spur and helical gears: a direct tooth-to-tooth exchange

An external **spur-gear** pair turns opposite ways, with speed ratio set by tooth count. Several pairs multiply their ratios, while their losses and clearances accumulate. Gears keep the drive compact but create tooth forces that push shafts apart. Tangential force transmits torque; the pressure angle produces an additional separating component. Shaft locations and housing stiffness therefore belong in the gear design.

A **helical gear** spreads tooth engagement across its face as the angled teeth enter mesh. That can make operation smoother, but it also creates axial thrust that the bearings and retainers must carry. Opposite-handed halves in a **double-helical or herringbone gear** oppose those thrusts; manufacturing error and unequal loading still deserve attention. Jönköping University's [herringbone explanation](https://mechanics.ju.se/MachineElements/herringbone-gears.html) connects the helix angle to that force. A pretty V-shaped tooth does not establish a load rating.

Spur gears are useful when you want a visible, comparatively simple first experiment. Helical gears become attractive when smoothness, noise, and available bearing support matter more than the simplest profile. For either, check tooth-root strength, contact stress, lubrication, center distance, and reversal clearance. Printed versions can teach motion at low loads; their layer strength, temperature sensitivity, surface finish, and wear must be measured. Purchased gears in a printed frame let you concentrate the printing lesson on alignment and support.

## Planetary reducers: compact and coaxial

A **planetary stage** places planet gears between a central sun and an internally toothed ring. The carrier holds the planet shafts. With the ring fixed, sun input, and carrier output, the ideal reduction is `N = 1 + Zring/Zsun`. A 60-tooth ring and 20-tooth sun give 4:1, with the carrier rotating in the sun's direction. Changing the fixed member changes the relationship. See the labeled [transmission comparison](#compare-types) and the [planetary derivation](https://mechanics.ju.se/MachineElements/planetary-gears.html).

Coaxial input and output help package a motor behind a joint. Several planets can distribute load, and multiple stages can provide more reduction. Those advantages require accurate geometry and support: planet loads are not automatically equal, and successive stages add length, friction, and clearance. Compare the assembled gearbox's backlash, rated torque at the intended speed and life, and permitted shaft loads. A planetary gearhead can make a useful general-purpose joint drive, but the output bearing may still need help carrying your cantilevered module.

## Harmonic drives: strain-wave gearing

**Strain-wave gearing** is the mechanism commonly meant by “harmonic drive.” **Harmonic Drive®** is a trademark used for commercial products. The reducer is a transmission; it becomes part of a servo actuator when combined with a motor, sensing, and control. That distinction lets us compare a brushless servo with a planetary reducer against a brushless servo with strain-wave gearing without changing two ideas at once.

In the common cup-type arrangement, the [three-part construction](https://harmonicdrive.de/en/technology/harmonic-drive-gears) creates the reduction:

1. The **wave generator** is the input: an elliptical hub and deformable bearing.
2. The **flexspline** is a thin, externally toothed cup. The wave generator makes its open end elliptical; its diaphragm connects to the output.
3. The **circular spline** is a rigid, internally toothed ring, fixed to the housing in this example. It has slightly more teeth than the flexspline.

Teeth engage in two opposite regions near the ellipse's long axis. Turning the wave generator moves these engagement regions around the ring. The flexspline slowly turns the other way because the tooth counts differ. The [manufacturer's operating-principle lesson](https://www.hds.co.jp/english/products/hd_theory/) shows this sequence. The elliptical outline rotates quickly; a marked piece of the flexible cup rotates slowly. They are different motions.

![Original end-view schematics identify the wave generator, flexspline, fixed circular spline, and two engagement zones in a strain-wave reducer, then distinguish the eccentric, stationary ring pins, orbiting disc, and output pins in a cycloidal reducer.](assets/reducer-strain-wave-cycloidal.svg)

*The colors identify parts, not materials. Tooth profiles and deformation are simplified. The cycloidal drawing shows one disc and an output flange behind it; the holes accommodate the disc's offset orbit while the flange rotates about the fixed main axis.*

Using the [fixed-ring kinematic relationship](https://mechanics.ju.se/MachineElements/cycloidal-strainwave.html), take a 202-tooth circular spline and a 200-tooth flexspline output:

`ωoutput / ωinput = −(202 − 200)/200 = −1/100`

One clockwise input turn produces **3.6° counterclockwise output**, so the reduction magnitude is 100:1. The formula depends on which member is fixed and which is the output. At our target 30 rpm output, this example needs 3,000 rpm input. That result alone says nothing about whether its thermal, life, or torque limits fit our arm.

The attraction is substantial reduction in a compact coaxial package, with very small tooth-clearance backlash in engineered units. The trade is a precision assembly with a repeatedly flexing component. **Low backlash is not infinite stiffness:** a loaded output can twist even when there is no free tooth clearance to take up. Hysteresis means its angle can also depend on loading history. Harmonic Drive's [SHF/SHG engineering catalog](https://www.harmonicdrive.net/media/support/catalogs/pdf/shf-shg.pdf) treats torsional stiffness, hysteresis, efficiency, backdriving torque, and life separately. Use the applicable current product data; the catalog is an example of what to ask for.

A **component set** and a **housed unit with an output bearing** are different purchases. The former leaves more housing, alignment, and support work to you; the latter may integrate a rated output support. The [manufacturer's product overview](https://harmonicdrive.de/en/technology/harmonic-drive-gears) explicitly separates those packages. Neither the reducer's torque rating nor a hollow center automatically supplies the bending support needed by the neighboring module.

For our printed project, a strain-wave demonstrator could teach deformation and ratio, but a durable flexspline is its own materials and fatigue project. Printing the shape does not reproduce the behavior or life of the specified steel part. For a working compact joint, first investigate a purchased reducer and print the surrounding mounts. Check continuous and intermittent torque, input speed, life, mounting accuracy, lubrication, stiffness, and the desired power-off behavior before committing to its envelope.

## Cycloidal reducers and RV drives

A **cycloidal reducer** starts with an eccentric input bearing: its center is offset from the main shaft axis. It carries a lobed disc around stationary pins in the housing. With one fewer disc lobe than ring pins, each input turn makes the disc turn back by one lobe pitch. Output pins attached to a concentric flange pass through enlarged holes in the disc. Those holes accommodate the orbit, while the pins collect the slow rotation. [Sumitomo's mechanism explanation](https://emeia.sumitomodrive.com/en-gb/cycloidal-gear-technology) identifies these two different pin sets.

For the simple fixed-ring, single-stage arrangement in the schematic, 11 ring pins and a 10-lobe disc give `ωoutput/ωinput = −1/10`. Ten clockwise eccentric turns produce one counterclockwise output turn. Changing the lobe difference or using a compound arrangement changes the formula. The schematic's enlarged holes are not accidental looseness: without room for eccentric motion, the disc would bind against the output pins. Real hole dimensions also include the roller diameter, fits, and clearance.

The useful feature is compact reduction with several load-carrying contacts. Well-engineered versions can provide high stiffness and shock capacity. The costs include accurate lobe geometry, eccentric bearing loads, pin fits, lubrication, and vibration management. Many designs use two discs phased to oppose their eccentric effects. Those details explain why a single printed disc that turns freely is not yet equivalent to an industrial reducer. Jönköping University's [cycloidal lesson](https://mechanics.ju.se/MachineElements/cycloidal-strainwave.html) develops the kinematics and output-hole geometry.

**Nabtesco RV** refers to a particular commercial two-stage architecture, not every cycloidal mechanism. An initial spur-gear stage drives crankshafts, followed by paired cycloidal discs. Their support arrangement and integrated main bearings are part of the design's capacity. [Nabtesco's engineering overview](https://www.nabtescoprecision.com/engineering/) shows both stages. Do not apply the simple ten-lobe ratio above directly to an RV unit; use its stated overall ratio and configuration.

For a larger, stiff joint, a purchased cycloidal/RV unit may be a useful candidate. For this small modular robot, compare its entire mass and envelope against the load before assuming a high-capacity industrial mechanism is desirable. A printed cycloidal experiment is also approachable as a separate learning project, with metal pins and bearings where appropriate, but its clearances, wear, reversal error, and load capacity need their own tests.

## Bevel and worm drives: turn a corner

**Bevel gears** transfer rotation between intersecting axes, commonly at 90°. A 1:1 miter pair can turn the drive through a corner without reducing speed. They help place a motor along a robot link, but gear mounting depth and shaft alignment affect contact. Both radial and axial loads must reach appropriate bearings; the [bevel-gear lesson](https://mechanics.ju.se/MachineElements/bevel-gears.html) explains those forces. A bevel pair changes the drive layout; it does not by itself reproduce our pivot's 45° split-joint geometry.

A **worm drive** uses a screw-like input meshing with a wheel, commonly on offset right-angle axes. It can provide substantial reduction in one stage, but sliding contact makes friction, lubrication, heat, and duty central selection questions. Some combinations resist backdriving; that depends on geometry and condition. Bodine's [gearmotor FAQ](https://bodine-electric.com/faqs/) warns against relying on self-locking gearing to prevent movement. If power loss must not drop the arm, provide a suitable holding arrangement and supported failure state. A difficult-to-turn gearbox is not a measured brake specification.

## Screws and racks: when the output should translate

A **sliding lead screw**, **ball screw**, and **roller screw** all convert relative screw–nut rotation into axial travel. They differ in how the load crosses that interface. This guide uses “lead screw” for the sliding-thread type; some catalogs use the term for the wider family. The **lead** is travel per revolution, which need not equal thread pitch. Our study uses a 2 mm lead, so 25 turns produce 50 mm travel regardless of which supported screw technology supplies that lead.

| Linear transmission | How force crosses the interface | Useful reason to investigate | Constraint to check |
| --- | --- | --- | --- |
| Sliding lead screw | Nut threads slide on screw threads | Straightforward, often economical; useful for modest-duty positioning | Frictional heat, wear, backlash, nut material, lubrication, and duty |
| Ball screw | Recirculating balls roll in screw and nut grooves | Efficient motion and predictable rated life for a defined load | Preload/clearance, ball-return speed, contamination, cost, and backdriving |
| Planetary roller screw | Threaded rollers transmit load between screw and nut | High-force motion where package size or life justifies the integration | Precision manufacture, price, lubrication, heat, and actual load–life rating |
| Rack and pinion | Rotating gear teeth engage a straight toothed rack | Long travel without a long rotating screw | Tooth loads, alignment, reversal clearance, rack joints, and a separate guide |

The distinctions in [Thomson's lead-screw discussion](https://www.thomsonlinear.com/en/support/20150128-uk) and [Tolomatic's screw comparison](https://www.tolomatic.com/info-center/resource-details/acme-ball-roller-screw-selection/) are useful selection questions, not universal rankings. The guide's 50 mm stage does not need an industrial roller screw merely because it is strong. All three screws need suitable thrust support and a mechanism that prevents unwanted rotation of the translating member. A long rotating screw also brings critical-speed and buckling checks. High efficiency can make a vertical load easier to backdrive, so plan the holding behavior. [Chapter 6](#chapter-06) develops the stage and its separate linear guide.

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
