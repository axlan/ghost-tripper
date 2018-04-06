from io import BytesIO
import argparse
import os

from formats import palette, Screen, parse_cpac, parse_section_data, \
                    split_into_8x8_tiles_4bit, split_into_8x8_tiles_8bit, \
                    parse_pallete_meta, parse_screen_meta,CPACSection, \
                    image_to_ppm
from lzss3 import decompress

from collections import namedtuple
from enum import Enum, auto


ImageEntry = namedtuple('ImageEntry', 'image_name palette_entry tile_entry tile_palette_bits screen_entry')

class PaletteBits(Enum):
    FOUR=auto()
    EIGHT=auto()


color = namedtuple('Color', 'r g b a')

def dummy_palette2():
    return [
    color(0xFF, 0x00, 0xFF, 0xFF), color(0x00, 0xFF, 0x00, 0xFF), color(0xFF, 0x00, 0x00, 0xFF), color(0x00, 0x00, 0xFF, 0xFF),
    color(0xFF, 0x00, 0xFF, 0xFF), color(0xFF, 0xFF, 0xFF, 0xFF), color(0x00, 0xFF, 0xFF, 0xFF), color(0xFF, 0xAA, 0x00, 0xFF),
    color(0xAA, 0xFF, 0x00, 0xFF), color(0x00, 0xAA, 0xFF, 0xFF), color(0x00, 0xFF, 0xAA, 0xFF), color(0xAA, 0x00, 0xAA, 0xFF),
    color(0xAA, 0xAA, 0x00, 0xFF), color(0xAA, 0xAA, 0xAA, 0xFF), color(0xFF, 0x00, 0xAA, 0xFF), color(0xAA, 0x00, 0xFF, 0xFF),
    ]


def dummy_gray_palette():
    gray_palette = []
    for i in range(256):
        gray_palette.append(color(
            r = i // 8,
            g = i // 8,
            b = i // 8,
            a = True
        ))
    return gray_palette


