/** Minimal project-specific combat runtime. Test seed: 60 simulation ticks/s.
 * Presentation schedules never own gameplay time. Mutants are named negative
 * controls, not alternative production policies or claimed agent mistakes.
 */
export class CombatWorld {
  constructor({reverse=false,mutant='none'}={}) {
    this.tick=0;this.events=[];this.trace=[];this.inputIds=new Set();this.hitIds=new Set();
    this.mutant=mutant;
    this.actors=['A','B','C'].map((id,i)=>({id,x:i===2?300:i*80,clock:0,freeze:0,hp:100,move:null,pending:null}));
    if(reverse)this.actors.reverse();
  }
  actor(id){return this.actors.find(a=>a.id===id);}
  start(actor,id){actor.move={id,age:0,born:this.tick,hit:false};}
  step(inputs=[]) {
    // Phase 1: accept semantic edges once, including during actor freeze.
    for(const input of [...inputs].sort((a,b)=>a.id.localeCompare(b.id))) {
      if(this.inputIds.has(input.id))continue;this.inputIds.add(input.id);
      const a=this.actor(input.actor);if(!a)throw new Error('Unknown actor');
      this.events.push({type:'input',tick:this.tick,id:input.id,actor:a.id,action:input.action});
      if(input.action==='attack'&&!a.move)this.start(a,input.id);
      if(input.action==='cancel'&&a.move?.hit&&!a.pending)a.pending=input.id;
    }
    // Phase 2: snapshot frozen set, then advance eligible actors only.
    const frozen=new Set(this.actors.filter(a=>a.freeze>0).map(a=>a.id));
    if(this.mutant==='global-freeze'&&frozen.size)for(const a of this.actors)frozen.add(a.id);
    for(const a of this.actors) {
      if(frozen.has(a.id)){a.freeze=Math.max(0,a.freeze-1);continue;}
      a.clock++;if(a.id==='C')a.x++;
      if(a.move&&a.move.born!==this.tick)a.move.age++;
    }
    // Phase 3: collect all eligible contacts before changing hit outcomes.
    const contacts=[];
    for(const a of this.actors) {
      if(frozen.has(a.id)||!a.move||a.move.age<2||a.move.age>5)continue;
      for(const b of this.actors)if(b.id!==a.id&&Math.abs(a.x-b.x)<=110)
        contacts.push({a,b,id:`${a.move.id}:${b.id}`});
    }
    contacts.sort((x,y)=>x.id.localeCompare(y.id));
    // Phase 4: commit simultaneous trades and coalesce sustained overlaps.
    for(const hit of contacts) {
      if(this.mutant==='sequential-trade'&&hit.a.freeze>0)continue;
      if(this.mutant!=='repeat-contact'&&this.hitIds.has(hit.id))continue;
      this.hitIds.add(hit.id);hit.b.hp-=10;hit.a.move.hit=true;
      hit.a.freeze=hit.b.freeze=4;
      this.events.push({type:'hit',tick:this.tick,id:hit.id,actor:hit.a.id,victim:hit.b.id});
    }
    // Phase 5: queued cancels start once after freeze, within authored window.
    for(const a of this.actors)if(!frozen.has(a.id)&&a.freeze===0) {
      if(a.pending&&a.move?.hit&&a.move.age<=5) {
        const id=a.pending;a.pending=null;this.start(a,id);
        this.events.push({type:'cancel',tick:this.tick,id,actor:a.id});
      }
      if(a.move?.age>=7){a.move=null;a.pending=null;}
    }
    this.trace.push({tick:this.tick,actors:[...this.actors].sort((a,b)=>a.id.localeCompare(b.id)).map(a=>({
      id:a.id,clock:a.clock,freeze:a.freeze,hp:a.hp,x:a.x,move:a.move?{...a.move}:null,pending:a.pending
    }))});
    this.tick++;
  }
}

export function replay(renderHz,{cancel=false,draw=()=>{},...options}={}) {
  if(![30,60,144].includes(renderHz))throw new Error('Unsupported test presentation schedule');
  const w=new CombatWorld(options);let accumulator=0,frames=0;
  const tape=[{tick:0,id:'press-a',actor:'A',action:'attack'},{tick:0,id:'press-b',actor:'B',action:'attack'}];
  if(cancel)tape.push({tick:3,id:'cancel-a',actor:'A',action:'cancel'},{tick:4,id:'cancel-a',actor:'A',action:'cancel'});
  while(w.tick<120) {
    accumulator+=60/renderHz;
    while(accumulator>=1-1e-9&&w.tick<120) {
      w.step(tape.filter(e=>e.tick===w.tick));accumulator-=1;
    }
    draw(w);frames++;
  }
  return {renderHz,frames,ticks:w.tick,trace:w.trace,events:w.events,tape};
}

export function normalChecks(result) {
  const final=result.trace.at(-1),c=final.actors.find(a=>a.id==='C');
  const hits=result.events.filter(e=>e.type==='hit');
  const checks=[
    {id:'unrelated-actor-progress',expected:120,observed:c.clock,pass:c.clock===120},
    {id:'one-hit-per-attack-victim',expected:2,observed:hits.length,pass:hits.length===2&&new Set(hits.map(h=>h.id)).size===2},
    {id:'simultaneous-trade',expected:['A>B','B>A'],observed:hits.filter(h=>h.tick===2).map(h=>`${h.actor}>${h.victim}`),pass:hits.filter(h=>h.tick===2).length===2},
    {id:'four-tick-local-stop',expected:4,observed:120-final.actors.find(a=>a.id==='A').clock,pass:final.actors.find(a=>a.id==='A').clock===116}
  ];
  return checks;
}
