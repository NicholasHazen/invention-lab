# From breadboard to PCB—and from switches to chips

A breadboard lets you change a circuit quickly. A printed circuit board, PCB, makes its connections repeatable, gives components mechanical support, and can fit the circuit into a product. It also freezes mistakes into copper. The goal of a first PCB is therefore to preserve a circuit you understand while learning how its physical form changes its behavior.

This chapter connects the logger's small circuits to schematic capture, layout, fabrication review, and the semiconductor devices inside integrated circuits. You will distinguish a symbol from a footprint, trace a current's return path, and prepare a simple board for review without needing to order it. Prerequisites are the circuit and signal chapters; basic embedded behavior helps explain the digital examples. The core lab uses free KiCad or graph paper.

## Four descriptions of one component

A schematic symbol describes electrical function and pin connections. A footprint describes copper pads, holes, outlines, and assembly clearances on the board. A manufacturer part number identifies an actual component with dimensions and ratings. A 3D model helps inspect shape and fit. These descriptions must agree, but none automatically proves the others correct.

For example, a two-pin connector symbol might connect pin 1 to SUPPLY and pin 2 to GND. If its footprint numbering is reversed relative to the real connector, an electrically tidy schematic can become a reversed power connection. A plausible 3D rendering may still use the wrong pin assignment. Check the manufacturer's drawing, including whether a view looks from the mating face or the solder side.

Record the selected part number, footprint, voltage or power rating, and relevant datasheet in the bill of materials, BOM. A description such as “10 kΩ resistor” is enough for an early circuit calculation but incomplete for assembly: tolerance, package, lead spacing, and power rating still matter. Save custom symbols and footprints with the project so another computer can reproduce it.

## A PCB still has a complete circuit

A trace is a shaped copper conductor. A pad provides a soldering or connection surface. A via connects copper between layers through a plated hole. A copper zone fills a region connected to a named net, often ground. The **stackup** specifies the sequence and thickness of copper and insulating layers. These physical choices affect resistance, capacitance, inductance, heat flow, and manufacturability.

Current that leaves a source must return. For slowly changing DC, resistance strongly shapes how return current divides between available paths. For rapidly changing signals, inductance matters, and a nearby continuous reference plane provides a compact return path. Cutting a slot through that plane beneath a signal can force the return to take a detour, enlarging the loop. A slow repetition rate does not guarantee a slow electrical edge: a digital signal toggling only occasionally may still change voltage very quickly.

Place circuits with their current paths in mind. Keep sensitive sensor connections away from noisy switching loops, and put decoupling connections close to the relevant supply and ground pins. Avoid assuming that splitting a ground plane automatically separates noise; the return still needs to get home. Analog Devices' [mixed-signal layout guidance](https://www.analog.com/en/resources/analog-dialogue/articles/what-are-the-basic-guidelines-for-layout-design-of-mixed-signal-pcbs.html) explains placement, layering, and ground-plane tradeoffs. A component's reference layout is often a useful starting constraint, especially for switching power supplies.

Our first resistor-divider board is deliberately forgiving. Its currents are small and its signal changes slowly. That makes it a good place to learn connectivity and assembly, but it does not validate the same layout habits for a radio, motor driver, or fast ADC.

## Checks answer different questions

Electrical rules checking, ERC, examines schematic relationships such as incompatible pin types and unconnected pins. Design rules checking, DRC, examines layout constraints such as copper clearance, track width, and unconnected nets. Both depend on the rules and component definitions you supplied. Neither knows that you selected the wrong sensor, reversed a physical connector, or calculated an unsuitable resistor.

Use the intended manufacturer's capabilities to set minimum trace widths, spacings, hole sizes, and copper-to-edge clearance. Minimum manufacturable geometry is not necessarily good engineering geometry: wider traces can reduce resistance, larger clearances can simplify assembly, and accessible test points can save hours later. Voltage, current, temperature, frequency, and assembly method determine what else is needed. There is no universal “safe PCB default” covering every application.

