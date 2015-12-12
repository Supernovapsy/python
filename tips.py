#!/usr/bin/python
# This file has interesting things about python

# Python is a structured language, as opposed to a free-form language like C.
# Since structure is imposed on Python, naturally readability
# becomes more imposed on Python.
# __name__ stores the name of the main module (this script) in a string.
print __name__ # Should be __main__
# Defining a function shadows already defined functions.
temp = list
def list():
    return "this function works"
list_object = list()
print list_object
# However, I can store the function as an object in some other variable,
# and later restore the original name with its original function.
list = temp
list_object = list()
print list_object

# However, one cannot shadow some built-in functions like print

# In python, each character in a file is a byte, and so when you go to a
# certain byte position using file.seek(), the number represents the
# character at the same position as the byte count you passed to seek().

# Python is able to make extensive use of the default parameter concept in C/C++
# that is futher improved in Python. Multiple parameters can assume default
# values, and by explicitly setting keyword arguments, function arguments do
# not have to be stated in order, and so not only the last argument can have a
# default value as is usually the case in C++.

# Each python file can be imported as a module, and all functions inside the file
# become functions of the module which can be used by an outside script.

# range(a, b) gives a list of integers [a, b)

# the for loop in python dereferences the object looped for you.

# The print separation operator for strings is the comma, and a space is
# automatically inserted between objects.

# The concatentation operator is +, and can be used for all iterables, not just strings.

# We can also redefine builtin variables.
tmp = True
True = False
whatami = True
print whatami
True = tmp # need to restore

# Use a while-loop only to loop forever, and that means probably never. This only applies to Python; other languages are different.

# Use a for-loop for all other kinds of looping, especially if there is a fixed or limited number of things to loop over.

# http://effbot.org/zone/python-with-statement.htm
# Do something "with" this "as" that

# In python, all variables declared in a file but not in a function is accessible
# anywhere in the file, including functions. This is especially important to note
# because if otherwise a variable undeclared in a function but defined in the file
# might be accidentally used in the function, causing undesired behaviour.
# but variable shadowing is NOT applicable in different scopes (indents in python).
# Only the function scope obeys variable isolation, and then only provides write-
# protection where global variables (variables in the file body and not functions)
# are read-only. In order to access these variables in functions, the global keyword
# must be used to declare the variable to remove write-protection in the function.

# The opposite of the split function of strings is the join function. By calling
# this function and passing in a list of strings, it concatenates the string
# elements and separates each with the string from which the join member function
# was called.

# One can index into lists just as one can index into arrays in
# matlab. [#:#] This is however done using the half-open range
# convention, not the closed range convention used by matlab.
# this is like the substr function in C++, except it applies to
# all lists in Python.

# not is !, and is &&, and or is || in Python;
# all other relational operators are the same as in other
# languages.

# When evaluated in an if statement, None is False.

# When iterating through a list of 2-tuples, one can unpack
# the variable after the "in" into two variables after the
# "for", which unpacks the list into two single-valued lists.

# Python does not allow for statements like below which might easily cause bugs.
# def this_doesnt_work(x):
#     return x = 5

# When calling or referring to functions, the brackets must
# be shown to distinguish them from other meanings such
# as types.

print dict
print dict()

# Further, each name can only represent one thing - whether it
# is a function, a class, or an object of some kind. It cannot
# be overloaded, even there is a simple method to separate them.
# Again, Python aims for code readability and minimization of
# coding errors

# When a list is referred on the RHS, it gives a reference to it.
# When a list is referred on the RHS with slicing, it returns a copy of the list.

# When defining a function, default arguments/parameters need to follow
# non-default arguments/parameters.

########################## FUNCTION PARAMETERS ##################################

# Python has a flexible way for calling parameters from functions.
# The parameter definition is broken into two parts: the formal parameters and the informal parameters.
# Formal parameters can take the form of a regular argument variable as in C, or can have a default
# argument applied to it, but variables with default values must be defined after the positional
# arguments in the formal portion of the parameter list.
# The formal arguments can be called using the positional method or the keyword method. The positional
# method applies values in the calling instance to function arguments in the order in which they are defined.
# The keyword method can be used anytime the user wishes to use keywords to specify argument values.
# The remaining arguments that are not called are assumed to have default values, which are assigned to the
# variables at function definition time and in this case will not be overwritten.

