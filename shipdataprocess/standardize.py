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
# Standardize Integer in a form of string because Pandas Series or DataFrame considers a column of integers with Nulls as a column of float
# Save it as a string column so that it can be uploaded as integer columns when uploading to BigQuery.
#
def standardize_int_str(elem, check_field=True):
    if check_field:
        if type(elem)==pd.core.series.Series:
            return elem.apply(lambda x: str(int(float(re.sub('[^\d\.]','',str(x))))) if (x==x)&(x!=None)&(x!='')&(x!=0) else None)
        elif type(elem)==pd.core.frame.DataFrame:
            return elem[check_field].apply(lambda x: str(int(float(re.sub('[^\d\.]','',str(x))))) if (x==x)&(x!=None)&(x!='')&(x!=0) else None)
        elif (elem!=elem)|(elem==None)|(elem=='')|(elem==0):
            return None
        elif (type(elem)==str)|(type(elem)==int)|(type(elem)==float):
            return str(int(float(re.sub('[^\d\.]','',str(elem)))))       
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

    
## flag mapping
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
        
## geartype mapping
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
