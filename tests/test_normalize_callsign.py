from shipdataprocess.normalize import normalize_callsign

def test_normalize_callsign_none():
    result = normalize_callsign(None)
    assert result == None

def test_normalize_callsign_upcase():
    result = normalize_callsign("MixEd")
    assert result == "MIXED"

def test_normalize_callsign_symbols():
    result = normalize_callsign("weird -+%()<>$;!&'`\\.#/")
    assert result == "WEIRD"

def test_normalize_callsign_spaces():
    result = normalize_callsign("  \tspaced  \nname      ")
    assert result == "SPACEDNAME"

def test_normalize_callsign_empty():
    result = normalize_callsign("")
    assert result == None

def test_normalize_callsign_1c():
    result = normalize_callsign("a")
    assert result == "A"

def test_normalize_callsign_starting_with_zero():
    result = normalize_callsign("0020300a")
    assert result == "20300A"
