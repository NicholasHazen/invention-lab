# Add or update a project

## Add a guide

1. Choose a permanent, lowercase, hyphenated project slug.
2. Create `docs/projects/<slug>/index.html` and keep the project's images and downloads alongside it in subfolders.
3. Add a project entry on `docs/index.html`. Use an actual project image, a short description, and a relative link such as `projects/<slug>/`.
4. Link from the guide back to the hub with `../../`. Use relative links for the guide's own assets so the site works under `/invention-lab/`.
5. Preview desktop and mobile layouts, check heading and keyboard navigation, and verify every linked download exists. Check any downloadable archives as well as visible page text for local machine paths or authoring-only files.
6. Commit and push to `main`. GitHub Pages publishes the updated `docs/` directory. Check the deployment result and the live project URL.

Keep drafts, credentials, machine-specific build state, and old working copies outside `docs/`. Publish only files deliberately included for readers.

## Version downloads

Create a GitHub Release for a complete offline bundle. Prefix tags with the project slug, for example `triangulated-pivot-v4.2`, so multiple projects can release independently in this repository.

Keep download links pinned to the matching version. Verify the archive contents, model counts, and checksums before publishing. If changing a published report for portability, label the derivative and update its affected hashes without implying a new physical test.

## Update the pivot guide

The prepared guide is exported by `scripts/export_guide.py`; see its command-line help for source and destination arguments. Preserve the complete relative asset layout. The authoring workflow lives separately from this static publishing repository; publishing prebuilt files does not require Fusion or a local runtime on GitHub.

Changing physical geometry requires fresh relevant checks and an explicit model revision. Editorial changes can retain the existing geometry while identifying the teaching revision separately.

## Update the handbook

The handbook has source chapters, researched resource records, original figures, examples, worksheets and browser tools in `handbook/`. See [its authoring guide](handbook/README.md). Build with `scripts/build_handbook.mjs`, package with `scripts/package_handbook.py`, then run `scripts/validate_handbook.py` and relevant example/browser checks. Keep prerequisite paths valid and preserve the distinction between illustrative calculations, executed software checks and physical observations. Use `handbook-vX.Y` tags for its independent releases.
