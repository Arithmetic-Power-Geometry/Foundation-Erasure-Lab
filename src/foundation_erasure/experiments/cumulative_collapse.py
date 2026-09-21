from __future__ import annotations
import csv,json
from pathlib import Path
from foundation_erasure.state_machine import AtomicFinality

ATTACKS=("rollback","successor_substitution","fork","replay","history_reorder","epoch_omission")

def build(T:int):
    j=AtomicFinality("ID",0,"F0","root0")
    history=[("F0","root0")]
    for t in range(1,T+1):
        oldroot=j.root
        j.prepare(f"F{t}",f"root{t}");assert j.authorize();assert j.finalize(t-1,oldroot)
        history.append((f"F{t}",f"root{t}"))
    return j,history

def attack(j,history,retired_epoch,kind):
    before=(j.epoch,j.family,j.root)
    oldfam,oldroot=history[retired_epoch]
    if kind=="rollback": j.rollback(retired_epoch,oldroot)
    elif kind in ("successor_substitution","fork"): j.adversarial_successor(oldfam,f"evil-{retired_epoch}")
    elif kind=="replay": j.finalize(retired_epoch,oldroot)
    elif kind in ("history_reorder","epoch_omission"):
        # History-only fabrication must not be accepted as a current-state write.
        j.adversarial_successor(oldfam,f"history-{kind}-{retired_epoch}")
    return int((j.epoch,j.family,j.root)!=before)

def run(out:Path,T:int=128):
    out.mkdir(parents=True,exist_ok=True);j,h=build(T);rows=[]
    for i in range(T):
      for a in ATTACKS:
        # fresh journal per trial, with all retired families assumed compromised
        x,hx=build(T);s=attack(x,hx,i,a)
        rows.append({"epochs":T,"retired_epoch":i,"retired_family":f"F{i}","attack":a,
                     "all_retired_compromised":1,"current_state_changed":s})
    with (out/"cumulative_collapse.csv").open("w",newline="") as f:
      w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
    summary={"epochs":T,"retired_families_compromised":T,"trials":len(rows),
             "accepted_current_state_replacements":sum(r["current_state_changed"] for r in rows)}
    (out/"cumulative_collapse_summary.json").write_text(json.dumps(summary,indent=2))
if __name__=="__main__":
 import argparse;p=argparse.ArgumentParser();p.add_argument("--out",default="results");p.add_argument("--epochs",type=int,default=128);a=p.parse_args();run(Path(a.out),a.epochs)