# Following the formal parameter list, there can be two special arguments, one preceded by a *, and another
# preceded by **. The one with * is called with an arbitrary number of positional arguments, whose name
# can be used by the function to access the arguments in order as a tuple type, and the ** one is a dict
# which can be used to access all non-formal keyword arguments. The ** parameter will pick up on any keyword
# arguments called which are not defined in the formal parameter list, and keyword arguments can be
# called in any order, whether they are in the formal list or not. However, the * parameter introduces a restriction
# to the function, which restricts the "keyword mode" of formal paramter to be used. When the * parameter is used in a
# function definition, all keyword arguments must be for the ** parameter.

# More conveniently, the rule can be stated as follows:
# 1. Positional arguments define parameter values from the first parameter in the order of parameter definition.
# 2 All positional arguments must precede keyword arguments. Keyword arguments can be called in any order, but cannot
# redefine positionally called arguments.
# 3. The ** parameter captures keyword arguments not defined in the function in a dict.
# 4. The * parameter captures the positional arguments after the formal parameter list in a tuple able to be accessed in
# the calling order. By the second rule, it implies that if the tuple were nonempty, no formal parameters can use the
# keyword argument feature and must be called positionally.

# Thus formal parameters are parameters that have an assigned name in the function definition.

def night_stalker(scythe_version, victim_name="Ashley", stalker_sound="OoooOoH", *argument, **keywords):
    print "The blood-red scythe %s moves silently in the night..." % scythe_version
    print "%s, %s! screams the stalker" % (stalker_sound, stalker_sound)
    print "AHHHAH, screams back %s" % victim_name

    print '-' * 60
    for arg in argument:
        print arg

    for key in sorted(keywords.keys()):
        print "The %s is %s." % (key, keywords[key])

def night_stalker_v2(scythe_version, victim_name, stalker_sound="OoooOoH", **keywords):
    print "The blood-red scythe %s moves silently in the night..." % scythe_version
    print "%s, %s! screams the stalker" % (stalker_sound, stalker_sound)
    print "AHHHAH, screams back %s" % victim_name

    print '-' * 60

    for key in sorted(keywords.keys()):
        print "The %s is %s." % (key, keywords[key])

night_stalker('4.2', 'Joyce', 'Happy Day', "Singing and Laughing", "Running and Screaming", town="Oakville", season="Mid-Autumn")

night_stalker_v2('4.2', stalker_sound="ooOOOOoOOoo", victim_name='Joyce', town="Oakville", season="Mid-Autumn")

def test(a, b=5, *c, **cc):
    print a
    print b
    for e in c:
        print e

    for k, v in cc.iteritems():
        print k, ":", v

# Since 1 maps with the positional argument 'a', test sees c and cc as empty arguments.
test(1)
print '\n'
# This is now allowed because positional arguments MUST precede keyword arguments
'''test(1, b=2, 3)'''
# Only extra positional arguments will be picked up by informal argument type 1 (i.e. *c),
# and only extra keyword arguments will be picked up by informal argument type 2 (i.e. **c)

# Also cannot redefine positional arguments
'''test(1, 2, 3, b=2)'''
test(1, 2, 3, d=2)
print '\n'
test(1, b=3, d=4, e=5)

def unpack(*l_local, **d_local):
    print l_local
    print d_local

print "\nUnpacking:"
l = [1, 2, 3]
d = dict(one=1, two=2, three=3)
unpack(l, d) # These are recognized as two elements in the tuple represented by l in the unpacking function.
unpack(*l, **d)

################################## END OF FUNCTION DEFINITION AND CALLING #############################

# Python's functions can be nested. Just like when they are defined in the immediate module scope,
# they will not be called unless called explicitly, and can only be called from its parent namespace.

