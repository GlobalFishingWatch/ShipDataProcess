# coding: utf-8

#
# field standardization functions
import pandas as pd
import numpy as np
import re
from django.utils.encoding import smart_str
from unidecode import unidecode


def imo_checksum(n):
    """
    This function for IMO numbers that are designed as 7-digit integer number

    :param n: String or Integer, Number to be subject to a IMO-checksum test
    :return: Boolean, True for valid IMO number checksum, False for otherwise
    """

    #
    # Cross check type of input, and the range of number
    # IMO number should be an integer with 7 digits
    try:
        n = int(n)
    except (ValueError, TypeError):
        return False

    if not (n >= 1000000) & (n <= 9999999):
        return False
    else:
        pass

    #
    # IMO checksum formula
    if ((n // 1000000 % 10) * 7 +
            (n // 100000 % 10) * 6 +
            (n // 10000 % 10) * 5 +
            (n // 1000 % 10) * 4 +
            (n // 100 % 10) * 3 +
            (n // 10 % 10) * 2) % 10 == (n % 10):
        return True
    else:
        return False


def standardize_imo(elem, check_field=True):
    """
    Standardize IMO numbers (ignore all letters and characters but numbers)
    If it comes with pandas Series or DataFrame, make sure
    it saves IMO numbers in STRING, as pandas Seires or DataFrame usually
    turn INTEGER to FLOAT in the presence of NULL in the same column.

    :param elem: Pandas Series, Series that contains a string field
    :param check_field: Boolean, field that contains IMO numbers
    :return: Pandas Series that is processed
    """

    if check_field:
        if type(elem) == pd.core.series.Series:
            elem = elem.apply(
                lambda x: re.sub(r'[^\d\.]', '', str(x))
                if (x == x) & (x is not None) & (x != '') & (x != 0) else None)
            elem = elem.apply(
                lambda x: str(int(float(x)))
                if (x == x) & (x is not None) & (x != '') & (x != 0) else None)
            elem = elem.apply(lambda x: x if imo_checksum(x) else None)
            return elem
        elif type(elem) == pd.core.frame.DataFrame:
            elem = elem[check_field].apply(
                lambda x: re.sub(r'[^\d\.]', '', str(x))
                if (x == x) & (x is not None) & (x != '') & (x != 0) else None)
            elem = elem.apply(
                lambda x: str(int(float(x)))
                if (x == x) & (x is not None) & (x != '') & (x != 0) else None)
            elem = elem.apply(lambda x: x if imo_checksum(x) else None)
            return elem
        elif (elem != elem) | (elem is None) | (elem == '') | (elem == 0):
            return None
        elif (type(elem) == str) | (type(elem) == int) | (type(elem) == float):
            elem = re.sub(r'[^\d\.]', '', str(elem))
            if elem == "":
                return None
            else:
                elem = str(int(float(elem)))
                if checksum(elem):
                    return elem
                else:
                    return None
        else:
            raise ValueError('Unknown type received')
    else:
        return None


#
# Standardize floating numbers. 
# Make sure to remove all comma separators (,). 
#
def standardize_float(elem, check_field=True):
    if check_field:
        if type(elem) == pd.core.series.Series:
            return elem.apply(
                lambda x: float(str(x).replace(',', ''))
                if (x == x) & (x is not None) & (x != '') & (x != 0) else np.nan)
        elif type(elem) == pd.core.frame.DataFrame:
            return elem[check_field].apply(
                lambda x: float(str(x).replace(',', ''))
                if (x == x) & (x is not None) & (x != '') & (x != 0) else np.nan)
        elif (elem != elem) | (elem is None) | (elem == '') | (elem == 0):
            return np.nan
        elif (type(elem) == str) | (type(elem) == int) | (type(elem) == float):
            return float(str(elem).replace(',', ''))
        else:
            raise ValueError('Unknown type received')
    else:
        return np.nan


def smart_upper(text):
    """
    Selective upper sensitive to upper/lower cases
    when it's related to URLs
    Source: https://stackoverflow.com/questions/6038061/regular-expression-to-find-urls-within-a-string

    :param text: String, giv en text
    :return: String, Upper cased text except the URL part
    """

    #
    # Find URLs in the given string and upper-case only the other texts
    # to preserve caps of URLs
    regex_for_url = r"((http|ftp|https)\:\/\/)?([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?"
    matched = re.finditer(regex_for_url, text)
    prev_end = 0
    for m in matched:
        url = m.group(0)
        start = m.start()
        end = m.end()

        text = \
            text[:prev_end] + \
            text[prev_end:start].upper() + \
            url + \
            text[end:]
        prev_end = end

    text = text[:prev_end] + text[prev_end:].upper()

    return text


def standardize_str(elem, check_field=True):
    """
    Standardize string.
    Make sure all excessive white space to just 1 space ' ',
    and turn all characters to capital letters except for URLs

    :param elem: Pandas Series, Series that contains a string field
    :param check_field: Boolean, field that contains the given strings
    :return: Pandas Series that is processed
    """

    if check_field:
        if type(elem) == pd.core.series.Series:
            elem = elem.apply(
                lambda x: smart_upper(re.sub(r'\s+', ' ', smart_str(x)).strip())
                if (x == x) & (x is not None) & (x != '') else None)
            return elem
        elif type(elem) == pd.core.frame.DataFrame:
            elem = elem[check_field].apply(
                lambda x: smart_upper(re.sub(r'\s+', ' ', smart_str(x)).strip())
                if (x == x) & (x is not None) & (x != '') else None)
            return elem
        elif (elem != elem) | (elem is None) | (elem == '') | (elem == 0):
            return None
        elif type(elem) == str:
            return smart_upper(re.sub(r'\s+', ' ', elem).strip())
        else:
            raise ValueError('Unknown type received')
    else:
        return None


#
# Standardize owner's names. Remove all variations of CO. LTD or similar types of suffixes
# and unionize all "fishery' to "fisheries".
#
def standardize_owner(elem, check_field=True):
    if check_field:
        elem = standardize_str(elem, check_field)

        text_to_remove = \
            ['CO LTD', 'COLTD', 'COMPANY LTD', 'CO LIMITED', 'COMPANY LIMITED', 'CO LIMTED', 'CO LTTD', 'CV LIMITADA',
             'LTD SA($)', 'LTD S A($)', 'CO SA($)', 'CO S A($)', 'CO AB($)', 'CO A B($)', 'CO PTY LTD($)', 'CO LRD($)',
             'PTY LIMITED($)', 'PTY LTD($)', 'SA PTY LTD($)', 'CORP LTD($)', 'LTDA EPP($)', 'JOINT STOCK COMPANY($)',
             'JOINTSTOCK COMPANY($)', 'CORPORATION PTE LTD($)', 'CORPORATION PTE($)', 'CORP PTE($)', 'CORP SA($)',
             'CORP INC($)', 'CORPORATION($)', 'CORP($)', 'INCORPORATED($)', 'INC($)', 'AP PTE LTD', 'CO PTE LTD',
             'GMBH CO', 'GMBH($)', 'LTD($)', 'LTDA($)', 'LIMITED($)', 'PTE($)', 'LIMITADA($)', 'LDA($)', 'LLC($)',
             'COMPANY NV($)', 'COMPANY N V($)', 'COMPANY BV($)', 'COMPANY B V($)', 'CO BV($)', 'CO B V($)', 'CO NV($)',
             'CO N V($)', 'SA DE CV($)', 'S A DE C V($)', 'SCL DE CV($)', 'S C L DE C V($)', 'SCL($)', 'S C L($)',
             'S C DE R L($)', 'S R L DE C V($)', 'SAC($)', 'S A C($)', 'EIRL($)', 'E I R L($)', 'SRL($)', 'S R L($)',
             ' CIA($)', 'EURL($)', '(^)EURL', 'SARL($)', '(^)SARL', 'SNC($)', '(^)SNC', 'SPC($)', '(^)SPC', 'SPA($)',
             'SAS($)', ' SA($)', ' S A($)', ' SL($)', ' S L($)', ' SC($)', ' S C($)', 'CO WLL($)', 'CO LIB($)',
             ' AS($)', ' A S($)', 'PJSC($)', 'P JSC($)', 'OJSC($)', 'CJSC($)' 'JSC($)', ' EPP($)', ' CB($)', ' C B($)',
             ' CA($)', ' C A($)', ' GIE($)', 'KABUSHIKI KAISHA($)', ' KK($)', 'K K($)', ' BV($)', ' B V($)',
             'YUGEN KAISHA', 'YUGEN', 'KAISHA', 'KAISYA', 'YUGEN KAISYA', 'GYOGYO', 'GYOGYOU', 'GAISHA', ' JU($)',
             'OOO($)', '(^)OOO', 'CO PVT($)', 'COMPANY PVT($)', ' PT($)', ' P T($)', '(^)PT', ' CC($)',
             ' CO($)',  'COMPANY($)', ' NV($)', ' N V($)', '^NA($)', '^N A($)', 'RPTD SOLD.*', 'OWNER UNKNOWN*',
             'CO LT', 'EHF($)', '(^)EHF']
        text_to_remove = '|'.join(text_to_remove)

        if type(elem) == pd.core.series.Series:
            elem = elem.apply(
                lambda x: unidecode(re.sub(r'\(.+\)', ' ', x)).strip() if (x == x) & (x != None) & (x != '') else None)
            elem = elem.apply(
                lambda x: unidecode(re.sub(r'[^\w]+', ' ', x)).strip() if (x == x) & (x != None) & (x != '') else None)
            elem = elem.apply(
                lambda x: re.sub(text_to_remove, ' ', x) if (x == x) & (x != None) * (x != '') else None)
            elem = elem.apply(
                lambda x: re.sub(r'\s+', ' ', x).strip() if (x == x) & (x != None) * (x != '') else None)
            return elem.apply(
                lambda x: re.sub('FISHERY', 'FISHERIES', x) if (x == x) & (x != None) * (x != '') else None)
        elif type(elem) == pd.core.frame.DataFrame:
            elem = elem[check_field].apply(
                lambda x: unidecode(re.sub(r'\(.+\)', ' ', x)).strip() if (x == x) & (x != None) & (x != '') else None)
            elem = elem[check_field].apply(
                lambda x: unidecode(re.sub(r'[^\w]+', ' ', x)).strip() if (x == x) & (x != None) & (x != '') else None)
            elem = elem[check_field].apply(
                lambda x: re.sub(text_to_remove, ' ', x) if (x == x) & (x != None) * (x != '') else None)
            elem = elem[check_field].apply(
                lambda x: re.sub(r'\s+', ' ', x).strip() if (x == x) & (x != None) * (x != '') else None)
            return elem[check_field].apply(
                lambda x: re.sub('FISHERY', 'FISHERIES', x) if (x == x) & (x != None) * (x != '') else None)
        elif (elem != elem) | (elem == None) | (elem == '') | (elem == 0):
            return np.nan
        elif type(elem) == str:
            elem = unidecode(re.sub(r'\(.+\)', ' ', elem)).strip()
            elem = unidecode(re.sub(r'[^\w]+', ' ', elem)).strip()
            elem = re.sub(text_to_remove, ' ', elem)
            elem = re.sub(r'\s+', ' ', elem).strip()
            return re.sub('FISHERY', 'FISHERIES', elem)
        else:
            raise ValueError('Unknown type received')
    else:
        return None


#
# Standardize Integer in a form of string
# because Pandas Series or DataFrame considers
# a column of integers with Nulls as a column of float
# Save it as a string column so that it can be uploaded
# as integer columns when uploading to BigQuery.
#
def standardize_int_str(elem, check_field=True):
    if check_field:
        if type(elem) == pd.core.series.Series:
            return elem.apply(
                lambda x: str(int(float(re.sub('[^\d\.]', '', str(x)))))
                if (x == x) & (x is not None) & (x != '') else None)
        elif type(elem) == pd.core.frame.DataFrame:
            return elem[check_field].apply(
                lambda x: str(int(float(re.sub('[^\d\.]', '', str(x)))))
                if (x == x) & (x is not None) & (x != '') else None)
        elif (elem != elem) | (elem is None) | (elem == ''):
            return None
        elif (type(elem) == str) | (type(elem) == int) | (type(elem) == float):
            return str(int(float(re.sub(r'[^\d\.]', '', str(elem)))))
        else:
            raise ValueError('Unknown type received')
    else:
        return None


#
# Standardize timestamp
#
def standardize_time(elem, check_field=True):
    if check_field:
        if type(elem)==pd.core.series.Series:
            return elem.apply(lambda x: pd.to_datetime(x, errors='coerce') if (x==x)&(x!=None)&(x!='') else None)
        elif type(elem)==pd.core.frame.DataFrame:
            return elem[check_field].apply(lambda x: pd.to_datetime(x, errors='coerce') if (x==x)&(x!=None)&(x!='') else None)
        elif (elem!=elem)|(elem==None)|(elem=='')|(elem==0):
            return np.nan
        elif (type(elem)==str)|(type(elem)==pd.Timestamp):
            return pd.to_datetime(elem, errors='coerce')
        else:
            raise ValueError('Unknown type received')
    else:
        return None


def clean_uvi(x):
    if (type(x)==float)|(type(x)==int):
        if (not np.isnan(x))&(x==x)&(x!=None):
            return str(int(x))
        else:
            return np.nan
    else:
        return re.sub('\s+', ' ', x).strip().upper()


def standardize_uvi(elem, check_field=True):
    if check_field:
        if type(elem)==pd.core.series.Series:
            return elem.apply(lambda x: clean_uvi(x))  
        elif type(elem)==pd.core.frame.DataFrame:
            return elem[check_field].apply(lambda x: clean_uvi(x))
        elif (elem!=elem)|(elem==None)|(elem=='')|(elem==0):
            return None
        elif (type(elem)==int)|(type(elem)==float):
            return str(int(elem))
        elif type(elem)==str:
            return re.sub('\s+',' ',elem).strip().upper()
        else:
            raise ValueError('Unknown type received')
    else:
        return None


def standardize_flag(df, field, rules):
    """
    Flag mapping based on YAML mapping file per registry

    :param df:
    :param field:
    :param rules:
    :return:
    """
    if field:
        if rules:
            #
            # In case it's explicitly "ALL" as an option,
            # returns the preset value
            if "ALL" in rules:
                return rules['ALL']
            #
            # If it's "SAME" option, use the values in the flag field
            elif 'SAME' in rules:
                return df[field]
            #
            # iso3 country code - note that all is turned to upper cases
            else:
                return df[field].apply(
                    lambda x: rules[unidecode(str(x)).strip().upper()]
                    if (x == x) & (x is not None) & (x != '') else None)
        else:
            return None
    else:
        return None


def standardize_geartype(df, field, rules):
    """
    Geartype mapping  based on YAML mapping file per registry

    :param df:
    :param field:
    :param rules:
    :return:
    """
    if field:
        if rules:
            if 'ALL' in rules:
                return rules['ALL']
            elif 'SAME' in rules:
                return df[field]
            #
            # note that when mapping geartype,
            # original values are all turned to lower keys
            else:
                return df[field].apply(
                    lambda x: rules[unidecode(str(x)).strip().lower()]
                    if (x == x) & (x is not None) & (x != '') else None)
        else:
            return None
    else:
        return None
