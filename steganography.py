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

    for i in range (startIndex, -1, -1):
        if(bitList[i] == '1'):
            value += pow(2, count)
        count += 1

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
    return (''.join(chr(x) for x in intList))

def binaryToInt(value):
    return int(value, 2)

def pixelLoop(im, pixelsNeeded, binaryData, isStartingSize, width, height):
    numEdits = 0
    length = len(binaryData)
    px = im.load()

    for i in range(pixelsNeeded):
        RGB = px[width, height]
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
            print("before: " + str(old))
            old[len(old) - 1] = col
            print("after: " + str(old))
            col = ''.join(old)
            col = binaryToInt(col)
            colors[y] = col
            numEdits += 1

        px[width, height] = (colors[0], colors[1], colors[2])
        width -= 1
        if(width < 0):
            width = im.width - 1;
            height -= 1;

    if(isStartingSize):
        remainingPixels = 11 - pixelsNeeded

        for x in range(remainingPixels):
            RGB = px[width, height]
            colors = []

            for i in range(3):
                colors.append(RGB[i])

            for y in range(3):
                #if y is 0, convert binaryData[0] & binaryData[1] into an int(color)

                col = "0"
                old = list(intToBinary(RGB[y]))
                old[len(old) - 1] = col
                col = ''.join(old)
                col = binaryToInt(col)
                colors[y] = col
                numEdits += 1

            px[width, height] = (colors[0], colors[1], colors[2])
            width -= 1

            if(width < 0):
                width = im.width - 1;
                height -= 1;

    return height

def convertToProperFormat(binaryData):
    count = 0
    sol = []

    for x in range(len(binaryData) - 1, -1, -1):
        if(binaryData[x] == ' '):
            if(count < 8):
                difference = 8 - count

                #we need to prepend 0 difference amount of times to get up to 8
                for i in range(0, difference, 1):
                    sol.insert(0,"0")

                count = 0
                continue

        sol.insert(0,binaryData[x])
        count += 1

    if(count < 8):
        difference = 8 - count

        #we need to append 0 difference amount of times to get up to 8
        for i in range(0, difference, 1):
            sol.insert(0,"0")

    sol = ''.join(sol)
    return sol

def storeBinaryInImage(binaryData, im):

    width = im.width - 1
    height = im.height - 1

    binaryData = convertToProperFormat(binaryData)
    length = len(binaryData)
    print("length of bits: " + str(length))

    binaryLength = intToBinary(length)
    binaryLength = convertToProperFormat(binaryLength)
    print("binary length: " + str(binaryLength))

    lengthOfBinaryLength = len(binaryLength)

    #Figure out how many pixels we need to loop over
    pixelsNeeded = int(math.ceil((float(lengthOfBinaryLength)/3)))

    if(pixelsNeeded > 11):
        print("The data is too large, try again with a smaller payload.")
        return

    height = pixelLoop(im, pixelsNeeded, binaryLength, True, width, height)
    width -= 11;

    # Need to check if we have to move the height index up and reset width
    if(width < 0):
        width = im.width - 1;
        height -= 1;

    #Figure out how many pixels we need to loop over
    pixelsNeeded = int(math.ceil((float(length)/3)))
    pixelLoop(im, pixelsNeeded, binaryData, False, width, height)

def readBinaryInImage(im):
    width = im.width - 1
    height = im.height - 1
    px = im.load()

    sizeBitArray = []
    #grab first 11 pixels for size
    for i in range(11):
        RGB = px[width, height]

        for i in range(2, -1, -1):
            col = intToBinary(RGB[i])
            sizeBitArray.insert(0,col[len(col) - 1])

        width -= 1
        if(width < 0):
            width = im.width - 1
            height -= 1

    length = ''.join(sizeBitArray)
    print("read bits: " + str(length))
    length = binaryToInt(length)
    print("read length: " + str(length))
    pixelLength = int(math.ceil((float(length)/3)))

    dataBitArray = []
    for i in range(pixelLength):
        RGB = px[width, height]

        for i in range(2, -1, -1):
            col = intToBinary(RGB[i])
            dataBitArray.insert(0,col[len(col) - 1])

        width -= 1
        if(width < 0):
            width = im.width - 1
            height -= 1

    text = ''.join(dataBitArray)
    text = binaryToText(text)
    return text


# open image for processing
im = Image.open("hacker.jpg")

# converts the string to be hidden into binary
binaryString = textToBinary("As advanced practiced Nurses research is and will be a key factor in how we practice our nursing.")

# hides the string and length
storeBinaryInImage(binaryString, im)

# read the data back from the image
text = readBinaryInImage(im)
print("Read Data From Picture: " + text)

# save as png and close the image
im.save("output.png")
im.close()
