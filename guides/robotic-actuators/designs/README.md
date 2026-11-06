# Actuator layout studies

These downloads accompany Chapters 5–7 of the robotic-actuators guide. They teach packaging, load paths, motion envelopes and Fusion modeling decisions. **They are not fabrication-ready assemblies or rated hardware.** Do not print an envelope and assume that it contains the required fits, holes, retention or manufacturing geometry.

## What each format contains

| Format | Intended use | Important limit |
| --- | --- | --- |
| `*-envelopes.f3d` | Open named components and editable sketch/extrude features in Fusion | Component placements are fixed snapshots. Reference user parameters do not regenerate the whole assembly; rectangular footprints are fixed, and no complete motion/joint assembly is supplied. |
| `*-envelopes.step` | Exchange and inspect solid component envelopes in other CAD tools | STEP does not contain the native modeling history or design constraints. |
| `*-fusion.png` | Actual Fusion perspective export of each envelope assembly | It shows reserved volumes, not a finished manufactured mechanism. |
| `*-front.dxf`, `*-axial.dxf`, `*-plan.dxf`, `*-end.dxf` | Import millimetre line/circle layout references | Fusion generally imports fixed sketch geometry. Rebuild the small native constrained skeleton described in the chapter to learn design intent. |
| `*-parameters.csv` | Read/copy the named study inputs | Human-readable table, not Fusion's specific CSV parameter-import schema. |
| `*-layout.json` | Reproduce the nominal layout and review assumptions | This contains study inputs rather than a selected-hardware bill of materials. |

All coordinates and DXF geometry use millimetres. Angular parameters are explicitly marked in degrees. `layout-checks.json` records numerical consistency, and `fusion-export-checks.json` records native feature-health and solid-body checks.

The manual Fusion recipes intentionally go beyond these envelope files: constrain the governing sketches; associate feature positions to those sketches; add joints and travel; select purchased components; then model fits, fasteners, service access and printable details. The supplied models are a visual starting point and a comparison reference, not evidence that all those steps have been completed.

## Study-specific omissions

- **Belt joint:** 20T/60T cylinders are pitch envelopes, not tooth profiles. The 200 mm pitch-length belt is a candidate layout input, not a verified SKU. The motor and its bracket are generic envelopes. Real pulley hubs, bearings, shaft retention, torque-transfer interfaces, belt installation/tensioning range, fasteners and guards need selection. There is no solid belt model. Overlapping housing/foot/base envelopes indicate intended structural connections that must become properly joined or fastened parts.
- **Screw stage:** the screw and nut have no threads. A sleeve and end-cap envelope show a positive nut-to-carriage load path; the real nut mount must follow the selected nut design. Fixed/floating support envelopes are not selected thrust bearings. The screw projects 10 mm into the coupling; the generic motor shaft leaves 1 mm between shaft ends. Coupling bores and clamp engagement remain to be specified. The motor body is a generic 32 mm square; no motor model or mounting standard is implied. Rail/block clearances and permissible moments remain unknown.
- **Tendon finger:** circles/cylinders describe effective tendon radii. The final groove, cord diameter, tendon anchor and wrap, selected hinge/spool bearings, return spring and motor connection are absent. Station legs and a side plate connect support/stop envelopes to the base. The simple finger rectangle gives nominal stop contact at 0° and 60°; stops must be rechecked against any changed finger outline. There is no tendon-contact or spring simulation. Finger arm and sector are separate overlapping envelopes that represent one eventual moving part.

No materials have been assigned to establish engineering mass properties. The guide's 0.25 kg payload and 0.08 kg arm are independent study inputs, not measured or computed masses of these CAD envelopes. Do not use their default appearance/material to infer torque, strength, stiffness, thermal performance or print mass.

## Regenerate the references

Run `python3 generate_layouts.py` with Python 3. It uses only the standard library and writes layout JSON, CSV, DXF and the six original SVG diagrams beside this guide. It also reports the exact ideal belt-centre solution. The script resolves paths relative to its own location. Keep it inside the supplied `designs` directory, with a sibling `assets` directory available.

For native models, keep `fusion_build_studies.py` and the three layout JSON files together. Run it as a Python script through Fusion's Scripts and Add-Ins interface. `OUTPUT_DIR` defaults to the script's directory; change it explicitly if you copy the script into another Fusion script folder. It creates three new temporary documents, exports F3D/STEP/PNG files, checks feature health and solid volumes, closes only its own temporary documents, and restores the previously active document. Existing user documents are neither saved nor modified. Existing study export files in the output directory are overwritten.

The native generator is an envelope builder, not a replacement for working through the constrained modeling exercises. It is specific to Fusion's API and cannot run as ordinary system Python. These exports were generated in Fusion on 2026-11-06. No printed assembly, powered motion, fit, load capacity, fatigue or service-life test has been performed.
