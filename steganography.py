from __future__ import print_function
from PIL import Image
import os, sys, math

def convertIntToBinary(value):
    return (format(value, "08b"))

def convertBinaryToInt(value):
    return int(value, 2)

#setOfPixels is a list of pixels
def hideData(data, width, height, im):
    #convert sizeOfData to binary and see how many bits it takes
    dataInBits = convertIntToBinary(data)
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

print()
print(im.format, im.size, im.mode)
print()

#dummy data
data = 222
print("WIDTH: " + str(width))
hideData(data, width, height, im)


im.save("output.jpg")

