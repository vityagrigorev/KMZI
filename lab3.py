import Image

import argparse

from itertools import product

def message_to_bin(message):

    message = bytes(message)
    len_message = len(message)

    binlen = bin(len_message)[2:]
    if len(binlen) < 8:
        binlen = '0' * (8 - len(binlen)) + binlen
        
    binmessage = []
    binmessage.append(binlen)

    for x in message:
        part = bin(ord(x))[2:]
        partlen = len(part)
        if (partlen < 8):
            part = '0' * (8 - partlen) + part
        binmessage.append(part)        
    return b''.join(binmessage)

def writeFile(fname, message):
    try:
        with open(fname, 'wb') as inFile_text:
                    inFile_text.write(''.join(message))
    except IOError:
        exit('No such file or directory ' + fname)
    
def readFile(fname):
    try:
        with open(fname, 'rb') as inFile_text:
                message = inFile_text.read()
    except IOError:
        exit('No such file or directory ' + fname)
    return message 

def hide_message(message, imagefile): #, outfile
    
    binmessage = message_to_bin(message)
    image = Image.open(imagefile)   
            
    pix = image.load()
    sizex, sizey = image.size
    
    if len(binmessage) > (sizex * sizey):
        raise Exception ("Very small image")
    
    next_index = product(range(sizex), range(sizey))

    for m in binmessage:
        index = next(next_index)
        r, g, b, a = pix[index]
        last_bit = bin(b)[-1:]
        if m == '0':
            if last_bit == '1':
                b -= 1
        elif m == '1':
            if last_bit == '0':
                b += 1
        
        pix[index] = r,g,b,a
    
    #image.save(outfile)
    image.save(imagefile + '_', 'png')
    
def unhide_message(imagefile):
    image = Image.open(imagefile)
    pix = image.load()
    sizex, sizey = image.size
    next_index = product(range(sizex), range(sizey))
   
    len_message = 0
    for i in range(7,-1,-1):
        index = next(next_index)
        b = pix[index][2]
        last_bit = bin(b)[-1:]
        if last_bit=='1':
            len_message += 2**i
            
    message = []
    for i in range(len_message):
        part = 0
        for i in range(7,-1,-1):
            index = next(next_index)
            b = pix[index][2]
            last_bit = bin(b)[-1:]
            if last_bit=='1':
                part += 2**i
        message.append(chr(part))
        
    return ''.join(message)
        
def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('image')
    parser.add_argument('inFile_text', nargs = '?')
    return parser.parse_args() 
    
if __name__ == '__main__':

    in_args = getArgs()
    if in_args.inFile_text:
        print('hide_message')
        message = readFile(in_args.inFile_text)
        try:
            hide_message(message, in_args.image)
        except Exception as err:
            exit("Error: {0}".format(err))
    else:
        print('unhide_message')
        final_value = ''	
        final_value = unhide_message(in_args.image)
        writeFile(in_args.image + ".txt", final_value) 
