from __future__ import annotations
import csv,json
from pathlib import Path
from foundation_erasure.verifier_trace import VerificationTrace,TracedVerifier,HistoricalChainVerifier

def run(out:Path):
    out.mkdir(parents=True,exist_ok=True);rows=[];raw=[]
    for t in (1,2,4,8,16,32,64,128):
        retired=[f"F{i}" for i in range(t)]; current=f"F{t}"
        for method,v in [
            ("historical_chain",HistoricalChainVerifier(retired+[current])),
            ("foundation_erasure",TracedVerifier(current))]:
            tr=VerificationTrace(); assert v.verify_current({},tr)
            retired_calls=sum(x in retired for x in tr.calls)
            rows.append({"method":method,"epochs":t,"total_verifier_calls":len(tr.calls),
                         "retired_foundation_calls":retired_calls,
                         "trace_asf_size":len(set(tr.calls))})
            raw.append({"method":method,"epochs":t,"calls":tr.calls})
    with (out/"verifier_trace.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
    (out/"verification_trace.json").write_text(json.dumps(raw,indent=2))
if __name__=="__main__":
 import argparse;p=argparse.ArgumentParser();p.add_argument("--out",default="results");a=p.parse_args();run(Path(a.out))
