# Ghost Tripper - Ghost Trick Rom Hacking Tools

## Setup

### Prerequisites

 * Python3 - https://www.python.org/downloads/
   * construct 2.5.3 - `pip install construct==2.5.3`

### Optional Tools

 * ndsfuse - https://github.com/magical/ndsfuse (build from source on Linux)
 * Rom Hacking Tool Pack - https://gbatemp.net/threads/the-ultimate-nintendo-ds-rom-hacking-guide.291274/
   * BatchLZ77
   * CrystalTile
   * DSBuff
   * etc.

### Unpacking the ROM

The first step is to use your tool of choice to unpack the ghost trick ROM. You should end up with a data directory with directories st01 - st15 (the script files) and cpac_2d.bin (the 2d assets) this directory will be reffered to as $DATA_DIR


## Editting the script

To get the contents of a script file, run: `python text.py $DATA_DIR/st01/st01_game000_Expand.en.xml.lz` with the script file you want to read.

## Editting the sprites

To extract the 2d assets, run `python sprites.py $DATA_DIR/cpac_2d.bin`

## CPAC Disection

LZ Archives:
========== Section 0 0x0469c0 bytes
========== Section 1 0x00177c bytes
0x000200: 0x000c00-U 0x00157c-C 0x000200 gap
0x0004e8: 0x000c00-U 0x001294-C 0x0002e8 gap
0x0007d0: 0x000c00-U 0x000fac-C 0x0002e8 gap
0x0009b4: 0x000c00-U 0x000dc8-C 0x0001e4 gap
0x000c90: 0x000c00-U 0x000aec-C 0x0002dc gap
0x000fb8: 0x000c00-U 0x0007c4-C 0x000328 gap
0x001228: 0x000c00-U 0x000554-C 0x000270 gap
0x0014f8: 0x000c00-U 0x000284-C 0x0002d0 gap
========== Section 2 0x0b1ec0 bytes
0x000a00: 0x002000-U 0x0b14c0-C 0x000a00 gap
0x0017e8: 0x000600-U 0x0b06d8-C 0x000de8 gap
0x001920: 0x004000-U 0x0b05a0-C 0x000138 gap
0x002c78: 0x000600-U 0x0af248-C 0x001358 gap
0x002e74: 0x000c00-U 0x0af04c-C 0x0001fc gap
0x0033f0: 0x000600-U 0x0aead0-C 0x00057c gap
0x00350c: 0x00c000-U 0x0ae9b4-C 0x00011c gap
0x0078f0: 0x00c000-U 0x0aa5d0-C 0x0043e4 gap
0x00bd24: 0x00c000-U 0x0a619c-C 0x004434 gap
0x00be0c: 0x000800-U 0x0a60b4-C 0x0000e8 gap
0x00be60: 0x00c000-U 0x0a6060-C 0x000054 gap
0x00bfe8: 0x000800-U 0x0a5ed8-C 0x000188 gap
0x00c078: 0x00c000-U 0x0a5e48-C 0x000090 gap
0x00c154: 0x000800-U 0x0a5d6c-C 0x0000dc gap
0x00c1ac: 0x000800-U 0x0a5d14-C 0x000058 gap
0x00c320: 0x000800-U 0x0a5ba0-C 0x000174 gap
0x00c3b8: 0x000800-U 0x0a5b08-C 0x000098 gap
0x00c52c: 0x000800-U 0x0a5994-C 0x000174 gap
0x00c5c4: 0x006000-U 0x0a58fc-C 0x000098 gap
0x00ccb8: 0x000800-U 0x0a5208-C 0x0006f4 gap
0x00d380: 0x006000-U 0x0a4b40-C 0x0006c8 gap
0x00d818: 0x000800-U 0x0a46a8-C 0x000498 gap
0x00dee0: 0x006000-U 0x0a3fe0-C 0x0006c8 gap
0x00e6ac: 0x000800-U 0x0a3814-C 0x0007cc gap
0x00ed74: 0x006000-U 0x0a314c-C 0x0006c8 gap
0x00f460: 0x000800-U 0x0a2a60-C 0x0006ec gap
0x00fb28: 0x006000-U 0x0a2398-C 0x0006c8 gap
...


### 0 - Palletes

offsets/lengths seem to be in units of thirty-two bytes

Initial pallete at 0x2d80 len 0x200

Starts with incrementing values:

Initial Header 0x000000 6 bytes:
`18000000 02000000 59454B50 18000000 54414450 802D0000`

Followed by incrementing count:

