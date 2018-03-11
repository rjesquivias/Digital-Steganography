from __future__ import print_function
from PIL import Image
import os, sys, math

def textToBinary(value):
    return (' '.join(format(x, 'b') for x in bytearray(value)))

def calculateInt(bitsFilled, bitList):
    difference = 8 - bitsFilled;
    startIndex = bitsFilled - 1;
    value = 0
    count = 0

    #print("bitsFilled: " + str(bitsFilled))
    #print("difference: " + str(difference))
    #print("startIndex: " + str(startIndex))
    for i in range (startIndex, -1, -1):
        #print("bit: " + str(bitList[i]))
        if(bitList[i] == '1'):
            value += pow(2, count)
        count += 1

    #print()
    #print(value)
    #print()
    return value

def binaryToText(bin):
    bitsFilled = 0
    bitList = [0,0,0,0,0,0,0,0]
    intList = [];

    for x in bin:
        if(x == ' '):
            #Store calculated integer
            intList.append(calculateInt(bitsFilled, bitList))
            #Reset variables
            for i in range(0, 7):
                bitList[i] = 0
            bitsFilled = 0
            continue

        bitList[bitsFilled] = x
        bitsFilled += 1

    #once more when we fall out of the for loop
    intList.append(calculateInt(bitsFilled, bitList))

    #for x in intList:
        #print(x)
    return (''.join(chr(x) for x in intList))

def convertBinaryToInt(value):
    return int(value, 2)

#setOfPixels is a list of pixels
def hideData(data, width, height, im):
    #convert sizeOfData to binary and see how many bits it takes
    dataInBits = textToBinary(data)
    print("data in bits: " + dataInBits + '\n')

    dataBitsSize = len(dataInBits);
    print("number of bits to store: " + str(dataBitsSize) + '\n')

    #if(dataBitsSize > (width * height) or dataBitsSize == 0):
    #	return False

    #Figure out how many pixels we need to loop over
    pixelsNeeded = int(math.ceil((float(dataBitsSize)/3)))
    print("Pixels needed for loop: " + str(pixelsNeeded) + '\n')

    numEdits = 0
    px = im.load()


    print("image height: " + str(width + 1))
    print("image width: " + str(height + 1))

    for i in range(pixelsNeeded):
        RGB = px[width, height]
        edits = 3 if dataBitsSize - numEdits >= 3 else dataBitsSize - numEdits
        colors = []

        for i in range(3):
            colors.append(RGB[i])

        for y in range(edits):
            #if y is 0, convert dataInBits[0] & dataInBits[1] into an int(color)
            col = dataInBits[numEdits]
            old = list(convertIntToBinary(RGB[y]));

            #print("Before:", end = ' ')
            #for x in old:
                #print(x, end = '')
            old[7] = col
            #print()
            #print("After:", end = ' ')
            #for x in old:
                #print(x, end ='')
            #print()

            col = ''.join(old)
            col = convertBinaryToInt(col)
            print("old color: " + str(RGB[y]))
            colors[y] = col
            print("new color: " + str(col))

            numEdits += 1

        px[width, height] = (colors[0], colors[1], colors[2])
        width -= 1




#im.save("hacker.jpg")



im = Image.open("hacker.jpg")
width = im.width - 1
height = im.height - 1
pixels = list(im.getdata())

#print(im.format, im.size, im.mode)
binaryString = textToBinary("Hello there nigger cheese")
#print(binaryString)
#print(len(binaryString))
text = binaryToText(binaryString)
print("length of binary: " + str(len(binaryString)))
print(text)




#dummy data
#data = 222
#print("WIDTH: " + str(width))
#hideData(data, width, height, im)
#im.save("output.jpg")

im.close()
