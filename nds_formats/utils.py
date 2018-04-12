import struct


def readUnsignedInt(data):
    return struct.unpack('<L', data.read(4))[0]

def readUnsignedShort(data):
    return struct.unpack('<H', data.read(2))[0]

def readUnsignedByte(data):
    return struct.unpack('<B', data.read(1))[0]

def readByte(data):
    return struct.unpack('<b', data.read(1))[0]