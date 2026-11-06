import test from 'node:test';
import assert from 'node:assert/strict';
import {rotary,linear,tendon} from '../guides/robotic-actuators/web/workbench.mjs';
const common={mass:.25,armMass:.08,length:100,angle:90,time:1,ratio:3,eta:.9,friction:.01,rotor:''};
const close=(a,b)=>assert.ok(Math.abs(a-b)<1e-9,`${a} != ${b}`);
test('rotary reference quantities agree with independent worked example',()=>{
 const r=rotary(common);close(r.gravity,.28449);close(r.inertia,.002766666666666667);close(r.alpha,2*Math.PI);close(r.outputRPM,30);close(r.motorRPM,90);close(r.envelope,.31187347914986354);close(r.transmission,.11550869598143094);assert.equal(r.total,null);
});
test('blank rotor remains incomplete; explicit rotor is accelerated at motor speed',()=>{
 assert.equal(rotary({...common,rotor:null}).rotor,null);const r=rotary({...common,rotor:.00001});close(r.rotor,.0001884955592153876);close(r.total,.11569719154064633);
});
test('length and move-time variations follow physical scaling',()=>{
 const r=rotary(common),long=rotary({...common,length:200}),fast=rotary({...common,time:.5});close(long.gravity/r.gravity,2);close(long.inertia/r.inertia,4);close(fast.alpha/r.alpha,4);close(fast.outputRPM/r.outputRPM,2);
});
test('screw power balances assumed forward efficiency',()=>{
 const r=linear({force:10,lead:2,speed:20,eta:.35});close(r.rpm,600);close(r.torque,.009094568176679734);close(r.outputPower,.2);close(r.inputPower,.5714285714285715);close(r.torque*r.rpm*Math.PI/30,r.inputPower);
});
test('tendon constant-radius work is conserved',()=>{
 const r=tendon({force:5,tip:30,tendon:10,spool:8,angle:60});close(r.tension,15);close(r.torque,.12);close(r.travel,10.471975511965976);close(r.angle,75);close(r.tension*r.travel/1000,r.torque*r.angle*Math.PI/180);
});
test('invalid, empty, nonfinite and impossible efficiencies are rejected',()=>{
 for(const values of [{time:0},{eta:0},{eta:1.1},{mass:-1},{length:''},{rotor:-1},{ratio:Infinity},{angle:361},{time:NaN}]) assert.throws(()=>rotary({...common,...values}));
 assert.throws(()=>linear({force:10,lead:0,speed:20,eta:.35}));assert.throws(()=>tendon({force:5,tip:30,tendon:0,spool:8,angle:60}));
 assert.throws(()=>linear({force:10,lead:2,speed:0,eta:.35}));
});
