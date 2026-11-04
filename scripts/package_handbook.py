#!/usr/bin/env python3
"""Package the generated handbook for offline reading, retaining external project links."""
from pathlib import Path
from urllib.parse import urlsplit, quote, unquote
from html import escape, unescape
import hashlib, json, re, zipfile, posixpath
from validate_handbook import Document
ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'docs/handbook'
BASE='https://nicholashazen.github.io/invention-lab/'

def sha(raw):return hashlib.sha256(raw).hexdigest()
def main():
    revision=json.loads((ROOT/'handbook/curriculum.json').read_text())['revision']
    name=f'invention-lab-handbook-v{revision}'
    directory=SITE/'downloads';directory.mkdir(exist_ok=True)
    archive=directory/(name+'.zip')
    contents={};changes=[]
    for p in sorted(SITE.rglob('*')):
        if not p.is_file() or 'downloads' in p.relative_to(SITE).parts or p.name.startswith('.') or p.suffix=='.pyc' or '__pycache__' in p.parts:continue
        raw=p.read_bytes();relative=p.relative_to(SITE).as_posix()
        if p.suffix=='.html':
            text=raw.decode()
            def link(match):
                attr,q,original=match.groups();href=unescape(original);u=urlsplit(href)
                if u.scheme or u.netloc or not u.path:return match.group(0)
                dest=(p.parent/unquote(u.path)).resolve()
                if dest.is_relative_to(SITE.resolve()) and 'downloads' not in dest.relative_to(SITE.resolve()).parts:return match.group(0)
                if not dest.is_relative_to((ROOT/'docs').resolve()):raise ValueError(f'Unexpected link {relative}: {href}')
                target=BASE+quote(dest.relative_to((ROOT/'docs').resolve()).as_posix())
                if u.query:target+='?'+u.query
                if u.fragment:target+='#'+u.fragment
                changes.append({'file':relative,'from':href,'to':target})
                return f'{attr}={q}{escape(target,quote=True)}{q}'
            text=re.sub(r'\b(href|src)=([\"\'])(.*?)\2',link,text)
            raw=text.encode()
        contents[relative]=raw
    # Verify the rewritten portable graph without relying on a browser file URL.
    parsed={}
    for filename,raw in contents.items():
        if filename.endswith('.html'):
            doc=Document();doc.feed(raw.decode());parsed[filename]=doc
    offline_links=0
    for filename,doc in parsed.items():
        for href in doc.links:
            u=urlsplit(href)
            if u.scheme or u.netloc:continue
            target=posixpath.normpath(posixpath.join(posixpath.dirname(filename),unquote(u.path))) if u.path else filename
            if target not in contents and target+'/index.html' in contents:target+='/index.html'
            assert target in contents,(filename,href,target)
            if u.fragment and target in parsed:assert unquote(u.fragment) in parsed[target].ids,(filename,href)
            offline_links+=1
    contents['READ-ME.txt']=(f'''The Invention Lab Handbook — revision {revision}

Extract the whole archive, then open index.html in a modern browser.
Chapter navigation, diagrams, library filters and workbench tools operate locally.
Open print.html for continuous reading; use your browser's Print command to save PDF.
Python examples require a separate Python 3 installation; see each examples/README.md.
Worksheets are editable Markdown and CSV files.

External courses/books/videos and the separate pivot project require internet access.
The pivot's CAD, print files and interactive assembly remain in its own complete kit:
https://nicholashazen.github.io/invention-lab/projects/triangulated-pivot/

Physical labs are proposed experiments unless specifically identified as observed.
Desktop results validate the stated software models, not physical devices.
manifest.json lists SHA-256 digests for the included files except itself.
''').encode()
    manifest={'title':'The Invention Lab Handbook','revision':revision,'source_checked_on':'2026-11-04','offline_scope':'Handbook pages, figures, local tools, code examples and worksheets. External learning resources and separate pivot project stay online.','offline_link_rewrites':changes,'files':{p:{'bytes':len(b),'sha256':sha(b)} for p,b in contents.items()}}
    contents['manifest.json']=(json.dumps(manifest,indent=2)+'\n').encode()
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p,b in contents.items():
            info=zipfile.ZipInfo(name+'/'+p,date_time=(2026,11,4,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,b)
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        for p,item in manifest['files'].items():assert sha(z.read(name+'/'+p))==item['sha256'],p
    checksum=sha(archive.read_bytes());(directory/'SHA256SUMS.txt').write_text(f'{checksum}  {archive.name}\n')
    result={'archive':archive.relative_to(ROOT).as_posix(),'bytes':archive.stat().st_size,'sha256':checksum,'files':len(contents),'offline_links_verified':offline_links,'verified':True}
    (directory/'release-info.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
