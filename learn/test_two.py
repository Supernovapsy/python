import os
import unittest

def say_hello(input_func):
    name = input_func()
    return "Hello " + name

def prompt_for_name():
    return raw_input("What is your name? ")

#print say_hello(prompt_for_name)
# Normally would pass in methods, but lambdas can be used for brevity
#print say_hello(lambda: open("a.txt").readline())
#print say_hello(lambda: os.environ.get("USER"))

class TestHello(unittest.TestCase):
    def test_say_hello(self):
        output = say_hello(lambda: "test")
        self.assertTrue(output == "Hello test")
        #with self.assertRaises(AssertionError):
        #    self.assertTrue(output == "Hello test")
            
if __name__ == '__main__':
    unittest.main()
    
