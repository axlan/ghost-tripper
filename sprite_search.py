from io import BytesIO
from struct import unpack
import argparse
import os

from formats import palette, Screen, parse_cpac, parse_section_data, parse_pallete_meta
from lzss3 import decompress

def split_into_tiles(data):
    t = []
    while data:
        t.append(data[:64])
        data = data[64:]
    return t

def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)



def explore_palettes(data_section, out_dir):
    pallete_meta_raw, pallete_data = parse_section_data(data_section)
    pallete_meta = parse_pallete_meta(pallete_meta_raw)
    with open(out_dir + '/meta.txt', 'w') as fd:
        for n, entry in enumerate(pallete_meta):
            print('{0:04} 0x{1.offset:06x} 0x{1.length:06x}'.format(n, entry), file=fd)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("cpac_file",
                        help="Target cpac_2d.bin file")
    parser.add_argument("-o","--out_dir",
                        help="directory for output files", default="out")
    parser.add_argument("-s", "--skip", action="store_true",
                        help="Skip decompressable chunks")
    args = parser.parse_args()

    mkdir(args.out_dir)

    # Dump cpac_2d.bin's sections to separate files for easier individual
    # staring-down
    with open(args.cpac_file, 'rb') as cpac_2d:
        data_sections = parse_cpac(cpac_2d)

    cpac_dir = args.out_dir + '/cpac'

    mkdir(cpac_dir)



    for n, section in enumerate(data_sections):

        test_dir = cpac_dir + '/{0}'.format(n)
        mkdir(test_dir)

        with open(cpac_dir + '/{0}.bin'.format(n), 'wb') as output:
            output.write(section)

        data = BytesIO(section)

        if n == 0:
            explore_palettes(data, test_dir)

        # BYTE_ALIGNMENT = 4
        # last_offset = 0
        # file_size = len(section)
        # print("========== Section {0} 0x{1:06x} bytes ".format(n, file_size))
        # with open(cpac_dir + '/{0}.bin'.format(n), 'wb') as output:
        #     output.write(section)

        # test_dir = cpac_dir + '/{0}'.format(n)
        # mkdir(test_dir)

        # data = BytesIO(section)
        # offset = 0
        # #while offset < file_size:
        # while offset < 0x0104d8:
        #     try:
        #         start = data.tell()
        #         chunk = decompress(data)
        #         u_size = len(chunk)
        #         c_size = data.tell() - offset
        #         offset_str = r'0x{0:06x}'.format(offset)
        #         with open(test_dir + '/' + offset_str + '.bin', 'wb') as output:
        #             output.write(chunk)
        #         print(offset_str + r': 0x{0:06x}-U 0x{1:06x}-C 0x{2:06x} gap'.format(u_size, c_size, offset - last_offset))
        #         last_offset = offset
        #         if args.skip and c_size > BYTE_ALIGNMENT:
        #             offset += c_size
        #         else:
        #             offset += BYTE_ALIGNMENT
        #     except:
        #         offset += BYTE_ALIGNMENT
        #     data.seek(offset)
        # if n == 2:
        #     break


if __name__ == '__main__':
    main()
