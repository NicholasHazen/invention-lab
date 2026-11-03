#!/usr/bin/env python3
"""Package the public pivot guide and all its downloads for an offline release."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / 'docs/projects/triangulated-pivot'
OUTPUT = ROOT / 'dist'
HUB = 'https://nicholashazen.github.io/invention-lab/'


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    OUTPUT.mkdir(exist_ok=True)
    files = {p.relative_to(PROJECT).as_posix(): p.read_bytes()
             for p in sorted(PROJECT.rglob('*')) if p.is_file()}
    published_manifest = json.loads(files['public-export-manifest.json'])
    for name, record in published_manifest['files'].items():
        assert digest(files[name]) == record['sha256'], name
    # Keep hub navigation useful when the guide is opened from the extracted ZIP.
    files['index.html'] = files['index.html'].replace(b'href="../../"', f'href="{HUB}"'.encode())
    files['README.txt'] = (
        'Invention Lab — Triangulated Pivot, Rev4.2\n\n'
        'Extract this entire archive, then open index.html in a browser. Keep the\n'
        'folders together: the figures, worksheets and individual model downloads\n'
        'work offline. The Invention Lab home and release links open the online site.\n\n'
        'The archive includes 15 editable Fusion checkpoints, 22 print meshes and\n'
        'one STEP exchange assembly. The numbered ZIP volumes are also included\n'
        'for convenience; their files are already extracted here.\n\n'
        'The guide teaches modeling, printing, assembly and measurement. It retains\n'
        'V4.1 geometry. No physical print, assembly or load rating is established.\n'
        'Start with the fit trials and follow the guide before printing housings.\n\n'
        'Public report copies normalize workstation provenance paths and identify\n'
        'their original evidence hashes. Native geometry bytes are unchanged.\n'
    ).encode()
    manifest = dict(published_manifest)
    manifest['archive_note'] = 'Offline derivative: the hub link in index.html is absolute; README.txt is added. All included file hashes below describe this archive.'
    manifest['published_index_sha256'] = published_manifest['files']['index.html']['sha256']
    manifest['files'] = {name: {'bytes': len(raw), 'sha256': digest(raw)}
                         for name, raw in sorted(files.items()) if name != 'public-export-manifest.json'}
    files['public-export-manifest.json'] = (json.dumps(manifest, indent=2) + '\n').encode()
    destination = OUTPUT / 'triangulated-pivot-v4.2.zip'
    with zipfile.ZipFile(destination, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, raw in files.items():
            archive.writestr(name, raw)
    with zipfile.ZipFile(destination) as archive:
        assert archive.testzip() is None
        for name, record in manifest['files'].items():
            assert digest(archive.read(name)) == record['sha256'], name
    sha = digest(destination.read_bytes())
    (OUTPUT / 'SHA256SUMS.txt').write_text(f'{sha}  {destination.name}\n')
    print(json.dumps({'archive': str(destination), 'bytes': destination.stat().st_size,
                      'files': len(files), 'sha256': sha}, indent=2))


if __name__ == '__main__':
    main()
