from io import BytesIO
from struct import unpack
import argparse
import os

from formats import palette, Screen, parse_cpac
from lzss3 import decompress

def split_into_tiles(data):
    t = []
    while data:
        t.append(data[:64])
        data = data[64:]
    return t


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

    for n, section in enumerate(data_sections):
        output = open(args.out_dir + '/{0}'.format(n), 'wb')
        output.write(section)


    # Rip a palette that goes with the Capcom logo
    data = BytesIO(data_sections[0])
    data.seek(0x2d80)
    capcom_palette = palette.parse(data.read(0x200))

    # Rip the Capcom logo
    data = BytesIO(data_sections[2])
    data.seek(0xa00)  # Pointer found at 0x14

    tiles = decompress(data)
    tiles = split_into_tiles(tiles)

    data.seek(0xa00 + 0xde8)
    screen = Screen(decompress(data))

    image = screen.image([capcom_palette], tiles)

    with open(args.out_dir + '/logo.ppm', 'w') as output:
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
