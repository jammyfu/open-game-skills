import * as THREE from 'three';
import {GLTFLoader} from '/runtime/vendor/three/examples/jsm/loaders/GLTFLoader.js';
import {CombatWorld,replay,normalChecks} from './simulation.mjs';
import {AssetPool} from './asset-pool.mjs';

const result={engine:{name:'three.js',revision:THREE.REVISION},scenarios:[],negative_controls:[],traces:{},overrides:['controlled-presentation-deltas','async-delivery-gates','synthetic-combat-contact'],session_mode:'replay-input + scripted-scene'};
const target=document.querySelector('#viewport');
const renderer=new THREE.WebGLRenderer({antialias:true,preserveDrawingBuffer:true});
renderer.setSize(target.clientWidth,target.clientHeight);renderer.setPixelRatio(1);target.append(renderer.domElement);renderer.domElement.tabIndex=0;
const gl=renderer.getContext(),debug=gl.getExtension('WEBGL_debug_renderer_info');
Object.assign(result.engine,{webgl:gl.getParameter(gl.VERSION),vendor:gl.getParameter(gl.VENDOR),renderer:debug?gl.getParameter(debug.UNMASKED_RENDERER_WEBGL):gl.getParameter(gl.RENDERER)});
const scene=new THREE.Scene();scene.background=new THREE.Color(0x142237);
const camera=new THREE.PerspectiveCamera(42,target.clientWidth/target.clientHeight,0.1,100);camera.position.set(5.5,5.5,11);camera.lookAt(0,1.4,0);
scene.add(new THREE.HemisphereLight(0xffffff,0x526375,2.5));const sun=new THREE.DirectionalLight(0xffffff,3);sun.position.set(3,6,6);scene.add(sun);
const floor=new THREE.Mesh(new THREE.PlaneGeometry(20,20),new THREE.MeshStandardMaterial({color:0x24364c,roughness:1}));floor.rotation.x=-Math.PI/2;scene.add(floor);
const grid=new THREE.GridHelper(20,20,0x48607a,0x2c4158);grid.position.y=.01;scene.add(grid);
const loader=new GLTFLoader();const assetUrl='/runtime/fixtures/banner_blue.gltf.glb';
function draw(){renderer.render(scene,camera);}
function memory(){return {...renderer.info.memory};}
function resources(root) {
  const geometries=new Set(),materials=new Set(),textures=new Set();
  root.traverse(o=>{if(!o.isMesh)return;geometries.add(o.geometry);for(const m of [].concat(o.material)){materials.add(m);for(const value of Object.values(m))if(value?.isTexture)textures.add(value);}});
  return {geometries,materials,textures};
}
function dispose(resource){
  const r=resources(resource.scene);for(const t of r.textures){t.dispose();t.source?.data?.close?.();}for(const m of r.materials)m.dispose();for(const g of r.geometries)g.dispose();
}
async function load(){return loader.loadAsync(assetUrl);}
const equal=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
function check(id,expected,observed,predicate){const row={id,status:predicate?'pass':'fail',expected,observed};result.scenarios.push(row);return row;}
function rowSummary(){document.querySelector('#checks').innerHTML=result.scenarios.map(r=>`<div class="row"><span>${r.id}</span><b class="${r.status}">${r.status.toUpperCase()}</b></div>`).join('');}
function deferred(){let resolve;const promise=new Promise(r=>resolve=r);return {promise,resolve};}
let nativeWorld=new CombatWorld(),edges=[],pressed=new Set(),edgeNumber=0;
renderer.domElement.addEventListener('keydown',event=>{
  if(!['Space','KeyC'].includes(event.code))return;event.preventDefault();
  if(event.repeat||pressed.has(event.code))return;pressed.add(event.code);
  edges.push({id:`native-${++edgeNumber}`,actor:'A',action:event.code==='Space'?'attack':'cancel',trusted:event.isTrusted});
});
renderer.domElement.addEventListener('keyup',e=>pressed.delete(e.code));
renderer.domElement.addEventListener('blur',()=>pressed.clear());
window.__lab={result,ready:false,armInput(){nativeWorld=new CombatWorld();edges=[];pressed.clear();edgeNumber=0;renderer.domElement.focus();},stepInput(n){for(let i=0;i<n;i++){nativeWorld.step(edges);edges=[];}return {tick:nativeWorld.tick,events:nativeWorld.events,trace:nativeWorld.trace};},nativeSnapshot(){return {events:nativeWorld.events,trace:nativeWorld.trace};}};

