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