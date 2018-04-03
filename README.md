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
capcom
0 0x000a00: 0x002000-U 0x0b14c0-C 0x000a00 gap
1 0x0017e8: 0x000600-U 0x0b06d8-C 0x000de8 gap

mobi
2 0x001920: 0x004000-U 0x0b05a0-C 0x000138 gap
3 0x002c78: 0x000600-U 0x0af248-C 0x001358 gap

nintendo
4 0x002e74: 0x000c00-U 0x0af04c-C 0x0001fc gap
5 0x0033f0: 0x000600-U 0x0aead0-C 0x00057c gap

title-jp
6 0x00350c: 0x00c000-U 0x0ae9b4-C 0x00011c gap
7 *uncompressed 0x000600

title-en
8 0x0078f0: 0x00c000-U 0x0aa5d0-C 0x0043e4 gap
9 *uncompressed 0x000600

10 0x00B724:  *uncompressed 0x000600
11 0x00bd24: 0x00c000-U 0x0a619c-C 0x004434 gap
12 0x00be0c: 0x000800-U 0x0a60b4-C 0x0000e8 gap
13 0x00be60: 0x00c000-U 0x0a6060-C 0x000054 gap
14 0x00bfe8: 0x000800-U 0x0a5ed8-C 0x000188 gap
15 0x00c078: 0x00c000-U 0x0a5e48-C 0x000090 gap
16 0x00c154: 0x000800-U 0x0a5d6c-C 0x0000dc gap
17 0x00c1ac: 0x000800-U 0x0a5d14-C 0x000058 gap
18 0x00c320: 0x000800-U 0x0a5ba0-C 0x000174 gap
19 0x00c3b8: 0x000800-U 0x0a5b08-C 0x000098 gap
20 0x00c52c: 0x000800-U 0x0a5994-C 0x000174 gap
21 0x00c5c4: 0x006000-U 0x0a58fc-C 0x000098 gap
22 0x00ccb8: 0x000800-U 0x0a5208-C 0x0006f4 gap
23 0x00d380: 0x006000-U 0x0a4b40-C 0x0006c8 gap
24 0x00d818: 0x000800-U 0x0a46a8-C 0x000498 gap
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

                    ct_o     ct_s     cs_o      cs_s    mt_o      mt_s    ms_o     ms_s      nt_o    nt_s     ns_o    ns_s      jpt_o    jpt_s    jps_o   jpt_s
00000000 00000000 00000000 E80D0080 E80D0000 38010080 200F0000 58130080 78220000 FC010080 74240000 7C050080 F0290000 1C010080 0C2B0000 E43D0080 F0680000 00060000
  ent_o    ent_s    ens_o   ent_s    10  unc 0xB724    11  comp 0xBD24      12  comp           13  comp          14  comp           15  comp        16  comp
F06E0000 34380080 24A70000 00060000 24AD0000 00060000 24B30000 E8000080 0CB40000 54000080 60B40000 88010080 E8B50000 90000080 78B60000 DC000080 54B70000 58000080
    17  comp          18  comp
ACB70000 74010080 20B90000 98000080 B8B90000 74010080 2CBB0000 98000080 C4BB0080 F4060080 3CC50200 EC060080 D4D80400 F4060080 C0ED0600 FC060080 88FE0800 C0060080 B8C20080 C8060080 28CC0200 C8060080 C8DF0400 C8060080 BCF40600 C8060080 48050900 C8060080 80C90080 98040080 F0D20200 04050080 90E60400 8C040080 84FB0600 68050080 100C0900 04050080 18CE0080 C8060080 F4D70200 C8060080 1CEB0400 C8060080 EC000700 C8060080 14110900 C8060080 E0D40080 CC070080 BCDE0200 CC070080 E4F10400 CC070080 B4070700 CC070080 DC170900 CC070080 ACDC0080 C8060080 88E60200 C8060080 B0F90400 C8060080 800F0700 C8060080 A81F0900 C8060080 74E30080 EC060080 50ED0200 B8070080 78000500 94070080 48160700 0C070080 70260900 64070080 60EA0080 C8060080 08F50200 C8060080 0C080500 C8060080 541D0700 C8060080 D42D0900 C8060080 28F10080 B0090080 D0FB0200 9C0A0080 D40E0500 740A0080 1C240700 040A0080 9C340900 380A0080 D8FA0080 C8060080 6C060300 C8060080 48190500 C8060080 202E0700 C8060080 D43E0900 C8060080 A0010180 E8060080 340D0300 04080080 10200500 D0070080 E8340700 80070080 9C450900 A4070080


0x002e74: 0x000c00-U 0x0af04c-C 0x0001fc gap
0x0033f0: 0x000600-U 0x0aead0-C 0x00057c gap

nintendo logo
pallete_offset = 0x2d80 + 0x400
pallete_size = 0x200
tile_offset = 0x2474 + 0xa00
screen_offset = 0x29f0 + 0xa00

pallet: 0x200
tiles = 3072 - 48 tiles WRONG! Turns out these tiles are 4bit instead of 8bit so there are 96 tiles


???????? section


Not a tile set       ?????????????                      ?????????????
  o          s       o        s        o          s       o        s
0C2B0000 E43D0080 F0680000 00060000 F06E0000 34380080 24A70000 00060000



Not a tile set
0x00350c: 0x00c000-U 0x0ae9b4-C 0x00011c gap size is 256x192

