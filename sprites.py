from io import BytesIO
import argparse
import os

from formats import palette, Screen, parse_cpac, parse_section_data, split_into_8x8_tiles_4bit, split_into_8x8_tiles_8bit, parse_pallete_meta, parse_screen_meta,CPACSection
from lzss3 import decompress

from collections import namedtuple
from enum import Enum, auto


ImageEntry = namedtuple('ImageEntry', 'image_name palette_entry tile_entry tile_palette_bits screen_entry screen_is_compressed')

class PaletteBits(Enum):
    FOUR=auto()
    EIGHT=auto()

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("cpac_file",
                    help="Target cpac_2d.bin file")
    parser.add_argument("-o","--out_dir",
                    help="directory for output files", default="out")
    # parser.add_argument("-a", "--annotate", action="store_true",
    #                     help="Replace ")
    args = parser.parse_args()

    if not os.path.exists(args.out_dir):
        os.makedirs(args.out_dir)

    # Dump cpac_2d.bin's sections to separate files for easier individual
    # staring-down
    with open(args.cpac_file, 'rb') as cpac_2d:
        data_sections = parse_cpac(cpac_2d)

    # #Capcom
    # pallete_offset = 0x2d80
    # pallete_size = 0x200
    # tile_offset = 0xa00 # Pointer found at 0x14
    # screen_offset = 0xa00 + 0xde8

    # MobiClip
    # pallete_offset = 0x2d80 + 0x200
    # pallete_size = 0x200
    # tile_offset = 0x001920
    # screen_offset = 0x002c78

    # pallete_offset = 0x2d80 + 0x400
    # pallete_size = 0x200
    # tile_offset = 0x002e74
    # screen_offset = 0x0033f0
    #, 'UNKNOWN'


    data = BytesIO(data_sections[0])
    pallete_meta_raw, pallete_data = parse_section_data(data)
    pallete_meta = parse_pallete_meta(pallete_meta_raw)

    data = BytesIO(data_sections[2])
    screen_meta_raw, screen_data = parse_section_data(data)
    screen_meta = parse_screen_meta(screen_meta_raw)

    IMAGE_LIST = [
        ImageEntry('capcom', pallete_meta[0], screen_meta[0], PaletteBits.EIGHT, screen_meta[1], True),
        ImageEntry('mobiclip', pallete_meta[1], screen_meta[2], PaletteBits.EIGHT, screen_meta[3], True),
        ImageEntry('nintendo', pallete_meta[2], screen_meta[4], PaletteBits.FOUR, screen_meta[5], True),
        ImageEntry('title-jp', pallete_meta[11], screen_meta[6], PaletteBits.EIGHT, screen_meta[7], False),
        ImageEntry('title-en', pallete_meta[11], screen_meta[8], PaletteBits.EIGHT, screen_meta[9], False),
    ]


    screen_idx = 0

    for image_meta in IMAGE_LIST:

        print("Loading " + image_meta.image_name)

        pallete_size = image_meta.palette_entry.length
        pallete_offset = image_meta.palette_entry.offset


        tile_offset = image_meta.tile_entry.offset
        screen_offset = image_meta.screen_entry.offset

        # Rip a palette
        data = BytesIO(pallete_data)
        data.seek(pallete_offset)
        image_palette = palette.parse(data.read(pallete_size))

        print("\tPalette 0x{0:06x} {1} bytes {2} colors".format(pallete_offset, pallete_size, len(image_palette)))


        print("\tTiles 0x{0:06x} ".format(tile_offset))

        data = BytesIO(screen_data)

        data.seek(tile_offset)
        tiles = decompress(data)
        # Is there another way to figure this out?
        #if screen.get_max_tile() > len(tiles) / 64:
        if image_meta.tile_palette_bits == PaletteBits.FOUR:
            tiles = split_into_8x8_tiles_4bit(tiles)
        else:
            tiles = split_into_8x8_tiles_8bit(tiles)
        max_palette = max([entry for tile in tiles for entry in tile])
        print("\tTiles 0x{0:06x} {1} 8x8 tiles max palette {2}".format(tile_offset, len(tiles), max_palette))

        data.seek(screen_offset)
        # Is there another way to figure this out?
        # if len(tiles) < 0xC000 then compressed
        if image_meta.screen_is_compressed:
            data = decompress(data)
        else:
            data = data.read(image_meta.screen_entry.length)
        screen = Screen(data)

        max_tile = max([ntfs.tile for ntfs in screen.ntfs])
        if len(screen.ntfs) != 256*192/64:
            raise ValueError('invalid ntfs size {0}'.format(len(screen.ntfs)))
        print("\tScreen 0x{0:06x} 256x128 max tile {1}".format(screen_offset, max_tile))

        image = screen.image([image_palette], tiles)


        with open(args.out_dir + '/'+image_meta.image_name+'.ppm', 'w') as output:
            # PPM header
            output.write(
                'P3\n'
                '256 192\n'
                '31\n'
            )

            for row in image:
                for pixel in row:
                    print(pixel.r, pixel.g, pixel.b, file=output, end='  ')

                print(file=output)

if __name__ == '__main__':
    main()
