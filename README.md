# shipdataprocess (current latest version 0.8.3)

shipdataprocess provides packages and modules that help users process raw ship data. The data may come from Automatic identification system (AIS) transmission or others. Ship data includes vessel's name, callsign, shiptype, geartype information etc. You might find the packages here useful for normalizing ship names and IRCS (International Radio Call Sign) and for dealing with various types of ships and fishing gears. Typical usage often looks like this:

    #!/usr/bin/env python

    from shipdataprocess.normalize import normalize_shipname, normalize_callsign

    from shipdataprocess.shiptype import determine_shiptype, make_shiptype_dict, reduce_to_specifics, reduce_to_specifics_with_multiples

    from shipdataprocess.standardize import standardize_imo, standardize_float, standardize_str, standardize_int_str, standardize_time, standardize_flag, standardize_geartype

    from shipdataprocess.collapse import non_zero_mean, non_zero_std, most_common_value, most_common_num, most_common_str, str_attached, min_time, max_time


# Contributors
This work was done based on the previous work of the team of Global Fishing Watch (GFW).

Jaeyoon Park, 
David Kroodsma,
Andres Arana,
Enrique Tuya,
Bjorn Bergman,
Paul Woods

# Development

```
virtualenv venv
source venv/bin/activate
pip install -e .
py.test tests
```

# Changes/updates
See `./CHANGES.md`
