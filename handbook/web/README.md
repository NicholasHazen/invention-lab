# Handbook site renderer

The handbook is a static site generated from `handbook/curriculum.json`, `handbook/chapters/*.md`, and every JSON array under `handbook/research/`. The repository's existing GitHub Pages workflow can publish the generated `docs/handbook/` tree. No service or database is required.

Run from the repository root:

```sh
node scripts/build_handbook.mjs
```

The renderer uses Marked 17.x. It first honors an absolute `HANDBOOK_MARKED_MODULE` path, then tries a local `marked` package, then the configured Codex desktop dependency bundle. To rebuild elsewhere, install `marked@17` in the checkout or provide the path to its `lib/marked.esm.js`. No browser dependencies are required for building.

The build refuses a missing or empty chapter, invalid prerequisites, or malformed research records. All twenty curriculum chapters must exist. Re-run after authoring changes or after another research file is added; the output library and resource count reflect the current files.

Outputs include the landing page, twenty chapter pages, learning paths, the resource library, a full print edition, shared CSS/JS, and a build manifest. Assets, examples, worksheets, and the separately authored tools source are merged into corresponding public folders. The build deliberately does not erase `docs/handbook/`, so separately maintained `tools/` and `downloads/` are preserved. The offline ZIP is packaged separately after the site is complete.

Local links explicitly end in `index.html`, allowing chapter navigation from both HTTP and offline `file://` pages. The print edition rewrites chapter links to namespaced anchors and adjusts asset, worksheet, example, and project paths. Resource cards remain readable with JavaScript disabled; JavaScript only adds filters, print controls, and a current-section highlight.

Chapter source is treated as Markdown, not trusted HTML. Raw HTML is escaped, attribute values are escaped, and unsafe URL protocols are rejected. Research metadata is rendered as text. External citations remain inline; exact cited resource URLs also connect chapters to annotated resource cards.

CSS follows the existing cream/teal hub palette and Georgia headings. Chapter pages provide a curriculum sidebar, an on-page contents list, prerequisites, and previous/next links. At smaller widths, native disclosure controls retain access to navigation. Tables and code blocks can scroll without widening the document.

For QA, check representative desktop/mobile pages, keyboard focus, library filters and reset, no-JavaScript content, print link targets, and local-file navigation. Do not infer physical prototype validation from a successful site build.