KiCad's [getting-started guide](https://docs.kicad.org/10.0/en/getting_started_in_kicad/getting_started_in_kicad.html) walks through schematic capture, footprint assignment, board layout, and fabrication outputs. The interface examples currently document version 10; match the documentation to your installed version. Use the [PCB editor manual](https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html) when you need the exact meaning of a rule or output setting.

## Lab: move the known divider onto a board

Use the 3.0 V, two-10 kΩ divider from [DC circuits](../circuits/). It has three nets: SUPPLY, MID, and GND. This exercise ends with a reviewed design and full-size paper fit check. It does not require a manufactured board or a new powered experiment.

1. Create a project called `divider_rev_a`. Place two resistor symbols, R1 and R2, and two two-pin connector symbols, J1 and J2. Connect J1 pin 1 to SUPPLY, R1 between SUPPLY and MID, R2 between MID and GND, and J1 pin 2 to GND. Connect J2 pin 1 to MID and J2 pin 2 to GND. Label the nets and add text stating “3.0 V input; signal output; not a regulated power supply.”
2. Add accessible test points for SUPPLY, MID, and GND. Predict the three voltages relative to GND: 3.0 V, 1.5 V, and 0 V. Predict 150 µA source current. This preserves the circuit's acceptance criteria before layout begins.
3. Select real or measured example parts. For a paper prototype, choose through-hole resistors with 7.62 mm lead spacing and headers with 2.54 mm pitch, then assign matching footprints. These dimensions are exercise choices, not a guarantee that parts in your drawer match. Inspect pad numbering and record dimensions on the BOM.
4. Run ERC and investigate each message. An externally powered connector may require an explicit indication that its net is driven; add that only after explaining where the actual power comes from. Do not suppress a warning simply to make the count zero.
5. Transfer the schematic connectivity into the PCB editor. Draw a closed 30 × 20 mm board outline on Edge.Cuts. Place the input connector at one edge and output at the opposite edge. Put resistors and test points where probes can reach them without touching adjacent conductors.
6. Route the connections on a two-layer board. For this practice layout, use generous 0.5 mm signal tracks and 0.5 mm spacing where practical; these are low-density exercise choices, not universal fabrication rules. If you add a GND zone, refill it and confirm that intended ground pads actually connect. Inspect any isolated copper islands.
7. Run DRC. Then independently highlight each net and compare it with the three-node circuit. Inspect both copper layers and the 3D view. A zero-error report is one checkpoint; the node-by-node comparison answers a different question.
8. Print at 1:1 scale with page fitting disabled. Verify a known dimension with a ruler: ten 2.54 mm pin intervals span 25.4 mm. Set the actual unpowered components on the print and check body clearance, connector access, and orientation. If the scale is wrong, the fit experiment is invalid even if the parts seem close.

On graph paper, do the same experiment at a stated scale, drawing pads and connections on two differently colored layers. This route teaches connectivity, fit, and assembly access while postponing software learning.

**Expected result:** the board layout implements exactly the divider already analyzed, with a probe-accessible midpoint and visible connector labels. Common faults include a symbol pin connected to the wrong footprint pad, a resistor assigned incompatible lead spacing, an open board outline, and a ground zone that looks filled but is disconnected. Diagnose these against the schematic, dimension drawing, and net highlighting rather than moving tracks randomly. This is a proposed lab; no board from it has been fabricated or tested for this handbook.

## A fabrication package needs its own review

Manufacturers commonly accept Gerber layer files and drill files, or another explicitly supported manufacturing format. Export only the intended board revision, open the exported files in an independent viewer, and inspect copper, solder-mask openings, silkscreen, outline, and holes. Check units, layer assignment, finished dimensions, and whether drill information is present. A correct source project does not guarantee a correct export selection.

Keep the source files, BOM, assembly notes, fabrication outputs, and a short review record together. Mark the board revision on copper or silkscreen where it remains readable after assembly. Before ordering, select exact components and confirm the manufacturer's rules; the paper exercise's generic parts are not an order-ready BOM.

