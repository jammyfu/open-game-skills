/** Optional maintainer rebuild. bun rebuild_case.ts /path/to/rig-c@2.79.0 */
import {resolve,join,basename} from 'node:path';
import {mkdtempSync,realpathSync,rmSync,mkdirSync,copyFileSync,readFileSync,writeFileSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {gzipSync} from 'node:zlib';
import {createHash} from 'node:crypto';
const here=import.meta.dir,root=resolve(here,'../..'),tool=realpathSync(resolve(process.argv[2]));
const pkg=JSON.parse(readFileSync(join(tool,'package.json'),'utf8'));
if(pkg.name!=='rig-c'||pkg.version!=='2.79.0')throw Error('Rebuild expects reviewed rig-c@2.79.0');
const {readModel,underNoSkin,poseRawAnimation,poseRawSetup}=await import(join(tool,'src/core/entry.ts'));
const demo=join(root,'docs/demos/weighted-skinning');mkdirSync(demo,{recursive:true});mkdirSync(join(here,'cases'),{recursive:true});
const temp=realpathSync(mkdtempSync(join(tmpdir(),'ogs-skin-case-')));
function command(args:string[]){const r=Bun.spawnSync([process.execPath,...args],{stdout:'pipe',stderr:'pipe'});if(r.exitCode)throw Error(new TextDecoder().decode(r.stdout)+new TextDecoder().decode(r.stderr));}
try{
 for(const name of ['current','narrow']){
  const build=join(temp,name);
  command([join(tool,'cli_core.ts'),'build','--rig',join(here,'source',name+'.rig.json'),'--motion',join(here,'source/motion.json'),'--out',build,'--copy-images']);
  const rig=JSON.parse(readFileSync(join(here,'source',name+'.rig.json'),'utf8'));const source=rig.skins.default.arm.arm;
  const document=JSON.parse(readFileSync(join(build,'skeleton.model.json'),'utf8'));
  // rig-c retains its build-to-source texture path in image provenance even
  // under --copy-images. Relocate that reference alongside the public model.
  for(const image of document.images){
   if(basename(image.page.replaceAll('\\','/'))!=='arm-setup.png')throw Error('Unexpected source image in public model');
   image.page='arm-setup.png';
  }
  const text=JSON.stringify(document,null,2)+'\n';const model=underNoSkin(readModel(text));
  const setup=poseRawSetup(model);const poses=poseRawAnimation(model,'bend',Array.from({length:120},()=>1/60));
  const trace={schema:'ogs.skin-trace/1',sampleRate:60,tolerances:{length:1e-5,scale:1e-6,loop:1e-5,weights:1e-6,area:1e-10,alphaThreshold:32},
   boneScales:Object.fromEntries(rig.bones.map((b:any)=>[b.name,[1,1]])),
   segments:[{a:'upper_arm',b:'forearm',length:rig.bones[1].length},{a:'forearm',b:'wrist',length:rig.bones[2].length}],
   meshes:{arm:{image:'arm-setup.png',sha256:createHash('sha256').update(readFileSync(join(here,'source/arm-setup.png'))).digest('hex'),uvs:source.uvs,triangles:source.triangles,weights:source.weights,setupVertices:setup.drawn[0].vertices}},
   frames:poses.map((p:any)=>({t:p.animationTime,bones:Object.fromEntries(p.bones.map((b:any)=>[b.name,{a:b.a,b:b.b,c:b.c,d:b.d,x:b.worldX,y:b.worldY}])),meshes:{arm:p.drawn[0].vertices}})),loops:[{first:0,last:120}],contacts:[],
   provenance:{driver:'rig-c2.79.0 own MIT core',scenario:'two-second joint sweep',officialSpineParser:'not-run',fullCharacterAccepted:false}};
  writeFileSync(join(here,'cases',name+'.trace.json.gz'),gzipSync(JSON.stringify(trace)+'\n',{level:9}));
  writeFileSync(join(demo,name+'.model.json'),text);
  command([join(tool,'cli_core.ts'),'render','--candidate',build,'--animation','bend','--fps','12','--max','640','--viewport','-2,-3,38,33','--poser','core','--out',join(temp,name+'-render')]);
 }
 copyFileSync(join(here,'source/arm-setup.png'),join(demo,'arm-setup.png'));
 // Presentation only; inputs are actual renderer frames from the two builds.
 const python=process.env.PYTHON||'python3';const r=Bun.spawnSync([python,join(here,'make_preview.py'),temp,join(demo,'preview.webp'),join(demo,'preview.gif')],{stdout:'pipe',stderr:'pipe'});
 if(r.exitCode)throw Error(new TextDecoder().decode(r.stderr));
 writeFileSync(join(demo,'rig-c-LICENSE.txt'),readFileSync(join(tool,'LICENSE')));
 const paths=['source/current.rig.json','source/narrow.rig.json','source/motion.json','source/arm-setup.png','rebuild_case.ts','make_preview.py','cases/current.trace.json.gz','cases/narrow.trace.json.gz'].map(p=>'examples/weighted-skinning/'+p)
  .concat(['current.model.json','narrow.model.json','arm-setup.png','ink-triangles.json','preview.gif','preview.webp'].map(p=>'docs/demos/weighted-skinning/'+p));
 const hashes=Object.fromEntries(paths.map(path=>[path,createHash('sha256').update(readFileSync(join(root,path))).digest('hex')]));
 writeFileSync(join(here,'case-manifest.json'),JSON.stringify({schema:'ogs.weighted-skin-case-artifacts/1',rigc:pkg.version,files:hashes},null,2)+'\n');
 console.log('Rebuilt evaluated traces, live models and common-camera preview. No official Spine runtime installed.');
}finally{rmSync(temp,{recursive:true,force:true});}
