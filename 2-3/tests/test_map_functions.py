import unittest

from lib.map_functions import get_key, map_lookup, lookup_val, map_set, set_val


class TestMapFunctions(unittest.TestCase):

    def test_get_key(self):
        """
        Test that it can split key into its component parts
        """
        result = get_key("hello/world")
        self.assertEqual(result, ["hello","world"]) 

        result = get_key("hello")
        self.assertEqual(result, ["hello"])

        result = get_key("")
        self.assertEqual(result, [""])

        result = get_key("hello/world-something-else:ipsom#abc")
        self.assertEqual(result, ["hello","world-something-else:ipsom#abc"])

        with self.assertRaises(AttributeError):
            get_key(123)

        with self.assertRaises(TypeError):
            get_key()

    def test_map_lookup(self):
        """
        Test that it can pull a value from a map based on a key
        """
        test_map = {'hello': {'world': {'a':'b','c': 1}},'extra': 'stuff'}

        result = map_lookup(test_map, "hello/world")
        self.assertEqual(result, {'a':'b','c': 1}) 

        result = map_lookup(test_map, "hello/world/a")
        self.assertEqual(result, 'b')

        result = map_lookup(test_map, "hello/world/c")
        self.assertEqual(result, 1)

        result = map_lookup(test_map, "")
        self.assertIsNone(result)

        result = map_lookup(test_map, "hello/you")
        self.assertIsNone(result) 

    def test_lookup_val(self):   
        """
        Test that it can pull a value from a map based on a list of keys
        """
        test_map = {'hello': {'world': {'a':'b','c': 1}},'extra': 'stuff'}

        result = lookup_val(test_map, ["hello","world"])
        self.assertEqual(result, {'a':'b','c': 1}) 

        result = lookup_val(test_map, ["hello","world","a"])
        self.assertEqual(result, 'b')

        result = lookup_val(test_map, ["hello","world","c"])
        self.assertEqual(result, 1)

        result = lookup_val(test_map, [""])
        self.assertIsNone(result)

        result = lookup_val(test_map, ["hello","you"])
        self.assertIsNone(result) 


    def test_map_set(self):
        """
        Test that it can assign a value to a supplied map based on a key
        """
        initial_map = {}

        result_map = {'hello':{'world':'a'}}
        map_set(initial_map, "hello/world", "a") 
        self.assertEqual(initial_map, result_map)

        result_map = {'hello':{'world':{'a':'b'}}}
        map_set(initial_map, "hello/world/a", "b") 
        self.assertEqual(initial_map, result_map)

        result_map = {'hello':{'world':{'a':'b'}}, 'something': 'else'}
        map_set(initial_map, "something", "else") 
        self.assertEqual(initial_map, result_map)

        result_map = {'hello':{'world':{'a':'b'}}, 'something': 'x'}
        map_set(initial_map, "something", "x") 
        self.assertEqual(initial_map, result_map)

    def test_set_val(self):
        """
        Test that it can assign a value to a supplied map based on a list of keys
        """
        initial_map = {}

        result_map = {'hello':{'world':'a'}}
        set_val(initial_map, ["hello","world"], "a") 
        self.assertEqual(initial_map, result_map)

        result_map = {'hello':{'world':{'a':'b'}}}
        set_val(initial_map, ["hello","world","a"], "b") 
        self.assertEqual(initial_map, result_map)

        result_map = {'hello':{'world':{'a':'b'}}, 'something': 'else'}
        set_val(initial_map, ["something"], "else") 
        self.assertEqual(initial_map, result_map)

        result_map = {'hello':{'world':{'a':'b'}}, 'something': 'x'}
        set_val(initial_map, ["something"], "x") 
        self.assertEqual(initial_map, result_map)

if __name__ == '__main__':
    unittest.main()
    
    