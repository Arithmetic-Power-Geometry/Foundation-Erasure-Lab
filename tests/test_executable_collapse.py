from foundation_erasure.experiments.executable_collapse import finalized_journal,execute,ATTACKS

def test_all_retired_family_attacks_fail_after_finalization():
    for old,new in (("RSA","ECC"),("ECC","ML-DSA"),("ML-DSA","RSA")):
        for attack in ATTACKS:
            j=finalized_journal(old,new)
            assert execute(j,old,attack)==0
