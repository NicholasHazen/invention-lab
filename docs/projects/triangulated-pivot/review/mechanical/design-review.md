# Independent mechanical review: integrated V4

Review scope: the approved 150 mm across-flats, 260 mm straight assembly, with integrated lattice housings and the retained metal-shaft core. This is a geometry and assembly review. It does not establish physical strength, fatigue life, bearing fits or printer performance. Native results belong in `native-mechanics-validation.json`; a proposed route is not a passed check until that report records it.

## Load path and member topology

The eight facets now share continuous corner rails. Each neighboring pair of triangular openings is offset 4 mm from a shared construction diagonal, leaving a nominal 8 mm in-plane brace. The radial shell/brace thickness is separately controlled at 4.5 mm. Corner rails join the side members to the solid distal rim and the joint-side frame; deep spokes connect that frame to the central bearing or hub carrier.

Triangulation provides an intentional path for forces through member intersections. The printed nodes are rigid and the member sections are plate-like, so this structure also develops bending. It is not the ideal pin-jointed, node-loaded truss used in elementary statics. [University of Alberta: Analysis of trusses](https://engcourses-uofa.ca/books/statics/structural-analysis/analysis-of-trusses/)

The default layout has 24 triangular openings per housing. A0's node fractions are 0, 0, 2/3, 5/6, 1, 1; B90 reverses its alternating side order. These are deliberate access-driven topology choices. Changing a width parameter does not create additional diagonal features automatically.

The 18 mm spokes do not have that full depth everywhere after bearing, collar and hub access cuts. In particular, B's central side openings remove part of the rear spoke-root region. Keep the final section visible when explaining the load path; do not infer capacity from the nominal `spokeDepth` alone.

## Retained core stack

| Item | Nominal q interval, mm |
| --- | --- |
| Front608 | 0.5…7.5 |
| A seat plus shoulder | 0.5…10.6 |
| Three metal support spacers | 10.6…22.6 |
| Rear holder D | 22.6…32.8 |
| Rear608 | 25.6…32.6 |
| Rear cap E | 32.8…35.8 |
| Metal shaft | −24…36 |
| Front collar | −12.5…−3.5 |
| Inner collar | 11.5…20.5 |
| F flange | −29…−23 |
| F pilot | −23…−21 |
| Hub body and front pilot envelope | −23…−13 |

The bearing centers are nominally q = 4.0 and 29.1 mm, a 25.1 mm separation. The rear seat has 0.2 mm nominal axial allowance and the front seat 0.1 mm; actual bearing and print fits control the physical result. The two bearings should align rather than being forced into alignment by tightening the three support screws.

A's carrier is 52 mm outside diameter. Preserve the 46 mm rear relief beginning at q = 10.6. Without that relief, a deep solid carrier would occupy the posts, collar and rear-holder region. C/D/E remain 44 mm outside diameter; enlarging the housing must not silently scale the shaft, bearing seats, support circle or collar stack.

## Access changes derived from actual tool paths

Rear M3 screw axes parallel q exit A's +Y wall at these outer-face coordinates:

| Axis | X, mm | Z, mm |
| --- | --- | --- |
| 1 | 75.000 | +17.000 |
| 2 | 95.821 | −8.500 |
| 3 | 54.179 | −8.500 |

The original uniform A0 chain put a diagonal across the first route. Moving its intermediate rail nodes to fractions 2/3 and 5/6 preserves all four triangular features. A Ø6 cylindrical approach, including its oblique passage through both wall faces, has conservative clearances of 2.079, 7.046 and 5.381 mm to the straight 4 mm-inset triangle edges. The smallest construction-triangle inradius is 11.505 mm, leaving 7.505 mm after the inset, so the 1.5 mm aperture rounds have geometric room. Native tool intersections still control the release.

A's two collar routes at q = 16, u = ±6.5 run along +Z. Their Ø6 design corridors fit A90's first opening with 2 mm minimum straight-edge clearance. The retained bulkhead bores clear intervening plastic closer to the collar.

B's positive-Z hub-pinch route at q = −19, u = +6.41055 crossed the original B90 diagonal. Reversing B90's chain to R0,L0,R0.5,L1,R1 retains three openings and moves the route into the first. Its Ø8 design envelope has 4 mm clearance to the leading edge, 1.098 mm to the straight rail edge and 31.946 mm to the diagonal. The closest rail point is away from the rounded corners. The opposite-Z pinch route already clears B270's first opening.

The four outer M4 routes exit B's −Y facet at X = −43 or −107 mm and Z = ±22.627 mm. They require local access scallops next to the shared corner rails. The intended passage is Ø5 for a bare 3 mm hex-key shaft, not a large socket bit. The native validation uses a Ø4 tool envelope; the hex key's across-corners size is approximately 3.464 mm.

Each reinforcing pad is a 12 mm-wide center-to-center slot, with its two centers separated by 6.5 mm along +X, extruded 6.5 mm inward from the −Y facet. A straight circular pad at the outer port would not follow the angled q-axis tool: its center shifts +6.5 mm in X across that radial depth. The capsule spans the complete corridor without enlarging the outer housing envelope. Inspect the final unions around the neighboring diagonal and corner rail instead of treating a round hole as automatically harmless.

The front collar is set before B is attached. The four inner hub-to-F screws are tightened on the bench before that subassembly enters B. Their final in-place access is optional and must not be confused with the required outer attachment and pinch-screw routes.

## Two-stage insertion contract

D and E can retain their q orientation while entering through A's open +X end. Their staging center lies on q = 60, u = v = 0, or X = Y = 42.426 mm. Enter at that constant Y and Z, move along −X until centered on q, then slide along −q to the seat. D's frontmost surface at staging is q = 54.9, beyond the shaft tail at q = 36; lateral entry therefore does not have to pass a closed ring through the shaft. Install the long support screws after D/E are seated.

For the axial stage, conservative annular swept envelopes are:

| Part | q extent, mm | Outer radius | Inner radius |
| --- | --- | --- | --- |
| D with rear608 | 22.6…65.1 | 22 mm | 4 mm |
| E | 32.8…61.5 | 22 mm | 9.75 mm |

F enters B before A/B are mated. Keep its q orientation and use a staging reference at q = −50, X = Y = −35.355 mm. Enter through the −X end at that constant Y, then move +q by 25 mm to the nominal F pose. Preassemble the hub, sleeves and four inner hub-to-F screws on the bench. Load B's four plain M4 nuts through its diagonal face. Preload the four outer M4 × 30 screws and 9 mm washers loosely into F: their 7 mm heads cannot pass through the 5 mm tool passages afterward.

The native insertion check includes the four outer shanks, heads and washers, for 15 projection envelopes and 15 continuous axial envelopes altogether. At staging, the outer screw tips reach q = −25, 2 mm behind B's q = −23 rear face. The flange governs the end-entry bore margin at 5.446 mm, or 3.446 mm after allowing for the pads' extra 2 mm inward projection. All axial envelopes clear the native B body. The final nominal screw intervals are shank −30…0, head −34…−30 and washer −30…−29 mm.

Thread engagement is an assembly operation, not a clear-cylinder motion. Keep the outer screws free to slide back as their tips encounter the preloaded nuts, guide F's pilot, start all four threads without force, and tighten evenly. Do not force a fully protruding screw through a nut as though the nut's thread were the modeled clearance bore.

These are clear-part paths, not a simulation of fingers, pliers, adhesive tape or flexible retention. Test the handling sequence with the printed parts before committing to the complete final assembly.

## Printing constraints

With the diagonal joint face down, longitudinal X rails are already 45° to the bed. On the ±Y facets, adding any cross-facet Z component makes a diagonal shallower than 45°. For a facet at angle θ and member displacement (ΔX,Δs), its build rise is `(ΔX−sin(θ)*Δs)/sqrt(2)`. Its bed-plane run is the square root of `ΔX²+Δs²−rise²`. A triangle drawn on a face is not by itself evidence of a self-supporting roof.

A0's two short late diagonals and its distal roof require explicit slice/trial review. The ±Y distal edge at constant X is also constant q, making a flat bridge at the end rim. The print review includes these actual roofs and a shallow A90 brace. Use removable support where the reviewed slice requires it, and confirm that the support can be extracted through the openings. Orientation and printer/material-specific fit trials remain part of the design process. [Prusa: Modeling with 3D printing in mind](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135)

The unrotated q-down hull is approximately 250.52×150×144.46 mm before support/brim. The print agent's 45° bed-yaw packing study reduces the in-plane bounding rectangle to approximately 230.18 mm square; that study and the actual deposited paths, including support, determine whether the selected X1C profile fits. The nominal machine build volume is 256 mm per axis. [Bambu Lab X1C specifications](https://public-cdn.bambulab.com/store/X1-Carbon%20tech%20specs.pdf)

Support removal has geometric access but remains a physical trial. A's bearing pocket opens directly at the joint face (22.2 mm mouth, 7.1 mm depth), with a separate 46 mm rear relief. B's four 7.2 mm across-flats nut pockets are 4 mm deep and open at the same face; its 50.3 mm cup and side openings are accessible. The distal roofs can be reached through the 141 mm end bore and the lattice. No sealed support cavity was identified. Interface fragments at the bearing shoulder or nut flats, and support branches that loop around braces, are still practical risks that the matching trials must resolve.

## Full-housing fixtures and load cases

The supported fixture set has three unique parts: two 148/140.6/116 mm across-flats end backers, two 8×40×6 mm flat shoes and one 45° setup block. The pilot is 10 mm deep and supports the solid end rim at |X| = 120…130 mm. Clamp at X = +125 mm; load the opposed B cord ports at X = −125 mm. Local backer cord axes are at Z = 9 mm, and the open slot floor is Z = 6.5 mm.

The vise must open at least 162 mm for the 150 mm housing and two 6 mm shoes, plus any lining and insertion clearance. Each 8×40 mm shoe occupies about 34×34 mm of jaw-face area in the 45° setup. Verify the actual jaw faces support those contacts.

Case 1 uses q horizontal and a centered vertical force perpendicular to q, producing transverse force plus bending. Case 2 uses q vertical, producing axial force plus an overturning moment. The nominal horizontal center-to-load-line arm is 125/√2 = 88.388 mm in both straight-pose arrangements. Measure the actual hanging line and use that value. At 250 g added mass, the nominal added moment is 0.21677 N·m; it is an experimental increment, not a load rating. Fixture seating, cord symmetry and slip observations belong in every test record.

The compact-core plate/bar arrangement is excluded from this integrated-housing release. The full-housing result includes the frame, pivot and workholding. Native interference checks, healthy CAD features and manifold meshes do not demonstrate physical capacity.

## Recorded native checks

The final `native-mechanics-validation.json` records 11 clear required driver routes, four correct +X capsule centerlines with 384 successful solid-material probes, clear conservative D/E/F insertion bounds including preloaded outer M4 fasteners, and no interference at seven nominal poses from 0° through 180°. Both end backers, the two clamp shoes and the Ø3 cord envelopes clear their intended native housing geometry. Two optional inner hub-screw approaches are blocked after installation; the guide therefore requires bench preassembly. Sampled motion is not a continuous swept-volume proof, and none of these checks is a physical print or load test.
