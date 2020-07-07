# coding: utf-8

### field standardization functions
import pandas as pd
import numpy as np
import re
from django.utils.encoding import smart_str
from unidecode import unidecode

#
# Standardize IMO numbers (ignore all letters and characters but numbers)
# If it comes with pandas Series or DataFrame, make sure it saves IMO numbers in STRING, 
# as pandas Seires or DataFrame usually turn INTEGER to FLOAT in the presence of NULL in the same column.
#
def standardize_imo(elem, check_field=True):
    if check_field:
        if type(elem)==pd.core.series.Series:
            return elem.apply(lambda x: str(int(float(re.sub('[^\d\.]','',str(x)))))\
                                if (x==x)&(x!=None)&(x!='')&(x!=0) else np.nan)
        elif type(elem)==pd.core.frame.DataFrame:
            return elem[check_field].apply(lambda x: str(int(float(re.sub('[^\d\.]','',str(x)))))\
                                if (x==x)&(x!=None)&(x!='')&(x!=0) else np.nan)
        elif (elem!=elem)|(elem==None)|(elem=='')|(elem==0):
            return np.nan
        elif (type(elem)==str)|(type(elem)==int)|(type(elem)==float):
            return int(float(re.sub('[^\d\.]','',str(elem))))
        else:
            raise ValueError('Unknown type received')
    else:
        return np.nan

#
# Standardize floating numbers. 
# Make sure to remove all comma separators (,). 
#
def standardize_float(elem, check_field=True):
    if check_field:
        if type(elem)==pd.core.series.Series:
            return elem.apply(lambda x: float(str(x).replace(',','')) if (x==x)&(x!=None)&(x!='')&(x!=0) else np.nan)
        elif type(elem)==pd.core.frame.DataFrame:
            return elem[check_field].apply(lambda x: float(str(x).replace(',','')) if (x==x)&(x!=None)&(x!='')&(x!=0) else np.nan)
        elif (elem!=elem)|(elem==None)|(elem=='')|(elem==0):
            return np.nan
        elif (type(elem)==str)|(type(elem)==int)|(type(elem)==float):
            return float(str(elem).replace(',',''))
        else:
            raise ValueError('Unknown type received')
    else:
        return np.nan
    
#
# Standardize string. Make sure all excessive white space to just 1 space ' '. 
#
def standardize_str(elem, check_field=True):
    if check_field:
        if type(elem)==pd.core.series.Series:
            return elem.apply(lambda x: re.sub('\s+',' ', smart_str(x)).strip().upper() if (x==x)&(x!=None)&(x!='') else None)
        elif type(elem)==pd.core.frame.DataFrame:
            return elem[check_field].apply(lambda x: re.sub('\s+',' ', smart_str(x)).strip().upper() if (x==x)&(x!=None)&(x!='') else None)
        elif (elem!=elem)|(elem==None)|(elem=='')|(elem==0):
            return np.nan
        elif type(elem)==str:
            return re.sub('\s+',' ',elem).strip().upper()
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
             ' CO($)',  'COMPANY($)', ' NV($)', ' N V($)', '^NA($)', '^N A($)', 'RPTD SOLD.*', 'OWNER UNKNOWN*']
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
# Standardize Integer in a form of string because Pandas Series or DataFrame considers a column of integers with Nulls as a column of float
# Save it as a string column so that it can be uploaded as integer columns when uploading to BigQuery.
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
        elif (elem != elem) | (elem is not None) | (elem == ''):
            return None
        elif (type(elem) == str) | (type(elem) == int) | (type(elem) == float):
            return str(int(float(re.sub('[^\d\.]', '', str(elem)))))
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

    
#
# Flag mapping based on YAML mapping file per registry
#
def standardize_flag(df, field, rules):
    if field:
        if rules:
            if "ALL" in rules:
                return rules['ALL']
            elif 'SAME' in rules:
                return df[field]
            else: ## iso3 country code - note that all is turned to upper cases
                return df[field].apply(lambda x: rules[unidecode(str(x)).strip().upper()] if (x==x)&(x!=None)&(x!='') else None)
        else:
            return None
    else:
        return None
        
#
# Geartype mapping  based on YAML mapping file per registry
#
def standardize_geartype(df, field, rules):
    if field:
        if rules:
            if 'ALL' in rules:
                return rules['ALL']
            elif 'SAME' in rules:
                return df[field]
            else: ## note that when mapping geartype, original values are all turned to lower keys
                return df[field].apply(lambda x: rules[unidecode(str(x)).strip().lower()] if (x==x)&(x!=None)&(x!='') else None)
        else:
            return None
    else:
        return None
