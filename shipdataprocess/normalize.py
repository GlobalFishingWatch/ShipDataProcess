"""
This file provides functions that normalize ship name and call sign of a vessel
either recorded in registries or in vessel tracking data. The normalization, or
standardization of string, will ensure that the strings are comparable to other
strings despite various ways of recording names of the same vessel.
It also removes all non-essential characters or white spaces.
"""
from unidecode import unidecode
import roman
import re


def normalize_shipname(name):
    """
    Return a normalized ship name by removing all non-essential characters,
    prefix, and suffix, and standardizing roman numerals or other parts
    of the vessel name.

    :param name: String, an original vessel name
    :return: String, a normalized vessel name
    """

    if (name is None) | (name != name) | (name == ""):
        return None

    #
    # Remove nasty characters and white spaces
    if issubclass(type(name), str):
        name = unidecode(name)
    elif isinstance(name, bytes):
        try:
            name = unidecode(str(name, "utf-8", "strict"))
        except UnicodeDecodeError:
            name = unidecode(str(name, "iso-8859-1", "strict"))
    elif isinstance(name, int):
        name = str(name)
    else:
        return None

    #
    # Turn to upper cases
    name = name.upper()

    name = re.sub(r"\s+", " ", name)
    name = name.strip()
    name = name.replace("\n", "").replace("\r", "")

    #
    # Remove fishing vessel code
    name = re.sub(r"MFV[^\w]+", " ", name)  # fishing vessel code in English
    name = re.sub(r"MPV[^\w]+", " ", name)  # fishing vessel code in English
    name = re.sub(r"HMS[^\w]+", " ", name)  # fishing vessel code in English
    name = re.sub(
        r"LPG[/|C]*[\W]*|LNG[/|C]*[\W]*", " ", name
    )  # LPG/LNG variations

    name = re.sub(
        r"(\s|^)F[^\w\s]*V[^\w]*", " ", name
    )  # fishing vessel code in English (F/V, F-V, F.V, FV: etc)
    name = re.sub(
        r"^F[^\w\s]*B[^\w]+", " ", name
    )  # fishing vessel code in English
    name = re.sub(r" F[^\w\s]*B[^\w]*(\s|$)", " ", name)
    name = re.sub(
        r"^M[^\w\s]*P[^\w]+", " ", name
    )  # fishing vessel code in Italy/Spain
    name = re.sub(r" M[^\w\s]*P[^\w]*(\s|$)", " ", name)
    name = re.sub(
        r"^M[^\w\s]*B[^\w]+", " ", name
    )  # fishing vessel code in Italy/Spain
    name = re.sub(r" M[^\w\s]*B[^\w]*(\s|$)", " ", name)
    name = re.sub(r"^G[^\w\s]*V[^\w]+", " ", name)  # mostly in UK
    name = re.sub(r"S+F+[^\w]+G[^\w\s]*V[^\w]*", " ", name)
    name = re.sub(r" G[^\w\s]*V[^\w]*(\s|$)", " ", name)
    name = re.sub(r"^M[^\w\s]*V[^\w]+", " ", name)  # in English
    name = re.sub(r" M[^\w\s]*V[^\w]*(\s|$)", " ", name)
    name = re.sub(r"^M[^\w\s]+S[^\w]+", " ", name)  # Merchant Ship
    name = re.sub(r" M[^\w\s]+S[^\w]*(\s|$)", " ", name)
    name = re.sub(r"^M[^\w\s]*K[^\w]+", " ", name)  # mostly in northern europe
    name = re.sub(r" M[^\w\s]+K[^\w]*(\s|$)", " ", name)
    name = re.sub(r"^R[^\w\s]*V[^\w]+", " ", name)  # Research Vessel
    name = re.sub(r" R[^\w\s]*V[^\w]*(\s|$)", " ", name)

    name = re.sub(r"^T[^\w\s]*T[^\w]+", " ", name)  # Tender To
    name = re.sub(r" T[^\w\s]*T[^\w]*($)", " ", name)
    name = re.sub(r"^S[^\w\s]*Y[^\w]+", " ", name)  # Steam Yacht
    name = re.sub(r" S[^\w\s]*Y[^\w]*($)", " ", name)
    name = re.sub(r"^M[^\w\s]*F[^\w]+", " ", name)  # Motor Ferry
    name = re.sub(r" M[^\w\s]*F[^\w]*($)", " ", name)
    name = re.sub(r"^S[^\w\s]*S[^\w]+", " ", name)  # Steam Ship
    name = re.sub(r" S[^\w\s]*S[^\w]*($)", " ", name)
    name = re.sub(r"^S[^\w\s]*V[^\w]+", " ", name)  # Sailing Vessel
    name = re.sub(r" S[^\w\s]*V[^\w]*($)", " ", name)
    name = re.sub(r"^M[^\w\s]*T[^\w]+", " ", name)  # Motor Tanker
    name = re.sub(r" M[^\w\s]*T[^\w]*($)", " ", name)
    name = re.sub(r"^M[^\w\s]+Y[^\w]+", " ", name)  # Motor Yacht
    name = re.sub(r" M[^\w\s]+Y[^\w]*($)", " ", name)
    name = re.sub(r"^[A-Z]/[A-Z][^\w]+", " ", name)  # All other types of X/X
    name = re.sub(r" [A-Z]/[A-Z]($)", " ", name)
    name = re.sub(
        r"^[A-Z]\\\\[A-Z][^\w]+", " ", name
    )  # All other types of X\X
    name = re.sub(r" [A-Z]\\\\[A-Z]($)", " ", name)
    name = re.sub(r"^KM[^\w]+", " ", name)  # Indonesia K.M
    name = re.sub(r"^E.B. ", " ", name)  # Dutch E.B. equivalent to NO.

    name = re.sub(
        r"\(.+\)", " ", name
    )  # All additional information in parentheses
    name = re.sub(r"\[.+\]", " ", name)

    #
    # Numbers in letters
    name = re.sub(r" ONE($)| UNO($)| UN($)", " 1", name)
    name = re.sub(r" TWO($)| DOS($)| DEUX($)", " 2", name)
    name = re.sub(r" THREE($)| TRES($)| TROIS($)", " 3", name)
    name = re.sub(r" FOUR($)| CUATRO($)| QUATRE($)", " 4", name)
    name = re.sub(r" FIVE($)| CINCO($)| CINQ($)", " 5", name)
    name = re.sub(r" SIX($)| SEIS($)", " 6", name)
    name = re.sub(r" SEVEN($)| SIETE($)| SEPT($)", " 7", name)
    name = re.sub(r" EIGHT($)| OCHO($)| HUIT($)", " 8", name)
    name = re.sub(r" NINE($)| NUEVE($)| NEUF($)", " 9", name)
    name = re.sub(r" TEN($)| DIEZ($)| DIX($)", " 10", name)
    name = re.sub(r" ELEVEN($)| ONCE($)| ONZE($)", " 11", name)
    name = re.sub(r" TWELVE($)| DOCE($)| DOUZE($)", " 12", name)
    name = re.sub(r" THIRTEEN($)| TRECE($)| TREIZE($)", " 13", name)
    name = re.sub(r" FOURTEEN($)| CATORCE($)| QUATORZE($)", " 14", name)
    name = re.sub(r" FIFTEEN($)| QUINCE($)| QUINZE($)", " 15", name)

    name = re.sub("1ST ", "FIRST ", name)
    name = re.sub("2ND ", "SECOND ", name)
    name = re.sub("3RD ", "THIRD ", name)
    name = re.sub("4TH ", "FOURTH ", name)
    name = re.sub("5TH ", "FIFTH ", name)

    #
    # Country specific appendix (S. Korea and China)
    name = re.sub(r"\d+\s*HO($)", " ", name)
    name = re.sub(r"\d+\s*HAO($)", " ", name)

    #
    # Remove NO.s such in NO.5, NO5, NO:5, NO. 5, NO 5, N5, N-5 etc
    name = re.sub(r"NO[^\w\s]*[\s]*(?=\d+)", "", name)
    name = re.sub(r"[\s]+N[\W_0]*(?=\d+)", "", name)
    name = re.sub(r"NO\.\s*(?=[^0-9]+)", "", name)

    #
    # Turn '&' to 'AND'
    name = re.sub(
        r"(?<=[A-Z])\s+&\s+(?=[A-Z])", " AND ", name
    )  # replace 'BLACK & WHITE' to 'BLACK AND WHITE'

    #
    # Replace STA and STA. to SANTA
    name = re.sub(r"((^(STA|STA.)|\s(STA|STA.))\s|\s(STA|STA.)$)", "SANTA", name)

    #
    # Deromanization
    vs = re.split(r"\s+|-|(?<=[A-Z]{3})\.", name)
    try:
        #
        # If last word from the name text has L/C/D/M then do not deromanize
        if re.search(r"[LCDM]", vs[-1]).group(0):
            pass
    except AttributeError:
        #
        # Try to deromanize the last word from the name text
        try:
            vs[-1] = roman.fromRoman(vs[-1])
            vs[-1] = str(int(vs[-1]))
        except roman.InvalidRomanNumeralError:
            #
            # No corresponding roman numeral found. Let's leave it as is.
            pass

    #
    # Attach the deromanized digits to the end
    name = "".join(vs)

    #
    # Now, remove all special characters
    name = re.sub(r"[\W_]", "", name)

    #
    # Check if the name starts with digits, if yes move it to the end
    obj = re.search(r"^\d+", name)
    if obj:
        first_digit = obj.group(0)
        name = re.sub(r"^\d+", "", name) + str(first_digit)

    #
    # Remove 0s from the numbers starting with 0s
    obj = re.search(r"\d+$", name)
    if obj:
        last_digit = obj.group(0)
        non_zeros = re.sub("^0+", "", last_digit)
        name = re.sub(r"\d+$", "", name) + str(non_zeros)

    #
    # Remove all excessive white spaces
    name = re.sub(r"\s+", " ", name)

    if name == "" or name == " ":
        return None
    else:
        return name


