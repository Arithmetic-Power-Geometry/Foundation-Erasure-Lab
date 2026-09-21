from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

class Phase(str,Enum):
    OLD="old"; PREPARED="prepared"; AUTHORIZED="authorized"; FINALIZED="finalized"

@dataclass
class Handoff:
    identity:str
    epoch:int
    old_family:str
    new_family:str
    old_root:str
    new_root:str
    phase:Phase=Phase.OLD

class AtomicFinality:
    def __init__(self,identity,epoch,family,root):
        self.identity=identity; self.epoch=epoch; self.family=family; self.root=root
        self.pending=None; self.forks=0
    def prepare(self,new_family,new_root):
        self.pending=Handoff(self.identity,self.epoch,self.family,new_family,self.root,new_root,Phase.PREPARED)
        return self.pending
    def authorize(self):
        if not self.pending or self.pending.phase!=Phase.PREPARED: return False
        self.pending.phase=Phase.AUTHORIZED; return True
    def finalize(self,expected_epoch,expected_root):
        p=self.pending
        if not p or p.phase!=Phase.AUTHORIZED: return False
        if expected_epoch!=self.epoch or expected_root!=self.root: return False
        self.epoch+=1; self.family=p.new_family; self.root=p.new_root;p.phase=Phase.FINALIZED;self.pending=None;return True
    def adversarial_successor(self,old_family,root):
        # Retired family has no write authority after atomic finalization.
        if old_family!=self.family: return False
        self.forks+=1; return False
    def rollback(self,epoch,root):
        return epoch>=self.epoch and root==self.root
