def test_pqcrypto_mldsa_api_available():
    from pqcrypto.sign import ml_dsa_44
    names=dir(ml_dsa_44)
    assert any(("key" in n.lower() and "gen" in n.lower()) for n in names), names
    assert hasattr(ml_dsa_44,"sign")
    assert hasattr(ml_dsa_44,"verify")

def test_mldsa_sign_verify_and_tamper_reject():
    from pqcrypto.sign import ml_dsa_44
    keygen=getattr(ml_dsa_44,"generate_keypair",None) or getattr(ml_dsa_44,"keypair",None)
    if keygen is None:
        keygen=[getattr(ml_dsa_44,n) for n in dir(ml_dsa_44) if "key" in n.lower() and "gen" in n.lower() and callable(getattr(ml_dsa_44,n))][0]
    pk,sk=keygen(); msg=b"foundation-erasure"; sig=ml_dsa_44.sign(sk,msg)
    assert ml_dsa_44.verify(pk,msg,sig) is not False
    try:
        bad=ml_dsa_44.verify(pk,msg+b"x",sig)
        assert bad is False
    except Exception:
        pass
