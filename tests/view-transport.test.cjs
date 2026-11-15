const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
const requests=[];const host=vm.createContext({XMLHttpRequest:function(){requests.push(this);this.open=()=>{};this.setRequestHeader=()=>{};this.send=()=>{};this.abort=()=>{this.aborted=true;this.onabort();};},entityListeners:{},onHaReady:[]});
vm.runInContext(fs.readFileSync(require('node:path').join(__dirname,'../examples/panel-v2/home-assistant.js'),'utf8'),host);
const h=host.PanelV2HomeAssistant.create(host,{}, {vacuum:'vacuum.example'},()=>{});let replies=0;
let cancel=h.fetchViewState('sensor.example','test',1,()=>replies++);cancel();requests[0].status=200;requests[0].responseText='{}';requests[0].onload();assert.equal(replies,0);assert.equal(requests[0].aborted,true);
cancel=h.fetchRobotRooms(()=>replies++);cancel();requests[1].onerror();assert.equal(replies,0);
h.readJSON('/manifest.json',(err,v)=>{assert.ifError(err);assert.equal(v.version,'v1');replies++;});requests[2].status=200;requests[2].responseText='{"version":"v1"}';requests[2].onload();requests[2].ontimeout();assert.equal(replies,1);
console.log('View GET and room POST aborts suppress callbacks; completion is single-shot PASS');
