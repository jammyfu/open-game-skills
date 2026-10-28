/** bun build_demo.ts /path/to/rig-c@2.79.0 /path/to/pixi.js@8 */
import {resolve} from 'node:path';
import {readFile,writeFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
const tool=resolve(process.argv[2]),pixi=resolve(process.argv[3]),root=resolve(import.meta.dir,'../..'),out=resolve(root,'docs/demos/weighted-skinning');
const pkg=JSON.parse(await readFile(resolve(tool,'package.json'),'utf8'));
if(pkg.name!=='rig-c'||pkg.version!=='2.79.0')throw Error('Expected reviewed rig-c@2.79.0');
const result=await Bun.build({entrypoints:[resolve(import.meta.dir,'demo.ts')],outdir:out,minify:true,target:'browser',plugins:[{name:'explicit-local-tools',setup(builder){
 builder.onResolve({filter:/^rig-c\/core$/},()=>({path:resolve(tool,'src/core/entry.ts')}));
 builder.onResolve({filter:/^pixi\.js$/},()=>({path:resolve(pixi,'lib/index.mjs')}));
}}]});
if(!result.success)throw Error(result.logs.map(String).join('\n'));
for(const file of result.outputs)if(file.path.endsWith('.js'))await writeFile(file.path,(await file.text()).replace(/^[ \t]+$/gm,'').replace(/^}[ \t]+$/gm,'}'));
await writeFile(resolve(out,'THIRD-PARTY-NOTICES.txt'),await readFile(resolve(tool,'LICENSE'),'utf8')+'\n\nPixiJS\n'+await readFile(resolve(pixi,'LICENSE'),'utf8'));
const files=['examples/weighted-skinning/demo.ts','examples/weighted-skinning/build_demo.ts','docs/demos/weighted-skinning/demo.js','docs/demos/weighted-skinning/THIRD-PARTY-NOTICES.txt'];
const hashes=Object.fromEntries(await Promise.all(files.map(async path=>[path,createHash('sha256').update(await readFile(resolve(root,path))).digest('hex')])));
await writeFile(resolve(out,'bundle-manifest.json'),JSON.stringify({schema:'ogs.demo-bundle/1',rigc:pkg.version,pixi:JSON.parse(await readFile(resolve(pixi,'package.json'),'utf8')).version,files:hashes},null,2)+'\n');
console.log('Built static live PixiJS comparison; no external CDN or official Spine runtime.');
