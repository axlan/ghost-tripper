import struct
import os

def readUnsignedInt(data):
    return struct.unpack('<L', data.read(4))[0]

def readUnsignedShort(data):
    return struct.unpack('<H', data.read(2))[0]

def readUnsignedByte(data):
    return struct.unpack('<B', data.read(1))[0]

def readByte(data):
    return struct.unpack('<b', data.read(1))[0]

def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def find_edges(img, color):
    pixels = img.load()
    max_x = 0
    max_y = 0
    min_x = 0
    min_y = 0
    for i in range(img.size[0]):    # for every col:
        for j in range(img.size[1]):    # For every row
            if pixels[i,j] != color:
                if i > max_x:
                    max_x = i
                if j > max_y:
                    max_y = j
                if min_x == 0:
                    min_x = i
                if min_y == 0:
                    min_y = j
    return min_x, min_y, max_x, max_y