When you later assemble a low-voltage prototype, learn soldering with suitable ventilation, eye protection, and a supported hot iron. Inspect joints and polarity with power disconnected. Check for shorts, then bring up the supply with an appropriate current limit and compare measured rail voltages and current against predictions before adding expensive modules. A regulator output at the wrong voltage is easier to fix before it powers a microcontroller. Do not use this beginner workflow for mains-connected boards or lithium battery-pack construction.

## What is happening inside the black package?

Semiconductors allow material structure and electric fields to control conduction. Doping changes the available charge carriers in regions of silicon. A junction between differently doped regions produces a diode whose current depends strongly and nonlinearly on applied voltage. It does not behave like a resistor with one fixed resistance. Forward drop, reverse voltage, leakage, current, and temperature all matter.

A transistor adds control. A bipolar transistor uses current into its base as part of controlling collector current. A MOSFET uses the electric field from an insulated gate to control a channel between source and drain. Its gate draws little steady DC current ideally, but switching requires charging and discharging capacitance. Fast switching can therefore require substantial brief drive current.

For an N-channel low-side switch, the source is commonly at GND and the load sits between the positive supply and drain. The relevant control voltage is gate relative to source. A gate pull-down gives an intentional off state while the controller is disconnected or starting. Real designs must also address gate drive, losses, transients, and the load's stored energy.

Do not choose a MOSFET solely because its threshold voltage is below 3.3 V. Threshold identifies the onset of conduction under a specified small-current test; it does not establish a low on-resistance at your load. Find `RDS(on)` specified at an available gate-source voltage, then check current, temperature, and thermal conditions. [Nexperia's MOSFET datasheet guide](https://assets.nexperia.com/documents/application-note/AN11158.pdf) explains these parameters. For an illustrative 0.050 Ω on-resistance carrying 0.20 A, conduction loss is `I²R = 0.002 W`; at 2 A it becomes 0.20 W. Switching losses and changing resistance with temperature are additional terms.

## Logic gates turn electrical behavior into rules

Digital circuits assign voltage ranges to logic zero and one. They require margins between a guaranteed output level and the next input's threshold. “Digital” does not mean voltage is irrelevant or that 5 V can safely enter a 3.3 V pin.

A NAND gate outputs zero only when both inputs are one:

| A | B | NAND output |
| --- | --- | --- |
| 0 | 0 | 1 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

Tie its two inputs together and the output becomes the inverse of that input. Combining gates makes arithmetic and decision circuits. Adding storage elements such as flip-flops gives a circuit state that persists between clock events. CMOS logic commonly combines complementary transistor arrangements; switching charges internal and external capacitances, which is one reason activity and clock rate influence power consumption.

The free self-study materials in [Nand to Tetris](https://www.nand2tetris.org/) build from logic toward a simulated computer. Start with its first gate project and test every truth-table row. It teaches the digital abstraction; it does not replace transistor physics, analog design, or PCB layout.

## Choose a next layer deliberately

**Predict:** Does DRC detect an incorrect sensor conversion equation? Does a low MOSFET threshold guarantee low heating at your gate voltage? Is an FPGA just a faster microcontroller?

**Answers:** DRC checks specified layout rules, not application meaning; on-resistance and thermal conditions still need checking; an FPGA configures hardware logic and connections that can operate concurrently, while a microcontroller executes instructions on its processor. Both can contain sophisticated timing and software interactions, but their design models differ.

For an independent challenge, add a connector and mounting arrangement for your chosen low-voltage sensor module to the paper PCB. Define every interface pin, probe point, and mechanical clearance. Ask another person to identify power polarity and the expected midpoint voltage using only your package.

If chip design itself becomes interesting, follow [Tiny Tapeout's learning material](https://tinytapeout.com/) through logic simulation and its semiconductor exercises before considering fabrication. Custom integrated circuits add process-specific device models, physical layout rules, verification, and manufacturing constraints. Learning and simulation can begin online; submitting silicon involves separate current program requirements and costs. Treat that as a later project with its own review, not a necessary purchase for learning electronics.
