#!/usr/bin/python3

import sys, re, fileinput
import memcache

def     sys_error(s):
    print ("Error: " + s)
    exit(1)

def     print_help():
    # triple quotes can be used for a multi-line string in python
    print('''Usage: simcache config [-rX] [tracefile]

config is a string like n,b,a
    n : log_2(size of data in bytes) 
    b : log_2(size of blocks in bytes) 
    a : log_2(associativity). 0 for direct mapped.

For example, 10,6,1 means 1 KiB data, 64-byte blocks, and 2-way
set associativiy. The cache has 16 blocks. Each set has two blocks.
Therefore, there are 8 sets.

Use '-rX' option to specify the cache replacement policy,
where X is an integer representing the policy.
    0 : use random replacement policy
    1 : use LRU

tracefile is text file containing memory traces. If no file 
is specified, the program tries to read from stdin.
''')
    exit(1)

def     parse_config(s):
    if s == '':
        return (0, 0, 0)
    fields = s.split(",")
    if (len(fields) != 3):
        sys_error("Invalid configuration. Need three numbers, like 10,6,0.")
    n = int(fields[0]) 
    b = int(fields[1]) 
    a = int(fields[2]) 
    assert n >= 6 and n <= 24
    assert b >= 1 and b <= 12 and b <= n
    assert a >= 0 and a + b <= n 
    return (n, b, a)

argc = len(sys.argv)
if (argc < 2): 
    print_help()

verbose = 0
config = ""
opt_replacement = 1
files = []

for a in sys.argv[1:]:
    if (a == '-v'):
        verbose = 1
    elif (a == '-h'):
        print_help()
    elif (a.startswith('-r')):
        opt_replacement = int(a[2:])
    elif (',' in a):
        config = a
    else: 
        files.append(a)

if verbose:
    print("config='{}' replacement policy='{}'".format(config, opt_replacement))

if (config == ''):
    sys_error("Specify a cache configuration.")

config_parsed = parse_config(config)

cache = memcache.Cache(*config_parsed, opt_replacement)
cache.set_verbose(verbose)

"""
    This regex pattern matches when the line begins with an address that can
    (optionally) be prefixed with '0x', followed by one or more alphanumeric characters,
    followed by whitespace and then either a 0, L, l (load) or 1, S, s (store)
"""
pattern = re.compile('^((0x)*([0-9A-Fa-f]+))\s+(0|1|L|l|S|s)')

n_lines = 0

for line in fileinput.input(files):
    n_lines += 1
    m = re.search(pattern, line)
    if (m):
        # in the pattern, each set of parentheses represents a "group"
        address = int(m.group(1), 0)
        # w = 1 if the current line is a STORE instruction
        w = 1 if m.group(4)[0] in '1Ss' else 0
        # print(address, outcome)
        cache.access(address, w)

cache.report()
