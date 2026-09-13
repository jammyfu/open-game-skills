import test from 'node:test';
import assert from 'node:assert/strict';
import {existsSync} from 'node:fs';

async function implementation() {
  assert.ok(existsSync(new URL('./simulation.mjs',import.meta.url)), 'Missing executable combat model');
  assert.ok(existsSync(new URL('./asset-pool.mjs',import.meta.url)), 'Missing executable lease pool');
  return {...await import('./simulation.mjs'), ...await import('./asset-pool.mjs')};
}

test('replay outcome and complete logical trace are invariant across presentation schedules and actor ordering',async()=>{
  const {replay} = await implementation();
  const baseline = replay(60).trace;
  for(const rate of [30,60,144]) for(const reverse of [false,true])
    assert.deepEqual(replay(rate,{reverse}).trace,baseline);
});
test('actor-local freeze, once-only hit, simultaneous trade, and on-hit cancel are observable',async()=>{
  const {replay,normalChecks} = await implementation();
  const checks=normalChecks(replay(60));
  for(const row of checks) assert.equal(row.pass,true,row.id+': '+JSON.stringify(row.observed));
  const cancelled=replay(60,{cancel:true});
  assert.equal(cancelled.events.filter(e=>e.type==='cancel').length,1);
  assert.equal(cancelled.events.filter(e=>e.type==='hit'&&e.actor==='A').length,2);
});
test('the same oracles reject intentionally broken global-freeze and repeat-contact implementations',async()=>{
  const {replay,normalChecks}=await implementation();
  for(const mutant of ['global-freeze','repeat-contact','sequential-trade'])
    assert.ok(normalChecks(replay(60,{mutant})).some(row=>!row.pass),mutant+' must be caught');
});
test('shared loading acquires once, cancels one consumer, disposes on last release',async()=>{
  const {AssetPool}=await implementation();
  let loadCount=0,disposals=0,deliver;
  const resource={id:'synthetic-resource'};
  const pool=new AssetPool(()=>{loadCount++;return new Promise(r=>deliver=r)},()=>disposals++);
  const a=pool.acquire('asset@1'),b=pool.acquire('asset@1');
  await Promise.resolve();a.release();deliver(resource);
  assert.equal(await a.ready,null);assert.equal(await b.ready,resource);
  assert.equal(loadCount,1);assert.equal(disposals,0);
  b.release();b.release();assert.equal(disposals,1);
});
test('a stale session cannot attach a late result; failure does not poison retries',async()=>{
  const {AssetPool}=await implementation();
  let current=true,dispose=0,deliver;
  const pool=new AssetPool(()=>new Promise(r=>deliver=r),()=>dispose++);
  const lease=pool.acquire('asset@1',()=>current);await Promise.resolve();current=false;deliver({});
  assert.equal(await lease.ready,null);assert.equal(dispose,1);
  let count=0;const retry=new AssetPool(()=>++count===1?Promise.reject(new Error('injected failure')):Promise.resolve({}),()=>{});
  await assert.rejects(retry.acquire('asset@1').ready,/injected/);
  const next=retry.acquire('asset@1');assert.ok(await next.ready);next.release();assert.equal(count,2);
});
test('lease oracles also reject stale-attach and premature-dispose controls',async()=>{
  const {AssetPool}=await implementation();
  const stale=new AssetPool(()=>Promise.resolve({id:1}),()=>{},'stale-attach');
  assert.notEqual(await stale.acquire('asset@1',()=>false).ready,null);
  let disposed=0;const early=new AssetPool(()=>Promise.resolve({}),()=>disposed++,'premature-dispose');
  const a=early.acquire('x'),b=early.acquire('x');await Promise.all([a.ready,b.ready]);
  a.release();assert.notEqual(disposed,0);b.release();
});
