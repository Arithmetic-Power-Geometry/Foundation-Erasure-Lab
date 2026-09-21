from foundation_erasure.verifier_trace import VerificationTrace,TracedVerifier,HistoricalChainVerifier

def test_current_verifier_never_calls_retired_foundation():
    tr=VerificationTrace();TracedVerifier("ML-DSA").verify_current({},tr)
    assert tr.calls==["finality","ML-DSA"]
    assert not tr.uses_family("RSA")
    assert not tr.uses_family("ECC")

def test_historical_chain_calls_retired_foundations():
    tr=VerificationTrace();HistoricalChainVerifier(["RSA","ECC","ML-DSA"]).verify_current({},tr)
    assert tr.uses_family("RSA") and tr.uses_family("ECC")
