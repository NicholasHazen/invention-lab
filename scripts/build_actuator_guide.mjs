#!/usr/bin/env node
/** Owns only docs/projects/robotic-actuators. Source files remain independently editable. */
import fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import crypto from 'node:crypto';
import {fileURLToPath,pathToFileURL} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const source=path.join(root,'guides/robotic-actuators'),output=path.join(root,'docs/projects/robotic-actuators');
let module;
for(const candidate of ['marked',path.join(os.homedir(),'.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/marked/lib/marked.esm.js')]) {
  try {module=await import(path.isAbsolute(candidate)?pathToFileURL(candidate).href:candidate);break;} catch(error){if(error.code!=='ERR_MODULE_NOT_FOUND'&&error.code!=='MODULE_NOT_FOUND')throw error;}
}
if(!module)throw new Error('Run npm ci to install the pinned Markdown renderer.');
const {Marked,Renderer}=module;
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const num=n=>String(n).padStart(2,'0');
const titles=['Start at the thing you want to move','Electric actuator families','Choosing a transmission','Size the complete motion','Design a belt-driven joint','Design a screw-driven stage','Design a tendon-driven finger','Other ways to create motion','Feedback, drives, and power','Measure before increasing the load'];
const filenames=['01-requirements.md','02-electric-families.md','03-transmissions.md','04-sizing.md','05-belt-joint.md','06-screw-stage.md','07-tendon-gripper.md','08-other-actuators.md','09-feedback-drives.md','10-bench-validation.md'];
const chapters=[];
for(let i=0;i<filenames.length;i++){
  const markdown=await fs.readFile(path.join(source,'chapters',filenames[i]),'utf8');
  if(!markdown.trim()||(markdown.match(/^# /gm)||[]).length!==1)throw new Error(`Expected one title in ${filenames[i]}`);
  const renderer=new Renderer(),seen=new Map();
  renderer.heading=function(t){if(t.depth===1)return '';const base=t.text.toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'');const count=(seen.get(base)||0)+1;seen.set(base,count);const depth=Math.min(6,t.depth+1);return `<h${depth} id="c${num(i+1)}-${base}${count>1?'-'+count:''}">${this.parser.parseInline(t.tokens)}</h${depth}>\n`;};
  renderer.image=function(t){return `<a class="figure-link" href="${esc(t.href)}" aria-label="Open full-size diagram: ${esc(t.text)}"><img src="${esc(t.href)}" alt="${esc(t.text)}" loading="lazy" decoding="async"></a>`;};
  renderer.table=function(t){const row=(cells,head)=>`<tr>${cells.map((c,j)=>`<${head?'th':'td'}${head?' scope="col"':''}${t.align[j]?` style="text-align:${t.align[j]}"`:''}>${this.parser.parseInline(c.tokens)}</${head?'th':'td'}>`).join('')}</tr>`;return `<div class="table-wrap" role="region" aria-label="Comparison table" tabindex="0"><table><thead>${row(t.header,true)}</thead><tbody>${t.rows.map(r=>row(r,false)).join('')}</tbody></table></div>`;};
  const parser=new Marked({renderer,gfm:true,breaks:false});
  chapters.push({number:i+1,file:filenames[i],title:titles[i],html:parser.parse(markdown),words:markdown.split(/\s+/).length});
}
const resources=[];
for(const file of (await fs.readdir(path.join(source,'research'))).filter(f=>f.endsWith('.json')).sort()){
  const records=JSON.parse(await fs.readFile(path.join(source,'research',file),'utf8'));
  if(!Array.isArray(records))throw new Error(`${file} must contain an array`);
  for(const r of records){for(const key of ['id','title','creator','url','format','topics','level','prerequisites','access','why','first_task','limitations','verified_on','evidence_url','evidence_note'])if(r[key]===undefined)throw new Error(`${file}: missing ${key}`);resources.push(r);}
}
if(new Set(resources.map(r=>r.id)).size!==resources.length)throw new Error('Duplicate resource IDs');
const uniqueResources=[...new Map(resources.map(r=>[r.url.replace(/\/$/,''),r])).values()].sort((a,b)=>a.title.localeCompare(b.title));
const workbench=await fs.readFile(path.join(source,'web/workbench.html'),'utf8');
const listFiles=async(dir,prefix='')=>{const all=[];for(const e of await fs.readdir(dir,{withFileTypes:true})){if(e.name.startsWith('.')||e.name==='__pycache__')continue;const rel=path.posix.join(prefix,e.name);if(e.isDirectory())all.push(...await listFiles(path.join(dir,e.name),rel));else all.push(rel);}return all.sort();};
const artifactGroups=[];
for(const folder of ['designs','examples','worksheets']){
  try{const files=await listFiles(path.join(source,folder));artifactGroups.push({folder,files});}catch(error){if(error.code!=='ENOENT')throw error;}
}
const fileLabel=name=>name.replace(/_/g,' ').replace(/-/g,' ');
const downloadList=artifactGroups.map(group=>`<details${group.folder==='designs'?' open':''}><summary>${group.folder==='designs'?'CAD layouts & modeling files':group.folder==='examples'?'Calculation labs & executable checks':'Requirements & measurement worksheets'}</summary><ul class="file-list">${group.files.map(f=>`<li><a href="${group.folder}/${esc(f)}" download>${esc(fileLabel(f))}</a><span>${esc(path.extname(f).slice(1).toUpperCase())}</span></li>`).join('')}</ul></details>`).join('');
const nav=chapters.map(c=>`<li><a href="#chapter-${num(c.number)}"><span>${num(c.number)}</span>${esc(c.title)}</a></li>`).join('');
const library=uniqueResources.map(r=>`<details class="resource-card" id="resource-${esc(r.id)}"><summary>${esc(r.title)}</summary><p class="metadata">${esc(r.creator)} · ${esc(r.format)} · ${esc(r.level)}</p><p><a href="${esc(r.url)}">Open the resource ↗</a></p><dl><dt>Why read it</dt><dd>${esc(r.why)}</dd><dt>Start with this</dt><dd>${esc(r.first_task)}</dd><dt>Before you begin</dt><dd>${esc(Array.isArray(r.prerequisites)?r.prerequisites.join('; '):r.prerequisites)}</dd><dt>Access & limits</dt><dd>${esc(r.access)} ${esc(r.limitations)}</dd></dl><p class="metadata">Link and scope checked ${esc(r.verified_on)}.</p></details>`).join('');
const body=chapters.map(c=>`<section class="chapter" id="chapter-${num(c.number)}" aria-labelledby="title-${num(c.number)}"><p class="eyebrow">Chapter ${num(c.number)} / 10</p><h2 class="chapter-title" id="title-${num(c.number)}">${esc(c.title)}</h2><div class="chapter-body">${c.html}</div><p class="chapter-end"><a href="#contents">Back to the guide map ↑</a></p></section>${c.number===4?workbench:''}`).join('\n');
const html=`<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Learn to choose, size, model, and test robotic actuators. Ten illustrated chapters, three Fusion design studies, calculation labs, and an interactive sizing workbench."><meta name="color-scheme" content="light"><title>Robotic actuators — From load to motion · Invention Lab</title><link rel="stylesheet" href="assets/guide.css"><script src="assets/guide.js" defer></script></head>
<body><a class="skip-link" href="#main">Skip to guide</a><header class="site-header"><a class="wordmark" href="../../index.html">Invention Lab</a><nav aria-label="Site navigation"><a href="../../handbook/index.html">Handbook</a><a href="../triangulated-pivot/index.html">45° pivot</a><a href="#downloads">Downloads</a><a href="https://github.com/NicholasHazen/invention-lab">GitHub ↗</a></nav></header>
<div class="hero"><div><p class="eyebrow">Mechanisms · CAD · control · experiments</p><h1>From load<br>to motion.</h1><p class="lede">Designing robotic actuators begins with the thing you want to move. Work back through the mechanism, motor, feedback, and power system—then give each decision a test.</p><div class="actions"><a class="button" href="#chapter-01">Start the guide →</a><a class="text-link" href="#sizing-workbench">Try the sizing workbench</a></div><p class="metadata">Robotic actuators · Edition 1.0 · Ten chapters · Three design studies</p></div><aside class="hero-card" aria-label="The three design studies"><h2>Three ways to make it move</h2><ol class="study-list"><li><span class="num">01</span><div><strong>A belt-driven rotary joint</strong><p>Support the output shaft, choose a reduction, and understand torque, speed, and inertia.</p></div></li><li><span class="num">02</span><div><strong>A screw-driven linear stage</strong><p>Turn rotation into travel while separating drive force from guide loads.</p></div></li><li><span class="num">03</span><div><strong>A tendon-driven finger</strong><p>Place the motor remotely and trace leverage, travel, compliance, and contact force.</p></div></li></ol></aside></div>
<p class="evidence"><strong>What you can build from this edition:</strong> editable mechanical layout studies and calculation experiments. The CAD demonstrates placement, dimensions, and motion relationships; purchased components, fits, retention, guards, wiring, and load ratings require a hardware-specific design pass. No actuator prototype has been physically built or validated for this guide.</p>
<div class="layout"><aside class="sidebar" id="contents"><details open><summary>Guide map</summary><ol class="chapter-nav">${nav}</ol><div class="extra-links"><a href="#sizing-workbench">Sizing workbench</a><a href="#downloads">Models & labs</a><a href="#resources">Further study</a><button class="secondary" data-print hidden>Print the guide</button></div></details></aside><main class="guide-main" id="main"><section class="start"><p class="eyebrow">How to use this guide</p><h2>Read, predict, model, measure.</h2><p>You can start without a motor. Work through the load example, change a parameter, and build a CAD layout before selecting hardware. The later chapters show how to turn those decisions into a careful bench experiment.</p><div class="route-grid"><div class="route-card"><strong>Understand the choices</strong>Chapters 1–4 connect actuator families, transmissions, and sizing. Chapter 8 broadens the comparison.</div><div class="route-card"><strong>Build your CAD skills</strong>Chapters 5–7 develop three dimensioned layouts, with Fusion tools, editable files, and inspection checkpoints.</div><div class="route-card"><strong>Prepare a real experiment</strong>Chapters 9–10 connect sensing, power, control, and measurement. Keep the load supported during first checks.</div></div><p class="metadata">No prior electronics build is required. Basic units and sketches help; the <a href="../../handbook/index.html">handbook</a> supplies the foundations. Each chapter includes a prediction, a way to check it, and a useful variation.</p></section>${body}
<section class="downloads" id="downloads"><p class="eyebrow">Keep learning at your desk</p><h2>Models, calculations, and worksheets</h2><p>Keep the guide beside Fusion, inspect the native layouts, and rerun the calculations with your own requirements. The offline bundle includes this guide, its illustrations, the design files, and the executable labs. External references and other Invention Lab guides still need an internet connection.</p><div class="actions"><a class="button" href="downloads/robotic-actuators-v1.0.zip" download>Download the complete guide</a><a class="text-link" href="downloads/manifest.json">File manifest & checksums</a></div><p class="note">Open each design's README before using its CAD files. Layout dimensions are teaching inputs, not a bill of purchased, compatible hardware. The Python labs calculate examples; they do not command motors.</p>${downloadList}<p><a href="https://github.com/NicholasHazen/invention-lab/tree/main/guides/robotic-actuators">Editable chapter and website source on GitHub ↗</a></p></section>
<section class="resources" id="resources"><p class="eyebrow">Go deeper with a purpose</p><h2>A small working library</h2><p>These ${uniqueResources.length} resources come from manufacturers, universities, and original projects. Use the suggested first task to connect a resource to your design. Product documentation is an example of how to read specifications, not an endorsement or a completed part selection.</p>${library}</section></main></div><footer class="site-footer"><p>Invention Lab · Robotic actuators · Edition 1.0<br>Sources checked November 6, 2026. Digital design studies; physical performance remains untested.</p><a href="../../index.html">Explore more projects →</a></footer></body></html>\n`;
// Finish all source reads before replacing this guide's generated directory.
await fs.rm(output,{recursive:true,force:true});await fs.mkdir(path.join(output,'assets'),{recursive:true});
await fs.writeFile(path.join(output,'index.html'),html);
await fs.cp(path.join(source,'assets'),path.join(output,'assets'),{recursive:true});
await fs.copyFile(path.join(source,'web/guide.css'),path.join(output,'assets/guide.css'));
// A classic script keeps the downloaded guide independent of module-fetch rules.
const models=(await fs.readFile(path.join(source,'web/workbench.mjs'),'utf8')).replace(/^export /gm,'');
const ui=(await fs.readFile(path.join(source,'web/guide.js'),'utf8')).replace(/^import .*?;\n/,'');
await fs.writeFile(path.join(output,'assets/guide.js'),`(()=>{\n'use strict';\n${models}\n${ui}\n})();\n`);
for(const {folder,files} of artifactGroups){for(const file of files){await fs.mkdir(path.dirname(path.join(output,folder,file)),{recursive:true});await fs.copyFile(path.join(source,folder,file),path.join(output,folder,file));}}
await fs.mkdir(path.join(output,'downloads'),{recursive:true});
const manifest=[];
for(const file of await listFiles(output)){const content=await fs.readFile(path.join(output,file));manifest.push({path:file,bytes:content.length,sha256:crypto.createHash('sha256').update(content).digest('hex')});}
await fs.writeFile(path.join(output,'downloads/manifest.json'),JSON.stringify({guide:'Robotic actuators',version:'1.0',generated_on:'2026-11-06',status:'Digital layout studies; no physical actuator validation',files:manifest},null,2)+'\n');
console.log(JSON.stringify({output,chapters:chapters.length,words:chapters.reduce((s,c)=>s+c.words,0),resources:uniqueResources.length,artifacts:artifactGroups.reduce((s,g)=>s+g.files.length,0)},null,2));
