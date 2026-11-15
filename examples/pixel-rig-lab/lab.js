'use strict';
const names=['head','torso','upper','forearm','thigh','shin','boot','scarf'];
const imgs={},pixels={},c=document.createElement('canvas');c.width=480;c.height=270;
const ctx=c.getContext('2d',{willReadFrequently:true}),view=document.querySelector('#view'),out=view.getContext('2d',{willReadFrequently:true});
let mode='scene',paused=false,time=0;
const P=(x,y)=>({x,y}),lerp=(a,b,t)=>a+(b-a)*t;
const matrix=(x,y,r=0)=>({a:Math.cos(r),b:Math.sin(r),c:-Math.sin(r),d:Math.cos(r),x,y});
const apply=(m,p)=>P(m.a*p.x+m.c*p.y+m.x,m.b*p.x+m.d*p.y+m.y);
function ik(a,target,l1,l2,sign){const dx=target.x-a.x,dy=target.y-a.y,d=Math.hypot(dx,dy);if(d>l1+l2||d<Math.abs(l1-l2))throw Error('unreachable IK');const q=Math.atan2(dy,dx)+sign*Math.acos(Math.max(-1,Math.min(1,(d*d+l1*l1-l2*l2)/(2*d*l1))));return P(a.x+l1*Math.cos(q),a.y+l1*Math.sin(q));}
function bone(a,b){return matrix(a.x,a.y,Math.atan2(b.y-a.y,b.x-a.x)-Math.PI/2);}
const weights=x=>{if(x<14){let w=Math.max(0,(x-8)/6);return [{bone:'cloth0',weight:1-w},{bone:'cloth1',weight:w}].filter(a=>a.weight>0);}let w=Math.max(0,Math.min(1,(x-22)/10));return [{bone:'cloth1',weight:1-w},{bone:'cloth2',weight:w}].filter(a=>a.weight>0);};
const ease=u=>u*u*(3-2*u);
function channel(t,keys){for(let i=1;i<keys.length;i++)if(t<=keys[i][0]){let u=ease((t-keys[i-1][0])/(keys[i][0]-keys[i-1][0]));return lerp(keys[i-1][1],keys[i][1],u);}return keys.at(-1)[1];}
function pose(t){t=((t%4)+4)%4;
 // A continuously eased beat avoids long holds followed by one-sample arm jumps.
 const beat=(1-Math.cos(t*Math.PI/2))/2;
 const anticipation=Math.sin(beat*Math.PI);
 const reach=beat*beat;
 const follow=Math.max(0,-Math.sin(t*Math.PI/2))*.2;
 const hip=P(225+2*anticipation+1.5*reach,127+4*anticipation-reach+follow);
 const joints={hip,neck:P(hip.x,hip.y-32),lh:P(hip.x-7,hip.y),rh:P(hip.x+7,hip.y),la:P(210,175),ra:P(241,175),ls:P(hip.x-11,hip.y-23),rs:P(hip.x+12,hip.y-23)};
 joints.lk=ik(joints.lh,joints.la,25,26,-1);joints.rk=ik(joints.rh,joints.ra,25,26,-1);
 joints.lw=P(204+19*anticipation+18*reach,150-14*anticipation-13*reach);
 joints.rw=P(250-10*anticipation+29*reach+5*follow,150-20*anticipation-29*reach-2*follow);
 joints.le=ik(joints.ls,joints.lw,22,28,1);joints.re=ik(joints.rs,joints.rw,22,28,-1);
 const B={root:matrix(hip.x,hip.y),head:matrix(joints.neck.x,joints.neck.y,.035*anticipation-.035*reach),lthigh:bone(joints.lh,joints.lk),lshin:bone(joints.lk,joints.la),lboot:matrix(joints.la.x,joints.la.y),rthigh:bone(joints.rh,joints.rk),rshin:bone(joints.rk,joints.ra),rboot:matrix(joints.ra.x,joints.ra.y),lupper:bone(joints.ls,joints.le),lfore:bone(joints.le,joints.lw),rupper:bone(joints.rs,joints.re),rfore:bone(joints.re,joints.rw),lk:matrix(joints.lk.x,joints.lk.y),rk:matrix(joints.rk.x,joints.rk.y),le:matrix(joints.le.x,joints.le.y),re:matrix(joints.re.x,joints.re.y),lw:matrix(joints.lw.x,joints.lw.y),rw:matrix(joints.rw.x,joints.rw.y)};
 const origin=P(hip.x-12,hip.y-30);let angle=Math.PI+.04*Math.sin(t*Math.PI/2);let joint=origin;
 for(let i=0;i<3;i++){if(i>0)angle+=.07*Math.sin(t*Math.PI/2-i*.55)-.07*Math.sin(-i*.55);B['cloth'+i]=matrix(joint.x,joint.y,angle);joint=apply(B['cloth'+i],P(14,0));}
 return {B,joints,g:reach,phase:t<.45?'IDLE':t<1?'ANTICIPATE':t<1.8?'GATHER':t<2.6?'RELEASE':'SETTLE'};
}
const attachments=[['lthigh','thigh',8,6],['lshin','shin',7,5],['lboot','boot',6,5],['lupper','upper',7,6],['lfore','forearm',7,6],['root','torso',15,34],['rthigh','thigh',8,6],['rshin','shin',7,5],['rboot','boot',6,5],['head','head',16,41],['rupper','upper',7,6],['rfore','forearm',7,6]];
let setup,meshSetup,clothSetup;
function clothVertices(B){const v=[];for(let x of [0,8,14,22,32,43])for(let y of [0,7,15]){let p=P(0,0);for(const w of weights(x)){const local=P(x-Number(w.bone.slice(-1))*14,y-5),q=apply(B[w.bone],local);p.x+=q.x*w.weight;p.y+=q.y*w.weight;}v.push(p.x,p.y);}return v;}
const uv=[],tris=[];for(let x of [0,8,14,22,32,43])for(let y of [0,7,15])uv.push(x/43,y/15);
for(let i=0;i<5;i++)for(let j=0;j<2;j++){let a=i*3+j;tris.push([a,a+3,a+1],[a+3,a+4,a+1]);}
function rasterCloth(B){const v=clothVertices(B),src=pixels.scarf;let dst=ctx.getImageData(0,0,480,270);
 for(const tr of tris){const ids=tr.map(i=>P(v[i*2],v[i*2+1])),a=ids[0],b=ids[1],d=ids[2];let den=(b.y-d.y)*(a.x-d.x)+(d.x-b.x)*(a.y-d.y);if(Math.abs(den)<1e-7)continue;
  for(let y=Math.max(0,Math.floor(Math.min(a.y,b.y,d.y)));y<=Math.min(269,Math.ceil(Math.max(a.y,b.y,d.y)));y++)for(let x=Math.max(0,Math.floor(Math.min(a.x,b.x,d.x)));x<=Math.min(479,Math.ceil(Math.max(a.x,b.x,d.x)));x++){
   const u=((b.y-d.y)*(x+.5-d.x)+(d.x-b.x)*(y+.5-d.y))/den,w=((d.y-a.y)*(x+.5-d.x)+(a.x-d.x)*(y+.5-d.y))/den,z=1-u-w;if(Math.min(u,w,z)<-1e-6)continue;
   const sx=Math.min(42,Math.max(0,Math.floor((uv[tr[0]*2]*u+uv[tr[1]*2]*w+uv[tr[2]*2]*z)*43))),sy=Math.min(14,Math.max(0,Math.floor((uv[tr[0]*2+1]*u+uv[tr[1]*2+1]*w+uv[tr[2]*2+1]*z)*15)));let si=(sy*43+sx)*4,di=(y*480+x)*4;if(src.data[si+3])for(let k=0;k<4;k++)dst.data[di+k]=src.data[si+k];
  }
 }ctx.putImageData(dst,0,0);
}
// Authored 5x7 bitmap labels: no antialiased font pixels inside the native scene.
const glyphs={A:[14,17,17,31,17,17,17],B:[30,17,17,30,17,17,30],C:[15,16,16,16,16,16,15],D:[30,17,17,17,17,17,30],E:[31,16,16,30,16,16,31],F:[31,16,16,30,16,16,16],G:[15,16,16,19,17,17,15],H:[17,17,17,31,17,17,17],I:[31,4,4,4,4,4,31],J:[7,2,2,2,18,18,12],K:[17,18,20,24,20,18,17],L:[16,16,16,16,16,16,31],M:[17,27,21,21,17,17,17],N:[17,25,21,19,17,17,17],O:[14,17,17,17,17,17,14],P:[30,17,17,30,16,16,16],Q:[14,17,17,17,21,18,13],R:[30,17,17,30,20,18,17],S:[15,16,16,14,1,1,30],T:[31,4,4,4,4,4,4],U:[17,17,17,17,17,17,14],V:[17,17,17,17,17,10,4],W:[17,17,17,21,21,21,10],X:[17,17,10,4,10,17,17],Y:[17,17,10,4,4,4,4],Z:[31,1,2,4,8,16,31],0:[14,17,19,21,25,17,14],1:[4,12,4,4,4,4,14],2:[14,17,1,2,4,8,31],3:[30,1,1,14,1,1,30],4:[2,6,10,18,31,2,2],5:[31,16,16,30,1,1,30],6:[14,16,16,30,17,17,14],7:[31,1,2,4,8,8,8],8:[14,17,17,14,17,17,14],9:[14,17,17,15,1,1,14],'/':[1,2,2,4,8,8,16],'-':[0,0,0,31,0,0,0],'+':[0,4,4,31,4,4,0],'|':[4,4,4,4,4,4,4],'>':[16,8,4,2,4,8,16],':':[0,4,4,0,4,4,0]};
function text(x,y,s,color='#ffe3a1',size=12){ctx.fillStyle=color;let pen=Math.round(x);for(const ch of s.toUpperCase()){let g=glyphs[ch]||[0,0,0,0,0,0,0];for(let row=0;row<7;row++)for(let col=0;col<5;col++)if(g[row]&(1<<(4-col)))ctx.fillRect(pen+col,Math.round(y)-7+row,1,1);pen+=6;}}
function drawPart(B,item){const [id,img,px,py]=item,m=B[id];ctx.save();ctx.setTransform(m.a,m.b,m.c,m.d,m.x,m.y);ctx.drawImage(imgs[img],-px,-py);ctx.restore();}
function draw(t,selected=mode){ctx.setTransform(1,0,0,1,0,0);ctx.imageSmoothingEnabled=false;ctx.drawImage(imgs.grove,0,0);const p=pose(t);
 if(selected==='parts'){ctx.fillStyle='#102c32';ctx.fillRect(0,0,480,270);names.forEach((n,i)=>{let x=30+(i%4)*116,y=70+Math.floor(i/4)*110;ctx.strokeStyle='#426359';ctx.strokeRect(x-4,y-4,86,80);ctx.drawImage(imgs[n],x+18,y);text(x,y+91,n);});}
 else{rasterCloth(p.B);attachments.forEach(a=>drawPart(p.B,a));
  if(selected==='scene'&&p.g>.1){const from=p.joints.rw,to=P(328,132);ctx.strokeStyle='#ffdc8b';ctx.beginPath();ctx.arc(from.x,from.y,4+2*p.g,0,Math.PI*2);ctx.stroke();for(let i=0;i<4;i++){const u=(t*1.2+i/4)%1;ctx.fillStyle='#ffe6a2';ctx.fillRect(Math.round(lerp(from.x,to.x,u)),Math.round(lerp(from.y,to.y,u)-Math.sin(u*Math.PI)*7),2,2);}}

  if(selected==='bones'){ctx.strokeStyle='#79ffe0';ctx.lineWidth=1;for(const [a,b]of [['lh','lk'],['lk','la'],['rh','rk'],['rk','ra'],['ls','le'],['le','lw'],['rs','re'],['re','rw'],['hip','neck']]){ctx.beginPath();ctx.moveTo(p.joints[a].x,p.joints[a].y);ctx.lineTo(p.joints[b].x,p.joints[b].y);ctx.stroke();}for(const q of Object.values(p.joints)){ctx.fillStyle='#ffdb74';ctx.fillRect(Math.round(q.x)-1,Math.round(q.y)-1,3,3);}const v=clothVertices(p.B);for(let i=0;i<v.length;i+=2){const x=[0,8,14,22,32,43][Math.floor(i/6)],rgb=[0,0,0];for(const w of weights(x)){const color=[[255,141,122],[255,211,113],[129,220,222]][Number(w.bone.slice(-1))];for(let k=0;k<3;k++)rgb[k]+=color[k]*w.weight;}ctx.fillStyle=`rgb(${rgb.map(Math.round).join(',')})`;ctx.fillRect(Math.round(v[i]),Math.round(v[i+1]),2,2);}text(20,72,'Rigid head / boots | 2-bone foot IK',undefined,11);text(20,88,'Scarf: 3 bones, bounded blend weights',undefined,11);}
 }
 ctx.fillStyle='#0a2027ee';ctx.fillRect(0,0,480,42);text(16,18,'PIXEL RIG / '+selected.toUpperCase());text(16,34,'8 source parts  /  12 rigid instances + cloth', '#a9cfbe',10);
 ctx.fillStyle='#0a2027ee';ctx.fillRect(0,245,480,25);text(16,261,p.phase+'  |  480x270 native -> 2x NEAREST',undefined,11);
 out.imageSmoothingEnabled=false;out.clearRect(0,0,960,540);out.drawImage(c,0,0,960,540);
 if(selected==='compare'){out.fillStyle='#0b2530';out.fillRect(0,0,960,540);let sx=190,sy=50;out.imageSmoothingEnabled=true;out.drawImage(c,sx,sy,100,145,80,70,300,435);out.imageSmoothingEnabled=false;out.drawImage(c,sx,sy,100,145,560,70,300,435);out.fillStyle='#ffe3a1';out.font='20px monospace';out.fillText('LINEAR 3x (rejected)',30,35);out.fillText('NEAREST 3x',520,35);}
 return p;
}
function observed(t){const p=pose(t),meshes={};for(const [id,n,px,py]of attachments){let w=imgs[n].width,h=imgs[n].height;meshes[id]=[P(-px,-py),P(w-px,-py),P(w-px,h-py),P(-px,h-py)].flatMap(q=>{const r=apply(p.B[id],q);return [r.x,r.y]});}meshes.scarf=clothVertices(p.B);return {t,bones:p.B,meshes};}
window.ready=Promise.all([...names,'grove'].map(n=>new Promise((ok,no)=>{const im=new Image();im.onload=()=>{imgs[n]=im;if(n==='scarf'){let cc=document.createElement('canvas');cc.width=43;cc.height=15;let cx=cc.getContext('2d');cx.drawImage(im,0,0);pixels.scarf=cx.getImageData(0,0,43,15);}ok();};im.onerror=no;im.src='assets/'+n+'.png';}))).then(()=>{setup=observed(0);window.lab={render:(t,m)=>{draw(t,m);return view.toDataURL('image/png');},native:()=>c.toDataURL(),observe:observed,meta:()=>({attachments,uv,tris,weights:[0,8,14,22,32,43].flatMap(x=>[0,7,15].map(y=>weights(x))),setup})};draw(0);});
document.querySelectorAll('[data-mode]').forEach(b=>b.onclick=()=>mode=b.dataset.mode);document.querySelector('#pause').onclick=()=>paused=!paused;document.querySelector('#native').onclick=()=>view.style.width=view.style.width==='480px'?'960px':'480px';
let previous;function frame(now){if(previous!==undefined&&!paused)time+=(now-previous)/1000;previous=now;if(window.lab)draw(Math.floor(time*12)/12);requestAnimationFrame(frame);}window.ready.then(()=>requestAnimationFrame(frame));