# One of Python's most important types is the iterable. They are objects which are or descendent of
# the iterable type, and can be referred to in the for loop to go over each one of them.
# Descendent from the iterable are three basic types.
# 1. Sequences are iterables which have the random-access property, such as lists.
# 2. Mappings are iterables which are to be accessed through keys, such as dicts.
# 3. Generators are iterables which can be accessed only one-by-one, as is used often in for loops.
#       Generators are the return types of the built-in function xrange, and of functions which use keyword yield.

# To iterate over them, there are some functions which can be used:
# zip() generates a tuple equivalent to adding the iterables together.
print 'zipped: ',
for i in zip(xrange(0, 10), xrange(10, 25), xrange(20, 40)):
    print i,
# reversed() generates a reversed iterable from a sequence.
print '\nreversed: ',
for i in reversed((1, 2, 3, 4, 5)):
    print i,
# sorted() generates a sorted iterable from a sequence.
print '\nsorted: ',
for i in sorted((3, 4, 2, 5, 1)):
    print i,
# enumerate() gives an iterable of pairs of (index, value) tuples.
print '\nenumerated: ',
for t in enumerate(xrange(100, 110)):
    print t,

# List comprehension can be used.

# Three of the most useful built-in functions for lists are filter(), reduce(), and map()
print "\nExperimenting with map using a function that returns a different type:"
def map_f(s):
    return len(s)
l = ['un', 'deux', 'trois', 'quatre', 'cinq']
print map(map_f, l)
print "Works!"

# Tuples, although similar to lists, are unlike them since they're immutable.
# HOWEVER, as you can see mutable objects can be part of tuples, and these can be changed within itself! Just the tuple
# cannot be changed.
print "\nTuples:"
tup = 1, 2, 3, [1, 2, 3]
tup[3][0] = 0
print tup
tup[3].append(4)
print tup
try:
    tup[0] = 0
except:
    print "Exception when trying to execute tup[0] = 0"
    print "Tuples are immutable!"

try:
    del tup[:]
except:
    # Note that the slash is needed here for writing a string on more than one line.
    print 'Exception when trying to execute "del tup[:]" ' \
          'tuple object does not support object deletion within itself' \
          ', as that would amount to change the tuple, which is immutable.'

del tup
try:
    print tup
except:
    print 'Exception when trying to print tup after executing "del tup"'

# Here is special syntax for creating empty and singleton tuples.
tup = ()
print tup
tup = 'hi',
print tup

# Since tuples are immutable, they can be used as dictionary keys!
d = {tup: "reader"}
print d[tup]

# One can create tuples using just commas, but a bracket is needed sometimes to eliminate ambiguity
tup = 1, 2, 3, [1, 2, 3]
try:
    tup in d
except:
    print "Trying to use a tuple that directly or indirectly contains a mutable" \
        " object gives the error unhashable type: 'list'. This is because only" \
        " immutable objects can be used as dict keys."

# The del keyword can be used to delete elements in dictionaries by specifying not the index of the element,
# but the key of the element of the dict.
del d['hi',]
print d

# There are 3 other notable ways of creating a list:
# 1. Casting to a dict using a sequence of key-value pairs
l = [(1, 'one'), (2, 'two'), (3, 'three')]
d = dict(l)
print d

# 2. Using dictcomps
d = {i: c for i, c in enumerate("dequeue") if c not in "cache"}
print d

# 3. Using the constructor which uses keyword arguments to create str to otherType mappings.
d = dict(one=1, # Putting arguments on different lines does not require \
    two=2, three=3)
print d

managers = 'Tyrel', 'Nish'
component = 'Placer', 'Router'

# zip returns a list of tuples from one or more sequences
# The index in the brace brackets specify which parameter in the format function will be used in the output.
for m, c in zip(managers, component):
    print "{0} manages {1}".format(m, c)

numbers = {5, 3, 2, 4, 1}
# sorted returns a new sorted list from the input iterable, but does not affect the original sequence.
print sorted(numbers)
print "The builtin function reversed() returns a reverse iterator over an iterable input"
# Presumably this is to improve efficiency to not have to create a new reverse-sorted list.
for n in reversed(sorted(numbers)):
    print n

