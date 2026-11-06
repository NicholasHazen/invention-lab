#!/usr/bin/env python3
"""Build a deterministic standalone reading kit; outside-project links stay online."""
from pathlib import Path
from urllib.parse import urlsplit, unquote, quote
from html import escape, unescape
import hashlib, json, re, zipfile, posixpath
from validate_actuator_guide import Document, ROOT, SITE

BASE='https://nicholashazen.github.io/invention-lab/'
VERSION=json.loads((ROOT/'guides/robotic-actuators/guide.json').read_text())['version']
NAME='robotic-actuators-v'+VERSION
def sha(raw):return hashlib.sha256(raw).hexdigest()
def main():
    contents={};rewrites=[]
    for p in sorted(SITE.rglob('*')):
        if not p.is_file() or 'downloads' in p.relative_to(SITE).parts or p.name.startswith('.') or '__pycache__' in p.parts:continue
        raw=p.read_bytes();rel=p.relative_to(SITE).as_posix()
        if p.suffix=='.html':
            def replace(m):
                attr,q,value=m.groups();u=urlsplit(unescape(value))
                if u.scheme or u.netloc or not u.path:return m.group(0)
                dest=(p.parent/unquote(u.path)).resolve()
                if dest.is_relative_to(SITE) and 'downloads' not in dest.relative_to(SITE).parts:return m.group(0)
                assert dest.is_relative_to(ROOT/'docs'),value
                target=BASE+quote(dest.relative_to(ROOT/'docs').as_posix())
                if u.query:target+='?'+u.query
                if u.fragment:target+='#'+u.fragment
                rewrites.append({'from':value,'to':target})
                return f'{attr}={q}{escape(target,quote=True)}{q}'
            raw=re.sub(r'\b(href|src|poster)=([\"\'])(.*?)\2',replace,raw.decode()).encode()
        contents[rel]=raw
    contents['READ-ME.txt']=(f'''Robotic actuators — From load to motion. Edition {VERSION}.

Extract the complete archive. index.html contains all ten chapters.
The guide, diagrams, three original silent motion clips, captions, transcripts,
CAD files, calculations, and worksheets are included. Local clips play with
native browser controls and are available as MP4 downloads. Third-party
video lessons require internet access; their direct watch links are retained.
YouTube players load only when explicitly selected. The figure gallery and
workbench enhance the page when JavaScript is available.
External references, the separate handbook and pivot project, and publication
metadata use online links. JavaScript enhances the sizing workbench; the
worked default values remain readable without JavaScript. The browser code
uses a classic script and no remote libraries. Browser verification was over
HTTP; the archive's files, checksums and relative links were checked directly.

Read designs/README.md before opening native CAD. These are editable layout
studies, not tested, fabrication-ready assemblies. Follow the chapters to
learn constrained Fusion modeling. Actual component data, fits, retention,
guards, electronics and physical validation remain a later design stage.

The Python examples require Python 3 and its standard library only.
They calculate and analyze data; they do not command physical hardware.
See examples/README.md for commands and expected outputs.

Online guide: https://nicholashazen.github.io/invention-lab/projects/robotic-actuators/
Source: https://github.com/NicholasHazen/invention-lab/tree/main/guides/robotic-actuators
manifest.json records SHA-256 digests of every included file except itself.
''').encode()
    docs={}
    for name,raw in contents.items():
        if name.endswith('.html'):
            doc=Document();doc.feed(raw.decode());docs[name]=doc
    checked=0
    for name,doc in docs.items():
        for href in doc.links:
            u=urlsplit(href)
            if u.scheme or u.netloc:continue
            target=posixpath.normpath(posixpath.join(posixpath.dirname(name),unquote(u.path))) if u.path else name
            assert target in contents,(name,href,target)
            if u.fragment and target in docs:assert unquote(u.fragment) in docs[target].ids,(name,href)
            checked+=1
    manifest={'guide':'Robotic actuators','version':VERSION,'offline_link_rewrites':rewrites,'files':{name:{'bytes':len(raw),'sha256':sha(raw)} for name,raw in contents.items()}}
    contents['manifest.json']=(json.dumps(manifest,indent=2)+'\n').encode()
    dest=SITE/'downloads';dest.mkdir(exist_ok=True);archive=dest/(NAME+'.zip')
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name,raw in contents.items():
            info=zipfile.ZipInfo(NAME+'/'+name,date_time=(2026,11,6,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,raw)
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        for name,item in manifest['files'].items():assert sha(z.read(NAME+'/'+name))==item['sha256'],name
    checksum=sha(archive.read_bytes());(dest/'SHA256SUMS.txt').write_text(f'{checksum}  {archive.name}\n')
    result={'archive':archive.relative_to(ROOT).as_posix(),'bytes':archive.stat().st_size,'sha256':checksum,'files':len(contents),'offline_links_verified':checked,'verified':True}
    (dest/'release-info.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
