import struct
from io import BytesIO

from PIL import Image

from nds_formats.data_structures.tiles import OamTile
from nds_formats.utils import readUnsignedByte, readByte, readUnsignedShort


# Ported from https://app.assembla.com/spaces/sdat4as/subversion/source/HEAD/Nitro/Graphics/CellOam.as
# A tile group that can be displayed as an OAM
class CellOam(OamTile):

#         /** The y position of the object, in pixels */
    y = None
#         /** The yx position of the object, in pixels */
    x = None
#         /** If the object should be hidden */
    hide=False
#         /** If the object should be displayed at double size */
    doubleSize=False
#         /** If the object should be flipped along the X axis when displayed */
    xFlip=False
#         /** If the object should be flipped along the Y axis when displayed */
    yFlip=False

#         /** Rends the tile group accordingly to the settings
#         @param palette The RGB888 palette to use when rendering the tiles
#         @param tiles The tiles pixel data to use
#         @param useSubImages If sub image addressing should be used
#         @param useTransparency If the tiles should be rendered using transparency
#         @return A DisplayObject that represents the tile group
#         */
    def rend(self,palette,tiles,useSubImages,useTranparency):
        oamR = super(CellOam, self).rend(palette,tiles,useSubImages,useTranparency)
        if(self.xFlip):
            oamR = oamR.transpose(Image.FLIP_LEFT_RIGHT)
        if(self.yFlip):
            oamR = oamR.transpose(Image.FLIP_TOP_BOTTOM)
        return oamR

#         /** Draws a rectangle that represents the OAM
#         @param boxColor The stroke color for the rectangle
#         @param useFill If the rectangle should be filled
#         @param tileNumbers If the tile number should be displayed
#         @return A DisplayObject that contains the drawn rectangle*/
#         public override function drawBox(boxColor:uint=0,useFill:Boolean=true,tileNumbers:Boolean=true):DisplayObject {
            
#             var spr:DisplayObject=super.drawBox(boxColor,useFill,tileNumbers);
#             spr.x=x;
#             spr.y=y;
            
#             return spr;
#         }
        
#         protected override function addTileNumber(spr:Sprite):void {
#             var tf:TextField=new TextField();
#             tf.autoSize=TextFieldAutoSize.LEFT;
#             tf.selectable=false;
#             tf.text=String(tileIndex);
            
#             if(xFlip) tf.appendText("XF");
#             if(yFlip) tf.appendText("YF");
            
#             spr.addChild(tf);
#         }

    def __init__(self, data, tileIndexShift, sectionNudge):
        self.y = readByte(data)
        atts0 = readUnsignedByte(data)

        rs = bool(atts0 & 1)
        if(rs):
            self.doubleSize=(atts0 & 2) ==2
        else:
            self.hide=(atts0 & 2) ==2

        self.colorDepth=atts0 >> 5 & 0x1

        shape=atts0 >> 6

        atts1=readUnsignedShort(data)

        self.x=atts1 & 0x1FF

        if(self.x>=0x100):
            self.x-=0x200

        if(not rs):
            self.xFlip=(atts1 & 0x1000)==0x1000
            self.yFlip=(atts1 & 0x2000)==0x2000

        objSize=atts1 >> 14

        atts2=readUnsignedShort(data)

        self.tileIndex=(atts2 & 0x3FF)

        self.tileIndex <<= tileIndexShift
        self.tileIndex += sectionNudge

        self.paletteIndex= atts2 >> 12

        self.priority=atts2 >> 10 & 0x3

        self.setSize(objSize, shape)


#         public function writeEntry(oamOut:ByteArray,shift:uint):void {
#             oamOut.writeByte(y);
#             oamOut.writeByte(att0());
#             oamOut.writeShort(att1());
#             oamOut.writeShort(att2(shift));
#         }
    
#         private function att0():uint {
#             var o:uint=0;
        
#             if(doubleSize) {
#                 o|=0x30;
#             } else if(hide) {
#                 o|=0x20;
#             }
        
#             o|=colorDepth<<5;
        
#             if(width==height) {
#                 o|=0;
#             } else if(width<height) {
#                 o|=0x80;
#             } else if(width>height) {
#                 o|=0x40;
#             } else {
#                 o|=0xC0;
#             }
        
#             return o;
#         }
    
#         private function att1():uint {
#             var o:uint=0;
        
#             o|=x&0x1FF;
        
#             if(xFlip) {
#                 o|=0x1000;
#             }
#             if(yFlip) {
#                 o|=0x2000;
#             }
        
#             o|=getSize()<<14;
        
#             return o;
#         }
    
#         private function att2(shift:uint):uint {
#             var o:uint=0;
        
#             var shiftedTileIndex:uint=tileIndex;
#             if(shift>0) {
#                 shiftedTileIndex>>>=shift;
#             }
#             return shiftedTileIndex | paletteIndex << 12;
#         }
    
#     }

# }




# Ported from https://app.assembla.com/spaces/sdat4as/subversion/source/HEAD/Nitro/Graphics/Cell.as
#/** A collection of OAMs that when renderd together compose a single picture */
class Cell(object):

    # /** The oams that the picture is composed of */
    def __init__(self, oams):
        self.oams = oams

    # /** Draws the cell
    # @param palette The palette to use when rendering the tiles, in RGB888 format
    # @param tiles The GraphicsBank where the tiles are stored
    # @param subImages True if the tiles are aranged in a big grid or false if they are aranged in one grid per object
    # @param useTransparence If the tiles should be rendered using transparency
    # @return A new DisplayObject that represents the cell */
    def rend(self, palette,tiles,useSubImages,useTranparency):
        spr = Image.new('RGB', (1024,1024))

        for oam in self.oams:
            oamR=oam.rend(palette,tiles,useSubImages,useTranparency)
            spr.paste(oamR, (oam.x+256, oam.y+256))

        return spr

    # /** Draws a rectangle for each object in the cell
    # @param boxColor The stroke color for the rectangles
    # @param useFill If the rectangles should be filled
    # @param tileNumbers If the tile numbers should be displayed
    # @return A DisplayObject with the boxes representing the objects*/
    # public function rendBoxes(boxColor:uint=0,useFill:Boolean=true,tileNumbers:Boolean=true):DisplayObject {
    #     var spr:Sprite=new Sprite();
        
        
        
    #     for each(var oam:CellOam in oams) {
    #         spr.addChild(oam.drawBox(boxColor,useFill,tileNumbers));
    #     }
        
    #     return spr;


# Ported from https://app.assembla.com/spaces/sdat4as/subversion/source/HEAD/Nitro/GhostTrick/CellBank.as
class CellBank(object):
    def __init__(self, data, cellCount):
        data = BytesIO(data)
        self.cells = [None for x in range(cellCount)]
        cellStarts = [val[0] * 2 for val in struct.iter_unpack('<H', data.read(cellCount * 2))]
        for cellItr in range(cellCount):
            cellStart=cellStarts[cellItr]
            data.seek(cellStart)
            cellLength = readUnsignedShort(data)
            oams = [None for x in range(cellLength)]
            for objItr in range(cellLength):
                obj = CellOam(data, 2 , 0)
                oams[objItr] = obj
            self.cells[cellItr] = Cell(oams)
