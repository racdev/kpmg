def get_key(key_string):
    return key_string.split("/")


def map_lookup(map, key_string):
    key = get_key(key_string)
    return lookup_val(map, key)

def lookup_val(map, keys):   
    local_map = map.copy() 
    for k in keys:
        if k in local_map:
            local_map = local_map[k]
        else:
            return None
    
    return local_map


def map_set(map, key_string, value):
    key = get_key(key_string)

    set_val(map, key, value)

def set_val(map, keys, value):
    for k in keys[:-1]:
        if k not in map:
            map = map.setdefault(k, {})
        elif not isinstance(map[k], dict):
            map[k] = {}
            map = map[k]
        else:
            map = map[k]
    map[keys[-1]] = value

