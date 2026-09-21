from __future__ import annotations
import csv,json
from pathlib import Path
from foundation_erasure.state_machine import AtomicFinality

FAMILIES=("RSA","ECC","ML-DSA")
ATTACKS=("retired_key_successor_forge","rollback","replay","fork")

def finalized_journal(old_family,new_family):
    j=AtomicFinality("ID",0,old_family,"root-old")
    j.prepare(new_family,"root-new");assert j.authorize();assert j.finalize(0,"root-old")
    return j

def execute(j,old_family,attack):
    # The adversary is modeled as having complete signing/forging power for old_family.
    # Success is defined only by changing/replacing the current canonical state.
    before=(j.epoch,j.family,j.root)
    if attack=="retired_key_successor_forge":
        j.adversarial_successor(old_family,"evil-root")
    elif attack=="rollback":
        j.rollback(0,"root-old")
    elif attack=="replay":
        j.finalize(0,"root-old")
    elif attack=="fork":
        j.adversarial_successor(old_family,"fork-root")
    return int((j.epoch,j.family,j.root)!=before)

def run(out:Path):
    out.mkdir(parents=True,exist_ok=True);rows=[]
    transitions=[("RSA","ECC"),("ECC","ML-DSA"),("ML-DSA","RSA")]
    for old,new in transitions:
      for a in ATTACKS:
        j=finalized_journal(old,new);s=execute(j,old,a)
        rows.append({"old_family":old,"new_family":new,"attack":a,"current_state_changed":s,
                     "final_epoch":j.epoch,"final_family":j.family})
    with (out/"executable_collapse_attacks.csv").open("w",newline="") as f:
      w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
    (out/"executable_collapse_summary.json").write_text(json.dumps({
      "trials":len(rows),"successes":sum(r["current_state_changed"] for r in rows),
      "scope":"post-finalization current-state attacks with complete retired-family authority"
    },indent=2))
if __name__=="__main__":
 import argparse;p=argparse.ArgumentParser();p.add_argument("--out",default="results");a=p.parse_args();run(Path(a.out))
