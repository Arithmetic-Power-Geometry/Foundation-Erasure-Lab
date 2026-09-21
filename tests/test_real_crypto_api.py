def test_pqcrypto_mldsa_api_available():
    from pqcrypto.sign import ml_dsa_44
    names=dir(ml_dsa_44)
    assert any(("key" in n.lower() and "gen" in n.lower()) for n in names), names
    assert hasattr(ml_dsa_44,"sign")
    assert hasattr(ml_dsa_44,"verify")
