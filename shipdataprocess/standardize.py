### field standardization functions
import pandas as pd
import numpy as np
import re

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
    
def standardize_str(elem, check_field=True):
    if check_field:
        if type(elem)==pd.core.series.Series:
            return elem.apply(lambda x: re.sub('\s+',' ', str(x)).strip().upper() if (x==x)&(x!=None)&(x!='') else None)
        elif type(elem)==pd.core.frame.DataFrame:
            return elem[check_field].apply(lambda x: re.sub('\s+',' ', str(x)).strip().upper() if (x==x)&(x!=None)&(x!='') else None)
        elif (elem!=elem)|(elem==None)|(elem=='')|(elem==0):
            return np.nan
        elif type(elem)==str:
            return re.sub('\s+',' ',elem).strip().upper()
        else:
            raise ValueError('Unknown type received')
    else:
        return None
    
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
    
def standardize_time(elem, check_field=True):
    if check_field:
        if type(elem)==pd.core.series.Series:
            return elem.apply(lambda x: pd.to_datetime(x, errors='coerce') if (x==x)&(x!=None)&(x!='') else None)
            #return elem.apply(lambda x: pd.to_datetime(x, format='%Y-%m-%d %H:%M:%S', errors='coerce')\
            #                    if (x==x)&(x!=None)&(x!='') else None)
        elif type(elem)==pd.core.frame.DataFrame:
            return elem[check_field].apply(lambda x: pd.to_datetime(x, errors='coerce') if (x==x)&(x!=None)&(x!='') else None)
        elif (elem!=elem)|(elem==None)|(elem=='')|(elem==0):
            return np.nan
        elif (type(elem)==str)|(type(elem)==pd.tslib.Timestamp):
            return pd.to_datetime(elem, errors='coerce')
            #return pd.to_datetime(elem, format='%Y-%m-%d %H:%M:%S', errors='coerce')
        else:
            raise ValueError('Unknown type received')
    else:
        return None
    
## flag mapping
def standardize_flag(elem, check_field):
    if check_field:
        if "ALL" in check_field:
            return check_field['ALL']
        elif 'SAME' in check_field:
            return elem
        else: ## iso3 country code - note that all is turned to upper cases
            return elem.apply(lambda x: check_field[x.strip().upper()] if (x==x)&(x!=None)&(x!='') else None)
    else:
        return None
        
## geartype mapping
def standardize_geartype(elem, check_field):
    if check_field:
        if 'ALL' in check_field:
            return check_field['ALL']
        elif 'SAME' in check_field:
            return elem
        else: ## note that when mapping geartype, original values are all turned to lower keys
            return elem.apply(lambda x: check_field[x.strip().lower()] if (x==x)&(x!=None)&(x!='') else None)
    else:
        return None
