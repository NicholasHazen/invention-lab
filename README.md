# Invention Lab

A maker handbook and build guides for understanding, fabricating, measuring, and improving useful systems.

**[Visit Invention Lab](https://nicholashazen.github.io/invention-lab/)**

## Handbook

**[The Invention Lab Handbook](https://nicholashazen.github.io/invention-lab/handbook/)** includes 20 chapters on math/physics, measurement, product design, CAD/CAM, materials, 3D printing, mechanics, electronics, embedded systems, PCBs/microelectronics, software, controls, robotics, AI and connected devices. Worked examples lead into low-energy bench or desktop labs, diagnostics, prediction checks and independent projects.

Use the [learning paths](https://nicholashazen.github.io/invention-lab/handbook/paths/) to choose a sequence and the [annotated library](https://nicholashazen.github.io/invention-lab/handbook/library/) to find primary-source courses, books and videos. Recommendations record prerequisites, access, starting tasks, limitations and the date checked. The handbook includes original figures, interactive workbench tools, downloadable code and worksheets, a print edition and an offline archive.

Authoring sources live in `handbook/`; `scripts/build_handbook.mjs` generates the static pages. See `handbook/README.md` for reproduction and validation. Physical labs are proposed experiments unless explicitly identified as observed; desktop model results are not physical validation.

## Projects

- **[Triangulated 45° pivot](https://nicholashazen.github.io/invention-lab/projects/triangulated-pivot/)** — learn Fusion, print and assemble an integrated octagonal joint, then measure its behavior. Rev4.2 teaching guide, with V4.1 geometry. Includes 52 steps, 69 figures, 15 Fusion checkpoints, 22 print meshes, and a STEP assembly.
- **[Complete pivot download](https://github.com/NicholasHazen/invention-lab/releases/tag/triangulated-pivot-v4.2.3)** — versioned offline project bundle, including an offline-capable 3D assembly viewer with individual part visibility, six alternate-view galleries, and orthographic comparisons.

The pivot is an experimental design. Its supplied geometry has digital checks; a physical print, assembly, or load-capacity validation has not been established. Follow the guide's fit trials and measurement procedure.

## Website layout

```text
docs/
  index.html                         # Shared project hub
  assets/                            # Shared presentation assets
  projects/
    triangulated-pivot/
      index.html                     # Guide and relative downloads
      images/
      checkpoints/
      print-files/
scripts/
  export_guide.py                     # Public export from the prepared guide
```

GitHub Pages serves `docs/` on the `main` branch. `.nojekyll` keeps the files as ordinary static HTML. Updating this folder and pushing to `main` publishes the next site revision automatically. The website needs no server, package installation, or external script service.

For a local preview, run `python3 -m http.server 8000 --directory docs` and open `http://localhost:8000/`.

## Adding another project

See [CONTRIBUTING.md](CONTRIBUTING.md) for the folder, links, preview, and release conventions. Existing project paths should remain stable when titles or revisions change.

## Public evidence copies

The published pivot reports label any normalized provenance paths and record hashes of the public files. The original engineering evidence is preserved separately. Geometry files retain their source bytes; rewriting a provenance path is not a new engineering test.
