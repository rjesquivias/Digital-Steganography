from __future__ import print_function
from PIL import Image
import os, sys, math


def intToBinary(value):

    return '{0:b}'.format(value)

def textToBinary(value):

    return (' '.join(format(x, 'b') for x in bytearray(value)))

def calculateInt(bitsFilled, bitList):

    difference = 8 - bitsFilled
    startIndex = bitsFilled - 1
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

    #store every section of bytes separated by ' ' in bitList
    bitsFilled = 0
    bitList = [0,0,0,0,0,0,0,0]
    intList = []

    for x in bin:
        if(x == ' ' or bitsFilled == 8):
            #Store calculated integer
            intList.append(calculateInt(bitsFilled, bitList))
            #Reset variables
            for i in range(0, 7):
                bitList[i] = 0

            if(bitsFilled != 8):
                bitsFilled = 0
                continue

            bitsFilled = 0


        bitList[bitsFilled] = x
        bitsFilled += 1

    #once more when we fall out of the loop
    intList.append(calculateInt(bitsFilled, bitList))

    #for x in intList:
        #print(x)
    return (''.join(chr(x) for x in intList))

def binaryToInt(value):
    return int(value, 2)

def pixelLoop(im, pixelsNeeded, binaryData, isStartingSize, width, height):
    numEdits = 0
    length = len(binaryData)
    px = im.load()

    for i in range(pixelsNeeded):
        RGB = px[width, height]
        if(isStartingSize):
            print("rgb: " + str(RGB))
        edits = 3 if length - numEdits >= 3 else length - numEdits
        colors = []

        for i in range(3):
            colors.append(RGB[i])

        for y in range(2, -1, -1):
            #if y is 0, convert binaryData[0] & binaryData[1] into an int(color)

            if(i < pixelsNeeded):
                if(y > edits or numEdits >= len(binaryData)):
                    col = "0"
                else:
                    col = binaryData[len(binaryData) - 1 - numEdits]
            else:
                col = "0"

            old = list(intToBinary(RGB[y]))
            #print("bit: " + str(col))
            print("unmodified bin: " + str(old))
            old[len(old) - 1] = col
            print("modified bin: " + str(old))


            col = ''.join(old)
            col = binaryToInt(col)
            #print("old color: " + str(RGB[y]))
            colors[y] = col
            print("new color: " + str(col))
            #print()

            numEdits += 1


        px[width, height] = (colors[0], colors[1], colors[2])
        width -= 1
        if(width < 0):
            width = im.width - 1;
            height -= 1;

    if(isStartingSize):
        remainingPixels = 11 - pixelsNeeded
        print("remaining pixels: " + str(remainingPixels))

        for x in range(remainingPixels):
            RGB = px[width, height]
            print("rgb: " + str(RGB))
            colors = []

            for i in range(3):
                colors.append(RGB[i])

            for y in range(3):
                #if y is 0, convert binaryData[0] & binaryData[1] into an int(color)

                col = "0"

                old = list(intToBinary(RGB[y]))
                #print("bit: " + str(col))
                print("unmodified bin: " + str(old))
                old[len(old) - 1] = col
                print("modified bin: " + str(old))


                col = ''.join(old)
                col = binaryToInt(col)
                print("old color: " + str(RGB[y]))
                colors[y] = col
                print("new color: " + str(col))
                #print()

                numEdits += 1

            px[width, height] = (colors[0], colors[1], colors[2])
            width -= 1
            print("decreased width to: " + str(width))
            if(width < 0):
                width = im.width - 1;
                height -= 1;

    return height

def convertToProperFormat(binaryData):
    count = 0
    sol = []
    print("Formatting below")
    print("Binary data: " + binaryData)
    for x in binaryData:
        if(x == ' '):
            if(count < 8):
                difference = 8 - count
                #we need to prepend 0 difference amount of times to get up to 8
                for i in range(0, difference, 1):
                    sol.insert(0,"0")
                count = 0
                continue

        sol.append(str(x))
        count += 1

    if(count < 8):
        difference = 8 - count
        #we need to append 0 difference amount of times to get up to 8
        for i in range(0, difference, 1):
            sol.insert(0,"0")

    sol = ''.join(sol)
    print("solution:    " + sol)
    return sol

#setOfPixels is a list of pixels
def storeBinaryInImage(binaryData, im):

    width = im.width - 1
    height = im.height - 1

    binaryData = convertToProperFormat(binaryData)
    #First 11 pixels will be used to store binaryLen
    length = len(binaryData)
    print("length: " + str(length))
    binaryLength = intToBinary(length)
    print("binary representation of length: " + str(binaryLength))
    binaryLength = convertToProperFormat(binaryLength)
    lengthOfBinaryLength = len(binaryLength)

    #Figure out how many pixels we need to loop over
    pixelsNeeded = int(math.ceil((float(lengthOfBinaryLength)/3)))
    print("Pixels needed for length storing loop: " + str(pixelsNeeded) + '\n')

    if(pixelsNeeded > 11):
        print("The data is too large, try again with a smaller payload.")
        return
    print("height: " + str(height))
    height = pixelLoop(im, pixelsNeeded, binaryLength, True, width, height)
    width -= 11;

    # Need to check if we have to move the height index up and reset width
    if(width < 0):
        width = im.width - 1;
        height -= 1;


    #if(dataBitsSize > (width * height) or dataBitsSize == 0):
    #	return False

    #Figure out how many pixels we need to loop over
    pixelsNeeded = int(math.ceil((float(length)/3)))
    #print("Pixels needed for loop: " + str(pixelsNeeded) + '\n')
    #print("binary: " + binaryData)
    #pixelLoop(im, pixelsNeeded, binaryData, False, width, height)


def readBinaryInImage(im):
    width = im.width - 1
    height = im.height - 1
    px = im.load()

    sizeBitArray = []
    #grab first 11 pixels for size
    for i in range(10, -1, -1):
        RGB = px[width, height]
        print("READ RGB: " + str(RGB))

        for i in range(2, -1, -1):
            #print("color read: " + str(RGB[i]))
            col = intToBinary(RGB[i])
            sizeBitArray.insert(0,col[len(col) - 1])


        width -= 1
        if(width < 0):
            width = im.width - 1
            height -= 1

    sol = ''.join(sizeBitArray)
    sol = binaryToInt(sol)
    print("solution: " + str(sol))

#im.save("hacker.jpg")



im = Image.open("hacker.jpg")
#pixels = list(im.getdata())

#print(im.format, im.size, im.mode)
binaryString = textToBinary("test 1234")
print("binary string: " + binaryString)

#get rid of spaces in the binary string

storeBinaryInImage(binaryString, im)
readBinaryInImage(im)
text = binaryToText(binaryString)
print("length of binary: " + str(len(binaryString)))
print(text)


#px = im.load()
#RGB = px[width, height]

#height = im.height - 1;
#for i in range(0, im.width/2, 1):
#    print("height: " + str(height))
#    px[i, height] = (0, 0, 255)
#    height -= 1
im.save("output.jpg")



#dummy data
#data = 222
#print("WIDTH: " + str(width))
#hideData(data, width, height, im)
#im.save("output.jpg")

im.close()
