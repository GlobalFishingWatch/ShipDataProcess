import pandas as pd
import numpy as np
import re
from collections import Counter


### helper functions for collapsing rows by vessel

def non_zero_mean(x):
    try:
        x = x[(x!=0)&(x!=None)]
        if len(x)==0: return 0.0
        else: return x.mean()
    except:
        return 0.0
    
def non_zero_std(x):
    try:
        x = x[(x!=0)&(x!=None)]
        if len(x)<2: return 0.0
        else: return x.std()
    except: 
        return 0.0
    
def most_common_value(x): ## remove if standard deviation is too big compared to mean value of all numbers
    '''remove if standard deviation is too big compared to mean value of all numbers'''
    if (type(x)==list)&(len(x)>0):
        x = pd.Series(x)
    if (type(x)==pd.core.series.Series)&(len(x.dropna())>0):
        x_mean = non_zero_mean(x)
        x_std = non_zero_std(x)
        if x_std > x_mean * 0.1:
            return np.nan
        else:
            return x_mean
    else:
        return np.nan

def most_common_value_with_confidence(cx):
    '''same functionality as most_common_value() but with confidence level taken account'''
    if (type(cx)==pd.core.series.Series)&(len(cx)>0):
        if len(cx.dropna())==0:
            return np.nan
        else:
            cx = list(cx.values)
    if (type(cx)==list)&(len(cx)>0):
        clist = [int(elem.split('-')[0]) for elem in cx if (elem==elem)&(elem!=None)]
        xlist = [elem for elem in cx if (elem==elem)&(elem!=None)]
        if len(clist)>0:
            max_c = max(clist)
            x = [float(elem.split('-')[1]) for elem in xlist if int(elem.split('-')[0])==max_c]
            return most_common_value(x)
        else:
            return np.nan
    else:
        return np.nan
    
def most_common_num(x): ## mostly for imo collapsing
    try:
        x = x.dropna()
        if len(x)==0:
            return np.nan
        else:
            vals = x.values
            vs = [v for v in vals if (v!=0)]
        #vs = list(set(vs))
            if len(vs)==0:
                return np.nan
            else: 
                data = Counter(vs)
                return max(vs, key=data.get)
    except:
        return np.nan
    
def most_common_str(x):
    try:
        x = x.dropna()
        if len(x)==0:
            return np.nan
        else:
            vals = x.values
            vs = [re.sub('\s+',' ',str(v)).strip().upper() for v in x.values]
            vs = [v for v in vs if v!='']
        #vs = list(set(vs))
            if len(vs)==0:
                return np.nan
            else:
                data = Counter(vs)
                return max(vs, key=data.get)

        #if len(vs)==1:
        #    return vs[0]
        #else:
        #    return None
    except:
        return np.nan
    
def str_attached(x): ## join all strings
    try:
        x = x.dropna()
        if len(x)==0:
            return np.nan
        else:
            x = x.apply(lambda v: str(int(v)) if (type(v)==float)|(type(v)==int)|(type(v)==long) else v)  
            vals = x.values.tolist()
        #vs = [str(v).strip() for v in vals if (v==v)&(v!=None)&(v!='')]
        #vs = [v for v in vs if (v!='')]
            vs = list(set(vals))
            return ', '.join(sorted(vs))
    except:
        return np.nan
    
def min_time(x):
    vals = x.values
    vs = [v for v in vals if (v==v)&(v!=None)&(v!='')]
    vs = pd.Series(vs)
    return vs.min()

def max_time(x):
    vals = x.values
    vs = [v for v in vals if (v==v)&(v!=None)&(v!='')]
    vs = pd.Series(vs)
    return vs.max()

def highest_confidence(x):
    x = x.dropna()
    if len(x)>0:
        return max(x.tolist())
    else:
        return 1
