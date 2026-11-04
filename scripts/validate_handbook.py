#!/usr/bin/env python3
"""Check generated handbook links, sources and learning paths. Python stdlib only."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from collections import Counter
import argparse, json, re, hashlib, ast

ROOT = Path(__file__).resolve().parents[1]
class Document(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]; self.ids=[]; self.images=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        for k in ('href','src'):
            if k in a:self.links.append(a[k])
        if tag=='img':self.images.append(a)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',type=Path)
    args=parser.parse_args();errors=[];warnings=[]
    source=ROOT/'handbook';site=ROOT/'docs/handbook'
    curriculum=json.loads((source/'curriculum.json').read_text())
    chapters={x['number']:x for x in curriculum['chapters']}
    for number,ch in chapters.items():
        for dep in ch['prerequisites']:
            if dep not in chapters:errors.append(f'Unknown prerequisite {dep} for {number}')
    def closure(n,seen):
        if n in seen:raise ValueError(f'Prerequisite cycle {seen+[n]}')
        return {p for d in chapters[n]['prerequisites'] for p in ({d}|closure(d,seen+[n]))}
    for n in chapters:closure(n,[])
    for route in curriculum['paths']:
        done=set()
        for n in route['chapters']:
            missing=closure(n,[])-done
            if missing:errors.append(f"Path {route['id']}: {n} is missing prior {sorted(missing)}")
            done.add(n)
    records=[]
    for p in sorted((source/'research').glob('*.json')):records.extend(json.loads(p.read_text()))
    required={'id','title','creator','url','format','topics','level','prerequisites','access','why','first_task','limitations','verified_on','evidence_url','evidence_note'}
    for r in records:
        if required-set(r):errors.append(f"Resource {r.get('id')} missing {required-set(r)}")
        for k in required:
            if not r.get(k):errors.append(f"Empty {k} in {r.get('id')}")
        if r.get('format') not in {'course','book','video','documentation','project'}:errors.append(f"Unknown format in {r.get('id')}")
        if not re.fullmatch(r'\d{4}-\d{2}-\d{2}',r.get('verified_on','')):errors.append(f"Invalid date in {r.get('id')}")
        if not str(r.get('url','')).startswith('https://'):warnings.append(f"Non-HTTPS resource {r.get('id')}")
    for rid,count in Counter(r['id'] for r in records).items():
        if count!=1:errors.append(f'Duplicate resource id {rid}')
    documents={};link_count=0
    for p in site.rglob('*.html'):
        d=Document();d.feed(p.read_text());documents[p.resolve()]=d
        duplicates=[k for k,v in Counter(d.ids).items() if v>1]
        if duplicates:errors.append(f'{p.relative_to(ROOT)} duplicate ids: {duplicates}')
        for im in d.images:
            if 'alt' not in im:errors.append(f'{p.name}: missing image alt {im.get("src")}')
    for p,d in documents.items():
        for raw in d.links:
            u=urlsplit(raw)
            if u.scheme or u.netloc:continue
            link_count+=1
            dest=(p.parent/unquote(u.path)).resolve() if u.path else p
            if dest.is_dir():dest=dest/'index.html'
            if not dest.exists():errors.append(f'{p.relative_to(ROOT)} broken link {raw}');continue
            if u.fragment and dest.suffix=='.html':
                target=documents.get(dest)
                if target is None:
                    target=Document();target.feed(dest.read_text())
                if unquote(u.fragment) not in target.ids:errors.append(f'{p.relative_to(ROOT)} missing anchor {raw}')
    words={}
    for ch in chapters.values():
        text=(source/'chapters'/ch['source']).read_text()
        words[ch['slug']]=len(re.findall(r"\b[\w'-]+\b",text))
        if len(re.findall(r'^# ',text,re.M))!=1:errors.append(f"Chapter {ch['slug']}: expected one H1")
    for p in (source/'examples').rglob('*.py'):ast.parse(p.read_text(),filename=str(p))
    for p in site.rglob('*'):
        if p.suffix in {'.html','.md','.json','.js','.css','.csv','.py','.svg','.txt'} and p.is_file():
            if '/Users/' in p.read_text():errors.append(f'Workstation path in {p.relative_to(ROOT)}')
        if p.name=='__pycache__' or p.suffix=='.pyc':errors.append(f'Generated Python artifact published: {p}')
    result={'passed':not errors,'chapters':len(chapters),'chapter_words':words,'total_chapter_words':sum(words.values()),'resources':len(records),'formats':dict(Counter(r['format'] for r in records)),'html_pages':len(documents),'local_links_checked':link_count,'figures':len(list((site/'assets').rglob('*.svg'))),'errors':errors,'warnings':warnings,'limits':'Static structure checks complement, and do not replace, technical and teaching review or physical experiments.'}
    if args.report:args.report.parent.mkdir(parents=True,exist_ok=True);args.report.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2));return 1 if errors else 0
if __name__=='__main__':raise SystemExit(main())
