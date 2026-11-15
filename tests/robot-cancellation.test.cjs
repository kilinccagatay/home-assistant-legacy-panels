const assert=require('node:assert/strict'),M=require('../examples/panel-v2/robot-map.js');
let requests=[],timers=[],aborted=0,frames=[];
function read(cb){const r={cb,cancelled:false};requests.push(r);return ()=>{r.cancelled=true;aborted++;};}
const m=M.create({fetchProgress:read,fetchMap:read,fetchTelemetry:read,telemetry:()=>{},progress:()=>{},frame:x=>frames.push(x),clear:()=>{},unavailable:()=>{},setTimeout:(fn,ms)=>{let t={fn,ms};timers.push(t);return t;},clearTimeout:t=>{timers=timers.filter(x=>x!==t);}});
m.sync(true,true);assert.equal(requests.length,3);assert.equal(timers.length,0,'slow responses cannot queue another poll');m.sync(false,true);assert.equal(aborted,3);requests[1].cb(null,{state:'late'});assert.deepEqual(frames,[]);assert.equal(timers.length,0);
m.sync(true,true);requests[3].cb(null,{state:'50'});assert.equal(timers.length,0);requests[4].cb(null,{state:'new'});requests[5].cb([]);assert.deepEqual(timers.map(t=>t.ms),[15000,5000]);m.sync(false,true);assert.equal(aborted,3,'completed requests do not need abort');assert.equal(timers.length,0);
let cancel=0;const select=M.createSelection({now:()=>0,setTimeout:()=>1,clearTimeout:()=>{},fetch:()=>()=>cancel++,open:()=>{}});select.tap({id:1},0,0);select.reset();assert.equal(cancel,1);
console.log('Pending polls and room reads abort, completed reads release, slow reads cannot overlap, stale callbacks ignored PASS');
