import pandas as pd
import numpy as np



def determine_shiptype(gears, shiptype_dict):
    ''' 
    determinte_shiptype module receives multiple types of ship and returns the most specific ship type.
    
    --------
    ARGUMENT
    --------
    gears: SERIES, LIST, OR STR, single or multiple combination of ship types joined by '|' (OR) 
    (examples: fixed_gear|set_longlines, cargo)
    --------

    ------
    RETURN 
    ------
    STR or None, select the most detailed type among the ship types received if they are all in one category, 
    otherwise a combination of ship types.
    (examples: fixed_gear|set_longlines -> set_longlines, trawler|fixed_gear|set_longlines -> trawler|set_longlines)
    ------
    '''
    

    ## if there is no information on gears, then return None
    if len(gears)==0:
        return None
    
    ### make sure the entry is a list of strings
    if type(gears)==str:
        gears = [gears]
    elif type(gears)==list:
        pass
    else: gears = gears.tolist()
    
    ### remove Nones
    gears = [gear.replace(' ','').strip() for gear in gears if (gear!=None)&(gear==gear)&(gear!='')]
    
    ### take only specific ones if there are several possibly duplicated ones (example: trawlers, trawlers|purse_seines)
    gears = reduce_to_specifics_with_multiples(gears, shiptype_dict)

    ### get rid of '|' and take all possible gears individually  
    gears_split=[]
    for g in gears:
        if '|' in g:
            gears_split += g.split('|')
        else:
            gears_split.append(g)
    
    ### map geartype_dict to compare categories (broader ones to be removed)
    gears = reduce_to_specifics(gears_split, shiptype_dict)

    ### remove redundant values and join together with '|'
    gears = list(set(gears))
    final_value = '|'.join(gears)
    if final_value=='':
        return None
    else:
        return final_value



### function that makes geartype dictionary from shiptypes yaml file
def make_shiptype_dict(shiptypes):
    '''
    This module returns a categorical dictionary of ship types from a ship type yml file received.
    Values of the dictionary show where a specific ship type is situated in the ship type category tree. 

    --------
    ARGUMENT
    --------
    shiptypes: DICT, usually loaded from a .yml file that place categorically all possible ship types as a tree
    --------

    ------
    RETURN
    ------
    shiptype_dict: DICT, shiptype categorical dictionary
    (examples: (key, value) -> (set_longlines, (fishing, fixed_gear, set_longlines)))
    ------
    '''
        
    ### create a geartype dictionary where each gear has categorical information
    shiptype_dict = {}
    for stype in shiptypes:
        for l1 in shiptypes[stype]:
            shiptype_dict[l1] = [stype, l1]
            if shiptypes[stype][l1] is not None:
                for l2 in shiptypes[stype][l1]:
                    shiptype_dict[l2] = [stype, l1, l2]
                    if shiptypes[stype][l1][l2] is not None:
                        for l3 in shiptypes[stype][l1][l2]:
                            shiptype_dict[l3] = [stype, l1, l2, l3]
                            if shiptypes[stype][l1][l2][l3] is not None:
                                for l4 in shiptypes[stype][l1][l2][l3]:
                                    shiptype_dict[l4] = [stype, l1, l2, l3, l4]
    
    ### other_fishing, other_not_fishing, unknown_fishing can be replaced by other more specific gears
    shiptype_dict['fishing'] = ['fishing']
    shiptype_dict['non_fishing'] = ['non_fishing']
    shiptype_dict['unknown'] = None
    shiptype_dict[''] = None
    
    return shiptype_dict


### function to choose only specific gear values if broader level values exist with specific level values
def reduce_to_specifics(gears, shiptype_dict):
    '''
    this module reduces the list of gear values only to contain specific gear values if there are broader gear values together

    --------
    ARGUMENT
    --------
    gears: LIST of strings that are gear types predefined
    --------

    ------
    RETURN
    ------
    values: LIST of string that are gear types predefined

    '''
    if len(gears)==0:
        return []
    
    ### reduce only single gear values
    singles = [gear for gear in gears if '|' not in gear]
    multiples = [gear for gear in gears if '|' in gear]

    ### mapped to shiptype dictionary values
    gears_mapped = [shiptype_dict[gear] for gear in singles if shiptype_dict[gear]!=None]
    
    for gear in gears_mapped:
        others = [g for g in gears_mapped if g!=gear]

        for other in others:
            ### see if the gear in question is a subset of anyone of the others, if true, remove it from the list
            if set(gear).issubset(other):
                if gear in gears_mapped:
                    gears_mapped.remove(gear)
       
    ### return only end values as in a list
    reduced = []
    for gear in gears_mapped:
        val = gear[-1]
        reduced.append(val)
    reduced = list(set(reduced))
    final = reduced + multiples
    
    return final



def reduce_to_specifics_with_multiples(gears, shiptype_dict):
    if len(gears)==0:
        return []
    
    ### reduce singles to specifics if possible
    gears = reduce_to_specifics(gears, shiptype_dict)
    singles = [gear for gear in gears if '|' not in gear]
    multiples = [gear for gear in gears if '|' in gear]
    
    if len(multiples)>0:
        for multiple in multiples:
            flags=[]
            elems = multiple.split('|')
            
            for elem in elems:
                ### look at elements of multiples if they can be reduced to specifics with single values
                vals = [reduce_to_specifics([elem, single], shiptype_dict) for single in singles \
                        if len(reduce_to_specifics([elem, single], shiptype_dict))==1]
                if len(vals)==1:
                    flags.append(1)
                    reduced = vals[0]
                else:
                    flags.append(0)

            ### if it can be reduced, then remove this multiple and put this reduced values
            if sum(flags)==1:
                gears.remove(multiple)
                gears = gears + reduced
    
    ### final clearing-up
    gears = reduce_to_specifics(gears, shiptype_dict)
    
    return gears



def is_fishing_vessel(gear, shiptype_dict):
    if (gear=='')|(gear==None)|(gear!=gear):
        return None

    else:
        gear = gear.replace(' ','')
        gear_mapped=[]
        gears = gear.split('|')
        
        ## create a list of gears mapped to 0s (non-fishing gear) or 1s (fishing gear)
        for gear in gears:
            if shiptype_dict[gear][0]=='fishing':
                gear_mapped.append(1)
            else:
                gear_mapped.append(0)
        if np.prod(gear_mapped)==1: ## if all mapped gears are 1s (therefore fishing vessel)
            isfishingvessel = True
        elif sum(gear_mapped)==0: ## if all mapped gears are 0s (therefore non-fishing vessel)
            isfishingvessel = False
        else: ## not determinable, return None
            return None
            
    return isfishingvessel
