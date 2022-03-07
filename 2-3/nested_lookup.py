import ast
import sys

from lib.map_functions import map_lookup

def main():
    if len(sys.argv) > 2:
        nested_object = ast.literal_eval(sys.argv[1])
        value = map_lookup(nested_object, sys.argv[2])
        print(value)
    else:
        print("usage: nested_lookup.py <nested object> <key>")

if __name__ == "__main__":
    main()
    

