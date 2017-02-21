'''import unittest

class Test_gold_room(unittest.TestCase):

    def test test_greedy(self):
        self.

def gold_room():
    print "You enter a room full of gold, how much gold do you take?"
    amount = raw_input('> ')
    if "0" in amount or "1" in amount:
        how_much = int(amount)
    else:
        dead("Man, learn to type a number.")
    
    if how_much < 50:
        print "Nice, you're not greedy, you win!"
        exit(0)
    else:
        dead("You greedy bastard!")
        
def dead(str):
    print str, "Good job!"
    
gold_room()'''

import os
def say_hello(input_func):
    name = input_func()
    return "Hello " + name

def prompt_for_name():
    return raw_input("What is your name? ")

print say_hello(prompt_for_name)
# Normally would pass in methods, but lambdas can be used for brevity
print say_hello(lambda: open("a.txt").readline())
print say_hello(lambda: os.environ.get("USER"))
