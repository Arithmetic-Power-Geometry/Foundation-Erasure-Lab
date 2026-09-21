from __future__ import annotations
import csv,json
from pathlib import Path
from foundation_erasure.model import SecurityDependencyGraph

EPOCHS=(2,4,8,16,32,64)

def chain_graph(method:str,t:int):
    g=SecurityDependencyGraph()
    current="current_state"
    # finality remains active in every method
    g.add("finality",current)
    if method=="semantic_reanchor":
        g.add(f"F{t}",current)
    elif method=="wrapped_chain":
        for i in range(t):
            g.add(f"F{i}",f"history_{i}")
            g.add(f"history_{i}",current)
        g.add(f"F{t}",current)
    elif method=="dual_hybrid":
        for i in range(t+1): g.add(f"F{i}",current)
    elif method=="successor_chain":
        for i in range(t):
            g.add(f"F{i}",f"transition_{i}")
            g.add(f"transition_{i}",current)
        g.add(f"F{t}",current)
    return g

def run(out:Path):
    out.mkdir(parents=True,exist_ok=True); rows=[]
    for t in EPOCHS:
        retired=[f"F{i}" for i in range(t)]
        resources=retired+[f"F{t}","finality"]
        for method in ("wrapped_chain","dual_hybrid","successor_chain","semantic_reanchor"):
            g=chain_graph(method,t)
            debt=len(g.retirement_debt("current_state",retired))
            asf=len(g.active_security_frontier("current_state",resources))
            rows.append({"method":method,"handoffs":t,"retired_foundations":t,
                         "retirement_debt":debt,"asf_size":asf,
                         "retirement_completion":round(1-(debt/max(1,t)),6)})
    with (out/"multi_epoch.csv").open("w",newline="") as fh:
        w=csv.DictWriter(fh,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
    (out/"multi_epoch.json").write_text(json.dumps(rows,indent=2))
if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser();p.add_argument("--out",default="results");a=p.parse_args();run(Path(a.out))
