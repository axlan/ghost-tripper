import struct
from io import BytesIO

from PIL import Image

from nds_formats.utils import readUnsignedByte, readByte, readUnsignedShort

# Ported from https://app.assembla.com/spaces/sdat4as/subversion/source/HEAD/Nitro/Graphics/Tile.as
class Tile(object):
# /** A single 8 by 8 tile. */

#         /** The pixel data for the tile. Each element is a palette index. */
    pixels = None
#         /** The width of a tile */
    width = 8
#         /** The height of a tile */
    height = 8

    def __init__(self):
        self.pixels = [None for x in range(self.width*self.height)]

#         /** Reads a tile from a ByteArray
#         @param bits The number of bits per pixel
#         @throws ArgumentError The number of bits per pixel is not supported
#         @param data The ByteArray to read from
#         */
    def readTile(self, bits, data):
        if bits == 4:
            for y in range(self.height):
                for x in range(0, self.width, 2):
                    nibble = readUnsignedByte(data)
                    index = x + y * self.width
                    self.pixels[index] = nibble & 0xF
                    index = x + 1 + y * self.width
                    self.pixels[index] = (nibble >> 4) & 0xF
        elif bits == 8:
            for y in range(self.height):
                for x in range(self.width):
                    index= x + y * self.width
                    self.pixels[index] = readUnsignedByte(data)
        else:
            raise ValueError('Only 4 and 8 bit tiles are supported!')


#         private var rendered:BitmapData;
#         private var renderedPalette:Vector.<uint>;
#         private var renderedPaletteOffset:uint;
#         private var renderedUseTransparency:Boolean;
        
#         /** Draws a tile to a BitmapData object
#         @param palette The palette to use when drawing, in RGB888 format
#         @param paletteOffset The subpalette to use
#         @param useTransparency If the tile should be drawn with palette index 0 as transparency
#         @return A BitmapData of the tile. */
    def toBMD(self, palette,paletteOffset,useTransparency):

        # if(rendered && renderedPalette==palette && renderedPaletteOffset==paletteOffset && renderedUseTransparency==useTransparency) {
        #     return rendered;
        # }

        #BitmapData = new BitmapData(width,height,useTransparency)
        if useTransparency:
            mode = 'RGBA'
        else:
            mode = 'RGB'

        bmd = Image.new(mode, (self.width,self.height))

        # index = 0
        # for y in range(self.height):
        #     for x in range(self.width):
        #         color=self.pixels[index]
        #         index += 1

        #         val = palette[color+paletteOffset*16]
        #         bmd.putpixel((x,y),val)
        #         print ((x,y),val)


        # ? if(color==0 && useTransparency)
        buffer = [palette[color+paletteOffset*16] for color in self.pixels]
        bmd.putdata(buffer)

        # rendered=bmd
        # renderedPalette=palette
        # renderedPaletteOffset=paletteOffset
        # renderedUseTransparency=useTransparency

        return bmd
#         /** Loads a tile from a BitmapData using a palette
#         @param colorIndexes The palette to use, in RGB555 format
#         @param useTransparency If the first palette index is transparency or not
#         @param bmd The BitmapData to load from
#         @param xStart The leftmost position of the tile in the BitmapData
#         @param yStart The topmost position of the tile in the BitmapData
#         @return A new Tile
#         */
#         public static function fromBitmap(colorIndexes:Object,useTransparency:Boolean,bmd:BitmapData,xStart:uint,yStart:uint):Tile {
#             var tile:Tile=new Tile();
            
#             for(var y:uint=0;y<height;++y) {
#                 for(var x:uint=0;x<width;++x) {
#                     var index:uint=x+y*width;
#                     var color:uint=bmd.getPixel32(x+xStart,y+yStart);
                    
#                     var alpha:uint=color >>> 24;
                    
#                     if(alpha < 0x80 && useTransparency) {
#                         tile.pixels[index]=0;
#                         continue;
#                     }
                    
#                     color=RGB555.toRGB555(color);
                    
#                     if(color in colorIndexes) {
#                         tile.pixels[index]=colorIndexes[color];
#                     } else {
#                         tile.pixels[index]=0;
#                     }
#                 }
#             }
            
#             return tile;
#         }
        
#         /** Writes a tile to a ByteArray
#         @param bits The number of bits per pixel
#         @param data The ByteArray to write to
#         @throws ArgumentError The number of bits per pixel is not supported
#         */
#         public function writeTile(bits:uint,data:ByteArray):void {
#             if(bits!=4 && bits!=8) throw new ArgumentError("Only 4 and 8 bit tiles are supported!");
            
