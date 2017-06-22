from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.graphics import Color
from kivy.graphics.vertex_instructions import Rectangle

from random import random,randint,choice
import time
import caves

DIR  = { 'UP': 0, 'UPRIGHT': 1, 'RIGHT': 2, 'DOWNRIGHT': 3, 'DOWN': 4, 'DOWNLEFT': 5, 'LEFT': 6, 'UPLEFT': 7 }
DIRX = [     0,          1,        1,            1,       0,          -1,      -1,        -1 ]
DIRY = [    -1,         -1,        0,            1,       1,           1,       0,        -1 ]

class TextureDict():
  def __init__(self,**kwargs):
    super(TextureDict,self).__init__(**kwargs)
    self.texture_dict = {}
    self.names = []
  
  def load_textures(self,filename):
    filename = filename + '.atlas'
    with open(filename) as f:
      k=f.readline()
      k=f.readline()
      for k in f.readlines():
        self.names.append(k[:k.find(':')].lstrip()[1:-1])
        self.texture_dict[self.names[-1]] = Image()
        self.texture_dict[self.names[-1]].source = 'atlas://'+filename+'/' + self.names[-1]

Textures = TextureDict()
Textures.load_textures('sprites1')

CAVES = {}

class Anim():
  def __init__(self,name,frames,fps):
    self.name = name
    self.frames = frames
    self.fps = fps
    self.reverse = reverse   #Si es True, la animacion llega al final, y se devuelve hasta el principio (ej: 1,2,3,4,3,2,1)

  def getSprite(self):
    now = time.time()
    fpstime = now-int(now)
    frame = int(self.fps * fpstime % len(self.frames))
    return Textures.texture_dict[self.name + frame]

class Sprite():
  def __init__(self,code,rounded,explodable,consumable,sprite,anims={}):
    #self.name = name
    self.code = code
    self.rounded = rounded
    self.explodable = explodable
    self.consumable = consumable
    self.sprite = sprite
    self.anims = anims
    self.flash = None

  def getSprite(self,anim=''):
    if self.anims == {}:
      return Textures.texture_dict[self.sprite]
    else:
      return self.anims[anim].getSprite()


class SpriteDict():
  def __init__(self):
    self.sprite_dict = {}

  def load_sprites(self):
    self.sprite_dict['space']=Sprite(code=0x00,rounded=False,explodable=False,consumable=True,sprite='space')
    self.sprite_dict['space'].flash = 'flash'
    self.sprite_dict['dirt']=Sprite(code= 0x01,rounded=False,explodable=False,consumable=True,sprite='dirt')
    self.sprite_dict['brickwall']=Sprite(code= 0x02,rounded= True,explodable=False,consumable=True,sprite='brickwall')
    self.sprite_dict['magicwall']=Sprite(code= 0x03,rounded=False,explodable=False,consumable=True,sprite='magicwall0',anims={'magicwall':Anim('magicwall',4,20)})
    self.sprite_dict['preoutbox']=Sprite(code= 0x04,rounded=False,explodable=False,consumable=False,sprite='prerf0')
    self.sprite_dict['outbox']=Sprite(code= 0x05,rounded= False,explodable=False,consumable=False,sprite='prerf0',anims={'prerf':Anim('prerf',2,4)})
    self.sprite_dict['steelwall']=Sprite(code= 0x07,rounded=False,explodable=False,consumable=False,sprite='prerf1')
    self.sprite_dict['firefly1']=Sprite(code= 0x08,rounded=False,explodable=True,consumable=True,sprite='firefly0',anims={'firefly':Anim('firefly',8,20)})
    self.sprite_dict['firefly2']=Sprite(code= 0x09,rounded=False,explodable=True,consumable=True,sprite='firefly0',anims={'firefly':Anim('firefly',8,20)})
    self.sprite_dict['firefly3']=Sprite(code= 0x0A,rounded=False,explodable=True,consumable=True,sprite='firefly0',anims={'firefly':Anim('firefly',8,20)})
    self.sprite_dict['firefly4']=Sprite(code= 0x0B,rounded=False,explodable=True,consumable=True,sprite='firefly0',anims={'firefly':Anim('firefly',8,20)})
    self.sprite_dict['boulder']=Sprite(code= 0x10,rounded=True,explodable=False,consumable=True,sprite='boulder')
    self.sprite_dict['boulderfalling']=Sprite(code= 0x12,rounded=False,explodable=True,consumable=True,sprite='boulder')
    self.sprite_dict['diamond']=Sprite(code= 0x14,rounded=True,explodable=False,consumable=True,sprite='diamond0',anims={'diamond':Anim('diamond',8,20)})
    self.sprite_dict['diamondfalling']=Sprite(code=0x16,rounded=False,explodable=False,consumable=True,sprite='diamond0',anims={'diamond':Anim('diamond',8,20)})
    self.sprite_dict['explodetospace0']=Sprite(code=0x1B,rounded=False,explodable=False,consumable=False,sprite='dexplode1')
    self.sprite_dict['explodetospace1']=Sprite(code=0x1C,rounded=False,explodable=False,consumable=False,sprite='dexplode2')
    self.sprite_dict['explodetospace2']=Sprite(code=0x1D,rounded=False,explodable=False,consumable=False,sprite='dexplode3')
    self.sprite_dict['explodetospace3']=Sprite(code=0x1E,rounded=False,explodable=False,consumable=False,sprite='dexplode2')
    self.sprite_dict['explodetospace4']=Sprite(code=0x1F,rounded=False,explodable=False,consumable=False,sprite='dexplode1')
    self.sprite_dict['explodetodiamond0']=Sprite(code=0x20,rounded=False,explodable=False,consumable=False,sprite='dexplode1')
    self.sprite_dict['explodetodiamond1']=Sprite(code=0x21,rounded=False,explodable=False,consumable=False,sprite='dexplode2')
    self.sprite_dict['explodetodiamond2']=Sprite(code=0x22,rounded=False,explodable=False,consumable=False,sprite='dexplode3')
    self.sprite_dict['explodetodiamond3']=Sprite(code=0x23,rounded=False,explodable=False,consumable=False,sprite='dexplode2')
    self.sprite_dict['explodetodiamond4']=Sprite(code=0x24,rounded=False,explodable=False,consumable=False,sprite='dexplode1')
    self.sprite_dict['prerockford1']=Sprite(code=0x25,rounded=False,explodable=False,consumable=False,sprite='prerf0',anims={'prerf':Anim('prerf',2,4)})
    self.sprite_dict['prerockford2']=Sprite(code=0x26,rounded=False,explodable=False,consumable=False,sprite='rfexp0')
    self.sprite_dict['prerockford3']=Sprite(code=0x27,rounded=False,explodable=False,consumable=False,sprite='rfexp1')
    self.sprite_dict['prerockford4']=Sprite(code=0x28,rounded=False,explodable=False,consumable=False,sprite='rfexp2')
    self.sprite_dict['butterfly1']=Sprite(code=0x30,rounded=False,explodable=True,consumable=True,sprite='butterfly0',anims={'butterfly':Anim('butterfly',8,20)})
    self.sprite_dict['butterfly2']=Sprite(code=0x31,rounded=False,explodable=True,consumable=True,sprite='butterfly0',anims={'butterfly':Anim('butterfly',8,20)})
    self.sprite_dict['butterfly3']=Sprite(code=0x32,rounded=False,explodable=True,consumable=True,sprite='butterfly0',anims={'butterfly':Anim('butterfly',8,20)})
    self.sprite_dict['butterfly4']=Sprite(code=0x33,rounded=False,explodable=True,consumable=True,sprite='butterfly0',anims={'butterfly':Anim('butterfly',8,20)})
    rleft = Anim('rleft',8,20)
    rright=Anim('rright',8,20)
    blink=Anim('blink',8,20)
    tap=Anim('tap',8,20)
    blinktap=Anim('blinktap',8,20)
    myanims = {'rleft':rleft,'rright':rright,'blink':blink,'tap':tap,'blinktap':blinktap}
    self.sprite_dict['rockford']=Sprite(code=0x38,rounded=False,explodable=True,consumable=True,sprite='stand',anims=myanims)
    self.sprite_dict['amoeba']=Sprite(code=0x3A,rounded=False,explodable=False,consumable=True,sprite='amoeba0',anims={'amoeba':Anim('amoeba',8,20)})

