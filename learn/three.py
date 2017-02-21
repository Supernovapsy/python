try:
    5 / 0
except NameError:
    print "What?"
except ZeroDivisionError: pass
except:
    print "I catch all errors but NameError."
    raise

