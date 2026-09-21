from __future__ import annotations
import csv
from pathlib import Path
from foundation_erasure.state_machine import AtomicFinality,Phase

ATTACKS=("substitute_successor","rollback","replay","fork")
BREAK_PHASES=(Phase.OLD,Phase.PREPARED,Phase.AUTHORIZED,Phase.FINALIZED)

def trial(break_phase,attack):
    j=AtomicFinality("ID",0,"RSA","root-rsa")
    h=j.prepare("ECC","root-ecc")
    if break_phase==Phase.OLD:
        return 1 # old authority still canonical: retirement not yet achieved
    if break_phase==Phase.PREPARED:
        return 1 # prepared but not authenticated/finalized
    j.authorize()
    if break_phase==Phase.AUTHORIZED:
        return 1 # old family still participates until atomic finalization
    assert j.finalize(0,"root-rsa")
    if attack=="rollback": return int(j.rollback(0,"root-rsa"))
    if attack in ("substitute_successor","fork"): return int(j.adversarial_successor("RSA","evil"))
    if attack=="replay": return int(j.finalize(0,"root-rsa"))
    return 1

def run(out:Path):
    out.mkdir(parents=True,exist_ok=True);rows=[]
    for p in BREAK_PHASES:
      for a in ATTACKS:
        s=trial(p,a);rows.append({"break_phase":p.value,"attack":a,"attack_success":s,
          "retired":int(p==Phase.FINALIZED)})
    with (out/"retirement_point_matrix.csv").open("w",newline="") as f:
      w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
if __name__=="__main__":
 import argparse;p=argparse.ArgumentParser();p.add_argument("--out",default="results");a=p.parse_args();run(Path(a.out))
