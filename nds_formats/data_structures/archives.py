import struct
from io import BytesIO
from collections import namedtuple

from nds_formats.utils import readUnsignedInt
from nds_formats.lzss3 import decompress

SubFileEntry = namedtuple('SubFileEntry', ['offset', 'size', 'compressed', 'unknownFlag'])

# Ported from https://app.assembla.com/spaces/sdat4as/subversion/source/HEAD/Nitro/Apollo/SubArchive.as
class SubArchive(object):
    __VAL_MASK = 0x7FFFFFFF
    __FLAG_MASK = ~0x7FFFFFFF

    def __init__(self, data):
        self.data = BytesIO(data)
        sections = self.__readSectionTable()
        if "TADB" in sections:
            self.dataBaseOffset = sections["TADB"]
        elif "TADP" in sections:
            self.dataBaseOffset = sections["TADP"]
        else:
            raise ValueError('File has no data base section!')
        if "YEKB" in sections:
            self.subfiles = self.__readYEKB(sections["YEKB"])
        elif "YEKP" in sections:
            self.subfiles = self.__readYEKP(sections["YEKP"])
        else:
            raise ValueError('File has no table base section!')


    def open(self, section_id):
        if section_id >= len(self.subfiles):
            raise ValueError('Id is larger than the number of subfiles!')
        entry = self.subfiles[section_id]
        self.data.seek(entry.offset + self.dataBaseOffset)
        if entry.size:
            size = entry.size
        else:
            size = self.subfiles[section_id + 1].offset - entry.offset
        out = self.data.read(size)
        if entry.compressed:
            out=decompress(out)
        return out


    def __readSectionTable(self):
        tbl = {}
        tblSize = readUnsignedInt(self.data)
        sectionCount = readUnsignedInt(self.data)
        for i in range(sectionCount):
            sectionName = self.data.read(4).decode("utf-8")
            sectionPos = readUnsignedInt(self.data)
            tbl[sectionName] = sectionPos
        return tbl


    def __readYEKB(self, tableStart):
        self.data.seek(tableStart)
        size = self.dataBaseOffset - tableStart
        return [
            SubFileEntry(val[0] & self.__VAL_MASK,
                         val[1] & self.__VAL_MASK,
                         bool(val[1] & self.__FLAG_MASK),
                         bool(val[0] & self.__FLAG_MASK)) for val in struct.iter_unpack('<2L', self.data.read(size))
            ]

    # Doesn't match behavior in Ghost Trick cpak 0 palettes
    def __readYEKP(self, tableStart):
        tableStart += 1
        self.data.seek(tableStart)
        size = self.dataBaseOffset - tableStart
        return [
            SubFileEntry(val[0] & self.__VAL_MASK,
                         None,
                         bool(val[0] & self.__FLAG_MASK),
                         None) for val in struct.iter_unpack('<L', self.data.read(size))
            ]



# Ported from https://app.assembla.com/spaces/sdat4as/subversion/source/HEAD/Nitro/GhostTrick/SplitArchive.as
class SplitArchive(object):
    def __init__(self, table, data):
        self.data = BytesIO(data)
        self.entries = [
            SubFileEntry(val[0], val[1], True,
                         False) for val in struct.iter_unpack('<2L', BytesIO(table).read())
        ]


    def length(self):
        return len(self.entries)


    def open(self, section_id):
        entry = self.entries[section_id]
        self.data.seek(entry.offset)
        return decompress(self.data)
