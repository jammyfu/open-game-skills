/** Explicitly owned shared resource leases, with injectable async loading.
 * No GPU types here: the Three.js adapter supplies real parsing and disposal.
 */
export class AssetPool {
  constructor(load,dispose,mutant='none') {
    this.load=load;this.dispose=dispose;this.mutant=mutant;this.entries=new Map();
    this.stats={loads:0,disposed:0,stale:0};
  }
  acquire(key,isCurrent=()=>true) {
    let e=this.entries.get(key);
    if(!e) {
      e={key,leases:new Set(),value:null,disposed:false};this.entries.set(key,e);this.stats.loads++;
      e.promise=Promise.resolve().then(()=>this.load(key)).then(value=>{
        e.value=value;if(!e.leases.size)this.drop(e);return value;
      },error=>{if(this.entries.get(key)===e)this.entries.delete(key);throw error;});
    }
    const lease={released:false};e.leases.add(lease);
    const release=()=>{
      if(lease.released)return;lease.released=true;e.leases.delete(lease);
      if(!e.leases.size||this.mutant==='premature-dispose')this.drop(e);
    };
    const ready=e.promise.then(value=>{
      if(lease.released||(this.mutant!=='stale-attach'&&!isCurrent())) {
        this.stats.stale++;release();return null;
      }
      return value;
    });
    return {ready,release};
  }
  drop(e) {
    if(e.value&&!e.disposed) {
      e.disposed=true;this.dispose(e.value);this.stats.disposed++;
      if(this.entries.get(e.key)===e)this.entries.delete(e.key);
    }
  }
}