#             var x:uint,y:uint;
#             var index:uint;
            
#             if(bits==4) {
                
#                 for(y=0;y<height;++y) {
#                     for(x=0;x<width;) {
#                         var nibble:uint;
                        
#                         index=(x++)+y*width;                        
#                         nibble=pixels[index] & 0xF;
                        
#                         index=(x++)+y*width;                        
#                         nibble|=(pixels[index] & 0xF )<<4 ;
#                         data.writeByte(nibble);
#                     }
#                 }
#             } else if(bits==8) {
#                 for(y=0;y<height;++y) {
#                     for(x=0;x<width;) {
#                         index=(x++)+y*width;
#                         data.writeByte(pixels[index]);
#                     }


# Ported from https://app.assembla.com/spaces/sdat4as/subversion/source/HEAD/Nitro/Graphics/GraphicsBank.as
class GraphicsBank(object):
    # /** The tiles the picture is composed of, if any
    # @see picture*/
    tiles = None
    # /** The pixels the picture is composed of, if any
    # @see tiles*/
    picture = None

    # /** The number of tiles along the x axis */
    tilesX = None
    # /** The number of tiles along the y axis */
    tilesY = None

    # /** The number of bits used to store each pixel.
    # <p>Must be either 4 or 8.</p>*/
    bitDepth = None

    def parseTiled(self, data, dataOffset, dataSize):
        data = BytesIO(data)
        endPos = dataSize + dataOffset
        data.seek(dataOffset)
        self.tiles = []
        #HACK
        self.tilesX = 8
        self.tilesY = 8
        while data.tell() < endPos:
            tile = Tile()
            tile.readTile(self.bitDepth,data)
            self.tiles.append(tile)

        # public function parseScaned(data:ByteArray,dataOffset:uint,dataSize:uint):void {
        #     var index:uint;
            
        #     picture=new Vector.<uint>();
        #     picture.length=dataSize*8/bitDepth;
        #     picture.fixed=true;
        #     index=0;
        #     while(data.position<dataSize+dataOffset) {
        #         var byte:uint=data.readUnsignedByte();
        #         if(bitDepth==2) {
        #             picture[index++]=byte & 3;
        #             byte>>=2;
        #             picture[index++]=byte & 3;
        #             byte>>=2;
        #             picture[index++]=byte & 3;
        #             byte>>=2;
        #             picture[index++]=byte & 3;
        #         } else if(bitDepth==4) {
        #             picture[index++]=byte & 0xF;
        #             picture[index++]=byte >> 4;
        #         } else {
        #             picture[index++]=byte;
        #         }
        #     }
        # }
        
        # /** Writes all the tiles in the bank to a ByteArray
        # @param o The ByteArray to write the tiles to
        # */
        # public function writeTiles(o:ByteArray):void {
        #     for each(var tile:Tile in tiles) {
        #         tile.writeTile(bitDepth,o);
        #     }
        # }
        
        # /** Renders a specific tile to a BitmapData
        # @param subTileIndex The number of the tile to render
        # @param palette The palette to use when rendering the tile, in RGB888 format
        # @param paletteIndex The subpalette index to use
        # @param useTransparency If the tile should be rendered using transparency
        # @return A BitmapData for the tile*/
    def renderTile(self,subTileIndex,palette,paletteIndex,useTransparency):
        tile=self.tiles[subTileIndex]

        #//ignore palette when in 8 bpp mode
        if(self.bitDepth==8):
            paletteIndex=0

        return tile.toBMD(palette,paletteIndex,useTransparency)

        # /** Renders an oam entry
        # @param oam The oam entry to render
        # @param palette The palette to use when rendering, in RGB888 format
        # @param subImages True if the tiles are aranged in a big grid or false if they are aranged in one grid per oam
        # @param useTransparency If the tiles should be rendered using transparency
        # @return A DisplayObject that represents the oam entry
        # */
    def renderOam(self,oam,palette,subImages,useTransparency):
        if(self.tiles):
            return self.renderTileOam(oam,palette,subImages,useTransparency)
        else:
            #return renderPictureOam(oam,palette,useTransparency)
            raise ValueError('Not Implemented!!')

        # private function renderPictureOam(oam:OamTile,palette:Vector.<uint>,useTransparency:Boolean): DisplayObject {
        #     var bmd:BitmapData=new BitmapData(oam.width,oam.height,useTransparency);
        #     bmd.lock();
            
        #     const offset:uint=oam.tileIndex*(bitDepth==4?64:32);
            
        #     for(var y:uint=0;y<oam.height;++y) {
        #         for(var x:uint=0;x<oam.width;++x) {
        #             var color:uint=picture[x+y*oam.width+offset];
        #             if(color==0 && useTransparency) {
        #                 bmd.setPixel32(x,y,0x00FFF00F);
        #             } else {
        #                 color=palette[color+oam.paletteIndex*16];
        #                 bmd.setPixel(x,y,color);
        #             }
        #         }
        #     }
        #     bmd.unlock();
        #     return new Bitmap(bmd);
        # }

    def renderTileOam(self, oam,palette,subImages,useTransparency):


        if self.bitDepth==8:
            tileIndex=oam.tileIndex>>1
        else:
            tileIndex=oam.tileIndex

        baseX=tileIndex%self.tilesX
        baseY=tileIndex//self.tilesX

        yTiles=int(oam.height/Tile.height)
        xTiles=int(oam.width/Tile.width)

        spr = Image.new('RGB', (oam.width, oam.height))

        if(self.tilesX==0xFFFF):
            subTileWidth=xTiles
        else:
            subTileWidth=self.tilesX

        for y in range(yTiles):
            for x in range(xTiles):
                if(subImages):
                    subTileYIndex=baseY+y
                    subTileXIndex=baseX+x
                    subTileIndex=subTileXIndex+subTileYIndex*subTileWidth
                else:
                    subTileIndex=tileIndex+x+y*xTiles
                # var tileR:DisplayObject=new Bitmap(renderTile(subTileIndex,palette,oam.paletteIndex,useTransparency))
                # tileR.x=Tile.width*x
                # tileR.y=Tile.height*y
                # spr.addChild(tileR)
                tileR = self.renderTile(subTileIndex,palette,oam.paletteIndex,useTransparency)
                spr.paste(tileR, (Tile.width * x, Tile.height * y))

        return spr

        # /** Converts an OAM to a single Vector with color indexes
        # @param oam The OAM to convert
        # @param subImages True if the tiles are aranged in a big grid or false if they are aranged in one grid per oam
        # @return A new Vector with the color indexes
        # */
        # public function oamToVector(oam:OamTile,subImages:Boolean):Vector.<uint> {
        #     if(tiles) {
        #         return tileOamToVector(oam,subImages);
        #     } else {
        #         return pictureOamToVector(oam);
        #     }
        # }
            
        # private function tileOamToVector(oam:OamTile,subImages:Boolean):Vector.<uint> {
        #     var o:Vector.<uint>=new Vector.<uint>();
        #     o.length=oam.height*oam.width;
        #     o.fixed=true;
            
        #     var tileIndex:uint=(bitDepth==8)?oam.tileIndex>>1:oam.tileIndex;
            
        #     const baseX:uint=tileIndex%tilesX;
        #     const baseY:uint=tileIndex/tilesX;
            
        #     const yTiles:uint=oam.height/Tile.height;
        #     const xTiles:uint=oam.width/Tile.width;
            
        #     var subTileWidth:uint;
        #     if(tilesX==0xFFFF) {
        #         subTileWidth=xTiles;
        #     } else {
        #         subTileWidth=tilesX;
        #     }
            
        #     for(var y:uint=0;y<yTiles;++y) {
        #         for(var x:uint=0;x<xTiles;++x) {
                    
        #             var subTileIndex:uint;
                    
        #             if(subImages) {
        #                 var subTileYIndex:uint=baseY+y;
        #                 var subTileXIndex:uint=baseX+x;
                        
        #                 subTileIndex=subTileXIndex+subTileYIndex*subTileWidth;
        #             } else {
        #                 subTileIndex=tileIndex+x+y*xTiles;
        #             }
                    
        #             var tile:Tile=tiles[subTileIndex];
                    
        #             for(var tileY:uint=0;tileY<Tile.height;tileY++) {
        #                 var totalY:uint=tileY+y*Tile.height;
        #                 for(var tileX:uint=0;tileX<Tile.width;tileX++) {
                            
        #                     var totalX:uint=tileX+x*Tile.width;
                            
        #                     var index:uint=totalX+totalY*oam.width;
        #                     o[index]=tile.pixels[tileX+tileY*Tile.height];
        #                 }
        #             }
        #         }
                
        #     }
            
        #     return o;
        # }
        
        # private function pictureOamToVector(oam:OamTile):Vector.<uint> {
        #     const offset:uint=oam.tileIndex*(bitDepth==4?64:32);
            
        #     return picture.slice(offset,oam.height*oam.width);
        # }
        
        # /** Builds a complete collection of concatinated oams.
        
        
        
        # @param useTiles If the data should be formated as a pixel stream or as tiled pixels
        # @param oamPixels The pixel data for each tile
        # @param oams The oams the pixel data belongs to
        
        # <p>The oams will be edited to contain correct tile indexes.</p>
        
        # @return A mapping from old indexes to new indexes
        # */
        # public function build(useTiles:Boolean,oamPixels:Vector.<Vector.<uint>>,oams:Vector.<OamTile>):Object {
            
        #     if(useTiles) {
        #         return buildTiles(oamPixels,oams);
        #     } else {
        #         return buildPicture(oamPixels,oams);
        #     }
        # }
        
        # private function buildTiles(oamPixels:Vector.<Vector.<uint>>,oams:Vector.<OamTile>):Object {
        #     var t:Vector.<Tile>=new Vector.<Tile>;
        #     var map:Object={};
            
        #     for(var i:uint=0;i<oams.length;++i) {
        #         var oam:OamTile=oams[i];
        #         var tilePixels:Vector.<uint>=oamPixels[i];
                
        #         map[oam.tileIndex]=t.length;
        #         oam.tileIndex=t.length;
                
        #         for(var yPos:uint=0;yPos<oam.height;yPos+=Tile.height) {
        #             for(var xPos:uint=0;xPos<oam.width;xPos+=Tile.width) {
        #                 var tile:Tile=new Tile();
                        
        #                 for(var tileYPos:uint=0;tileYPos<Tile.height;++tileYPos) {
        #                     for(var tileXPos:uint=0;tileXPos<Tile.width;++tileXPos) {
                                
        #                         var tileOffset:uint=tileYPos*Tile.width+tileXPos;
        #                         var pixelsOffset:uint=(yPos*Tile.height+tileYPos)*Tile.width+(xPos*Tile.width+tileXPos);
                                
        #                         tile.pixels[tileOffset]=tilePixels[pixelsOffset];
        #                     }
        #                 }
                        
        #                 t.push(tile);
        #             }
        #         }
        #     }
        #     tiles=t;
        #     picture=null;
            
        #     tilesX=0xFFFF;
        #     tilesY=0xFFFF;
            
        #     return map;
        # }
        
        # private function buildPicture(oamPixels:Vector.<Vector.<uint>>,oams:Vector.<OamTile>):Object {
        #     var pixels:Vector.<uint>=new Vector.<uint>;
        #     var map:Object={};
            
        #     for(var i:uint=0;i<oams.length;++i) {
        #         var oam:OamTile=oams[i];
        #         var tilePixels:Vector.<uint>=oamPixels[i];
                
        #         var tileIndex:uint=pixels.length/(Tile.width*Tile.height);
        #         pixels=pixels.concat(tilePixels);
        #         map[oam.tileIndex]=tileIndex;
        #         oam.tileIndex=tileIndex;
        #     }
            
        #     picture=pixels;
        #     tiles=null;
            
        #     tilesX=0xFFFF;
        #     tilesY=0xFFFF;
            
        #     return map;
        # }
        
        
        
        # /** Renders the full bank as one big picture
        # @param palette The palette to use when rendering, in RGB888 format
        # @param paletteIndex The subpalette index to use
        # @param useTransparency If the tiles should be rendered using transparency
        # @return A new DisplayObject that represents the bank
        # */
        # public function render(palette:Vector.<uint>,paletteIndex:uint=0,useTransparency:Boolean=true):DisplayObject {
        #     var x:uint;
        #     var y:uint;
        #     var index:uint;
        #     var bmd:BitmapData;
            
        #     if(tiles) {
            
        #         var spr:Sprite=new Sprite();
        #         for(y=0;y<tilesY;++y) {
        #             for(x=0;x<tilesX;++x) {
        #                 index=x+y*tilesX;
        #                 var tile:Tile=tiles[index];
                        
        #                 bmd=tile.toBMD(palette,paletteIndex,useTransparency);
        #                 var bitmap:Bitmap=new Bitmap(bmd);
        #                 bitmap.x=x*Tile.width;
        #                 bitmap.y=y*Tile.height;
                        
        #                 spr.addChild(bitmap);
        #             }
        #         }
        #         return spr;
        #     } else {
        #         const w:uint=tilesX*Tile.width;
        #         const h:uint=tilesY*Tile.height;
        #         bmd=new BitmapData(w,h,useTransparency);
        #         bmd.lock();
                
        #         for(y=0;y<h;++y) {
        #             for(x=0;x<w;++x) {
        #                 var color:uint=picture[x+y*w];
        #                 if(color==0 && useTransparency) {
        #                     bmd.setPixel32(x,y,0x00FFF00F);
        #                 } else {
        #                     color=palette[color+paletteIndex*16];
        #                     bmd.setPixel(x,y,color);
        #                 }
        #             }
        #         }
                
        #         bmd.unlock();
                
        #         return new Bitmap(bmd);
        #     }
        # }
        
        # /** If the bank file can be renderd without a NCER file */
        # public function get independentRenderPossible():Boolean {
        #     return tiles && tilesX!=0xFFFF && tilesY!=0xFFFF;
        # }
        
        # internal function loadTiles(ts:Vector.<Tile>,tx:uint,ty:uint):void {
        #     tiles=ts;
        #     tilesX=tx;
        #     tilesY=ty;
        # }


