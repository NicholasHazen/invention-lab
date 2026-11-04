# The Invention Lab Handbook

Twenty original teaching chapters connect foundations to practical projects. The collection includes worked examples, proposed low-energy bench experiments, runnable desktop labs, prediction checks, diagnostics, and independent capstone briefs. It complements the separate triangulated pivot case study and preserves its geometry and interactive viewer.

## Read and use

- Public edition: https://nicholashazen.github.io/invention-lab/handbook/
- Choose a learning path before assuming chapter numbering is a mandatory sequence. Embedded systems builds on the software chapter even though it appears earlier in the topic grouping.
- Use the library to choose one relevant resource, then do its first useful task. Recommendations are based on official contents, syllabi, or documentation review, not claims of personal course completion.
- Open `docs/handbook/print.html` for continuous reading and browser printing.
- Extract the offline ZIP completely before opening its `index.html`. External courses and the separate pivot project remain online links; all handbook text, diagrams, tools, examples and worksheets are included.

## Authoring and build

Sources:

- `curriculum.json`: chapter metadata, prerequisites and learning paths.
- `chapters/`: original Markdown prose.
- `research/`: annotated primary-source resource records with access, prerequisites, first task, limitations and verification evidence.
- `assets/`: original SVG teaching figures.
- `examples/`: original teaching programs and synthetic inputs; read the README in each folder.
- `worksheets/`: editable project and experiment templates.
- `tools/`: dependency-free browser calculators; these are educational models, not engineering ratings.
- `web/`: shared site presentation and behavior.

From the repository root, use Node.js 20 or newer and Python 3.10 or newer:

```sh
npm ci --ignore-scripts
node scripts/build_handbook.mjs
python3 scripts/package_handbook.py
python3 scripts/validate_handbook.py
python3 -m http.server 8000 --directory docs
```

Open `http://localhost:8000/handbook/`. The generated website requires no server-side application, package installation, CDN or analytics. The renderer can also use `HANDBOOK_MARKED_MODULE` pointing to a local `marked.esm.js` installation.

After a chapter or asset edit, rebuild and repackage before validation. `build_handbook.mjs` owns the handbook outputs and copies the tools; it preserves downloads so `package_handbook.py` can replace the archive after the build. It does not modify the hub or pivot guide. The package script rewrites links leaving the handbook to the public site for the offline archive and records file hashes.

## Validation and evidence

Run desktop examples exactly as their READMEs specify. Computing examples have nine behavioral tests; the circuit, sampling and debounce labs have their own checks. The optional Pico adaptation has not been exercised on a physical board. Simulated values are labeled and do not establish mechanical, electrical or real-time hardware performance.

The static validator checks local files/anchors, duplicate IDs, image alternatives, resource schema, prerequisite closure, Python syntax and accidental workstation/cache artifacts. Browser checks also cover mobile and keyboard navigation, resource filters, no-JavaScript reading, calculators, print layout, archive integrity and offline path resolution. Direct `file://` browser execution was not tested because the review browser prohibits that URL scheme; the site runtime was checked through the permitted local HTTP preview. These checks complement technical and teaching review; word counts alone do not establish curriculum quality.

When adding a resource, open its primary page, record what was actually verified, state access limits, and give the learner one specific starting action. Use `access_group` (`free`, `mixed`, `paid`, `check`) for filtering; keep the fuller `access` description. Do not infer price or course enrollment from a free landing page. When updating examples, retain the distinction between a model, a proposed physical experiment and a performed test.

For a new release, update the curriculum revision, rebuild, package, validate and publish a matching `handbook-vX.Y` GitHub release. Existing pivot releases remain separate.
