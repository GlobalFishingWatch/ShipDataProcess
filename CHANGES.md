Changes
=======

Higher level changes affecting the API or data.

v0.1.0, 2017-10-10 -- Initial release  
v0.2.0, 2017-10-24 -- Update on new shipcodes, removal of special cases for roman numeral attachment  
v0.2.1, 2017-10-24 -- Treatment of letters encoded in utf8 or iso_8859-1  
v0.2.4, 2017-10-26 -- Change in readme file  
v0.2.5, 2017-10-26 -- Fix a bug with R/V  
v0.3.0, 2017-10-27 -- Convert numbers in letter to numerals and add country specific appendixes  
v0.3.1, 2017-10-27 -- Change package name to shipdataprocess  
v0.3.2, 2017-10-28 -- Change project name to shipdataprocess  
v0.4.0, 2017-11-30 -- Add standardize.py and collapse.py, revise shiptype.py  
v0.4.1, 2017-12-05 -- Add type of Pandas DataFrame in standardize.py  
v0.4.3, 2017-12-17 -- Change in make_shiptype_dict()  
v0.5.0, 2017-12-29 -- Add setup.py, fix unit tests  
v0.5.1, 2018-01-04 -- Add new module reduce_to_general() in shiptype.py   
v0.5.2, 2018-01-25 -- Add determine_shiptype_simple() in shiptype.py  
v0.5.3, 2018-01-25 -- Fix a bug with list sort in determine_shiptype and determine_shiptype_simple() in shiptype.py  
v0.5.4, 2018-01-25 -- Fix a bug in reduce_to_specific() in shiptype.py to remove redundant gear types  
v0.5.5, 2018-02-27 -- Add determine_shiptype_with_confidence() in shiptype.py to pull best values taken with confidence level of registries  
v0.5.6, 2018-02-27 -- Add select_high_confidence_geartype() in shiptype.py to select higher confident value between the two geartypes  
v0.5.7, 2018-02-27 -- Fix a bug in select_high_confidence_geartype()  
v0.6.0, 2018-04-25 -- Add new modules with confidence level, fix several modules in collapse.py and standardize.py  
v0.6.1, 2018-04-26 -- Add standardize_uvi() and add new lines for normalization of 1ST, 2ND ...  
v0.6.2, 2018-04-27 -- Fix a bug in standardize_uvi() by adding clean_uvi() module  
v0.6.6, 2018-04-27 -- Fix a bug in standardize_uvi()  
v0.6.7, 2019-02-13 -- Make it compatible with Python 3.x for unicode/unidecode   
v0.6.8, 2019-03-02 -- Fix a bug in standardize_flag and standardize_geartype for the case when fields are Null  
v0.6.9, 2019-04-19 -- Upgrade pd.tslib.Timestamp with pd.Timestamp as tslib is depreciated now  
v0.6.10, 2019-7-28 -- Add standardize_owner()  
v0.6.11, 2019-7-28 -- Fix a bug in standardize_owner()  
v0.6.12, 2019-07-29 -- Add several more standardization rules for standardize_owner()  
v0.6.13, 2019-08-21 -- Not convert int 0 to Null string in standardize_int_str()  
v0.6.14, 2020-11-05 -- Add imo_checksum(), fix standardize_imo() to remove any number that does not get through IMO checksum nor noisy string. Fix standardize_str() to preserve upper/lower cases for URLs  
v0.6.15, 2020-11-06 -- Fix a bug in normalize_shipname() and normalize_callsign() regarding None  
v0.6.16, 2020-11-26 -- Make smart_upper() to capture multiple URLs not to capitalize them  
v0.6.17, 2021-07-30 -- Add Indonesian prefix and Chinese HAO suffix to the list of prefix/suffix to be removed 
v0.6.18, 2021-08-04 -- Fix a bug in normalize_callsign() regarding NULL/NONE  
v0.7.0, 2022-01-26 -- Fix it to work only in Python 3.6 or above, codes are compliant with PEP8, dependencies are clearer (Django removed)   
v0.7.1, 2022-01-27 -- Fix a bug related to the shift to Python 3.6 or above compatibility  
v0.8.0, 2023-06-07 -- Improve normalize_shipname() to replace STA and STA. values to SANTA and fix discrepancy with the trailing 0s and suffix N
v0.8.2, 2023-08-21 -- Fix a bug in normalize_shipname() regarding STA./STA replace feature.
v0.8.3, 2024-04-04 -- Fix a bug in standardize_int_str(). Check if string is an integer before trying to cast.

 
