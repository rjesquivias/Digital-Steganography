Raul Esquivias

My application's architecture follows 2 simple states.
One of these states, the 'encode' state, is supplied
an input file name and an optional output file name.
It opens the image from the supplied input file name, converts
text from a file 'encode.txt' to binary, and stores it before exporting to the output file name.
The second state, 'decode', is supplied with an input file name
and an optional output file name.  It reads the first 11 pixels to
figure out the size of encoded data, and goes about reconstructing
the text.

The file output.png has the stored source code inside of it.

Usage Instructions
Encoding:
1) Fill the file 'encode.txt' with whatever text you would like encoded into the file.
2) python3 steganography.py encode -i "hacker.jpg"
3) (optional output file specification) python3 steganography.py encode -i "hacker.jpg" -o "myfile.png"
Note: If no -o option is given, the file will output to "output.png"

Decoding:
1) python3 steganography.py decode -i "output.jpg"
2) The text will be printed to the console.

Github: https://github.com/rjesquivias/Digital-Steganography