def normalize_callsign(callsign):
    """
    Return a normalized International Radio Call Sign by removing non-essential
    characters and ignoring meaningless call sign including 'NONE', 'UNKNOWN'

    :param callsign: String, an original call sign
    :return: String, a normalized call sign
    """

    if (
        (callsign is None)
        | (callsign != callsign)
        | (callsign == "")
        | (callsign == "NONE")
        | (callsign == "UNKNOWN")
        | (callsign == "NIL")
        | (callsign == "NULL")
    ):
        return None

    #
    # Turn to upper cases
    callsign = callsign.upper()

    #
    # Remove nasty characters, white space
    try:
        #
        # get rid of nasty characters, but sometimes this fails
        callsign = unidecode(str(callsign))
    except UnicodeDecodeError:
        try:
            callsign = unidecode(str(callsign.decode("utf8")))
        except UnicodeDecodeError:
            callsign = unidecode(str(callsign.decode("iso_8859-1")))

    callsign = callsign.strip()
    callsign = re.sub(r"\s+", " ", callsign)

    #
    # Get rid of all non-word characters
    callsign = re.sub(r"[\W_]", "", callsign)

    #
    # Remove 0s from callsign starting with 0s
    callsign = re.sub(r"^0+", "", callsign)

    if callsign == "":
        return None
    else:
        return callsign
