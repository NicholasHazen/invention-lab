# Invention Lab

Build guides for mechanical prototypes, 3D printing, and experiments.

**[Visit Invention Lab](https://nicholashazen.github.io/invention-lab/)**

## Projects

- **[Triangulated 45° pivot](https://nicholashazen.github.io/invention-lab/projects/triangulated-pivot/)** — learn Fusion, print and assemble an integrated octagonal joint, then measure its behavior. Rev4.2 teaching guide, with V4.1 geometry. Includes 52 steps, 69 figures, 15 Fusion checkpoints, 22 print meshes, and a STEP assembly.
- **[Complete pivot download](https://github.com/NicholasHazen/invention-lab/releases/tag/triangulated-pivot-v4.2.2)** — versioned offline project bundle, including six alternate-view galleries, orthographic facet comparisons, and clearer bearing cutaways.

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
