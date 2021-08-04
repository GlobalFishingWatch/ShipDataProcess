from unidecode import unidecode
import roman
import re
import sys


def normalize_shipname(name):
        
    if (name is None)|(name != name)|(name == ''):
        return None

    #
    # Turn to upper cases
    name = name.upper()
    

    #
    # Remove nasty characters and white spaces
    if sys.version_info[0] < 3:
        try:
            name = unidecode(str(name)) # get rid of nasty characters, but sometimes this fails
        except:
            try:
                name = unidecode(str(name.decode('utf8')))
            except:
                name = unidecode(str(name.decode('iso_8859-1')))
    else:
        name = unidecode(str(name))

    name = re.sub('\s+',' ',name)
    name = name.strip()
    name = name.replace('\n','').replace('\r','')
 
    #
    # Remove fishing vessel code
    name = re.sub('MFV[^\w]+', ' ', name)  # fishing vessel code in English
    name = re.sub('MPV[^\w]+', ' ', name)  # fishing vessel code in English
    name = re.sub('HMS[^\w]+', ' ', name)  # fishing vessel code in English
    name = re.sub('LPG[/|C]*[\W]*|LNG[/|C]*[\W]*', ' ', name)  # LPG/LNG variations
    
    name = re.sub('(\s|^)F[^\w\s]*V[^\w]*', ' ', name)  # fishing vessel code in English (F/V, F-V, F.V, FV: etc)
    name = re.sub('^F[^\w\s]*B[^\w]+', ' ', name)  # fishing vessel code in English
    name = re.sub(' F[^\w\s]*B[^\w]*(\s|$)', ' ', name)    
    name = re.sub('^M[^\w\s]*P[^\w]+', ' ', name)  # fishing vessel code in Italy/Spain
    name = re.sub(' M[^\w\s]*P[^\w]*(\s|$)', ' ', name)
    name = re.sub('^M[^\w\s]*B[^\w]+', ' ', name)  # fishing vessel code in Italy/Spain
    name = re.sub(' M[^\w\s]*B[^\w]*(\s|$)', ' ', name)
    name = re.sub('^G[^\w\s]*V[^\w]+', ' ', name)  # mostly in UK
    name = re.sub('S+F+[^\w]+G[^\w\s]*V[^\w]*', ' ', name)
    name = re.sub(' G[^\w\s]*V[^\w]*(\s|$)', ' ', name)
    name = re.sub('^M[^\w\s]*V[^\w]+', ' ', name)  # in English
    name = re.sub(' M[^\w\s]*V[^\w]*(\s|$)', ' ', name)
    name = re.sub('^M[^\w\s]+S[^\w]+', ' ', name)  # Merchant Ship
    name = re.sub(' M[^\w\s]+S[^\w]*(\s|$)', ' ', name)
    name = re.sub('^M[^\w\s]*K[^\w]+', ' ', name)  # mostly in northern europe
    name = re.sub(' M[^\w\s]+K[^\w]*(\s|$)', ' ', name)
    name = re.sub('^R[^\w\s]*V[^\w]+', ' ', name)  # Research Vessel
    name = re.sub(' R[^\w\s]*V[^\w]*(\s|$)', ' ', name)
    
    name = re.sub('^T[^\w\s]*T[^\w]+', ' ', name)  # Tender To
    name = re.sub(' T[^\w\s]*T[^\w]*($)', ' ', name)
    name = re.sub('^S[^\w\s]*Y[^\w]+', ' ', name)  # Steam Yacht
    name = re.sub(' S[^\w\s]*Y[^\w]*($)', ' ', name)
    name = re.sub('^M[^\w\s]*F[^\w]+', ' ', name)  # Motor Ferry
    name = re.sub(' M[^\w\s]*F[^\w]*($)', ' ', name)
    name = re.sub('^S[^\w\s]*S[^\w]+', ' ', name)  # Steam Ship
    name = re.sub(' S[^\w\s]*S[^\w]*($)', ' ', name)
    name = re.sub('^S[^\w\s]*V[^\w]+', ' ', name)  # Sailing Vessel
    name = re.sub(' S[^\w\s]*V[^\w]*($)', ' ', name)
    name = re.sub('^M[^\w\s]*T[^\w]+', ' ', name)  # Motor Tanker
    name = re.sub(' M[^\w\s]*T[^\w]*($)', ' ', name)
    name = re.sub('^M[^\w\s]+Y[^\w]+', ' ', name)  # Motor Yacht
    name = re.sub(' M[^\w\s]+Y[^\w]*($)', ' ', name)
    name = re.sub('^[A-Z]/[A-Z][^\w]+', ' ', name)  # All other types of X/X
    name = re.sub(' [A-Z]/[A-Z]($)', ' ', name)
    name = re.sub('^[A-Z]\\\\[A-Z][^\w]+', ' ', name) ## All other types of X\X
    name = re.sub(' [A-Z]\\\\[A-Z]($)', ' ', name)
    name = re.sub('^KM[^\w]+', ' ', name)  # Indonesia K.M
    name = re.sub('^E.B. ', ' ', name)  # Dutch E.B. equivalent to NO.

    name = re.sub('\(.+\)', ' ', name)  # All additional information in parentheses
    name = re.sub('\[.+\]', ' ', name)
    
    #
    # Numbers in letters
    name = re.sub(' ONE($)| UNO($)| UN($)', ' 1', name)
    name = re.sub(' TWO($)| DOS($)| DEUX($)', ' 2', name)
    name = re.sub(' THREE($)| TRES($)| TROIS($)', ' 3', name)
    name = re.sub(' FOUR($)| CUATRO($)| QUATRE($)', ' 4', name)
    name = re.sub(' FIVE($)| CINCO($)| CINQ($)', ' 5', name)
    name = re.sub(' SIX($)| SEIS($)| SIX($)', ' 6', name)
    name = re.sub(' SEVEN($)| SIETE($)| SEPT($)', ' 7', name)
    name = re.sub(' EIGHT($)| OCHO($)| HUIT($)', ' 8', name)
    name = re.sub(' NINE($)| NUEVE($)| NEUF($)', ' 9', name)
    name = re.sub(' TEN($)| DIEZ($)| DIX($)', ' 10', name)
    name = re.sub(' ELEVEN($)| ONCE($)| ONZE($)', ' 11', name)
    name = re.sub(' TWELVE($)| DOCE($)| DOUZE($)', ' 12', name)
    name = re.sub(' THIRTEEN($)| TRECE($)| TREIZE($)', ' 13', name)
    name = re.sub(' FOURTEEN($)| CATORCE($)| QUATORZE($)', ' 14', name)
    name = re.sub(' FIFTEEN($)| QUINCE($)| QUINZE($)', ' 15', name)

    name = re.sub('1ST ', 'FIRST ', name)
    name = re.sub('2ND ', 'SECOND ', name)
    name = re.sub('3RD ', 'THIRD ', name)
    name = re.sub('4TH ', 'FOURTH ', name)
    name = re.sub('5TH ', 'FIFTH ', name)

    #
    # Country specific appendix (S. Korea and China)
    name = re.sub('\d+\s*HO($)', ' ', name)
    name = re.sub('\d+\s*HAO($)', ' ', name)

    #
    # Remove NO.s such in NO.5, NO5, NO:5, NO. 5, NO 5, N5, N-5 etc
    name = re.sub('NO[^\w\s]*[\s]*(?=\d+)', '', name)
    name = re.sub('[\s]+N[\W_0]*(?=\d+)', '', name)
    name = re.sub('NO\.\s*(?=[^0-9]+)', '', name)
    
    #
    # Turn '&' to 'AND'
    name = re.sub('(?<=[A-Z])\s+&\s+(?=[A-Z])', ' AND ', name)  # replace 'BLACK & WHITE' to 'BLACK AND WHITE'
    
    #
    # Deromanization
    vs = re.split('\s+|-|(?<=[A-Z]{3})\.',name)
    try:
        #
        # If last word from the name text has L/C/D/M then do not deromanize
        if re.search('[LCDM]', vs[-1]).group(0): pass
    except:
        #
        # Try to deromanize the last word from the name text
        try:
            vs[-1] = roman.fromRoman(vs[-1])
            vs[-1] = str(int(vs[-1]))
        except:
            pass
    
    #
    # Attach the deromanized digits to the end
    name = ''.join(vs)

        
    #
    # Now, remove all special characters
    name = re.sub('[\W_]', '', name)
    
    #
    # Check if the name starts with digits, if yes move it to the end
    try: 
        first_digit = re.search('^\d+', name).group(0)
        name = re.sub('^\d+', '', name) + str(first_digit)
    except:
        pass

    #
    # Remove 0s from the numbers starting with 0s
    try:
        last_digit = re.search('\d+$', name).group(0)
        non_zeros = re.sub('^0+', '', last_digit)
        name = re.sub('\d+$', '', name) + str(non_zeros)
    except:
        pass

    if name == '':
        return None
    
    return name


def normalize_callsign(callsign):

    if (callsign is None) | (callsign != callsign) | (callsign == '') | \
            (callsign == "NONE") | (callsign == "UNKNOWN") | (callsign == "NIL") | (callsign == "NULL"):
        return None

    #
    # Turn to upper cases
    callsign = callsign.upper()
    
    #
    # Remove nasty characters, white space
    try:
        callsign = unidecode(str(callsign))  # get rid of nasty characters, but sometimes this fails
    except:
        try:
            callsign = unidecode(str(callsign.decode('utf8')))
        except:
            callsign = unidecode(str(callsign.decode('iso_8859-1')))

    callsign = callsign.strip()
    callsign = re.sub('\s+',' ',callsign)

    #
    # Get rid of all non-word characters
    callsign = re.sub('[\W_]', '', callsign) 
    
    #
    # Remove 0s from callsign starting with 0s
    callsign = re.sub('^0+', '', callsign)
    
    if callsign == '':
        return None

    return callsign