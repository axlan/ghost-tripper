from construct import Adapter, Container, GreedyRange, ULInt16
from PIL import Image
from archives import Tile

class NTFSAdapter(Adapter):
    """A single tile in a screen.

    No relation to the filesystem of the same name.
    """

    def _encode(self, obj, context):
        return obj.tile | obj.transformation << 10 | obj.palette << 12

    def _decode(self, obj, context):
        return Container(
            palette=obj >> 12,
            xFlip=bool(obj >> 10 & 0x1),
            yFlip=bool(obj >> 11 & 0x1),
            tile=obj & 0x3ff
        )

ntfs = NTFSAdapter(ULInt16('tile'))
ntfs_repeater = GreedyRange(ntfs)

# Ported from https://app.assembla.com/spaces/sdat4as/subversion/source/HEAD/Nitro/Graphics/TileMappedScreen.as
class TileMappedScreen(object):

    # /** The height of the screen data, measured in pixels. */
    def height(self):
        return Tile.height * self.rows
    # /** The width of the screen data, measured in pixels */
    def width(self):
        return Tile.width * self.cols
    # /** Loads tile entries from a ByteArray
    # @param data The ByteArray to load entries from
    # @param cols The number of colums in the screen
    # @param rows The number of rows in the screen
    # @param advanced If the advanced tilemap format is used
    # */
    def __init__(self, data, cols):
        self.cols=cols
        self.entries = ntfs_repeater.parse(data)
        self.rows = int(len(self.entries) / cols)


    # /** Renders the screen to a new Sprite
    # @param tiles The GraphicsBank from which to read the tiles
    # @param convertedPalette The palette to use when rendering the tiles, in RGB888 format
    # @param useTransparency If the screen should be rendered using transparency
    # @return A new Sprite with the tiles of the screen correctly laid out
    # */
    def render(self, tiles,convertedPalette,useTransparency=True):
        return self.renderViewport(tiles,convertedPalette,useTransparency)


    def renderViewport(self, tiles,convertedPalette,useTransparency=True,startX=0,startY=0,endX=0xFFFFFFFF,endY=0xFFFFFFFF):
        mode = 'RGB'
        if useTransparency:
            mode += 'A'
        if(endX==0xFFFFFFFF): endX=self.cols
        if(endY==0xFFFFFFFF): endY=self.rows
        spr = Image.new(mode, ((endX - startX) * Tile.width, (endY - startY) * Tile.height))
        for tileY in range(startY, endY):
            y=tileY*Tile.height
            for tileX in range(startX, endX):
                x=tileX*Tile.width
                index=tileX+tileY*self.cols #not the endX value, but the width
                entry=self.entries[index]
                bmd=tiles.renderTile(entry.tile,convertedPalette,entry.palette,useTransparency)
                if(entry.xFlip):
                    bmd = bmd.transpose(Image.FLIP_LEFT_RIGHT)
                if(entry.yFlip):
                    bmd = bmd.transpose(Image.FLIP_TOP_BOTTOM)
                spr.paste(bmd, (x, y))
        return spr
