from shipdataprocess.normalize import normalize_shipname

def test_normalize_shipname_none():
    result = normalize_shipname(None)
    assert result == ""

def test_normalize_shipname_upcase():
    result = normalize_shipname("MixEd")
    assert result == "MIXED"

def test_normalize_shipname_symbols():
    result = normalize_shipname("weird -+%()<>$;!&'`\\.#/")
    assert result == "WEIRD"

def test_normalize_shipname_spaces():
    result = normalize_shipname("  \tspaced  \nname      ")
    assert result == "SPACEDNAME"

def test_normalize_shipname_FB():
    result = normalize_shipname("f/b boat f/v r/v fv othername")
    assert result == "BOATOTHERNAME"

def test_normalize_shipname_nodot():
    result = normalize_shipname("no. boat")
    assert result == "BOAT"

def test_normalize_shipname_nonumber():
    result = normalize_shipname("no537 boat")
    assert result == 'BOAT537'

def test_normalize_shipname_romans():
    result = normalize_shipname("boat IX")
    assert result == "BOAT9"

def test_normalize_shipname_empty():
    result = normalize_shipname("")
    assert result == ""

def test_normalize_shipname_1c():
    result = normalize_shipname("a")
    assert result == "A"

def test_normalize_shipname_no():
    result = normalize_shipname("no")
    assert result == "NO"
