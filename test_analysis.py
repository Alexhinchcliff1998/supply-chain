from analyze import analyze

def test_vendor_summary():
    rows=analyze()
    assert sum(r[1] for r in rows)==300
    assert all(0<=r[2]<=100 and r[3]>0 for r in rows)
    assert [r[2] for r in rows]==sorted([r[2] for r in rows],reverse=True)
