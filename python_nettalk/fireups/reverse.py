from sys import argv

def reverse_str_c_style(cstr):
    begin, end = 0, len(cstr) - 1
    ret_list = list(cstr)
    while begin < end:
        ret_list[begin], ret_list[end] = ret_list[end], ret_list[begin]
        begin += 1
        end -= 1
    return "".join(ret_list)

forward, reverse = argv[1], reverse_str_c_style(argv[1])
print "forward: %s" % forward
print "reverse: %s" % reverse
# print "reverse: %s" % "".join(list(reversed(forward)))
