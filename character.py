#Character Classes 

#The Character is the minimal Tile Unit in the Game

from kivy.uix.image import Image

class ColorDict():
  #Diccionario de Colores
  def __init__(self,**kwargs):
    self.color_dict = {}

  def load_colors(self,filename):
    with open(filename) as f:
      seq = f.readlines()
      seq = [s.strip() for s in seq]
      for line in seq:
        line_list = [i for i in line.split(',')]
        if line_list[0][0] != '#':
          name = line_list[0]
          r = hex((int(line_list[1],16)&0xFF0000)>>16
          g = hex((int(line_list[1],16)&0x00FF00)>>8
          b = hex((int(line_list[1],16)&0x0000FF))
          a = float(1.0)
          print(name+str(r)+','+str(g)+','+str(b))
          self.color_dict[name] = [r,g,b,a]  
          
  def save_color(self,filename):
    for name in self.color_dict:
      r = str(color_dict[name][0])
      g = str(color_dict[name][1])
      b = str(color_dict[name][2])
      a = str(color_dict[name][3])
      seq += name + ',' + r + ',' + g + ',' + b + ',' + a + '\n'    
    with open(filename,'w') as f: 
      f.write(seq)

Colors = ColorDict()
Colors.load_colors('colors.def')

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

class Anim():
  def __init__(self,name,frames,fps):
    self.name = name
    self.frames = frames
    self.fps = fps

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

Sprites = SpriteDict()
Sprites.load_sprites()
