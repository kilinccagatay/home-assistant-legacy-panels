const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const {JSDOM}=require('jsdom');
const root=path.resolve(__dirname,'..'),base=JSON.parse(fs.readFileSync(path.join(root,'examples/panel-v2/config.example.json')));
const cfg={...base,profile:'office',robotEnabled:false,nativeBatteryBadge:false,agenda:'sensor.example_agenda'};
const dom=new JSDOM('<body>'+['Ana','Işıklar','Diğer'].map(x=>'<main class="screen" id="screen-'+x+'"></main>').join(''),{url:'http://panel.test/office/#screen-Ana',runScripts:'outside-only',pretendToBeVisual:true});
const w=dom.window,d=w.document,states={};w.HTMLMediaElement.prototype.play=()=>Promise.resolve();w.PANEL_V2_CONFIG=cfg;w.entityListeners={[cfg.agenda]:[]};w.onHaReady=[];w.haSocketReady=true;
const now=Date.now()/1000,day=new Date();day.setHours(0,0,0,0);
states[cfg.agenda]={entity_id:cfg.agenda,state:'ready',attributes:{valid_until:now+90,day_start:day.getTime()/1000,events:[{title:'<img src=x onerror=alert(1)>',start:now+60,end:now+120},{title:'Synthetic next',start:now+300,end:now+600},{title:'Later example',start:now+1200,end:now+1800}]}};
w.goFetch=(url,cb)=>cb(null,states[decodeURIComponent(url.split('/states/')[1].split('?')[0])]);w.haSend=()=>Promise.reject(Error('read-only fixture'));
for(const file of ['core.js','panel.js'])w.eval(fs.readFileSync(path.join(root,'examples/panel-v2',file),'utf8'));
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{try{
 d.dispatchEvent(new w.Event('DOMContentLoaded'));await sleep(30);
 function update(){const s=states[cfg.agenda];for(const cb of w.entityListeners[cfg.agenda])cb(s.state,s.attributes);}
 update();await sleep(30);
 if(process.env.AGENDA_PREVIEW){
   const css=['panel.css','office.css'].map(f=>fs.readFileSync(path.join(root,'examples/panel-v2',f),'utf8')).join('\n');
   const safe=d.documentElement.outerHTML.replace('</head>','<style>html,body{margin:0;height:100%;}.screen{height:100vh;}#screen-Işıklar,#screen-Diğer{display:none;}'+css+'</style></head>');
   fs.writeFileSync(process.env.AGENDA_PREVIEW,safe);
 }
 assert.equal(d.querySelectorAll('#panel-v2 .pv2-card').length,2);
 assert.equal(d.querySelectorAll('.pv2-agenda-event').length,2);
 assert.match(d.querySelector('.pv2-agenda').textContent,/Synthetic next/);
 assert.equal(d.querySelector('.pv2-agenda img'),null,'calendar titles are text, never HTML');
 for(const type of ['touchstart','selectstart','contextmenu']){const hold=new w.Event(type,{bubbles:true,cancelable:true});d.querySelector('.pv2-agenda-title').dispatchEvent(hold);assert(hold.defaultPrevented,'read-only agenda must cancel native '+type);}
 assert.match(d.querySelector('.pv2-agenda-heading').textContent,/Bugün/);
 states[cfg.agenda].attributes.events=[];update();await sleep(20);assert.match(d.querySelector('.pv2-agenda-empty').textContent,/Bugün başka toplantı yok/);
 states[cfg.agenda].attributes.valid_until=now-1;update();await sleep(20);assert.match(d.querySelector('.pv2-agenda-empty').textContent,/Takvim güncellenemiyor/);
 states[cfg.agenda].attributes.valid_until=now+90;w.haSocketReady=false;update();await sleep(20);assert.match(d.querySelector('.pv2-agenda-empty').textContent,/Takvim güncellenemiyor/);
 console.log('Agenda: two-cell layout, two upcoming items, escaped titles, empty versus expired and disconnected states passed.');
}finally{dom.window.close();}})().catch(e=>{console.error(e);process.exitCode=1;});
