#!/usr/bin/env python3
"""Validate the generated actuator guide and its local link graph."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import hashlib, json, xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'docs/projects/robotic-actuators'

class Document(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]; self.ids=set(); self.duplicates=[]; self.images=[]; self.h1=0; self.videos=[]; self.frames=[]; self.tracks=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if 'id' in a:
            if a['id'] in self.ids:self.duplicates.append(a['id'])
            self.ids.add(a['id'])
        if tag=='h1':self.h1+=1
        if tag=='img' and a.get('src'):self.images.append(a)
        if tag=='video':self.videos.append(a)
        if tag=='iframe':self.frames.append(a)
        if tag=='track':self.tracks.append(a)
        for key in ('href','src','poster'):
            if key in a:self.links.append(a[key])

def parse(file):
    d=Document();d.feed(file.read_text());return d

def main():
    documents={p:parse(p) for p in SITE.rglob('*.html')}
    checks=0
    for p,doc in documents.items():
        assert not doc.duplicates,(p,doc.duplicates)
        assert doc.h1==1,(p,'Expected one H1')
        for image in doc.images:assert image.get('alt','').strip(),(p,'Missing image alternative')
        for href in doc.links:
            u=urlsplit(href)
            if u.scheme or u.netloc:
                assert u.scheme in ('http','https','mailto'),href
                continue
            target=(p.parent/unquote(u.path)).resolve() if u.path else p
            if target.is_dir():target=target/'index.html'
            assert target.is_relative_to(ROOT/'docs'),(p,href,'Outside site')
            assert target.is_file(),(p,href,'Missing target')
            if u.fragment and target.suffix=='.html':
                other=documents.get(target) or parse(target)
                assert unquote(u.fragment) in other.ids,(p,href,'Missing fragment')
            checks+=1
    doc=documents[SITE/'index.html']
    assert all(f'chapter-{n:02}' in doc.ids for n in range(1,11))
    assert 'compare-types' in doc.ids and 'motion-library' in doc.ids
    assert len(doc.videos)==3 and all('controls' in v and 'autoplay' not in v for v in doc.videos)
    assert len(doc.tracks)==3 and all(t.get('kind')=='captions' for t in doc.tracks)
    assert not doc.frames, 'Third-party players must be click-to-load'
    for track in doc.tracks:assert (SITE/track['src']).read_text().startswith('WEBVTT')
    for video in doc.videos:assert video.get('poster') and video.get('aria-label')
    svgs=list(SITE.rglob('*.svg'))
    for p in svgs:
        e=ET.parse(p).getroot();assert e.attrib.get('viewBox'),p
        assert not any('http' in v and k.endswith('href') for n in e.iter() for k,v in n.attrib.items()),(p,'External SVG dependency')
    manifest=json.loads((SITE/'downloads/manifest.json').read_text())
    for item in manifest['files']:
        raw=(SITE/item['path']).read_bytes()
        assert len(raw)==item['bytes'] and hashlib.sha256(raw).hexdigest()==item['sha256'],item['path']
    for p in SITE.rglob('*.py'):compile(p.read_text(),str(p),'exec')
    for p in SITE.rglob('*'):
        if p.is_file() and p.suffix in ('.html','.js','.css','.json','.csv','.py','.md','.svg'):
            assert '/Users/nick/' not in p.read_text(),(p,'Private/nonportable source path')
    result={'passed':True,'html_pages':len(documents),'local_links_checked':checks,'images':len(doc.images),'local_videos':len(doc.videos),'caption_tracks':len(doc.tracks),'svg_diagrams':len(svgs),'manifest_files':len(manifest['files'])}
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
