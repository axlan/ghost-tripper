from io import BytesIO
import argparse
import os

from formats import palette, Screen, parse_cpac, parse_section_data, split_into_8x8_tiles_4bit, split_into_8x8_tiles_8bit, parse_pallete_meta, parse_screen_meta
from lzss3 import decompress

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
    image_names = ['capcom', 'mobiclip', 'nintendo']


    data = BytesIO(data_sections[0])
    pallete_meta_raw, pallete_data = parse_section_data(data)
    pallete_meta = parse_pallete_meta(pallete_meta_raw)

    data = BytesIO(data_sections[2])
    screen_meta_raw, screen_data = parse_section_data(data)
    screen_meta = parse_screen_meta(screen_meta_raw)

    for image_num, image_name in enumerate(image_names):

        pallete_size = pallete_meta[image_num].length
        pallete_offset = pallete_meta[image_num].offset
        tile_offset = screen_meta[image_num].tile.offset
        screen_offset = screen_meta[image_num].screen.offset


        # Rip a palette that goes with the Capcom logo
        data = BytesIO(pallete_data)
        data.seek(pallete_offset)
        capcom_palette = palette.parse(data.read(pallete_size))

        # Rip the Capcom logo
        data = BytesIO(screen_data)
        data.seek(tile_offset)

        tiles = decompress(data)

        data.seek(screen_offset)
        screen = Screen(decompress(data))

        # Is there another way to figure this out?
        if screen.get_max_tile() > len(tiles) / 64:
            tiles = split_into_8x8_tiles_4bit(tiles)
        else:
            tiles = split_into_8x8_tiles_8bit(tiles)

        image = screen.image([capcom_palette], tiles)

        with open(args.out_dir + '/'+image_name+'.ppm', 'w') as output:
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
