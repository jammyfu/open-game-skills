/** Repository-owned driver/oracles; neither is imported from a candidate.
 * 60 ticks/s belongs to this specimen. Controls always use the reference code.
 * This separation is not a security sandbox for adversarial JavaScript.
 */
import {CombatWorld as CandidateWorld} from 'candidate/simulation.mjs';
import {AssetPool as CandidatePool} from 'candidate/asset-pool.mjs';
import {CombatWorld as ControlWorld} from 'reference/simulation.mjs';
import {AssetPool as ControlPool} from 'reference/asset-pool.mjs';

export const CombatWorld = CandidateWorld;
export class AssetPool {
  constructor(load, dispose, mutant = 'none') {
    const Pool = mutant === 'none' ? CandidatePool : ControlPool;
    return new Pool(load, dispose, mutant);
  }
}

export function replay(renderHz, {cancel = false, draw = () => {}, ...options} = {}) {
  if (![30, 60, 144].includes(renderHz)) throw new Error('Unsupported presentation schedule');
  const World = options.mutant && options.mutant !== 'none' ? ControlWorld : CandidateWorld;
  const world = new World(options), trace = [];
  const tape = [{tick: 0, id: 'press-a', actor: 'A', action: 'attack'},
                {tick: 0, id: 'press-b', actor: 'B', action: 'attack'}];
  if (cancel) tape.push({tick: 3, id: 'cancel-a', actor: 'A', action: 'cancel'},
                        {tick: 4, id: 'cancel-a', actor: 'A', action: 'cancel'});
  let accumulator = 0, frames = 0;
  while (trace.length < 120) {
    accumulator += 60 / renderHz;
    while (accumulator >= 1 - 1e-9 && trace.length < 120) {
      const tick = trace.length;
      if (world.tick !== tick) throw new Error('Candidate logical clock diverged before tick ' + tick);
      world.step(tape.filter(row => row.tick === tick));
      if (world.tick !== tick + 1) throw new Error('Candidate did not advance exactly one tick');
      // Observe runtime fields, not the candidate's replay()/normalChecks()/trace.
      trace.push({tick, actors: ['A', 'B', 'C'].map(id => {
        const actor = world.actor(id);
        return {id: actor.id, clock: actor.clock, freeze: actor.freeze, hp: actor.hp,
          x: actor.x, move: actor.move ? structuredClone(actor.move) : null, pending: actor.pending};
      })});
      accumulator -= 1;
    }
    draw(world); frames++;
  }
  return {renderHz, frames, ticks: world.tick, trace, events: structuredClone(world.events), tape};
}

export function normalChecks(result) {
  const final = result.trace.at(-1), hits = result.events.filter(event => event.type === 'hit');
  const c = final.actors.find(actor => actor.id === 'C');
  const a = final.actors.find(actor => actor.id === 'A');
  const trade = hits.filter(event => event.tick === 2).map(event => `${event.actor}>${event.victim}`);
  return [
    {id: 'unrelated-actor-progress', expected: 120, observed: c.clock, pass: c.clock === 120},
    {id: 'one-hit-per-attack-victim', expected: 2, observed: hits.length,
      pass: hits.length === 2 && new Set(hits.map(hit => hit.id)).size === 2},
    {id: 'simultaneous-trade', expected: ['A>B', 'B>A'], observed: trade,
      pass: JSON.stringify([...trade].sort()) === JSON.stringify(['A>B', 'B>A'])},
    {id: 'four-tick-local-stop', expected: 4, observed: 120 - a.clock, pass: a.clock === 116}
  ];
}
