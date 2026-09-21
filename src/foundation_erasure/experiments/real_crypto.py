from __future__ import annotations
import csv,json,statistics,time
from pathlib import Path
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa,ec,padding

MESSAGE=b"foundation-erasure-canonical-state-v1"

def bench(fn,n=100):
    xs=[]
    for _ in range(n):
        t=time.perf_counter_ns();fn();xs.append(time.perf_counter_ns()-t)
    return int(statistics.median(xs)),round(statistics.mean(xs),2)

def rsa_suite():
    sk=rsa.generate_private_key(public_exponent=65537,key_size=2048);pk=sk.public_key()
    def sign(): return sk.sign(MESSAGE,padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),hashes.SHA256())
    sig=sign()
    def verify(): pk.verify(sig,MESSAGE,padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),hashes.SHA256())
    return sk,pk,sign,verify,len(sig)

def ecc_suite():
    sk=ec.generate_private_key(ec.SECP256R1());pk=sk.public_key()
    def sign(): return sk.sign(MESSAGE,ec.ECDSA(hashes.SHA256()))
    sig=sign()
    def verify(): pk.verify(sig,MESSAGE,ec.ECDSA(hashes.SHA256()))
    return sk,pk,sign,verify,len(sig)

def mldsa_suite():
    from pqcrypto.sign import ml_dsa_44
    pk,sk=ml_dsa_44.generate_keypair()
    def sign(): return ml_dsa_44.sign(sk,MESSAGE)
    sig=sign()
    def verify(): assert ml_dsa_44.verify(pk,MESSAGE,sig)
    return sk,pk,sign,verify,len(sig)

def run(out:Path):
    out.mkdir(parents=True,exist_ok=True);rows=[]
    for name,factory in [("RSA-2048",rsa_suite),("ECDSA-P256",ecc_suite),("ML-DSA-44",mldsa_suite)]:
        t=time.perf_counter_ns();sk,pk,sign,verify,sigbytes=factory();keygen=time.perf_counter_ns()-t
        sm,sa=bench(sign);vm,va=bench(verify)
        rows.append({"foundation":name,"keygen_ns":keygen,"sign_median_ns":sm,"sign_mean_ns":sa,
                     "verify_median_ns":vm,"verify_mean_ns":va,"signature_bytes":sigbytes})
    with (out/"real_crypto_performance.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
    (out/"real_crypto_manifest.json").write_text(json.dumps({
      "message_bytes":len(MESSAGE),"repetitions":100,
      "interpretation":"primitive performance only; foundation-erasure benefit is evaluated separately by post-finalization collapse/non-interference tests"
    },indent=2))
if __name__=="__main__":
    import argparse;p=argparse.ArgumentParser();p.add_argument("--out",default="results");a=p.parse_args();run(Path(a.out))
