import struct
from io import BytesIO
from collections import namedtuple

PaletteEntry = namedtuple('PaletteEntry', ['offset', 'size', 'subindex', 'unknownFlag'])
Color = namedtuple('Color', 'r g b a')


def readUnsignedInt(data):
    return struct.unpack('<L', data.read(4))[0]

class PaletteArchive(object):
    __VAL_MASK = 0x7F
    __FLAG_MASK = ~0x80

    def __init__(self, data):
        self.data = BytesIO(data)
        sections = self.__readSectionTable()
        if "TADP" in sections:
            self.dataBaseOffset = sections["TADP"]
        else:
            raise ValueError('File has no data base section!')
        if "YEKP" in sections:
            self.subfiles = self.__readYEKP(sections["YEKP"])
        else:
            raise ValueError('File has no table base section!')


    def readPalette(self, section_id):
        if section_id >= len(self.subfiles):
            raise ValueError('Id is larger than the number of subfiles!')
        entry = self.subfiles[section_id]
        self.data.seek(entry.offset + self.dataBaseOffset)
        # Add logic for multi part palette / flags
        pal = []
        for color in struct.iter_unpack('<H', self.data.read(entry.size)):
            pal.append(Color(
                r=(color[0] & 0x1f) << 3,
                g=(color[0] >> 5 & 0x1f) << 3,
                b=(color[0] >> 10 & 0x1f) << 3,
                a= 0xFF * (1 - (color[0] >> 15))
            ))
        return pal

    def __readSectionTable(self):
        tbl = {}
        tblSize = readUnsignedInt(self.data)
        sectionCount = readUnsignedInt(self.data)
        for i in range(sectionCount):
            sectionName = self.data.read(4).decode("utf-8")
            sectionPos = readUnsignedInt(self.data)
            tbl[sectionName] = sectionPos
        return tbl


    def __readYEKP(self, tableStart):
        self.data.seek(tableStart)
        size = self.dataBaseOffset - tableStart
        return [
            PaletteEntry(val[2] * 32,
                         val[1] * 32,
                         val[0] & self.__VAL_MASK,
                         bool(val[0] & self.__FLAG_MASK)) for val in struct.iter_unpack('<BBH', self.data.read(size))
            ]
