// Teaching models in SI units internally. These are demand estimates, not ratings.
function number(value, label, min=0, max=Infinity, strict=false) {
  if (value === '' || value === null || value === undefined) throw new Error(`Enter ${label}.`);
  const n = Number(value);
  if (!Number.isFinite(n) || (strict ? n <= min : n < min) || n > max) throw new Error(`Check ${label}; it must be ${strict ? 'greater than' : 'at least'} ${min}${Number.isFinite(max) ? ` and no more than ${max}` : ''}.`);
  return n;
}
export function rotary(p) {
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
export function linear(p) {
  const force=number(p.force,'axial resistance'), lead=number(p.lead,'screw lead',0,Infinity,true)/1000, speed=number(p.speed,'linear speed',0,Infinity,true)/1000, eta=number(p.eta,'forward efficiency',0,1,true);
  const result={rpm:speed/lead*60,torque:force*lead/(2*Math.PI*eta),outputPower:force*speed,inputPower:force*speed/eta};
  if(Object.values(result).some(n=>!Number.isFinite(n))) throw new Error('These inputs exceed the numerical range.');
  return result;
}
export function tendon(p) {
  const force=number(p.force,'tip force'), tip=number(p.tip,'tip moment arm',0,Infinity,true)/1000, tendon=number(p.tendon,'tendon moment arm',0,Infinity,true)/1000, spool=number(p.spool,'spool radius',0,Infinity,true)/1000, angle=number(p.angle,'finger rotation',0,360)*Math.PI/180;
  const tension=force*tip/tendon, travel=tendon*angle;
  const result={tension,torque:tension*spool,travel:travel*1000,angle:travel/spool*180/Math.PI};
  if(Object.values(result).some(n=>!Number.isFinite(n))) throw new Error('These inputs exceed the numerical range.');
  return result;
}
