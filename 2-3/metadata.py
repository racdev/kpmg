import requests
import json
import sys
import os

from lib.map_functions import map_set, map_lookup

# function that returns metadata from the metadata server
def get_metadata(url, is_value=False):
    value = requests.get(url).text
    if is_value:
        return value
    else:
        path_list = [x for x in value.splitlines()]
        return path_list

def main():

    metadata_server = "http://localhost:1338/latest/meta-data/" if os.environ.get('METADATA_TEST_SERVER') == "1" else "http://169.254.169.254/latest/meta-data/" 
    path_dict = {}
    path_list = get_metadata(metadata_server)
    for path in path_list:
        path_value = get_metadata(metadata_server+path, True)
        map_set(path_dict, path, path_value)
    
    if len(sys.argv) > 1:
        path = sys.argv[1]
        value = map_lookup(path_dict, path)
        print(value)
    else:
        json_data = json.dumps(path_dict, indent=4)
        print(json_data)

if __name__ == "__main__":
    main()
    