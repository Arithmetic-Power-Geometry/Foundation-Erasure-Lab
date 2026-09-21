from __future__ import annotations
from dataclasses import dataclass,field

@dataclass
class VerificationTrace:
    calls:list[str]=field(default_factory=list)
    def use(self,resource:str): self.calls.append(resource)
    def uses_family(self,family:str)->bool:
        return any(x==family or x.startswith(family+":") for x in self.calls)

class TracedVerifier:
    def __init__(self,current_family:str,finality_resource:str="finality"):
        self.current_family=current_family;self.finality_resource=finality_resource
    def verify_current(self,state,trace:VerificationTrace)->bool:
        trace.use(self.finality_resource)
        trace.use(self.current_family)
        return True

class HistoricalChainVerifier:
    def __init__(self,families:list[str],finality_resource:str="finality"):
        self.families=families;self.finality_resource=finality_resource
    def verify_current(self,state,trace:VerificationTrace)->bool:
        trace.use(self.finality_resource)
        for f in self.families: trace.use(f)
        return True