class Cave():
  def __init__(self):
    self.caves = Caves()

  def set_cave(self,width,height,cells,fps,caveTime,diamondsNeeded,initialDiamondValue,extraDiamondValue,amoebaMaxSize,
               amoebaSlowGrowthTime,magicWallMillingTime):
    self.width = width
    self.height = height
    self.cells = cells
    self.frame = 0
    self.fps = fps
    self.step = 1/self.fps
    self.timer    = caveTime                 # seconds allowed to complete this cave
    self.flash    = False;                   # trigger white flash when rockford has collected enought diamonds
    self.won      = False;                   # set to true when rockford enters the outbox
    self.diamonds = {
      'collected': 0,                                # how many diamonds collected so far
      'needed': diamondsNeeded,                 # how many diamonds needed to exit the cave
      'value':  initialDiamondValue,            # how many points for each required diamond
      'extra':  extraDiamondValue}               # how many points for each additional diamond
    self.amoeba = {
      'max': amoebaMaxSize,                     # how large can amoeba grow before it turns to boulders
      'slow': amoebaSlowGrowthTime/this.step}    # how long before amoeba growth rate speeds up
    self.magic = {
      'active': False,                               # are magic walls active
      'time': magicWallMillingTime/this.step }  # how long do magic walls stay active
    for y in range(self.height):
      self.cells.append([])
      for x in range(self.width):
        self.cells[y].append(self.sprite_dict[cave.map[x][y]], {'frame': 0, 'p': Point(x,y)})

  def Point(self,x, y, dir):
    x = x + (DIRX[dir])
    y = y + (DIRY[dir])
    return (x,y)

class Game():
  def __init__(self):
    self.cave = Cave()
    self.cells = self.cave.cells

  def get(self,p,dir):
    return self.cells[p.x + (DIRX[dir])][p.y + (DIRY[dir])]['object']

  def eachCell(self,fn,thisArg):
    for y in range(self.cave.height):
      for x in range(self.cave.width):
        fn(thisArg)

class MyWidget(Widget):
  def __init__(self):
    super(MyWidget, self).__init__()
    self.spritesize = 32,32
    self.cols,self.rows = 20,11
    self.size = self.spritesize[0]*self.cols,self.spritesize[1]*self.rows
    self.sprites = SpriteDict()
    self.sprites.load_sprites()
    #self.myimage.size = self.size
    #self.add_widget(self.myimage)
    i=0
    mycolor = [random(),random(),random(),1]
    for row in range(self.rows):
      for col in range(self.cols):
        position = (col*self.spritesize[0],(self.rows-row-1)*self.spritesize[1])
        mytexture = self.sprites.sprite_dict['dirt'].getSprite().texture
        with self.canvas:
          Color(*mycolor)
          Rectangle(pos=position,size=self.spritesize,texture=mytexture)
        i+=1

  

class BoulderKivyApp(App):
  def build(self):
    widg = MyWidget()
    Window.size = widg.size
    return widg

if __name__ == "__main__":
  BoulderKivyApp().run()