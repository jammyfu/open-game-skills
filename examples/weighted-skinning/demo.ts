import {Application,Assets,Mesh,MeshGeometry,Graphics,Container} from 'pixi.js';
import {readModel,underNoSkin,poseRawAnimation} from 'rig-c/core';

const app=new Application();
await app.init({width:1120,height:610,background:0x172235,antialias:true,resolution:Math.min(devicePixelRatio,2),autoDensity:true});
document.querySelector('#stage')!.appendChild(app.canvas);
const texture=await Assets.load('./arm-setup.png');
const ink=await (await fetch('./ink-triangles.json')).json();
const panes:any[]=[];
for(const [i,name] of ['narrow','current'].entries()){
 const model=underNoSkin(readModel(await (await fetch(`./${name}.model.json`)).text()));
 const initial=poseRawAnimation(model,'bend',[0]).at(-1)!,source=initial.drawn[0];
 const positions=new Float32Array(source.vertices.length);
 const geometry=new MeshGeometry({positions,uvs:new Float32Array(source.uvs),indices:new Uint32Array(source.triangles)});
 const group=new Container();const background=new Graphics().roundRect(12,12,536,586,14).fill(0x202d40);
 const mesh=new Mesh({geometry,texture});const overlay=new Graphics();group.addChild(background,mesh,overlay);group.x=i*560;app.stage.addChild(group);
 const area=(v:number[],a:number,b:number,c:number)=>(v[b*2]-v[a*2])*(v[c*2+1]-v[a*2+1])-(v[b*2+1]-v[a*2+1])*(v[c*2]-v[a*2]);
 const restAreas=Array.from({length:source.triangles.length/3},(_,j)=>area(source.vertices,...source.triangles.slice(j*3,j*3+3)));
 panes.push({model,positions,geometry,source,overlay,restAreas,area});
}
const slider=document.querySelector<HTMLInputElement>('#time')!,play=document.querySelector<HTMLButtonElement>('#play')!;
const bones=document.querySelector<HTMLInputElement>('#bones')!,wire=document.querySelector<HTMLInputElement>('#wire')!,folds=document.querySelector<HTMLInputElement>('#folds')!;
const slow=document.querySelector<HTMLInputElement>('#slow')!;
let playing=true,t=1;
document.querySelector<HTMLButtonElement>('#zoom')!.onclick=()=>{
 const stage=document.querySelector('#stage')!,on=stage.classList.toggle('zoom');
 const button=document.querySelector<HTMLButtonElement>('#zoom')!;button.textContent=on?'Fit comparison':'Full size';button.setAttribute('aria-pressed',String(on));
};
play.onclick=()=>{playing=!playing;play.textContent=playing?'Pause':'Play';play.setAttribute('aria-pressed',String(!playing));};
slider.oninput=()=>{playing=false;play.textContent='Play';play.setAttribute('aria-pressed','true');t=Number(slider.value);draw();};
function draw(){
 let highlighted=0;
 for(const pane of panes){
  const pose=poseRawAnimation(pane.model,'bend',[t]).at(-1)!,v=pose.drawn[0].vertices;
  const x=(n:number)=>33+(n+2)*13,y=(n:number)=>555-(n+3)*13;
  for(let i=0;i<v.length;i+=2){pane.positions[i]=x(v[i]);pane.positions[i+1]=y(v[i+1]);}
  pane.geometry.getBuffer('aPosition').update();const g=pane.overlay;g.clear();
  const tri=pane.source.triangles;
  for(let i=0;i<tri.length;i+=3){
   const [a,b,c]=tri.slice(i,i+3);const bad=pane.area(v,a,b,c)*pane.restAreas[i/3]<0&&ink[i/3];
   if(wire.checked||folds.checked&&bad){
    g.moveTo(pane.positions[a*2],pane.positions[a*2+1]).lineTo(pane.positions[b*2],pane.positions[b*2+1]).lineTo(pane.positions[c*2],pane.positions[c*2+1]).closePath();
    if(folds.checked&&bad){g.fill({color:0xff525f,alpha:.65});highlighted++;}
    if(wire.checked)g.stroke({color:0x77c7ed,alpha:.22,width:.6});
   }
  }
  if(bones.checked){
   const chain=['upper_arm','forearm','wrist'].map(name=>pose.bones.find((b:any)=>b.name===name)!);
   for(let i=0;i<chain.length;i++){
    const b=chain[i];if(i)g.moveTo(x(chain[i-1].worldX),y(chain[i-1].worldY)).lineTo(x(b.worldX),y(b.worldY)).stroke({color:0x8ef1ce,width:2.5});
    g.circle(x(b.worldX),y(b.worldY),4).fill(0xeafffa);
   }
  }
 }
 slider.value=String(t);
 document.querySelector('#clock')!.textContent=`${t.toFixed(2)}s / 2.00s · ${Math.round(90*(1-Math.abs(t-1)))}° flexion`;
 document.querySelector('#live')!.textContent=`${highlighted} ink-touching inverted triangles highlighted at this pose`;
}
for(const input of [bones,wire,folds])input.onchange=()=>draw();
app.ticker.add(ticker=>{if(!playing)return;t=(t+Math.min(ticker.deltaMS,100)/1000*(slow.checked ? .25 : 1))%2;draw();});
document.querySelector('#loading')!.remove();draw();