print "numbers is unaffected by the function sorted() as it is a set:", sorted(numbers)
def reverse_cmp(x, y):
    if x > y:
        return -1
    elif x < y:
        return 1
    else:
        return 0
print "To get a reversed version of the list, use a comp function:", sorted([i for i in numbers], reverse_cmp)
print "Or simply use the reverse keyword", sorted([i for i in numbers], reverse = True)

if 1 <= 5 == 6 - 1 or not 4 + 6 == 5:
    print "1 <= 5 == 6 - 1 or not 4 + 6 == 5 is " "True!"

# The try statement and loops have else statements.
# The else clause is executed when no exception occurs for a try,
# and no breaks occur for a loop

for i in range(1, 10):
    if i == 10:
        break
else:
    print "Range(1, 10) does not include 10, this is because it declares a half-open range [1, 10) because" \
            " Python is a real programming language."

try:
    import pkg_test
except ImportError:
    print "__init__.py is required to designate a folder as a package folder for multiple modules."

print "__init__.py is defined for pkg_test_2"
import pkg_test_2.useful_module
print "the dir() function returns a list of defined names inside the package", dir(pkg_test_2)
pkg_test_2.useful_module.print_hi()

from pkg_test_3 import *
try:
    useful_module.print_hi()
except NameError:
    print "A module will not be imported using * unless it is referred to in a list variable __all__ in __init__.py"
from pkg_test_3 import useful_module
print "You can only import it directly"
useful_module.print_hi()

print "Or, of course, have __all__ = ['useful_module_4'] in __init__.py"
from pkg_test_4 import *
useful_module_4.print_hi()

# Python exceptions has a 'finally' statement which always gets excecuted in a
# try-except-else block for cleanup operations, even if there is a return
# statement in the try clause.

# Since functions will return the last value specified by a return statement,
# the code below will return what is in the finally clause, but not what is in
# the try clause.

def finally_always():
    try:
        return 'Hello one world!\n'
    finally:
        return 'Hello two world!\n'

print finally_always()

################## CLASSES #######################
## Namespaces DO THESE TESTS IN ORDER ##
# To test the property that global names are accessible by all
# middle and lowest-level scopes (i.e. all lower-level scopes):
# 1) Comment [2] and [5]
# 2) Uncomment all code from [1], [3], [4a], [4b]
# Explanation: global names are accessible in any middle and local scope;
# further, since the value of variables are determined dynamically, even though
# a is defined before a function, as long as it exists at the time the function
# is being called, its value will be retrieved.

# To test the read-only property of global names, and that
# scopes are defined TEXTUALLY before runtime:
# 1) Uncomment [2]
# Scopes are defined textually, and is determined by WHERE something is defined.
# So, both inner2() and class Test
# will not access the local a inside inner(), which is not part of their namespace
# search sequence because inner() is not part of the branch of the namespace tree
# which contains these two textual regions during their definitions. Instead they will access
# the global a above which they are defined.

# To test the property that global names can only be accessed this
# way if the global name has been defined at runtime of the
# function which refers to it (i.e. the actual search for names
# is done dynamically, aka dynamic name resolution):
# 1) Comment [2]
# 2) Uncomment [5]
# Explanation: Even though a is a global name and thus can be recognized
# inside the function scope, without it first being defined before
# running the function, python will not recognize it and complain
# that it has not been defined.

# Remember: scopes are determined statically, but the actual searching
# for names is done dynamically at runtime.

# To test the property that an equal-level class cannot use the
# already-defined names of an equal-level function:
# 1) Comment [5]
# 2) Uncomment [2]
# 3) Comment out [4]

# To test the property that an equal-level function cannot use
# the already-defined names of an equal-level function:
# 1) Comment [5]
# 2) Uncomment [2]
# 3) Comment out [4a] and [4b]
# 4) Comment out just ", a" from [3]

# To test the property that a lower-level function CAN use an
# already-defined name of an upper-level function:
# To test inner2():
# 1) Comment [5]
# 2) Uncomment [2]
# 3) Comment out [4a] and [4b]
# 4) Comment out just ", a" from [3]
# 5) Comment out just ", a" at [1]

def inner2():
    print "inner2:", a # [1]

