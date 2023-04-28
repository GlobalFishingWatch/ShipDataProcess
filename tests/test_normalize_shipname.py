from shipdataprocess.normalize import normalize_shipname


def test_normalize_shipname_none():
    result = normalize_shipname(None)
    assert result is None


def test_normalize_shipname_upcase():
    result = normalize_shipname("MixEd")
    assert result == "MIXED"


def test_normalize_shipname_num():
    result = normalize_shipname(123456)
    assert result == "123456"


def test_normalize_shipname_float():
    result = normalize_shipname(123.456)
    assert result is None


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
    assert result == "BOAT537"


def test_normalize_shipname_romans():
    result = normalize_shipname("boat IX")
    assert result == "BOAT9"


def test_normalize_shipname_empty():
    result = normalize_shipname("")
    assert result is None


def test_normalize_shipname_empty_space():
    result = normalize_shipname(" ")
    assert result is None


def test_normalize_shipname_1c():
    result = normalize_shipname("a")
    assert result == "A"


def test_normalize_shipname_no():
    result = normalize_shipname("no")
    assert result == "NO"


#
# Below are added in Jan 2022 for encoding tests
def test_normalize_shipname_utf8():
    result = normalize_shipname("ÆØÅæøå")
    assert result == "AEOAAEOA"


def test_normalize_shipname_utf8_b():
    result = normalize_shipname("ÇÊÎŞÛ")
    assert result == "CEISU"


def test_normalize_shipname_utf8_encoded():
    result = normalize_shipname(b"pyth\xc3\xb6n!")
    assert result == "PYTHON"


def test_normalize_shipname_latin_encoded():
    result = normalize_shipname(b"\xe1")
    assert result == "A"
