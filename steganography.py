from __future__ import print_function
from PIL import Image
import os, sys, math, argparse
parser = argparse.ArgumentParser()
parser.add_argument("mode", help="encode/decode: If encoding data, pass in --text, --input, --output. If decoding data, pass in --input.")
parser.add_argument("-o", "--output", default="output.png", help="Specified output file (something.png)")
parser.add_argument("-i", "--input", default="input.jpg", help="Specified input file (something.jpg)")
args = parser.parse_args()

def intToBinary(value):
    return '{0:b}'.format(value)

def textToBinary(value):
    return (' '.join(format(x, 'b') for x in bytearray(value, 'utf8')))

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
    #print("Binary Data: " + str(binaryData))
    px = im.load()

    for i in range(pixelsNeeded):
        RGB = px[width, height]
        colors = []

        for i in range(3):
            colors.append(RGB[i])

        for y in range(3):
            if(numEdits >= len(binaryData)):
                break
            if(isStartingSize):
                if(numEdits == 32):
                    break

            old = list(intToBinary(RGB[y]))
            old[len(old) - 1] = binaryData[numEdits]
            numEdits += 1
            col = ''.join(old)
            col = binaryToInt(col)
            colors[y] = col

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

    if(len(sol) < 32):
        difference = 32 - len(sol)

        #we need to append 0 difference amount of times to get up to 8
        for i in range(0, difference, 1):
            sol.insert(0,"0")

    sol = ''.join(sol)
    return sol

def storeBinaryInImage(binaryData, im):

    width = im.width - 1
    height = im.height - 1

    binaryData = convertToProperFormat(binaryData)
    #print("Binary data in converted format: " + binaryData)
    length = len(binaryData)
    #print("Length of bits: " + str(length))

    binaryLength = intToBinary(length)
    binaryLength = convertToProperFormat(binaryLength)
    #altLength = intToBinary(length * 8)
    #altLength = convertToProperFormat(altLength)
    #print("Length of bits in binary format: " + str(binaryLength)) # GOOD UP TO HERE
    #print("Alt Length of bits in binary format: " + str(altLength)) # GOOD UP TO HERE


    lengthOfBinaryLength = len(binaryLength)
    #print("Length of length of binary bits: " + str(lengthOfBinaryLength))

    if(lengthOfBinaryLength > 32):
        print("The data is too large, try again with a smaller payload.")
        return

    #Figure out how many pixels we need to loop over
    pixelsNeeded = int(math.ceil((float(lengthOfBinaryLength)/3)))

    #print("Inserting binary length into picture...")
    height = pixelLoop(im, pixelsNeeded, binaryLength, True, width, height)
    width -= 11;

    # Need to check if we have to move the height index up and reset width
    if(width < 0):
        width = im.width - 1;
        height -= 1;

    #Figure out how many pixels we need to loop over
    pixelsNeeded = int(math.ceil((float(length)/3)))
    #print("Inserting data into picture...")
    pixelLoop(im, pixelsNeeded, binaryData, False, width, height)

def readBinaryInImage(im):
    width = im.width - 1
    height = im.height - 1
    px = im.load()

    sizeBitArray = []
    counter = 0
    #grab first 11 pixels for size
    #on the 11th pixel we don't read the B of the rgbs
    for i in range(11):
        RGB = px[width, height]
        #print(RGB)

        #for i in range(2, -1, -1):
        for i in range(3):
            if(counter < 32):
                col = intToBinary(RGB[i])
                #print(col)
                #sizeBitArray.insert(0,col[len(col) - 1])
                sizeBitArray.append(col[len(col) - 1])
                counter += 1

        width -= 1
        if(width < 0):
            width = im.width - 1
            height -= 1

    length = ''.join(sizeBitArray)
    #print("Binary of length: " + str(length))
    length = (binaryToInt(length))
    #print("read length: " + str(length))
    pixelLength = int(math.ceil((float(length)/3)))
    #print("Need to read " + str(pixelLength) + " pixels.")

    if(pixelLength > (im.width * im.height)):
        print("ERROR: Stored length size is bigger than the size of the picture!")
        return

    dataBitArray = []
    readCounter = 0
    for i in range(pixelLength):
        RGB = px[width, height]

        #for i in range(2, -1, -1):
        for i in range(3):
            if(readCounter < length):
                col = intToBinary(RGB[i])
                #dataBitArray.insert(0,col[len(col) - 1])
                dataBitArray.append(col[len(col) - 1])
                readCounter += 1

        width -= 1
        if(width < 0):
            width = im.width - 1
            height -= 1

    text = ''.join(dataBitArray)
    #print("Binary text: " + str(text))
    text = binaryToText(text)
    return text

#print(args)
# Here is the main
if(args.mode == "encode"):
    # open image for processing
    im = Image.open(args.input)
    #print(os.getcwd())
    #text = os.getcwd()
    f = open('encode.txt', 'r')
    text = f.read()

    # converts the string to be hidden into binary
    binaryString = textToBinary(text)
    #print("Binary representation of " + var + ": " + binaryString)

    # hides the string and length
    storeBinaryInImage(binaryString, im)

    # save as png and close the image
    im.save(args.output)
    print("Text succesfully stored in " + str(args.output))
    im.close()

elif(args.mode == "decode"):
    # open image for processing
    im = Image.open(args.input)

    # read the data back from the image
    text = readBinaryInImage(im)
    print("Read Data From Picture: " + str(text))

    im.close()
elif(args.mode == "red"):
    im = Image.open(args.input)
    px = im.load()
    for i in range(11):
        px[im.width - i - 1, im.height-1] = (255, 0, 0)
    im.save("red.jpg")
    im.close()

else:
    print("ERROR: incorrect mode argument passed through command line.")
    print("Correct mode encode usage: python3 encode -t 'hello world' -i 'input.jpg' -o 'output.png'")
    print("Correct mode decode usage: python3 decode -i 'input.jpg'")
