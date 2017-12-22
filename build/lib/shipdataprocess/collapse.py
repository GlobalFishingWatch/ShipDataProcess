import pandas as pd
import numpy as np
import re


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
    x_mean = non_zero_mean(x)
    x_std = non_zero_std(x)
    if x_std > x_mean * 0.1:
        return None
    else:
        return x_mean
    
def most_common_num(x): ## mostly for imo collapsing
    try:
        vals = x.values
        vs = [v for v in vals if (v==v)&(v!=None)&(v!=0)&(v!='0')&(v!='')]
        vs = list(set(vs))
        if len(vs)==1:
            return vs[0]
        else: 
            return None
    except:
        return None
    
def most_common_str(x):
    try:
        vals = x.values
        vs = [v for v in vals if (v==v)&(v!=None)]
        vs = list(set(vs))
        if len(vs)==1:
            return vs[0]
        else:
            return None
    except:
        return None
    
def str_attached(x): ## join all strings
    try:
        vals = x.values
        vs = [str(v).strip() for v in vals if (v==v)&(v!=None)&(v!='')]
        vs = [v for v in vs if (v!='')]
        vs = list(set(vs))
        if len(vs)==0:
            return None
        else:
            return ', '.join(vs)
    except:
        return None
    
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
