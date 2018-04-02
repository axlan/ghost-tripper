from collections import namedtuple
from operator import itemgetter
import struct

from construct import Adapter, Container, GreedyRange, ULInt16

### Sprite-related structs

class NTFPAdapter(Adapter):
    """A DS palette entry.

    RGBA, five bits per colour channel and one bit for transparency.
    """

    def _encode(self, rgba, context):
        return rgba.r | rgba.g << 5 | rgba.b << 10 | rgba.a << 15

    def _decode(self, color, context):
        return Container(
            r=color & 0x1f,
            g=color >> 5 & 0x1f,
            b=color >> 10 & 0x1f,
            a=bool(color >> 15)
        )

class NTFSAdapter(Adapter):
    """A single tile in a screen.

    No relation to the filesystem of the same name.
    """

    def _encode(self, obj, context):
        return obj.tile | obj.transformation << 10 | obj.palette << 12

    def _decode(self, obj, context):
        return Container(
            palette=obj >> 12,
            transformation=obj >> 10 & 0x3,
            tile=obj & 0x3ff
        )


ntfp = NTFPAdapter(ULInt16('color'))
palette = GreedyRange(ntfp)

ntfs = NTFSAdapter(ULInt16('tile'))
ntfs_repeater = GreedyRange(ntfs)

class Screen():
    """A sprite that takes up the entire screen.

    A collection of NTFS cells in action.  Essentially an NSCR/NRCS without the
    headers.
    """

    def __init__(self, source):
        self.ntfs = ntfs_repeater.parse(source)

    def get_max_tile(self):
        max_tile = 0
        for tile in self.ntfs:
            if tile.tile > max_tile:
                max_tile = tile.tile
        return max_tile

    def image(self, palettes, tiles):
        """Actually put together the sprite."""
        # Prep the pixel matrix; each pixel is pixels[y][x] for easy iterating
        pixels = [[None for x in range(256)] for y in range(192)]

        for tile_num, tile in enumerate(self.ntfs):
            tile_x = tile_num % 32
            tile_y = tile_num // 32

            for pixel_num, pixel in enumerate(tiles[tile.tile]):
                # The pixel's location within the entire image
                if tile.transformation == 0:
                    # No change
                    x = pixel_num % 8 + tile_x * 8
                    y = pixel_num // 8 + tile_y * 8
                elif tile.transformation == 1:
                    # Flip along the y axis
                    x = 7 - pixel_num % 8 + tile_x * 8
                    y = pixel_num // 8 + tile_y * 8
                elif tile.transformation == 2:
                    # Flip along the x axis
                    x = pixel_num % 8 + tile_x * 8
                    y = 7 - pixel_num // 8 + tile_y * 8
                else:
                    # XXX Is this actually invalid or does it just do both flips?
                    raise ValueError('invalid NTFS transformation')

                pixels[y][x] = palettes[tile.palette][pixel]

        return pixels


### cpac stuff
# XXX Turn these into pretty structs, too

CPACSection = namedtuple('CPACSection', ['offset', 'length'])

ImageSet = namedtuple('ScreenSet', ['tile', 'screen'])

def _cpac_pointers(source):
    source.seek(0)
    pointers_length, = struct.unpack('<L', source.read(4))

    source.seek(0)
    source = source.read(pointers_length)

    while source:
        yield CPACSection(*struct.unpack('<LL', source[:8]))
        source = source[8:]

def parse_cpac(source):
    sections = []

    for section in _cpac_pointers(source):
        source.seek(section.offset)
        sections.append(source.read(section.length))

    return sections

def split_into_8x8_tiles_8bit(data):
    t = []
    while data:
        t.append(data[:64])
        data = data[64:]
    return t

def split_into_8x8_tiles_4bit(data):
    t = []
    while data:
        raw = data[:32]
        unpacked = []
        for val in raw:
            unpacked.append(val & 0xF)
            unpacked.append(val >> 4)
        t.append(unpacked)
        data = data[32:]
    return t

def parse_section_data(data):
    HEADER_SIZE = 24
    section_header = struct.unpack('<6L', data.read(HEADER_SIZE))
    data_offset = section_header[5]
    meta_data = data.read(data_offset - HEADER_SIZE)
    data = data.read()
    return meta_data, data

def parse_pallete_meta(data):
    data = data[4:]
    entries = []
    for val in  struct.iter_unpack('<BBH', data):
        pallete_size = val[1] * 32
        pallete_offset = val[2] * 32
        entries.append(CPACSection(pallete_offset, pallete_size))
    return entries

def parse_screen_meta(data):
    data = data[8:]
    return [ImageSet(CPACSection(val[0], val[1]), CPACSection(val[2], val[3] & 0xffff)) for val in struct.iter_unpack('<4L', data)]