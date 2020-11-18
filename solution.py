import numpy as np
from bitstring import *
import binascii

#the array H needed for decoding
H = np.array([[1,0,1,0,1,0,1], [0,1,1,0,0,1,1], [0,0,0,1,1,1,1]])

#used to open our file as a binary string
def openFile(path):
    return BitArray(filename = path).bin

#called with a binary string, will decode the string using Hamming(7,4)   
def decodeMessage(binaries):
    message = ''
    for i in range(0, len(binaries) //  7):
        i *= 7 #to get to next set of 7 bits
        R = np.matrix(list(binaries[i:i+7]), dtype=np.int) #convert to length 7 np.array, each bit is represented as an int
        Z = getZ(R.T) #multiply H and R to get Z (NOTE: R is transposed to turn to column vector)
        
        if(Z.any()): #if not null vector, then we have an error i.e. mean we keep this data
            flippedIndex = np.where((H.T == Z.T).all(axis=1))[0][0] # the index of the data to flip

            toFlip = binaries[i + flippedIndex] #get bit we are supposed to flip based on index
            toFlip = (int(toFlip) + 1) % 2 #flip from 0 to 1 or vice versa

            fixedPart = (binaries[i:i + flippedIndex] + str(toFlip) + binaries[i + flippedIndex + 1: i + 7]) #fix with corrected bit
        
            message += fixedPart[2] + fixedPart[4] + fixedPart[5] + fixedPart[6] #append to our result
            
    return binascii.unhexlify(hex(int(message,2))[2:]).decode('utf-8', 'replace') #return result as ASCII
    
#the syndrome vector        
def getZ(R):
    return (H * R) % 2


if __name__ == "__main__":
    binaries = openFile("output.bin")
    print(decodeMessage(binaries))