#Jeremy Reiser
#CSE4302 Project 1
#Cache Simulator
import random

CS_VALID = 1
CS_DIRTY = 2

class Cache: 

    # constructor 
    # 2**n : total number of bytes in cache
    # 2**b : block size
    # 2**a : set associativity
    # repl : replacement policy 
    #           0:  random
    #           1:  LRU
    def __init__(self, n, b, a, repl):
        self.verbose = 0 
        self.nb_n = n
        self.nb_b = b
        self.nb_a = a
        self.replacement = repl
        self.number_of_sets = self.nb_n - self.nb_b - self.nb_a  #log of # of sets
        
        # keep track of the numbers of refectories and misses
        self.num_references = 0
        self.num_misses = 0

        self.set_counter = []     #counts how many ways in a set have been used
        for i in range(0, 2**self.number_of_sets):
            self.set_counter.append(0)  #initializes the set counter array
        self.index_plus_offset = self.nb_n - self.nb_a  #calculates how many bits to shift to obtain tag
        
        
        k = 2**self.number_of_sets  #k = number of sets
        m = 2**self.nb_a            #m = no. of ways per set
        self.set_flags = [[0 for x in range(k)] for y in range(m)]  #initialize set_flags array
        self.tags = [[0 for x in range(k)] for y in range(m)]       #initialize tags array
        self.flags = [[0 for x in range(k)] for y in range(m)]      #initialize flags array


    def set_verbose(self, v):
        self.verbose = v

    # find a block in a set where the new block can be placed
    def find_way(self, index):
        way = 0
        if(self.set_counter[index] < 2**self.nb_a):    #if set is not full
            way = self.set_counter[index]               #assign next open way
            self.set_counter[index] += 1                #increment set counter
            
        elif(self.replacement == 1):                   #if LRU
            max = 0                                     #determine the max flag
            for i in range(0, 2**self.nb_a):            #iterate across all ways
                if(self.set_flags[i][index] > max):
                    max = self.set_flags[i][index]
                    way = i                         #way with LRU tag is overwritten
                    
        else:
            way = random.randint(0, 2**self.nb_a-1) #if random, choose way randomly
            
        return way 

    # bookkeeping. Just accessed block identified by index and way
    def update_set_flags(self, index, way):
        for i in range(0, 2**self.nb_a):    #least recently used tags have high flag
            self.set_flags[i][index] = self.set_flags[i][index] + 1

        self.set_flags[way][index] = 0      #most recently used tag set back to zero
        return


    def access(self, addr, write):
        self.num_references += 1
        hit = 0
        way = 0
        index = 0
        
        tag = addr >> self.index_plus_offset    #shifts right to obtain tag
        index = (addr >> self.nb_b) & ((2**self.number_of_sets)-1) #uses bitwise AND to extract index
        
        for i in range(0, 2**self.nb_a):        #checks set to see if tag is saved
            if(tag == self.tags[i][index]):
                self.update_set_flags(index, i) #if so, update flag, return hit
                return 1
        else:
            way = self.find_way(index)          #else, find which way to use
            self.tags[way][index] = tag         #store tag in tag array
            self.update_set_flags(index, way)   #update flag
            self.num_misses += 1                #return miss
            return 0
        # cache access. ignore write for now.

        return 

    # reports the statistics
    def report(self):
        print("Number of references = {}".format(self.num_references))
        print("Number of misses     = {}".format(self.num_misses))
        print("Number of hits       = {}".format(self.num_references - self.num_misses))
        if (self.num_references):
            print("Miss rate            = {:.2f}%".format(self.num_misses * 100.0 / self.num_references))

#Date: February 21st
#Time Spent: 1 hour
#Work Done: Installed LiClipse IDE, Installed Python 3.0, attempted to run code,
#received import error on line import memcache, attempted to solve error

#Date: March 1st
#Time Spent: 4 hours
#Work Done: fixed error with import memcache by deleting project and creating new
#attempted to run code, received error: "syntax error only named arguments may 
#follow *expression" discovered source of error was Python version, 
#version 3.0 does not work, Python 3.7.2 installed, error fixed after 3 hours
#completed init, worked on access and find_way, program crashed, lost 1 hour of work

#Date:: March 2nd
#Time Spent: 3 hours
#Work Done: Worked on functions, received index out of bounds error, fixed by
#correcting calculation of cache index, received another index out of bounds
#error for random replacement, resolved by subtracting 1 from maximum way value
#Finished all functions, tested on test case files. Code worked for
#gcc-1k.mem.txt, but not for gcc_1M.txt. Troubleshooted, discovered error was
#in LRU logic, fixed error, all test files now work as they should.

