import pytest
from shipdataprocess.normalize import normalize_shipname
from shipdataprocess.normalize import normalize_shipname_parts

def test_normalize_shipname_none():
    result = normalize_shipname(None)
    assert result == None

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
    result = normalize_shipname("f/b boat f/v othername")
    assert result == "BOATOTHERNAME"

def test_normalize_shipname_RV():
    result = normalize_shipname("r/v boat othername")
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
    assert result == None

def test_normalize_shipname_1c():
    result = normalize_shipname("a")
    assert result == "A"

def test_normalize_shipname_no():
    result = normalize_shipname("no")
    assert result == "NO"

@pytest.mark.parametrize("name, expected", [
    ("A",         {"basename":"A", "status": None}),
    ("AAA12",     {"basename":"AAA12", "status": None}),
    ("AAA 12%",   {"basename":"AAA", "status": "12%"}),
    ("AAA 12",    {"basename":"AAA12", "status": None}),
    ("AAA@@12V",  {"basename":"AAA", "status": "12V"}),
    ("AAA@@12V0", {"basename":"AAA", "status": "12V0"}),
    ])
def test_normalize_shipname_parts(name, expected):
    assert normalize_shipname_parts(name) == expected
