"""
This file contains functions that help collapse (multiple) rows
for each vessel found in the process of producing Global Fishing Watch's
internal vessel database.

Last updated: 2022-01-24
Jaeyoon Park
"""

import pandas as pd
import numpy as np
import re
from collections import Counter


def non_zero_mean(x):
    try:
        x = x[(x != 0) & (x is not None)]
        if len(x) == 0:
            return 0.0
        else:
            return x.mean()
    except AttributeError:
        return 0.0


def non_zero_std(x):
    try:
        x = x[(x != 0) & (x is not None)]
        if len(x) < 2:
            return 0.0
        else:
            return x.std()
    except AttributeError:
        return 0.0


def most_common_value(x):
    """
    Remove if standard deviation is too big compared to mean value of
    all numbers. The standard deviation threshold is set to be 10%.

    x: Pandas Series or list, a list of numerical values
    (for length, tonnage, engine power)
    """
    if (type(x) == list) & (len(x) > 0):
        x = pd.Series(x)
    if (type(x) == pd.core.series.Series) & (len(x.dropna()) > 0):
        x_mean = non_zero_mean(x)
        x_std = non_zero_std(x)
        if x_std > x_mean * 0.1:
            return np.nan
        else:
            return x_mean
    else:
        return np.nan


def most_common_value_with_confidence(cx):
    """
    same functionality as most_common_value() but with confidence level
    taken into account

    cx: Pandas Series or list, a list of numerical values
    (for length, tonnage, engine power)
    with a confidence level indicator attached with '-' in front of the value.
    """
    if (type(cx) == pd.core.series.Series) & (len(cx) > 0):
        if len(cx.dropna()) == 0:
            return np.nan
        else:
            cx = list(cx.values)
    if (type(cx) == list) & (len(cx) > 0):
        clist = [
            int(elem.split("-")[0])
            for elem in cx
            if (elem == elem) & (elem is not None)
        ]
        xlist = [elem for elem in cx if (elem == elem) & (elem is not None)]
        if len(clist) > 0:
            max_c = max(clist)
            x = [
                float(elem.split("-")[1])
                for elem in xlist
                if int(elem.split("-")[0]) == max_c
            ]
            # Call the function to return the most common value
            return most_common_value(x)
        else:
            return np.nan
    else:
        return np.nan


def most_common_num(x):
    """
    Return the most common number (mostly for imo collapsing).

    x: Pandas Series, a list of numbers
    """
    try:
        x = x.dropna()
        if len(x) == 0:
            return np.nan
        else:
            vals = x.values
            vs = [v for v in vals if (v != 0)]
            # vs = list(set(vs))
            if len(vs) == 0:
                return np.nan
            else:
                data = Counter(vs)
                return max(vs, key=data.get)
    except AttributeError:
        return np.nan


def most_common_str(x):
    """
    Return the most common string.

    x: Pandas Series, a list of values in string
    """
    try:
        x = x.dropna()
        if len(x) == 0:
            return np.nan
        else:
            vs = [
                re.sub(r"\s+", " ", str(v)).strip().upper() for v in x.values
            ]
            vs = [v for v in vs if v != ""]
            # vs = list(set(vs))
            if len(vs) == 0:
                return np.nan
            else:
                data = Counter(vs)
                return max(vs, key=data.get)

    except AttributeError:
        return np.nan


def str_attached(x):
    """
    Return all strings joined. If the values are in numbers, convert them
    to string and combined.

    :param x: Pandas Series or list
    :return: A joined string
    """
    try:
        x = x.dropna()
        if len(x) == 0:
            return np.nan
        else:
            x = x.apply(
                lambda v: str(int(v))
                if (type(v) == float) | (type(v) == int)
                else v
            )
            vals = x.values.tolist()
            # vs = [str(v).strip() for v in vals if (v==v)&(v!=None)&(v!='')]
            # vs = [v for v in vs if (v!='')]
            vs = list(set(vals))
            return ", ".join(sorted(vs))
    except AttributeError:
        return np.nan


def min_time(x):
    """
    Return the minimum time

    :param x: Pandas Series
    :return: Timestamp
    """
    vals = x.values
    vs = [v for v in vals if (v == v) & (v is not None) & (v != "")]
    vs = pd.Series(vs)

    return vs.min()


def max_time(x):
    """
    Return the maximum time

    :param x: Pandas Series
    :return: Timestamp
    """
    vals = x.values
    vs = [v for v in vals if (v == v) & (v is not None) & (v != "")]
    vs = pd.Series(vs)

    return vs.max()


def highest_confidence(x):
    """
    Return the maximum confidence if none return 1 (the lowest).

    :param x: Pandas Series or list
    :return: Integer
    """
    x = x.dropna()
    if len(x) > 0:
        return max(x.tolist())
    else:
        return 1