# Ported from https://app.assembla.com/spaces/sdat4as/subversion/source/HEAD/Nitro/Graphics/OamTile.as
# A basic tile group that can be used for storing just the data about the tile in genera
class OamTile(object):

    # The sub palette index to use for rendering the tiles
    paletteIndex = None
    # The start index of the tiles in the associated GraphicsBank
    tileIndex = None
    colorDepth = None

    # The width of the tile group, in pixels
    width = None
    # The height of the tile group, in pixels
    height = None


    # /** Rends the tile group accordingly to the settings
    # @param palette The RGB888 palette to use when rendering the tiles
    # @param tiles The tiles pixel data to use
    # @param useSubImages If sub image addressing should be used
    # @param useTransparency If the tiles should be rendered using transparency
    # @return A DisplayObject that represents the tile group
    # */
    def rend(self, palette,tiles,useSubImages,useTranparency):
        oamR=tiles.renderOam(self,palette,useSubImages,useTranparency)
        return oamR

    # /** Draws a rectangle that represents the OAM
    # @param boxColor The stroke color for the rectangle
    # @param useFill If the rectangle should be filled
    # @param tileNumbers If the tile number should be displayed
    # @return A DisplayObject that contains the drawn rectangle*/
    # public function drawBox(boxColor:uint=0,useFill:Boolean=true,tileNumbers:Boolean=true):DisplayObject {
        
    #     var spr:Sprite=new Sprite();
    #     spr.graphics.lineStyle(1,boxColor);
        
    #     if(useFill) {
    #         spr.graphics.beginFill(0xFFFFFF);
    #     }            
    #     spr.graphics.drawRect(0,0,width,height);
    #     if(useFill) {
    #         spr.graphics.endFill();
    #     }
        
        
    #     if(tileNumbers) {
    #         addTileNumber(spr);
    #     }
    #     return spr;
    # }
    
    # protected function addTileNumber(spr:Sprite):void {
    #     var tf:TextField=new TextField();
    #     tf.autoSize=TextFieldAutoSize.LEFT;
    #     tf.selectable=false;
    #     tf.text=String(tileIndex);
        
    #     spr.addChild(tf);
    # }

    def setSize(self, size,shape):
        if shape == 0:
            self.height=8 << size
            self.width=self.height
        elif shape == 1:
            self.width=[16,32,32,64][size]
            self.height=[8,8,16,32][size]
        elif shape == 2:
            self.width=[8,8,16,32][size]
            self.height=[16,32,32,64][size]

    # internal function getSize():uint {
    #     switch(width) {
    #         case 8:
    #             switch(height) {
    #                 case 8: return 0;
    #                 case 16: return 0;
    #                 case 32: return 1;
    #             }
    #         break;
            
    #         case 16:
    #             switch(height) {
    #                 case 16: return 1;
    #                 case 8: return 0;
    #                 case 32: return 2;
    #             }
    #         break;
            
    #         case 32:
    #             switch(height) {
    #                 case 32: return 2;
    #                 case 8: return 1;
    #                 case 16: return 2;
    #                 case 64: return 3;
    #             }
    #         break;
            
    #         case 64:
    #             switch(height) {
    #                 case 64: return 3;
    #                 case 32: return 3;
    #             }
    #         break;
    #     }
    #     throw new Error("invalid h/w combo");
    # }
    
    # public function cloneOamTile():OamTile {
    #     var o:OamTile=new OamTile();
    #     o.paletteIndex=paletteIndex;
    #     o.tileIndex=tileIndex;
    #     o.width=width;
    #     o.height=height;
    #     return o;
    # }