```
 00000000 00100000 00101000 00102000 00013000 00013100 00013200 00013300 00013400 00013500 00013600 00013700 00103800 00104800 00105800 00106800 00107800 00108800 00109800 0010A800 0001B800 0001B900 0001BA00 0001BB00 0001BC00 0001BD00 0001BE00 0001BF00 0001C000 0001C100 0001C200 0001C300 0010C400 0001D400 0001D500 0001D600 0001D700 0001D800 0001D900 0001DA00 0001DB00 0010DC00 0010EC00 0010FC00 00100C01 00101C01 00102C01 00103C01 00104C01 00105C01 00106C01 00107C01 00108C01 00109C01 0010AC01 0010BC01 0010CC01 0001DC01 0001DD01 0001DE01 0001DF01 0001E001 0001E101 0001E201 0001E301 0001E401 0001E501 0001E601 0001E701 0001E801 0001E901 0001EA01 0001EB01 0001EC01 0001ED01 0001EE01 0001EF01 0001F001 0001F101 0001F201 0001F301 0001F401 0001F501 0001F601 0001F701 0001F801 0001F901 0001FA01 0001FB01 0001FC01 0001FD01 0001FE01 0001FF01
```
Then another
```
00010002 00010102 00010202 00010302 00010402 00010502 00010602 00010702 00010802 00100902 00101902 00102902 00103902 00104902 00105902 00106902 00107902 00108902 00109902 0010A902 0010B902 0010C902 0010D902 0010E902 0010F902
```
And so on. Some breaks in this pattern, but the last byte clearly increments across these sections from 0x00 - 0x21 which ends at 0x2d80

My interpretation, the counts are some form of offset from the start value, at least at first:
0: 0x2D90 + 0x00000 - 0x00100
0: 0x2D90 + 0x00100 - 0x10000
0: 0x2D90 + 0x10100 - 0x00100
0: 0x2D90 + 0x10200 - 0x02E00
0: 0x2D90 + 0x13000

### 1 - Fonts:

### 2 - images:
first couple things are the Capcom logo and the Mobi Clip or whatever logo

`18000000 02000000 59454B42 18000000 54414442 000A0000`

capcom tiles: 0xa00 capcom screen: 0x0017e8
mobi tiles: 0x001920 mobi screen: 0x002c78

???: 0x002e74
???: 0x0033f0

0x000a00: 0x002000 bytes 0x000a00 gap
0x0017e8: 0x000600 bytes 0x000de8 gap
0x001920: 0x004000 bytes 0x000138 gap
0x002c78: 0x000600 bytes 0x001358 gap
0x002e74: 0x000c00 bytes 0x0001fc gap
0x0033f0: 0x000600 bytes 0x00057c gap
0x00350c: 0x00c000 bytes 0x00011c gap

    #Capcom
    # pallete_offset = 0x2d80
    # pallete_size = 0x200
    # tile_offset = 0xa00 # Pointer found at 0x14
    # screen_offset = 0xa00 + 0xde8

0x000a00: 0x002000-U 0x0b14c0-C 0x000a00 gap
0x0017e8: 0x000600-U 0x0b06d8-C 0x000de8 gap
pallet: 0x200 - 256 colors allocated, ? used
tiles: 0x2000 - 128 64 byte arrays (8x8 tiles)
screen: 0x300 - 768 entries
256x192 image
8x8 tiles




0x001920: 0x004000-U 0x0b05a0-C 0x000138 gap
0x002c78: 0x000600-U 0x0af248-C 0x001358 gap


    # MobiClip
    # pallete_offset = 0x2d80 + 0x200
    # pallete_size = 0x200
    # tile_offset = 0x001920
    # screen_offset = 0x002c78

    adjust all by + 0xA00
    #Capcom
    # tile_offset   0x000000 = 0x000000 + 0x000000 # Pointer found at 0x14
    # screen_offset 0x000DE8 = 0x000000 + 0x000de8
    # MobiClip
    # tile_offset   0x000F20 = 0x000DE8 + 0x000138
    # screen_offset 0x002c78 = 0x000F20 + 0x001D58

                    ct_o     ct_s     cs_o      cs_s    mt_o      mt_s    ms_o     ms_s      ?t_o    ?t_s     ?s_o    ?s_s
00000000 00000000 00000000 E80D0080 E80D0000 38010080 200F0000 58130080 78220000 FC010080 74240000 7C050080 F0290000 1C010080 0C2B0000 E43D0080 F0680000 00060000 F06E0000 34380080 24A70000 00060000


0x002e74: 0x000c00-U 0x0af04c-C 0x0001fc gap
0x0033f0: 0x000600-U 0x0aead0-C 0x00057c gap

???
pallete_offset = 0x2d80 + 0x400
pallete_size = 0x200
tile_offset = 0x2474 + 0xa00
screen_offset = 0x29f0 + 0xa00

pallet: 0x200
tiles = 3072 - 48 tiles WRONG! Turns out these tiles are 4bit instead of 8bit so there are 96 tiles