def inner():
    # a = 512 # [2]
    print "inner:", a
    test = Test() # Note: scope for test's functions (of class Test) are in the global scope.
    inner2() # Note: scope for inner2() is in the global scope.
    def inner_of_inner():
        print "inner_of_inner:", a
    inner_of_inner()

# This class' scope can only refer to the global namespace and
# cannot refer to the function which instantiates an object from
# its definition.
class Test:
    def __init__(self):
        print "Class test:", a # [3]

# inner() # [5]
a = 5 # [4a]
inner()
print "global:", a # [4b]

print "Notice that the scope immediately within the main module defines a" \
    " global namespace (directly under that of the built-in namespace) which" \
    " is accessible by all functions and classes, or any scope. However," \
    " names defined in a non-local and non-global scope, or a middle scope in" \
    " some function or class cannot be used by another function or class" \
    " defined in the same parent scope as that middle scope, even if" \
    " that middle scope calls the user of that name.\n" \
## END Namespaces ##

###### Classes ###########
try:
    a_function(5)
except NameError:
    print "a_function has to be textually before any calls to it."

def a_function(b):
    print b

a_function("Now a_function is defined.\n")

# A class definition defines a class object.
class InvestmentClass(object):
    def __init__(self):
        self.investment = 0
    @staticmethod
    def print_success_msg(amount):
        print "An investment of %f has been successfully added." % amount
    # If "self." is not used as the parent identifier to a function,
    # then the function name is assumed to be global.
    # Class scope is never used as a global scope (likely by design to avoid
    # confusion), and so to reference class functions without using a parent
    # identifier, the class name must be used.
    # This is different than C++ where the class name is not needed within
    # a class function's scope.
    # Thus, all unqualified names referenced within a class are either local to the method,
    # in the global scope of the class, or a data attribute within the class;
    # an unqualified function referred within a class or class function CANNOT be in the class scope.
    def add_investment(self, amount):
        self.investment += amount
        # NOTE how the static method here has to be called with the class name qualified.
        # otherwise, the function is assumed to be global, in which case it will not be found.
        InvestmentClass.print_success_msg(amount)
    def add_investment_twice(self, amount):
        self.add_investment(amount)
        InvestmentClass.add_investment(self, amount)
    def print_investment(self):
        print self.investment

inv = InvestmentClass()
inv.add_investment_twice(5)

class Op:
    # The name self has absolutely no special meaning in Python.
    # The only special meaning occurs when an object's method is called. In
    # this case, the function is called with the first argument the object
    # reference to the object itself.
    def __init__(self, u):
        self.x = u
    # Special functions have names of the form __<name>__.
    # NOTE that since they don't meet the requirement of 2 or more preceding
    # underscores and NO MORE than 1 underscore appended, there is no name mangling.
    def __lt__(self, other):
        print "__lt__ is being called."
        return self.x < other.x

o = Op(5)
p = Op(10)
print o < p

# In python you can use the object deque from the collections module.
# Simply say "from collections import deque."

# Interesting useful things with dict.
# 1. Uniquification:
import random
randns = [random.randrange(10) for i in range(20)]
uniques = dict.fromkeys(randns).keys()
print uniques

# 2. References.
counts = dict()
for i in randns:
  counts[i] = counts.get(i, 0) + 1
for i in sorted(counts.keys()):
  print "%d: %d" % (i, counts[i])

'''
refs = dict()
for pagenumber, page in enumerate(pages):
  for word in page:
    refs.setdefault(word, []).append(pagenumber)
'''
class base:
    def __init__(self):
        x = 0

class derived(base):
    def __init__(self):
        x = 10

print " issubclass and isinstance helps to check the whether an object or class" \
        " is or is inherited from a class."
print "%r" % issubclass(base, derived)  # False
print "%r" % issubclass(derived, base)  # True
print "%r" % issubclass(base, base)     # True
x_inst = base()
y_inst = derived()
print "%r" % isinstance(x_inst, base)   # True
print "%r" % isinstance(x_inst, derived)# False
print "%r" % isinstance(y_inst, base)   # True
print "%r" % isinstance(y_inst, derived)# True