Uncompressed data at 0x68F0 + 0xa00 = 72F0 , just a literal count?

0x0078f0: 0x00c000-U 0x0aa5d0-C 0x0043e4 gap

0x00bd24: 0x00c000-U 0x0a619c-C 0x004434 gap

0x00be0c: 0x000800-U 0x0a60b4-C 0x0000e8 gap

72f0:
00000100 02000300 04000500 06000700 08000900 0A000B00 0C000D00 0E000F00 10001100 12001300 14001500 16001700 18001900 1A001B00 1C001D00 1E001F00 20002100 22002300 24002500 26002700 28002900 2A002B00 2C002D00 2E002F00 30003100 32003300 34003500 36003700 38003900 3A003B00 3C003D00 3E003F00 40004100 42004300 44004500 46004700 48004900 4A004B00 4C004D00 4E004F00 50005100 52005300 54005500 56005700 58005900 5A005B00 5C005D00 5E005F00 60006100 62006300 64006500 66006700 68006900 6A006B00 6C006D00 6E006F00 70007100 72007300 74007500 76007700 78007900 7A007B00 7C007D00 7E007F00 80008100 82008300 84008500 86008700 88008900 8A008B00 8C008D00 8E008F00 90009100 92009300 94009500 96009700 98009900 9A009B00 9C009D00 9E009F00 A000A100 A200A300 A400A500 A600A700 A800A900 AA00AB00 AC00AD00 AE00AF00 B000B100 B200B300 B400B500 B600B700 B800B900 BA00BB00 BC00BD00 BE00BF00 C000C100 C200C300 C400C500 C600C700 C800C900 CA00CB00 CC00CD00 CE00CF00 D000D100 D200D300 D400D500 D600D700 D800D900 DA00DB00 DC00DD00 DE00DF00 E000E100 E200E300 E400E500 E600E700 E800E900 EA00EB00 EC00ED00 EE00EF00 F000F100 F200F300 F400F500 F600F700 F800F900 FA00FB00 FC00FD00 FE00FF00 00010101 02010301 04010501 06010701 08010901 0A010B01 0C010D01 0E010F01 10011101 12011301 14011501 16011701 18011901 1A011B01 1C011D01 1E011F01 20012101 22012301 24012501 26012701 28012901 2A012B01 2C012D01 2E012F01 30013101 32013301 34013501 36013701 38013901 3A013B01 3C013D01 3E013F01 40014101 42014301 44014501 46014701 48014901 4A014B01 4C014D01 4E014F01 50015101 52015301 54015501 56015701 58015901 5A015B01 5C015D01 5E015F01 60016101 62016301 64016501 66016701 68016901 6A016B01 6C016D01 6E016F01 70017101 72017301 74017501 76017701 78017901 7A017B01 7C017D01 7E017F01 80018101 82018301 84018501 86018701 88018901 8A018B01 8C018D01 8E018F01 90019101 92019301 94019501 96019701 98019901 9A019B01 9C019D01 9E019F01 A001A101 A201A301 A401A501 A601A701 A801A901 AA01AB01 AC01AD01 AE01AF01 B001B101 B201B301 B401B501 B601B701 B801B901 BA01BB01 BC01BD01 BE01BF01 C001C101 C201C301 C401C501 C601C701 C801C901 CA01CB01 CC01CD01 CE01CF01 D001D101 D201D301 D401D501 D601D701 D801D901 DA01DB01 DC01DD01 DE01DF01 E001E101 E201E301 E401E501 E601E701 E801E901 EA01EB01 EC01ED01 EE01EF01 F001F101 F201F301 F401F501 F601F701 F801F901 FA01FB01 FC01FD01 FE01FF01 00020102 02020302 04020502 06020702 08020902 0A020B02 0C020D02 0E020F02 10021102 12021302 14021502 16021702 18021902 1A021B02 1C021D02 1E021F02 20022102 22022302 24022502 26022702 28022902 2A022B02 2C022D02 2E022F02 30023102 32023302 34023502 36023702 38023902 3A023B02 3C023D02 3E023F02 40024102 42024302 44024502 46024702 48024902 4A024B02 4C024D02 4E024F02 50025102 52025302 54025502 56025702 58025902 5A025B02 5C025D02 5E025F02 60026102 62026302 64026502 66026702 68026902 6A026B02 6C026D02 6E026F02 70027102 72027302 74027502 76027702 78027902 7A027B02 7C027D02 7E027F02 80028102 82028302 84028502 86028702 88028902 8A028B02 8C028D02 8E028F02 90029102 92029302 94029502 96029702 98029902 9A029B02 9C029D02 9E029F02 A002A102 A202A302 A402A502 A602A702 A802A902 AA02AB02 AC02AD02 AE02AF02 B002B102 B202B302 B402B502 B602B702 B802B902 BA02BB02 BC02BD02 BE02BF02 C002C102 C202C302 C402C502 C602C702 C802C902 CA02CB02 CC02CD02 CE02CF02 D002D102 D202D302 D402D502 D602D702 D802D902 DA02DB02 DC02DD02 DE02DF02 E002E102 E202E302 E402E502 E602E702 E802E902 EA02EB02 EC02ED02 EE02EF02 F002F102 F202F302 F402F502 F602F702 F802F902 FA02FB02 FC02FD02 FE02FF02