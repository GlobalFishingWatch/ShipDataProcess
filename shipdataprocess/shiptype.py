



def determine_shiptype(gears, shiptype_dict):
    ''' 
    determinte_shiptype module receives multiple types of ship and returns the most specific ship type.
    
    --------
    ARGUMENT
    --------
    types: STR, single or multiple combination of ship types joined by '|' (OR) 
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
    
    gears = gears.tolist()
    ### remove Nones
    gears = [gear.replace(' ','').strip() for gear in gears if gear!=None]
    
    ### if 'drifting_longlines|set_longlines' occurs with another entry specifying between the two, take only the specific 
    if 'drifting_longlines|set_longlines' in gears:
        if ('drifting_longlines' in gears)&('set_longlines' in gears):
            gears = [gear for gear in gears if (gear!='drifting_longlines')&(gear!='set_longlines')]
        elif ('drifting_longlines' not in gears)&('set_longlines' not in gears):
            pass
        else:
            gears = [gear for gear in gears if gear!='drifting_longlines|set_longlines']
    
    ### get rid of '|' and take all possible gears individually  
    gears_split=[]
    for g in gears:
        if '|' in g:
            gears_split += g.split('|')
        else:
            gears_split.append(g)
    
    ### map geartype_dict to compare categories (broader ones to be removed)
    #geartype_dict = make_geartype_dict()
    gears = [shiptype_dict[gear] for gear in gears_split if shiptype_dict[gear]!=None]
 
    new_gears = gears[:]
    for gear in new_gears:
        others = [x for x in gears if x!=gear]
        
        for other in others:
            ### see if the gear in question is a subset of anyone of the others, if true, remove it from the list
            if set(gear).issubset(other):
                if gear in gears:
                    gears.remove(gear)

    ### take only end-values (not the categorical information that was mapped from the dictionary)
    values = []
    for gear in gears:
        val = gear[-1]
        if val=='fishing':
            val = 'unknown_fishing'
        elif val=='non_fishing':
            val = 'unknown_not_fishing'
        else:
            pass
        values.append(val)
       
    ### remove redundant values and join together with '|'
    values = list(set(values))
    return '|'.join(values)



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
    
    ### other_fishing, other_not_fishing, unknown_fishing can be replaced by other more specific gears
    #shiptype_dict['other_fishing'] = ['fishing']
    #shiptype_dict['other_not_fishing'] = ['non_fishing']
    shiptype_dict['unknown_fishing'] = ['fishing']
    shiptype_dict['unknown_not_fishing'] = ['non_fishing']
    shiptype_dict['unknown'] = None
    
    return shiptype_dict
