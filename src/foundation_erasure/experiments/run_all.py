from __future__ import annotations
import argparse,csv,json,statistics,time
from pathlib import Path
from foundation_erasure.attacks import fork_attack,retired_family_collapse,rollback_attack,successor_substitution
from foundation_erasure.finality import FinalityRegistry
from foundation_erasure.methods import *
from foundation_erasure.metrics import measure
from foundation_erasure.model import CanonicalState
from foundation_erasure.primitives import ToyFoundation

REPEATS=200

def run(out:Path):
    out.mkdir(parents=True,exist_ok=True)
    state=CanonicalState("identity-001",1,"owner-A","canonical-payload")
    forged=CanonicalState("identity-001",1,"attacker-X","forged-payload")
    old=ToyFoundation("legacy-family-A",b"legacy-secret")
    new=ToyFoundation("successor-family-B",b"successor-secret")
    rotated=ToyFoundation("legacy-family-A-rotated",b"rotated-secret")
    methods=[
      ("key_rotation",lambda f:key_rotation_same_foundation(state,old,rotated,f),rotated),
      ("wrapped_old_root",lambda f:wrapped_old_root(state,old,new,f),new),
      ("chained_successor",lambda f:chained_successor_authorization(state,old,new,f),new),
      ("evidence_renewal",lambda f:evidence_renewal_chain(state,old,new,f),new),
      ("dual_hybrid_anchor",lambda f:dual_hybrid_anchor(state,old,new,f),new),
      ("proactive_refresh",lambda f:proactive_refresh(state,old,new,f),new),
      ("transparency_rollover",lambda f:transparency_rollover(state,old,new,f),new),
      ("semantic_reanchor",lambda f:semantic_reanchor(state,old,new,f),new)]
    metrics=[]; attacks=[]; perf=[]
    for name,builder,current in methods:
      samples=[]; result=None; finality=None
      for _ in range(REPEATS):
        finality=FinalityRegistry(); t=time.perf_counter_ns(); result=builder(finality); samples.append(time.perf_counter_ns()-t)
      m=measure(result,old.name,current.name); metrics.append(vars(m))
      perf.append({"method":name,"repeats":REPEATS,"median_handoff_ns":int(statistics.median(samples)),
                   "mean_handoff_ns":round(statistics.mean(samples),2),"stdev_handoff_ns":round(statistics.pstdev(samples),2)})
      aa=[retired_family_collapse(state,forged,result,old,current,finality),rollback_attack(result,old),
          successor_substitution(result,old),fork_attack(result,old)]
      for a in aa: attacks.append({"method":name,"attack":a.attack,"success":int(a.success)})
    def write(name,rows):
      with (out/name).open("w",newline="") as fh:
        w=csv.DictWriter(fh,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
    write("foundation_erasure.csv",metrics); write("attack_success.csv",attacks); write("performance.csv",perf)
    summary=[]
    for m in metrics:
      ar=[a for a in attacks if a["method"]==m["method"]]
      summary.append({"method":m["method"],"retirement_debt":m["retirement_debt"],
        "old_foundation_active":m["old_foundation_active"],"collapse_attack_success_rate":sum(a["success"] for a in ar)/len(ar),
        "asf_size":m["active_security_frontier_size"]})
    write("comparison_summary.csv",summary)
    (out/"dependency_frontier.json").write_text(json.dumps({m["method"]:m for m in metrics},indent=2))
    (out/"experiment_manifest.json").write_text(json.dumps({"schema":2,"repeats":REPEATS,
      "scope":"abstract dependency-security benchmark; baseline labels model structural patterns, not full protocol implementations",
      "warning":"attack success denotes modeled dependency exposure, not measured cryptanalytic break probability"},indent=2))
def main():
    p=argparse.ArgumentParser();p.add_argument("--out",default="results");a=p.parse_args();run(Path(a.out))
if __name__=="__main__":main()