async function run() {
  draw();const baseline=memory();
  const gltf=await load(),rs=resources(gltf.scene);
  let vertices=0,triangles=0;for(const g of rs.geometries){vertices+=g.attributes.position.count;triangles+=(g.index?.count??g.attributes.position.count)/3;}
  const dimensions=[...rs.textures].map(t=>[t.image.width,t.image.height]);
  check('GLB-and-texture-decode','geometry and decoded image',{meshes:rs.geometries.size,vertices,triangles,dimensions},vertices>0&&dimensions.length>0&&dimensions.every(([w,h])=>w>0&&h>0));
  const actors=['A','B','C'].map((id,i)=>{const o=gltf.scene.clone(true);o.position.set((i-1)*2.8,0,0);o.name=id;scene.add(o);return o;});
  draw();const pixels=new Uint8Array(64*64*4);gl.readPixels(0,0,64,64,gl.RGBA,gl.UNSIGNED_BYTE,pixels);
  const glError=gl.getError();
  check('WebGL-draw','nonempty geometry draw',{calls:renderer.info.render.calls,triangles:renderer.info.render.triangles,error:glError},renderer.info.render.calls>0&&renderer.info.render.triangles>=triangles&&glError===gl.NO_ERROR);
  const canonical=replay(60);
  for(const hz of [30,60,144])for(const reverse of [false,true]) {
    const r=replay(hz,{reverse,draw:w=>{actors[2].position.x=2.8+(w.actor('C').x-300)/100;draw();}});
    const id=`replay-${hz}-${reverse?'reversed':'forward'}`;
    check(id,'same complete logical trace', {ticks:r.ticks,presentationFrames:r.frames,traceEqual:equal(r.trace,canonical.trace)},equal(r.trace,canonical.trace));
    result.traces[id]=r;
  }
  for(const c of normalChecks(canonical))check(c.id,c.expected,c.observed,c.pass);
  const cancel=replay(60,{cancel:true});result.traces['cancel-during-freeze']=cancel;
  const ce=cancel.events.filter(e=>e.type==='cancel');
  check('buffered-cancel-once',{count:1,tick:7},{count:ce.length,tick:ce[0]?.tick},ce.length===1&&ce[0].tick===7);
  for(const mutant of ['global-freeze','repeat-contact','sequential-trade']) {
    const observation=replay(60,{mutant}),failed=normalChecks(observation).filter(c=>!c.pass);
    result.negative_controls.push({mutant,status:failed.length?'detected':'survived',failed_assertions:failed});result.traces[mutant]=observation;
  }
  // Remove the showcase before taking resource lifetime baselines.
  actors.forEach(o=>scene.remove(o));dispose(gltf);draw();
  const clean=memory();check('showcase-cleanup',baseline,clean,equal(baseline,clean));
  const pool=new AssetPool(load,dispose),a=pool.acquire('banner@1'),b=pool.acquire('banner@1');
  const [ar,br]=await Promise.all([a.ready,b.ready]);
  const ac=ar.scene.clone(true),bc=br.scene.clone(true);scene.add(ac,bc);draw();const allocated=memory();
  scene.remove(ac);a.release();draw();const held=memory();
  check('shared-lease-survives',{loads:1,same:true,disposed:0,memory:allocated},{loads:pool.stats.loads,same:ar===br,disposed:pool.stats.disposed,memory:held},pool.stats.loads===1&&ar===br&&pool.stats.disposed===0&&equal(held,allocated));
  scene.remove(bc);b.release();b.release();draw();check('last-lease-disposes-once',{disposed:1,memory:clean},{disposed:pool.stats.disposed,memory:memory()},pool.stats.disposed===1&&equal(memory(),clean));
  // Gate a REAL parsed GLB delivery, not a dummy resource.
  const gate=deferred(),parsed=deferred();let current=true;
  const late=new AssetPool(async()=>{const value=await load();parsed.resolve();await gate.promise;return value;},dispose);
  const lease=late.acquire('late',()=>current);await parsed.promise;current=false;gate.resolve();
  const lateValue=await lease.ready;
  check('stale-session-rejected',{attached:false,disposed:1},{attached:!!lateValue,disposed:late.stats.disposed},lateValue===null&&late.stats.disposed===1);
  const cancelGate=deferred(),cancelParsed=deferred();
  const shared=new AssetPool(async()=>{const value=await load();cancelParsed.resolve();await cancelGate.promise;return value;},dispose);
  const x=shared.acquire('shared-loading'),y=shared.acquire('shared-loading');await cancelParsed.promise;x.release();cancelGate.resolve();
  const [xv,yv]=await Promise.all([x.ready,y.ready]);
  check('cancel-one-shared-load',{cancelled:true,otherReady:true,loads:1,disposed:0},{cancelled:xv===null,otherReady:!!yv,loads:shared.stats.loads,disposed:shared.stats.disposed},xv===null&&!!yv&&shared.stats.loads===1&&shared.stats.disposed===0);y.release();
  let attempt=0;const retry=new AssetPool(async()=>{if(++attempt===1)throw new Error('injected transient delivery failure');return load();},dispose);
  let failure='';try{await retry.acquire('retry').ready;}catch(e){failure=e.message;}
  const successful=retry.acquire('retry'),rv=await successful.ready;
  check('failure-retry', {failure:true,retried:true,attempts:2},{failure:!!failure,retried:!!rv,attempts:attempt},!!failure&&!!rv&&attempt===2);successful.release();
  const samples=[];for(let i=0;i<8;i++){const p=new AssetPool(load,dispose),l=p.acquire(`loop-${i}`),r=await l.ready;scene.add(r.scene);draw();scene.remove(r.scene);l.release();draw();samples.push(memory());}
  check('eight-load-unload-cycles','all geometry/texture counts return to baseline',{baseline:clean,samples},samples.every(s=>equal(s,clean)));
  for(const mutant of ['stale-attach','premature-dispose']) {
    const broken=new AssetPool(load,dispose,mutant);
    if(mutant==='stale-attach') {
      const l=broken.acquire('control-stale',()=>false),v=await l.ready;
      result.negative_controls.push({mutant,status:v?'detected':'survived',expected:'null stale result',observed:!!v});l.release();
    } else {
      const l=broken.acquire('control-shared'),r=broken.acquire('control-shared');await Promise.all([l.ready,r.ready]);l.release();
      result.negative_controls.push({mutant,status:broken.stats.disposed!==0?'detected':'survived',expected:0,observed:broken.stats.disposed});r.release();
    }
  }
  // Final screenshot is presentation evidence, not the gameplay oracle.
  const finalModel=await load();['A','B','C'].forEach((id,i)=>{const o=finalModel.scene.clone(true);o.position.x=(i-1)*2.8;scene.add(o);});draw();
  const failures=result.scenarios.filter(r=>r.status==='fail');
  result.status=failures.length||result.negative_controls.some(r=>r.status!=='detected')?'fail':'pass';
  document.querySelector('#badge').textContent=`${result.scenarios.length} CHECKS / ${result.negative_controls.length} CONTROLS`;
  document.querySelector('#trace').textContent=`PROJECT CLOCK  60 ticks/s     CONTACT ID  attack × victim\nA/B frozen 4 ticks · C advances all 120 ticks · no duplicate contact\nSOURCE GLB  ${vertices} vertices / ${triangles} triangles · textured CC0 input`;
  rowSummary();window.__lab.ready=true;return result;
}
window.__lab.completion=run().catch(error=>{result.status='blocked';result.error=String(error.stack||error);window.__lab.ready=true;document.querySelector('#trace').textContent=result.error;return result;});
