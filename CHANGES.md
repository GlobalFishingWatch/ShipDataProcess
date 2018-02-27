Changes
=======

Higher level changes affecting the API or data.

v0.1.0, 2017-10-10 -- Initial release.
v0.2.0, 2017-10-24 -- Update on new shipcodes, removal of special cases for roman numeral attachment.
v0.2.1, 2017-10-24 -- Treatment of letters encoded in utf8 or iso_8859-1.
v0.2.4, 2017-10-26 -- Change in readme file.
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