# Extract Full Screen Images From cpac_2d.bin Partition 2
def extract_cpac2_images(args):
    # Dump cpac_2d.bin's sections to separate files for easier individual
    # staring-down
    with open(args.cpac_file, 'rb') as cpac_2d:
        data_sections = parse_cpac(cpac_2d)

    data = BytesIO(data_sections[0])
    pallete_meta_raw, pallete_data = parse_section_data(data)
    pallete_meta = parse_pallete_meta(pallete_meta_raw)

    data = BytesIO(data_sections[2])
    screen_meta_raw, screen_data = parse_section_data(data)
    screen_meta = parse_screen_meta(screen_meta_raw)

    gray_palette = dummy_gray_palette()

    IMAGE_LIST = [
        ImageEntry('capcom', pallete_meta[0], screen_meta[0], PaletteBits.EIGHT, screen_meta[1]),
        ImageEntry('mobiclip', pallete_meta[1], screen_meta[2], PaletteBits.EIGHT, screen_meta[3]),
        ImageEntry('nintendo', pallete_meta[2], screen_meta[4], PaletteBits.FOUR, screen_meta[5]),
        ImageEntry('title-jp', pallete_meta[11], screen_meta[6], PaletteBits.EIGHT, screen_meta[7]),
        ImageEntry('title-en', pallete_meta[12], screen_meta[8], PaletteBits.EIGHT, screen_meta[9]),
        # ??? 10 -20 metal Shutter affect?
        # CREDITS
        # palette ?
        ImageEntry('folder1', pallete_meta[20], screen_meta[301], PaletteBits.FOUR, screen_meta[302]),
        # palette ?
        ImageEntry('folder2', pallete_meta[20], screen_meta[303], PaletteBits.FOUR, screen_meta[304]),
        # palette ?
        ImageEntry('box', pallete_meta[20], screen_meta[305], PaletteBits.FOUR, screen_meta[306]),
    ]

    for i in range(28):
        for z in range(5):
            offset = 21 + i * 10 + z
            IMAGE_LIST.append(
            ImageEntry('credits{:02}-{}'.format(i, z), pallete_meta[22], screen_meta[offset], PaletteBits.FOUR, screen_meta[offset + 5])
            )

    # for i in range(30):
    #     #if pallete_meta[i].length == 0x200:
    #     #if pallete_meta[i].length == 0x20:
    #     IMAGE_LIST.append(
    #     ImageEntry('unknown'+str(i), pallete_meta[i], screen_meta[301], PaletteBits.FOUR, screen_meta[302]),
    #     )


    for image_meta in IMAGE_LIST:

        print("Loading " + image_meta.image_name)


        # Rip a palette
        if image_meta.palette_entry:
            pallete_size = image_meta.palette_entry.length
            pallete_offset = image_meta.palette_entry.offset
            data = BytesIO(pallete_data)
            data.seek(pallete_offset)
            image_palette = palette.parse(data.read(pallete_size))

            print("\tPalette 0x{0:06x} {1} bytes {2} colors".format(pallete_offset, pallete_size, len(image_palette)))
        else:
            image_palette = gray_palette


        tile_offset = image_meta.tile_entry.offset
        screen_offset = image_meta.screen_entry.offset

        data = BytesIO(screen_data)

        data.seek(tile_offset)
        if image_meta.tile_entry.flag2:
            tiles = decompress(data)
        else:
            tiles = data.read(image_meta.tile_entry.length)
        # Is there another way to figure this out?
        #if screen.get_max_tile() > len(tiles) / 64:
        if image_meta.tile_palette_bits == PaletteBits.FOUR:
            tiles = split_into_8x8_tiles_4bit(tiles)
        else:
            tiles = split_into_8x8_tiles_8bit(tiles)
        max_palette = max([entry for tile in tiles for entry in tile])
        print("\tTiles 0x{0:06x} {1} 8x8 tiles max palette {2}".format(tile_offset, len(tiles), max_palette))

        data.seek(screen_offset)
        if image_meta.screen_entry.flag2:
            data = decompress(data)
        else:
            data = data.read(image_meta.screen_entry.length)
        screen = Screen(data)

        max_tile = max([ntfs.tile for ntfs in screen.ntfs])
        # if len(screen.ntfs) != 256*192/64:
        #     raise ValueError('invalid ntfs size {0}'.format(len(screen.ntfs)))
        print("\tScreen 0x{0:06x} 256x128 max tile {1}".format(screen_offset, max_tile))

        image = screen.image([image_palette], tiles)


        with open(args.out_dir + '/'+image_meta.image_name+'.ppm', 'w') as output:
            image_to_ppm(image, output)

# Extract Animations From cpac_2d.bin Partition 3
def extract_cpac3_images(args):
    with open(args.cpac_file, 'rb') as cpac_2d:
        data_sections = parse_cpac(cpac_2d)

    from archives import SubArchive, SplitArchive, CellBank, GraphicsBank

    subArchive = SubArchive(data_sections[3])

    pixelsTableId = 14692
    pixelsDataId = 14694
    cellBankId = 14693
    cellId = 0


    subsub =  SplitArchive(subArchive.open(pixelsTableId), subArchive.open(pixelsDataId))

    cellBank = CellBank(subArchive.open(cellBankId), subsub.length())


    tileData=subsub.open(cellId)

    tileSet= GraphicsBank()
    tileSet.bitDepth=4
    tileSet.parseTiled(tileData, 0, len(tileData))

    cell=cellBank.cells[cellId]

    pal = dummy_palette2()

    obj = cell.rend(pal,tileSet,False,True)

    # obj.x=180;
    # obj.y=150;
    # out.addChild(obj);

    # data = BytesIO(screen_data)
    # data.seek(screen_meta[pixelsTableId].offset)
    # subsub_table = decompress(data)

    # data = BytesIO(screen_data)
    # data.seek(screen_meta[pixelsDataId].offset)
    # subsub_data = decompress(data)





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

    #extract_cpac2_images(args)
    extract_cpac3_images(args)

if __name__ == '__main__':
    main()
