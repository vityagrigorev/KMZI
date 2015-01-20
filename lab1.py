from itertools import cycle
    
import sys
import argparse
   
LEN = 256

def full_encode(value, key):
    return ''.join(map(lambda x: chr((ord(x[0]) + ord(x[1])) % LEN), zip(value, cycle(key))))

def full_decode(value, key):
    return ''.join(map(lambda x: chr((ord(x[0]) - ord(x[1]) + LEN) % LEN), zip(value, cycle(key))))

def write(fname, final_value):
    outFile = open(fname, 'w')
    outFile.write(''.join(final_value))

def read(fname):
    try:
        with open(fname, 'r') as inFile:
            text = inFile.read()
    except IOError:
            exit('No file ' + fname)
    return text

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('inF')
    parser.add_argument('keyF')
    parser.add_argument('outF')
    parser.add_argument('mod', choices=['c', 'd'])
    return parser.parse_args()

if __name__ == "__main__":

    in_arg = getArgs()
    data = read(in_arg.inF)
    key = read(in_arg.keyF)
    
    if in_arg.mod == 'c':
        final_value = full_encode(data, key)
    if in_arg.mod == 'd':
        final_value = full_decode(data, key)
        
    write(in_arg.outF, final_value)
