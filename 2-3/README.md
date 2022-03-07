
> **NOTE:** Both of these challenges are essentially asking for the same thing, functions to read and set map values based on keys of the form 'a/b/c', hence why they are bundled together and share a common map_functions module.

# Challenge #2

We need to write code that will query the meta data of an instance within aws and provide a json formatted output. The choice of language and implementation is up to you.

**Bonus Points**: The code allows for a particular data key to be retrieved individually

## [metadata.py](metadata.py)

Pulls the list of metadata URLs from the AWS Metadata API and then builds a python dictionary from the resulting key (path to key) and API response value.

Outputs the full json formatted meta data with no paramaters, or a specific value if passed the path key 

To run:
```
python metadata.py [data/key/as/path]
```

Can be used along with [ec2-metadata-mock](https://github.com/aws/amazon-ec2-metadata-mock) to test locally. Set an environment variable to refer to the test server:
```
METADATA_TEST_SERVER=1
```

# Challenge #3

We have a nested object, we would like a function that you pass in the object and a key and get back the value. How this is implemented is up to you.

## [nested_lookup.py](nested_lookup.py)

Looks up a specific value in the supplied nested object (pyhton dictionary in this case) for the supplied key (of the form 'a/b/c') 

To run:
```
python nested_lookup.py {'hello':{'world':'test'}} hello/world

> test
```

## Tests

Associated tests [here](./tests/test_map_functions.py)