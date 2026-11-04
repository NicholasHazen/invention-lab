#!/usr/bin/env node
/** Build the handbook without touching the project hub, pivot, tools, or downloads. */
import fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import { fileURLToPath, pathToFileURL } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const source = path.join(root, 'handbook');
const output = path.join(root, 'docs', 'handbook');
const escape = value => String(value ?? '').replace(/[&<>"']/g, c => ({ '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;' }[c]));
const readJSON = async file => JSON.parse(await fs.readFile(file, 'utf8'));

async function loadMarked() {
  const candidates = [
    process.env.HANDBOOK_MARKED_MODULE,
    'marked',
    process.env.CODEX_DEPENDENCY_ROOT && path.join(process.env.CODEX_DEPENDENCY_ROOT, 'node/node_modules/marked/lib/marked.esm.js'),
    path.join(os.homedir(), '.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/marked/lib/marked.esm.js'),
  ].filter(Boolean);
  for (const candidate of candidates) {
    try { return await import(path.isAbsolute(candidate) ? pathToFileURL(candidate).href : candidate); }
    catch (error) { if (error.code !== 'ERR_MODULE_NOT_FOUND' && error.code !== 'MODULE_NOT_FOUND') throw error; }
  }
  throw new Error('Install marked 17.x locally, or set HANDBOOK_MARKED_MODULE to its marked.esm.js file.');
}
const { Marked, Renderer } = await loadMarked();
const curriculum = await readJSON(path.join(source, 'curriculum.json'));
const chapters = curriculum.chapters;
const chapterByNumber = new Map(chapters.map(c => [c.number, c]));
const chapterBySlug = new Map(chapters.map(c => [c.slug, c]));
const bands = [...new Set(chapters.map(c => c.band))];
if (chapters.length !== 20) throw new Error(`Expected 20 chapters; found ${chapters.length}.`);
if (new Set(chapters.map(c => c.slug)).size !== chapters.length) throw new Error('Duplicate chapter slug.');
for (const chapter of chapters) {
  if (!/^[a-z0-9-]+$/.test(chapter.slug)) throw new Error(`Unsafe chapter slug: ${chapter.slug}`);
  chapter.markdown = await fs.readFile(path.join(source, 'chapters', chapter.source), 'utf8');
  if (!chapter.markdown.trim()) throw new Error(`Empty chapter: ${chapter.source}`);
  for (const number of chapter.prerequisites) if (!chapterByNumber.has(number)) throw new Error(`Unknown prerequisite ${number}`);
}

const requiredFields = ['id','title','creator','url','format','topics','level','prerequisites','access','why','first_task','limitations','verified_on','evidence_url','evidence_note'];
const researchFiles = (await fs.readdir(path.join(source, 'research'))).filter(f => f.endsWith('.json')).sort();
const resources = [];
const resourceIds = new Set();
for (const file of researchFiles) {
  const records = await readJSON(path.join(source, 'research', file));
  if (!Array.isArray(records)) throw new Error(`${file} must contain an array.`);
  for (const record of records) {
    for (const field of requiredFields) if (record[field] === undefined) throw new Error(`${file}: ${record.id} missing ${field}`);
    if (!/^[a-z0-9-]+$/.test(record.id) || resourceIds.has(record.id)) throw new Error(`Invalid or duplicate resource ID: ${record.id}`);
    if (!Array.isArray(record.topics)) throw new Error(`${record.id}: topics must be an array.`);
    if (!['course','book','video','documentation','project'].includes(record.format)) throw new Error(`${record.id}: invalid format.`);
    for (const key of ['url','evidence_url']) if (!/^https?:\/\//i.test(record[key])) throw new Error(`${record.id}: invalid ${key}`);
    resourceIds.add(record.id);
    resources.push(record);
  }
}
resources.sort((a,b) => a.title.localeCompare(b.title));
const canonical = url => { try { const u = new URL(url); for(const key of [...u.searchParams.keys()]) if(/^utm_|^(fbclid|gclid)$/.test(key)) u.searchParams.delete(key); return `${u.hostname.replace(/^www\./,'')}${u.pathname.replace(/\/$/,'')}${u.search}`; } catch { return url; } };
const slugify = text => text.normalize('NFKD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[^\p{Letter}\p{Number}]+/gu,'-').replace(/^-|-$/g,'') || 'section';
const topicKey = text => String(text).trim().toLowerCase().replace(/[-_]+/g,' ').replace(/\s+/g,' ');
const plain = text => text.replace(/<[^>]*>/g,'').replace(/[*_`]/g,'');
const safeURL = href => {
  const value = String(href ?? '').trim();
  if (/^[\u0000-\u0020]*[a-z][a-z\d+.-]*:/i.test(value) && !/^(https?:|mailto:)/i.test(value)) return null;
  if (/^\/\//.test(value) || /[\u0000-\u001f]/.test(value)) return null;
  return value;
};
function indexLinks(href) {
  const [beforeHash, ...hash] = href.split('#');
  const [pathname, ...query] = beforeHash.split('?');
  const local = !/^(https?:|mailto:)/i.test(href);
  const normalized = local && pathname.endsWith('/') ? pathname + 'index.html' : pathname;
  return normalized + (query.length ? '?' + query.join('?') : '') + (hash.length ? '#' + hash.join('#') : '');
}
function chapterURL(href, chapter, print = false) {
  const safe = safeURL(href);
  if (safe === null) return null;
  if (!print) return indexLinks(safe);
  if (/^(https?:|mailto:)/i.test(safe)) return safe;
  if (safe.startsWith('#')) return `#${chapter.slug}--${safe.slice(1)}`;
  const match = safe.match(/^\.\.\/([a-z0-9-]+)\/(?:index\.html)?(?:#(.+))?$/);
  if (match && chapterBySlug.has(match[1])) return match[2] ? `#${match[1]}--${match[2]}` : `#chapter-${match[1]}`;
  if (safe.startsWith('../../')) return indexLinks(safe.slice(3));
  if (safe.startsWith('../')) return indexLinks(safe.slice(3));
  return indexLinks(`${chapter.slug}/${safe}`);
}
function renderChapter(chapter, print = false) {
  const headings = [], seen = new Map(), citations = new Set();
  const renderer = new Renderer();
  renderer.heading = function(token) {
    const text = plain(token.text);
    if (token.depth === 1) { chapter.displayTitle = text; return ''; }
    const base = slugify(text), count = seen.get(base) || 0;
    seen.set(base, count + 1);
    const localID = base + (count ? `-${count + 1}` : '');
    const id = print ? `${chapter.slug}--${localID}` : localID;
    if (token.depth <= 3) headings.push({ depth:token.depth, title:text, id });
    return `<h${token.depth} id="${escape(id)}">${this.parser.parseInline(token.tokens)}</h${token.depth}>\n`;
  };
  renderer.link = function(token) {
    const href = chapterURL(token.href, chapter, print);
    const label = this.parser.parseInline(token.tokens);
    if (!href) return label;
    if (/^https?:/i.test(href)) citations.add(canonical(href));
    return `<a href="${escape(href)}"${token.title ? ` title="${escape(token.title)}"` : ''}>${label}</a>`;
  };
  renderer.image = function(token) {
    const href = chapterURL(token.href, chapter, print);
    if (!href) return escape(token.text);
    const image = `<img src="${escape(href)}" alt="${escape(token.text)}" loading="${print ? 'eager' : 'lazy'}" decoding="async"${token.title ? ` title="${escape(token.title)}"` : ''}>`;
    return print ? image : `<a class="figure-link" href="${escape(href)}" aria-label="Open full-size diagram: ${escape(token.text)}">${image}</a><span class="figure-hint">Select the diagram to open it at full size.</span>`;
  };
  // Source chapters are Markdown. Render literal HTML as text instead of trusting it.
  renderer.html = token => escape(token.text);
  renderer.table = function(token) {
    const row = (cells, header) => `<tr>${cells.map(cell => `<${header ? 'th scope="col"' : 'td'}>${this.parser.parseInline(cell.tokens)}</${header ? 'th' : 'td'}>`).join('')}</tr>`;
    return `<div class="table-scroll" tabindex="0" role="region" aria-label="Scrollable table"><table><thead>${row(token.header,true)}</thead><tbody>${token.rows.map(cells=>row(cells,false)).join('')}</tbody></table></div>`;
  };
  const parser = new Marked({ renderer, gfm:true, breaks:false });
  return { html:parser.parse(chapter.markdown), headings, citations };
}
for (const chapter of chapters) {
  chapter.rendered = renderChapter(chapter);
  chapter.references = resources.filter(r => chapter.rendered.citations.has(canonical(r.url)));
}

const checked = escape(curriculum.checked_on);
const number = n => String(n).padStart(2,'0');
const chapterLink = (chapter, base = '') => `${base}${chapter.slug}/index.html`;
function header(base, active = '') {
  const nav = [['Chapters',base+'index.html','chapters'],['Paths',base+'paths/index.html','paths'],['Library',base+'library/index.html','library'],['Workbench',base+'tools/index.html','tools']];
  return `<a class="skip-link" href="#main">Skip to content</a><header class="site-header"><a class="wordmark" href="${base}../index.html"><span class="mark" aria-hidden="true"></span>Invention Lab</a><nav aria-label="Handbook navigation">${nav.map(([name,url,id])=>`<a href="${url}"${active===id?' aria-current="page"':''}>${name}</a>`).join('')}</nav></header>`;
}
function footer(base) {
  return `<footer class="site-footer"><p>The Invention Lab Handbook <span>v${escape(curriculum.revision)}</span><br>Sources checked ${checked}. Physical prototypes remain subject to their stated test limits.</p><div><a href="${base}print.html">Print edition</a><a href="${base}../projects/triangulated-pivot/index.html">Pivot case study</a><a href="https://github.com/NicholasHazen/invention-lab">Source on GitHub</a></div></footer>`;
}
function documentHTML({title, description, base='', active='', body, bodyClass=''}) {
  return `<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="${escape(description)}"><meta name="color-scheme" content="light"><title>${escape(title)} · Invention Lab</title><link rel="stylesheet" href="${base}assets/handbook.css"><script src="${base}assets/handbook.js" defer></script></head><body class="${escape(bodyClass)}">${header(base,active)}${body}${footer(base)}</body></html>\n`;
}
function chapterList(base='', current=null) {
  return bands.map(band=>`<section class="nav-band"><h3>${escape(band)}</h3><ol>${chapters.filter(c=>c.band===band).map(c=>`<li><a href="${chapterLink(c,base)}"${current?.slug===c.slug?' aria-current="page"':''}><span>${number(c.number)}</span>${escape(c.title)}</a></li>`).join('')}</ol></section>`).join('');
}
function toc(headings, prefix='') {
  return `<ol class="toc-list">${headings.filter(h=>h.depth===2).map(h=>`<li><a href="${prefix}#${escape(h.id)}">${escape(h.title)}</a></li>`).join('')}</ol>`;
}
function prerequisiteHTML(chapter, base='../', print=false) {
  return chapter.prerequisites.length ? `<div class="prerequisites"><span>Builds on</span>${chapter.prerequisites.map(n=>{const c=chapterByNumber.get(n);return `<a href="${print?'#chapter-'+c.slug:chapterLink(c,base)}">${number(c.number)} · ${escape(c.title)}</a>`;}).join('')}</div>` : '<p class="prerequisites"><span>Start here</span>No prior handbook chapters required.</p>';
}
const accessGroups = { free:'Free access available', mixed:'Free + paid options', paid:'Paid / library access', check:'Check access details' };
function accessGroup(text) {
  const free = /free|public|open[- ]source|open textbook|opencourseware/i.test(text);
  const paid = /paid|commercial|sold|purchase|subscription/i.test(text);
  return free ? (paid ? 'mixed':'free') : paid ? 'paid':'check';
}
function resourceCard(resource, {base='../', compact=false, print=false}={}) {
  const related = chapters.filter(c=>c.references.some(r=>r.id===resource.id));
  const topics = resource.topics.map(topicKey);
  const heading = compact ? 'h3' : 'h2';
  const search = [resource.title,resource.creator,resource.why,resource.level,...topics].join(' ').toLowerCase();
  const data = compact || print ? '' : ` data-resource data-format="${escape(resource.format)}" data-access="${resource.access_group || accessGroup(resource.access)}" data-topics="${escape(topics.join('|'))}" data-search="${escape(search)}"`;
  return `<article class="resource-card${compact?' compact':''}" tabindex="-1" id="${print?'resource-':''}${escape(resource.id)}"${data}><div class="resource-meta"><span>${escape(resource.format)}</span><span>${escape(resource.level)}</span></div><${heading}><a href="${escape(resource.url)}">${escape(resource.title)} <span aria-hidden="true">↗</span></a></${heading}><p class="resource-creator">${escape(resource.creator)}</p><p>${escape(resource.why)}</p><dl><div><dt>Access</dt><dd>${escape(resource.access)}</dd></div><div><dt>Before you start</dt><dd>${escape(resource.prerequisites)}</dd></div><div class="first-task"><dt>First useful task</dt><dd>${escape(resource.first_task)}</dd></div><div><dt>Keep in mind</dt><dd>${escape(resource.limitations)}</dd></div></dl>${related.length&&!compact?`<p class="resource-related">Used in ${related.map(c=>`<a href="${print?'#chapter-'+c.slug:chapterLink(c,base)}">Chapter ${c.number}</a>`).join(', ')}</p>`:''}<details class="source-evidence"><summary>Source review · ${escape(resource.verified_on)}</summary><p>${escape(resource.evidence_note)} <a href="${escape(resource.evidence_url)}">Review the official source</a>.</p></details></article>`;
}
async function write(relative, value) {
  const file = path.join(output,relative);
  await fs.mkdir(path.dirname(file),{recursive:true});
  await fs.writeFile(file,value);
}

const landing = `<main id="main" class="landing"><section class="book-intro"><div><p class="eyebrow">A field guide for curious builders · Edition ${escape(curriculum.revision)}</p><h1>Learn the foundations.<br>Make something of your own.</h1><p class="lede">A practical engineering handbook for the workbench: understand a principle, try a small experiment, and use the evidence to make your next decision.</p><div class="actions"><a class="button" href="start/index.html">Start with Chapter 1 <span aria-hidden="true">→</span></a><a href="paths/index.html">Choose a learning path</a></div><p class="intro-note">Twenty chapters. Small labs. Worked examples. A path from a first bracket to a connected sensing system.</p></div><aside class="book-map" aria-label="How to use this handbook"><span class="map-kicker">The working rhythm</span><ol><li><b>01</b><div><h2>Understand</h2><p>Trace the cause. Check the units. Name the assumptions.</p></div></li><li><b>02</b><div><h2>Try</h2><p>Make a small, reversible experiment that answers one question.</p></div></li><li><b>03</b><div><h2>Explain</h2><p>Record what happened and decide what to change next.</p></div></li></ol></aside></section><section class="entry-grid" aria-label="Ways into the handbook"><a class="entry-card" href="paths/index.html"><span class="eyebrow">Follow a purpose</span><h2>Four learning paths <span aria-hidden="true">↗</span></h2><p>Foundations, fabrication, sensing, or an intelligent system. Start where your project needs you.</p></a><a class="entry-card" href="library/index.html"><span class="eyebrow">Go deeper</span><h2>The annotated library <span aria-hidden="true">↗</span></h2><p>Courses, books, videos, and official references—with prerequisites and a concrete first task.</p></a><a class="entry-card" href="../projects/triangulated-pivot/index.html"><span class="eyebrow">Study a full example</span><h2>The triangulated pivot <span aria-hidden="true">↗</span></h2><p>A detailed Fusion-to-print case study, model downloads, and an interactive assembly viewer.</p></a></section><section id="chapters" class="contents-section"><div class="section-heading"><div><p class="eyebrow">The curriculum</p><h2>Pick up a chapter. Bring it to the bench.</h2></div><a href="print.html">Read the full print edition →</a></div>${bands.map(band=>`<section class="contents-band"><h3>${escape(band)}</h3><ol class="chapter-cards">${chapters.filter(c=>c.band===band).map(c=>`<li><a href="${chapterLink(c)}"><span class="chapter-number">${number(c.number)}</span><div><h4>${escape(c.title)}</h4><p>${escape(c.summary)}</p></div><span class="card-arrow" aria-hidden="true">↗</span></a></li>`).join('')}</ol></section>`).join('')}</section><section class="download-panel"><div><p class="eyebrow">Keep it nearby</p><h2>Your workbench copy</h2><p>Use the print edition for continuous reading, or download the handbook, diagrams, examples, and worksheets for offline use. The pivot’s larger model downloads remain with its project guide.</p></div><div class="actions"><a class="button" href="downloads/invention-lab-handbook-v1.0.zip" download>Download offline handbook</a><a href="print.html">Print or save as PDF</a></div></section><p class="publication-note">This is a learning handbook. Example calculations, simulations, and prototype status are labeled where they appear; they do not establish a rating for a manufactured part. External recommendations are based on official contents and documentation review.</p></main>`;
await write('index.html',documentHTML({title:curriculum.title,description:curriculum.subtitle,active:'chapters',body:landing}));

for (let i=0;i<chapters.length;i++) {
  const c=chapters[i], previous=chapters[i-1], next=chapters[i+1];
  const related = c.references.length ? `<section class="chapter-references" id="go-deeper"><p class="eyebrow">Continue with a purpose</p><h2>Resources used in this chapter</h2><p>Choose one resource for the question in front of you. Pair a lesson with its first useful task.</p><div class="reference-grid">${c.references.map(r=>resourceCard(r,{compact:true})).join('')}</div><p><a href="../library/index.html">Explore the full annotated library →</a></p></section>` : '';
  const pagination = `<nav class="chapter-pagination" aria-label="Adjacent chapters">${previous?`<a href="${chapterLink(previous,'../')}"><span>← Previous · ${number(previous.number)}</span><strong>${escape(previous.title)}</strong></a>`:'<div></div>'}${next?`<a href="${chapterLink(next,'../')}"><span>Next · ${number(next.number)} →</span><strong>${escape(next.title)}</strong></a>`:`<a href="../paths/index.html"><span>Choose your next project →</span><strong>Return to the learning paths</strong></a>`}</nav>`;
  const body=`<div class="chapter-layout"><aside class="chapter-sidebar"><details class="chapter-menu" open><summary>All twenty chapters</summary><nav aria-label="Chapter navigation">${chapterList('../',c)}</nav></details><a class="sidebar-print" href="../print.html#chapter-${c.slug}">Open in print edition ↗</a></aside><main id="main" class="chapter-main"><header class="chapter-heading"><p class="eyebrow">${escape(c.band)} · Chapter ${number(c.number)}</p><h1>${escape(c.displayTitle || c.title)}</h1><p class="chapter-deck">${escape(c.summary)}</p>${prerequisiteHTML(c)}</header><details class="mobile-toc"><summary>In this chapter</summary>${toc(c.rendered.headings)}</details><article class="prose">${c.rendered.html}</article>${related}${pagination}</main><aside class="page-toc"><p class="eyebrow">In this chapter</p><nav aria-label="On this page">${toc(c.rendered.headings)}${related?'<p><a href="#go-deeper">Resources used</a></p>':''}</nav><a class="back-top" href="#main">Back to top ↑</a></aside></div>`;
  await write(`${c.slug}/index.html`,documentHTML({title:`${number(c.number)} · ${c.displayTitle||c.title}`,description:c.summary,base:'../',active:'chapters',body,bodyClass:'chapter-page'}));
}

const pathsBody=`<main id="main" class="collection-main"><header class="collection-heading"><p class="eyebrow">Start with an outcome</p><h1>A path through the ideas.</h1><p class="lede">You do not need to finish every chapter before making something useful. Choose a path, check the prerequisites, and keep one small project alongside the reading.</p></header><div class="path-grid">${curriculum.paths.map((p,i)=>`<section class="path-card" id="${escape(p.id)}"><p class="eyebrow">Path ${number(i+1)}</p><h2>${escape(p.title)}</h2><p class="path-result">${escape(p.result)}</p><ol>${p.chapters.map(n=>{const c=chapterByNumber.get(n);if(!c)throw new Error(`Unknown path chapter ${n}`);return `<li><a href="${chapterLink(c,'../')}"><span>${number(n)}</span>${escape(c.title)}</a></li>`;}).join('')}</ol><a class="text-link" href="${chapterLink(chapterByNumber.get(p.chapters[0]),'../')}">Start this path →</a></section>`).join('')}</div><section class="reading-note"><h2>Let the project set the pace.</h2><p>Read until you can make a prediction. Run the smallest useful experiment. Record what surprised you. Return to a prerequisite when a missing concept prevents you from explaining the result.</p><p><a href="../independent-projects/index.html">The independent-project chapter</a> supplies briefs for a sensor mount, a bench logger, and a small positioning system.</p></section></main>`;
await write('paths/index.html',documentHTML({title:'Learning paths',description:'Four practical routes through the Invention Lab Handbook.',base:'../',active:'paths',body:pathsBody}));

const topics=[...new Set(resources.flatMap(r=>r.topics.map(topicKey)))].sort();
const starters = [
  ['Math and physics','foundation-openstax-physics','College Physics','Algebra-based foundation'],
  ['Product design','design-stanford-bootleg','Design Thinking Bootleg','Begin with an observed task'],
  ['CAD','fab-fusion-design-intent','Fusion design intent','A little Fusion familiarity'],
  ['Print design','fab-prusa-print-design','Modeling for 3D printing','Inspect a model and a slice'],
  ['Mechanics','fab-engineering-statics','Engineering Statics','Algebra and basic trigonometry'],
  ['Circuits and measurement','adafruit-multimeters','Multimeters','Begin with low-voltage measurement'],
  ['Programming','cs50-python','CS50 Python','No programming background required'],
  ['Embedded systems','micropython-rp2-reference','MicroPython RP2 reference','After Python and basic circuits'],
  ['PCB design','kicad-getting-started','Getting Started in KiCad','After a simple circuit you can explain'],
  ['Control','mathworks-pid-videos','Understanding PID Control','After reference, error, and feedback'],
  ['Robotics','modern-robotics-videos','Modern Robotics videos','After trigonometry; deeper math later'],
  ['AI and vision','isl-python','Statistical Learning in Python','After Python and introductory statistics'],
  ['Connected devices','mosquitto-docs','Mosquitto documentation','After the Chapter 19 message lab'],
];
for(const [,id] of starters) if(!resourceIds.has(id)) throw new Error(`Starter resource is missing: ${id}`);
const starterMap = `<details class="starter-map" open><summary>Choose one starting resource <span>Thirteen entry points</span></summary><p>Follow the question you are working on. The full card keeps the prerequisites, access details, and first task together.</p><div class="starter-grid">${starters.map(([skill,id,title,note])=>`<div><h2>${escape(skill)}</h2><a href="#${escape(id)}" data-starter-link>${escape(title)} →</a><p>${escape(note)}</p></div>`).join('')}</div></details>`;
const libraryBody=`<main id="main" class="collection-main library-main"><header class="collection-heading"><p class="eyebrow">An annotated shelf · ${resources.length} resources</p><h1>Find the next useful lesson.</h1><p class="lede">Choose one primary resource for the obstacle you are facing. Pair each lesson with a small task; the goal is a better decision or a working experiment.</p><p class="library-guidance">Selections reflect review of official contents, syllabi, and documentation—not a claim that every course was completed. Free archived materials are different from enrolled instruction, feedback, shop access, or certificates. Check each access note before committing.</p></header>${starterMap}<form class="library-filters" data-library-filters hidden role="search" aria-label="Filter learning resources"><div class="search-field"><label for="resource-search">Search the library</label><input id="resource-search" name="q" type="search" placeholder="Try bearings, Python, or measurement…" autocomplete="off"></div><div><label for="resource-topic">Topic</label><select id="resource-topic" name="topic"><option value="">All topics</option>${topics.map(t=>`<option value="${escape(t)}">${escape(t.replace(/-/g,' '))}</option>`).join('')}</select></div><div><label for="resource-format">Format</label><select id="resource-format" name="format"><option value="">All formats</option>${['book','course','video','documentation','project'].map(f=>`<option value="${f}">${f[0].toUpperCase()+f.slice(1)}</option>`).join('')}</select></div><div><label for="resource-access">Access</label><select id="resource-access" name="access"><option value="">All access types</option>${Object.entries(accessGroups).map(([key,label])=>`<option value="${key}">${label}</option>`).join('')}</select></div><button type="reset" class="reset-button">Clear filters</button></form><noscript><p class="notice">All resources are listed below. Use your browser’s Find command to search this page.</p></noscript><div class="library-status"><p data-resource-count role="status" aria-live="polite">${resources.length} resources</p><p>Sources checked ${checked}</p></div><p class="empty-state" data-empty-state hidden>No resources match those filters. Try a broader topic or clear the filters.</p><div class="resource-grid">${resources.map(r=>resourceCard(r)).join('')}</div></main>`;
await write('library/index.html',documentHTML({title:'Annotated resource library',description:'Courses, books, videos, and primary references with prerequisites, access notes, and first tasks.',base:'../',active:'library',body:libraryBody}));

const printBody=`<main id="main" class="print-main"><header class="print-cover"><p class="eyebrow">Invention Lab · Edition ${escape(curriculum.revision)}</p><h1>${escape(curriculum.title)}</h1><p class="lede">${escape(curriculum.subtitle)}</p><p>Complete reading edition · Sources checked ${checked}</p><p class="screen-only"><button class="button" type="button" data-print>Print or save as PDF</button> <a href="index.html">Return to chapter navigation</a></p></header><nav class="print-contents" aria-label="Print edition contents"><h2>Contents</h2><ol>${chapters.map(c=>`<li><a href="#chapter-${c.slug}">${number(c.number)} · ${escape(c.title)}</a></li>`).join('')}<li><a href="#resource-library">Annotated resource library</a></li></ol></nav>${chapters.map(c=>`<section class="print-chapter" id="chapter-${c.slug}"><header class="chapter-heading"><p class="eyebrow">${escape(c.band)} · Chapter ${number(c.number)}</p><h1>${escape(c.displayTitle||c.title)}</h1>${prerequisiteHTML(c,'',true)}</header><article class="prose">${renderChapter(c,true).html}</article></section>`).join('')}<section class="print-bibliography" id="resource-library"><h1>Annotated resource library</h1><p>Choose one primary resource for your current obstacle, then complete its first useful task. Recommendations reflect official contents, syllabus, or documentation review; they are not claims of course completion. Archived free materials do not include live instruction or certificates unless explicitly stated.</p>${resources.map(r=>resourceCard(r,{base:'',print:true})).join('')}</section></main>`;
await write('print.html',documentHTML({title:'Complete print edition',description:'All twenty handbook chapters and the annotated resource library in one readable document.',body:printBody,bodyClass:'print-edition'}));

// Merge source trees, including root-authored tools; never erase tools/ or downloads/.
for (const directory of ['assets','examples','worksheets','tools']) {
  const from=path.join(source,directory);
  try { await fs.cp(from,path.join(output,directory),{recursive:true,filter:file => !['__pycache__','.DS_Store'].includes(path.basename(file)) && !file.endsWith('.pyc')}); }
  catch(error) { if(error.code!=='ENOENT') throw error; }
}
async function cleanGeneratedCaches(directory) {
  let entries;
  try { entries = await fs.readdir(directory,{withFileTypes:true}); } catch(error) { if(error.code==='ENOENT') return; throw error; }
  for(const entry of entries) {
    const file=path.join(directory,entry.name);
    if(entry.name==='__pycache__' || entry.name==='.DS_Store' || entry.name.endsWith('.pyc')) await fs.rm(file,{recursive:true,force:true});
    else if(entry.isDirectory()) await cleanGeneratedCaches(file);
  }
}
for(const directory of ['assets','examples','worksheets']) await cleanGeneratedCaches(path.join(output,directory));
await fs.mkdir(path.join(output,'assets'),{recursive:true});
for (const file of ['handbook.css','handbook.js']) await fs.copyFile(path.join(source,'web',file),path.join(output,'assets',file));
await write('build-manifest.json',JSON.stringify({revision:curriculum.revision,checked_on:curriculum.checked_on,chapters:chapters.map(c=>({number:c.number,slug:c.slug,source:c.source,headings:c.rendered.headings.map(h=>h.id),references:c.references.map(r=>r.id)})),research_files:researchFiles,resource_count:resources.length,generated_pages:chapters.length+4,notes:['tools/ and downloads/ are maintained separately and are preserved.','No physical manufacturing validation is implied by this site build.']},null,2)+'\n');
console.log(`Built ${chapters.length} chapters, ${curriculum.paths.length} paths, ${resources.length} resources, and the print edition in docs/handbook/.`);
console.log(`Research inputs: ${researchFiles.join(', ')}. Rebuild after other authors update their inputs.`);
