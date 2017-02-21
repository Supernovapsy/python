#!/usr/bin/python # Doesn't work for some reason.

import argparse

# The assumed type of each argument is by default str.
parser = argparse.ArgumentParser(description="Returns the product of two numbers", epilog="argparse practice")
parser.add_argument("number1", help="The first of two multipliers", type=float)
parser.add_argument("number2", help="The second of two multipliers", type=float)
parser.add_argument("-v", "--verbosity", action="count", default=0, help="Increase amount of description for the output (repeat flag for a maximum of 2 times to further increase verbosity)") # add the parameter 'action="store_true"' to make this argument a flag instead of something that takes a value as an argument.
args = parser.parse_args()

if args.verbosity == 1:
    #print str(args.number1) + " x " + str(args.number2) + " = ",
    print "%f x %f = " % (args.number1, args.number2),
elif args.verbosity >= 2:
    print "The product of %f and %f is " % (args.number1, args.number2),

print args.number1 * args.number2
