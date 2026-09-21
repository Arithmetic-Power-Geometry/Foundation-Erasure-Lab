from __future__ import annotations
import csv,json
from pathlib import Path

METHODS=("rotation","hybrid","successor_chain","semantic_reanchor")
FAMILIES=("RSA","ECC","PQC")

def simulate(method,epochs):
    retired=[f"{FAMILIES[i%3]}@{i}" for i in range(epochs)]
    current=f"{FAMILIES[epochs%3]}@{epochs}"
    if method=="semantic_reanchor":
        active={current,"finality"}
    elif method=="hybrid":
        active=set(retired+[current,"finality"])
    elif method=="rotation":
        active=set(retired+[current,"finality"])
    else:
        active=set(retired+[current,"finality"])
    debt=len(set(retired)&active)
    # Post-finalization Collapse Non-Interference proxy:
    # collapse changes current attack surface iff a retired resource remains active.
    pfcni=int(debt==0)
    return debt,len(active),pfcni

def run(out:Path):
    out.mkdir(parents=True,exist_ok=True);rows=[]
    for e in (1,2,4,8,16,32,64,128):
      for m in METHODS:
        debt,asf,pfcni=simulate(m,e)
        rows.append({"method":m,"epochs":e,"retirement_debt":debt,"asf_size":asf,
                     "post_finalization_collapse_noninterference":pfcni})
    with (out/"hard_collapse_matrix.csv").open("w",newline="") as f:
      w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
    (out/"hard_test_scope.json").write_text(json.dumps({
      "lenses":["cryptographic","information-dependency","temporal","state-machine","non-equivocation","resource-cost"],
      "warning":"PFCNI here is a structural dependency test, not empirical defeat of RSA/ECC/ML-DSA."
    },indent=2))
if __name__=="__main__":
    import argparse;p=argparse.ArgumentParser();p.add_argument("--out",default="results");a=p.parse_args();run(Path(a.out))
