(()=>{
'use strict';
// Teaching models in SI units internally. These are demand estimates, not ratings.
function number(value, label, min=0, max=Infinity, strict=false) {
  if (value === '' || value === null || value === undefined) throw new Error(`Enter ${label}.`);
  const n = Number(value);
  if (!Number.isFinite(n) || (strict ? n <= min : n < min) || n > max) throw new Error(`Check ${label}; it must be ${strict ? 'greater than' : 'at least'} ${min}${Number.isFinite(max) ? ` and no more than ${max}` : ''}.`);
  return n;
}
function rotary(p) {
  const mass=number(p.mass,'payload mass'), armMass=number(p.armMass,'arm mass'), length=number(p.length,'arm length',0,Infinity,true)/1000;
  const angle=number(p.angle,'sweep angle',0,360,true)*Math.PI/180, time=number(p.time,'move time',0,Infinity,true);
  const ratio=number(p.ratio,'reduction ratio',0,Infinity,true), eta=number(p.eta,'forward efficiency',0,1,true), friction=number(p.friction,'friction allowance');
  const gravity=(mass+armMass/2)*9.81*length, inertia=(mass+armMass/3)*length**2, alpha=4*angle/time**2;
  const outputRPM=2*angle/time*60/(2*Math.PI), envelope=gravity+inertia*alpha+friction;
  const transmission=envelope/(ratio*eta);
  const rotor = p.rotor === '' || p.rotor === undefined || p.rotor === null ? null : number(p.rotor,'motor rotor inertia')*ratio*alpha;
  const result={gravity,inertia,alpha,outputRPM,motorRPM:outputRPM*ratio,envelope,transmission,rotor,total:rotor===null?null:transmission+rotor};
  if(Object.values(result).some(n=>n!==null&&!Number.isFinite(n))) throw new Error('These inputs exceed the numerical range. Use finite, practical values.');
  return result;
}
function linear(p) {
  const force=number(p.force,'axial resistance'), lead=number(p.lead,'screw lead',0,Infinity,true)/1000, speed=number(p.speed,'linear speed',0,Infinity,true)/1000, eta=number(p.eta,'forward efficiency',0,1,true);
  const result={rpm:speed/lead*60,torque:force*lead/(2*Math.PI*eta),outputPower:force*speed,inputPower:force*speed/eta};
  if(Object.values(result).some(n=>!Number.isFinite(n))) throw new Error('These inputs exceed the numerical range.');
  return result;
}
function tendon(p) {
  const force=number(p.force,'tip force'), tip=number(p.tip,'tip moment arm',0,Infinity,true)/1000, tendon=number(p.tendon,'tendon moment arm',0,Infinity,true)/1000, spool=number(p.spool,'spool radius',0,Infinity,true)/1000, angle=number(p.angle,'finger rotation',0,360)*Math.PI/180;
  const tension=force*tip/tendon, travel=tendon*angle;
  const result={tension,torque:tension*spool,travel:travel*1000,angle:travel/spool*180/Math.PI};
  if(Object.values(result).some(n=>!Number.isFinite(n))) throw new Error('These inputs exceed the numerical range.');
  return result;
}

const format=(n,d=4)=>n.toLocaleString('en-US',{maximumFractionDigits:d});
const row=(label,value,unit)=>`<div><dt>${label}</dt><dd>${value} <span>${unit}</span></dd></div>`;
const calculate={rotary,linear,tendon};
for(const form of document.querySelectorAll('.calculator')) {
  const result=form.querySelector('.calculation-result');
  const update=()=>{
    try {
      const values=Object.fromEntries(new FormData(form));
      const r=calculate[form.dataset.model](values);
      let html;
      if(form.dataset.model==='rotary') html=row('Maximum gravity torque',format(r.gravity),'N·m')+row('Modeled load inertia',format(r.inertia,7),'kg·m²')+row('Acceleration magnitude',format(r.alpha),'rad/s²')+row('Peak output / motor speed',`${format(r.outputRPM)} / ${format(r.motorRPM)}`,'rpm')+row('Conservative output envelope',format(r.envelope),'N·m')+row('Transmission torque subtotal',format(r.transmission,6),'N·m')+(r.rotor===null?row('Motor rotor contribution','Not entered','total not calculated'):row('Motor rotor contribution',format(r.rotor,7),'N·m')+row('Estimated motor envelope',format(r.total,6),'N·m'));
      if(form.dataset.model==='linear') html=row('Screw speed',format(r.rpm),'rpm')+row('Steady screw torque',format(r.torque,6),'N·m')+row('Useful mechanical power',format(r.outputPower),'W')+row('Screw input mechanical power',format(r.inputPower),'W');
      if(form.dataset.model==='tendon') html=row('Ideal tendon tension',format(r.tension),'N')+row('Ideal spool torque',format(r.torque),'N·m')+row('Tendon travel',format(r.travel),'mm')+row('Spool rotation',format(r.angle),'°');
      result.innerHTML=`<dl class="result-grid">${html}</dl>`;
      result.classList.remove('error');
    } catch(error) { result.textContent=error.message; result.classList.add('error'); }
  };
  form.addEventListener('submit',event=>{event.preventDefault();update();});
  form.addEventListener('invalid',()=>{result.textContent='Correct the highlighted input and calculate again. Earlier results have been cleared.';result.classList.add('error');},true);
  form.addEventListener('input',()=>{result.textContent='Inputs changed. Calculate to update the result.';result.classList.remove('error');});
  form.addEventListener('reset',()=>{setTimeout(update,0);});
}
const switcher=document.querySelector('.study-switcher');
if(switcher) {
  switcher.hidden=false;
  const select=switcher.querySelector('select');
  const panels=[...document.querySelectorAll('.study-panel')];
  const change=()=>panels.forEach(panel=>panel.hidden=panel.id!==select.value);
  select.addEventListener('change',change);change();
}
const printButton=document.querySelector('[data-print]');
if(printButton){printButton.hidden=false;printButton.addEventListener('click',()=>window.print());}
let printDetails=[];
window.addEventListener('beforeprint',()=>{
  printDetails=[...document.querySelectorAll('main details')].map(el=>({el,open:el.open}));
  printDetails.forEach(({el})=>{el.open=true;});
});
window.addEventListener('afterprint',()=>{printDetails.forEach(({el,open})=>{el.open=open;});printDetails=[];});
const chapterLinks=[...document.querySelectorAll('.chapter-nav a')];
if('IntersectionObserver' in window) {
  const observer=new IntersectionObserver(entries=>{
    for(const entry of entries) if(entry.isIntersecting) {
      chapterLinks.forEach(link=>{if(link.hash===`#${entry.target.id}`)link.setAttribute('aria-current','location');else link.removeAttribute('aria-current');});
    }
  },{rootMargin:'-8% 0px -65% 0px'});
  document.querySelectorAll('section.chapter').forEach(section=>observer.observe(section));
}

})();
