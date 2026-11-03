#!/usr/bin/env python3
"""Prepare the existing illustrated guide for public static hosting.

Usage: python3 scripts/export_guide.py --source ../tutorial-v7/publish
The original export is read-only. Geometry is copied byte for byte.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import shutil
from urllib.parse import unquote, urlsplit
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DESTINATION = ROOT / 'docs/projects/triangulated-pivot'
RELEASE = 'https://github.com/NicholasHazen/invention-lab/releases/download/triangulated-pivot-v4.2.1/triangulated-pivot-v4.2.1.zip'
TEXT_SUFFIXES = {'.json', '.md', '.html', '.csv', '.txt'}
MODELS = {'.f3d', '.stl', '.step'}
PROVENANCE = 'Public derivative: local workstation prefixes have been replaced with workspace-relative provenance paths. Historical measurements and geometry are unchanged; original evidence is retained in the authoring workspace.'


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode()


def normalize_paths(text: str) -> str:
    text = re.sub(r'/Users/[^/\s]+/Desktop/Invention/', '', text)
    text = re.sub(r'/Users/[^/\s]+/\.cache/codex-runtimes/', 'authoring-runtime/', text)
    return text


def public_text(name: str, raw: bytes) -> bytes:
    text = raw.decode('utf-8')
    normalized = normalize_paths(text)
    if text == normalized:
        return raw
    if name.endswith('.json'):
        value = json.loads(normalized)
        assert isinstance(value, dict), name
        value['public_export'] = {'note': PROVENANCE, 'source_sha256': digest(raw)}
        return json_bytes(value)
    return normalized.encode()


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        for attr in ('href', 'src'):
            if attr in attrs:
                self.links.append(attrs[attr])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True, type=Path)
    args = parser.parse_args()
    source = args.source.resolve()
    assert (source / 'index.html').is_file(), 'Select the prepared publish directory.'
    assert source != DESTINATION.resolve()
    # This directory belongs entirely to this exporter; other project folders
    # and the hub landing page are intentionally outside its scope.
    if DESTINATION.exists():
        shutil.rmtree(DESTINATION)
    shutil.copytree(source, DESTINATION)
    changes = []
    for path in sorted(DESTINATION.rglob('*')):
        if path.is_file() and path.suffix in TEXT_SUFFIXES:
            before = path.read_bytes()
            after = public_text(path.relative_to(DESTINATION).as_posix(), before)
            if before != after:
                path.write_bytes(after)
                changes.append(path.relative_to(DESTINATION).as_posix())

    # Keep the report's current-file table accurate after provenance changes.
    summary_path = DESTINATION / 'review/fdm/release-summary.json'
    summary = json.loads(summary_path.read_text())
    summary['source_file_hashes'] = dict(summary['file_hashes'])
    for name in summary['file_hashes']:
        path = DESTINATION / name
        if not path.is_file():
            path = summary_path.parent / name
        summary['file_hashes'][name] = digest(path.read_bytes())
    summary['public_export'] = {'note': PROVENANCE, 'source_sha256': digest((source / summary_path.relative_to(DESTINATION)).read_bytes())}
    summary_path.write_bytes(json_bytes(summary))
    changes.append(summary_path.relative_to(DESTINATION).as_posix())

    for path in sorted(DESTINATION.glob('review/*/geometry-continuity.json')):
        value = json.loads(path.read_text())
        value['source_validation_passed'] = value.pop('passed')
        value['public_files_match_listed_sha256'] = True
        for name, record in value['files'].items():
            current = digest((DESTINATION / name).read_bytes())
            if current != record['sha256']:
                record['source_recorded_sha256'] = record['sha256']
                record['sha256'] = current
                record['matches_v4_1'] = False
                record['public_copy_note'] = ('Learning worksheet superseded by the Rev4.2 walkthrough polish; geometry unchanged.' if name == 'load-test-log.csv' else 'Public provenance and derivative metadata only; original report hash retained.')
        value['public_export'] = {'note': PROVENANCE, 'source_sha256': digest((source / path.relative_to(DESTINATION)).read_bytes()), 'hash_scope': 'sha256 identifies the included public file. source_recorded_sha256, when present, is historical evidence, not the public file hash.'}
        path.write_bytes(json_bytes(value))
        changes.append(path.relative_to(DESTINATION).as_posix())

    html_path = DESTINATION / 'index.html'
    html = html_path.read_text()
    old = '<div class="masthead-mark"><span class="mark" aria-hidden="true"></span>Mechanical workshop</div>'
    assert html.count(old) == 1
    html = html.replace(old, '<div class="masthead-mark"><span class="mark" aria-hidden="true"></span><a href="../../">Invention Lab</a><span aria-hidden="true">/</span><span>Pivot guide</span></div>')
    anchor = '    <p class="image-help" hidden>'
    assert html.count(anchor) == 1
    html = html.replace(anchor, '    <p class="public-downloads"><a href="' + RELEASE + '">Download the complete guide and model kit</a> · <a href="#downloads-and-evidence">Browse individual downloads</a></p>\n' + anchor)
    footer = '<span>Build, measure, and compare the result.</span>'
    html = html.replace(footer, '<span>Build, measure, and compare the result. <a href="public-export-manifest.json">Public-file manifest</a></span>')
    html_path.write_text(html)
    changes.append('index.html')

    # Rebuild only archives whose text changed. Preserve native model volumes
    # exactly; each rebuilt volume gets a new, verified download manifest.
    archive_changes = {}
    for archive in sorted(DESTINATION.glob('*.zip')):
        with zipfile.ZipFile(archive) as z:
            infos = z.infolist()
            contents = {i.filename: z.read(i.filename) for i in infos}
        changed = []
        for name, raw in list(contents.items()):
            if Path(name).suffix not in TEXT_SUFFIXES or name == 'download-manifest.json':
                continue
            public_file = DESTINATION / name
            after = public_file.read_bytes() if public_file.is_file() else public_text(name, raw)
            if after != raw:
                contents[name] = after
                changed.append(name)
        if not changed:
            continue
        manifest = json.loads(contents['download-manifest.json'])
        manifest['files_sha256'] = {name: digest(raw) for name, raw in contents.items() if name != 'download-manifest.json'}
        manifest['public_export'] = {'note': PROVENANCE, 'source_archive_sha256': digest((source / archive.name).read_bytes()), 'modified_files': changed}
        contents['download-manifest.json'] = json_bytes(manifest)
        with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
            for info in infos:
                z.writestr(info, contents[info.filename])
        with zipfile.ZipFile(archive) as z:
            assert z.testzip() is None
            for name, expected in manifest['files_sha256'].items():
                assert digest(z.read(name)) == expected, name
        archive_changes[archive.name] = changed
        changes.append(archive.name)

    models = [p for p in DESTINATION.rglob('*') if p.is_file() and p.suffix in MODELS]
    for path in models:
        assert path.read_bytes() == (source / path.relative_to(DESTINATION)).read_bytes()
    counts = Counter(path.suffix for path in models)
    assert counts == {'.f3d': 15, '.stl': 22, '.step': 1}, counts
    for path in DESTINATION.rglob('*'):
        if not path.is_file():
            continue
        if path.suffix in TEXT_SUFFIXES:
            assert '/Users/' not in path.read_text(), path
        elif path.suffix == '.zip':
            with zipfile.ZipFile(path) as z:
                for name in z.namelist():
                    if Path(name).suffix in TEXT_SUFFIXES:
                        assert '/Users/' not in z.read(name).decode(), (path, name)
    manifest = {'publication': 'Invention Lab / Triangulated Pivot', 'revision': 'V4.2 teaching / V4.1 geometry', 'public_derivative': True, 'provenance_note': PROVENANCE, 'physical_print_tested': False, 'load_tested': False, 'geometry_bytes_unchanged': True, 'model_counts': dict(counts), 'modified_public_files': changes, 'rebuilt_archives': archive_changes, 'hash_scope': 'All public project files except this manifest itself.', 'files': {p.relative_to(DESTINATION).as_posix(): {'bytes': p.stat().st_size, 'sha256': digest(p.read_bytes())} for p in sorted(DESTINATION.rglob('*')) if p.is_file()}}
    (DESTINATION / 'public-export-manifest.json').write_bytes(json_bytes(manifest))
    links = Links()
    links.feed(html)
    for href in links.links:
        url = urlsplit(href)
        if url.scheme or url.netloc:
            continue
        if not url.path:
            assert not url.fragment or unquote(url.fragment) in links.ids, href
        elif url.path != '../../':
            assert (DESTINATION / unquote(url.path)).is_file(), href
    print(json.dumps({'destination': str(DESTINATION), 'model_counts': dict(counts), 'modified_public_files': changes, 'rebuilt_archives': archive_changes, 'local_link_checks': len(links.links), 'files': len(manifest['files']) + 1}, indent=2))


if __name__ == '__main__':
    main()
