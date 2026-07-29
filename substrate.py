CHOSEN_PALETTE = "paleamethyst" 
speed_int = 3
TARGET_FPS = 120 
CRACK_COL = (125, 137, 159, 85) #(0, 0, 0, 85)

import os
import datetime
savedir = datetime.datetime.now().strftime("%H%M%S") 
os.makedirs(savedir) 
ssid = 0 

# Substrate Watercolor
# j.tarbell   June, 2004
# Albuquerque, New Mexico
# complexification.net

# Processing 0085 Beta syntax update
# j.tarbell   April, 2005

import numpy as np
import math
import random 
PI = math.pi 

WIDTH = dimx = 1000;
HEIGHT = dimy = 500;
num = 0;
maxnum = 100;

cracks = []; # list of Cracks 
sands = []; # SandPainters

occupied = []


from palettes import PALETTES 




# UTILS
def point(x, y, rgba):
  # in p5js it's like stroke(*strokeparams) but there's 2? 
  ''' pygame.draw.circle(
    screen,
    rgba,
    (int(x), int(y)),
    1
  )'''
  #screen.set_at((int(x), int(y)), rgba)
  #pygame.gfxdraw.pixel(screen, int(x), int(y), rgba)
  point = pygame.Surface((1, 1), pygame.SRCALPHA)
  point.fill(rgba)
  screen.blit(point, (x, y))



def makeCrack() :
  global num 
  if (num<maxnum): 
    # make a new crack instance
    cracks.append(Crack())
    num+= 1;

def begin() :
  global grid
  global occupied
  global num 
  # erase crack grid
  '''for (int y=0;y<dimy;y++) {
    for (int x=0;x<dimx;x++) {
      grid[y,x] = 10001;
    }
  }'''

  grid = np.full((HEIGHT, WIDTH), 10001, dtype=np.int16)
  occupied = [] 
  
  # make random crack seeds
  for k in range(16): 
    i = random.randrange(dimx*dimy-1)
    y = i//dimx
    x = i%dimx 
    grid[y,x]=random.randrange(360)
    occupied.append((y,x))
  

  # make just three cracks
  num=0
  for _ in range(3): 
    makeCrack()
  
  screen.fill((255,255,255, 255))


def somecolor() :
  # pick some random good color
  return random.choice(palette)

# CLASSES 
class Crack :
    
  def __init__(self):
    # find placement along existing crack
    #print("NEW CRACK") 
    self.findStart()
    #print("FOUND START") 
    self.sp = SandPainter()
  
  
  def findStart(self) :
    # pick random point
    px=0;
    py=0;

    yx = random.choice(occupied)
    a = int(grid[yx[0], yx[1]])
    if (random.random()<0.5) :
      a-=90+random.randint(-2,2);
    else :
      a+=90+random.randint(-2,2);
    
    self.startCrack(yx[1], yx[0], a)
    #return 

    '''
    # shift until crack is found
    found=False;
    timeout = 0;
    while ((not found) or (timeout>1000)) :
      #print("a")
      timeout += 1 
      px = random.randrange(dimx);
      py = random.randrange(dimy);
      if (grid[py,px]<10000) :
        found=True;
      
    
    
    if (found) :
      # start crack
      a = grid[py,px];
      if (random.rand()<0.5) :
        a-=90+random.randint(-2,2);
      else :
        a+=90+random.randint(-2,2);
      
      self.startCrack(px,py,a);
    else:
      print("TIMEOUT FINDING START") 
    #else {
      #println("timeout: "+timeout);
    ''' 
   
  def startCrack(self, X:int, Y:int, T:int) :
    self.x = X
    self.y = Y
    self.t = T 
    self.x+=0.61*math.cos(T*math.pi/180);
    self.y+=0.61*math.sin(T*math.pi/180);  
  
             
  def move(self) :
    #print("MOVING CRACK")
    # continue cracking
    self.x+=0.42*math.cos(self.t*math.pi/180);
    self.y+=0.42*math.sin(self.t*math.pi/180); 
    
    # bound check
    z = 0.33;
    cx = round(self.x+random.uniform(-z,z));  # add fuzz
    cy = round(self.y+random.uniform(-z,z));
    
    # draw sand painter
    self.regionColor();
    
    # draw black crack
    point(self.x+random.uniform(-z,z),self.y+random.uniform(-z,z), CRACK_COL)     
    
    if ((cx>=0) and (cx<dimx) and (cy>=0) and (cy<dimy)) :
      # safe to check
      if ((grid[cy,cx]>10000) or (abs(grid[cy,cx]-self.t)<5)) :
        # continue cracking
        grid[cy,cx]=self.t;
        occupied.append((cy,cx))
      elif (abs(grid[cy,cx]-self.t)>2) :
        # crack encountered (not self), stop cracking
        self.findStart();
        makeCrack();
      
    else :
      # out of bounds, stop cracking
      self.findStart();
      makeCrack();
    
  
  
  def regionColor(self) :
    # start checking one step away
    rx=self.x;
    ry=self.y;
    openspace=True;
    
    # find extents of open space
    while (openspace) :
      # move perpendicular to crack
      rx+=0.81*math.sin(self.t*math.pi/180);
      ry-=0.81*math.cos(self.t*math.pi/180);
      cx = int(rx);
      cy = int(ry);
      if ((cx>=0) and (cx<dimx) and (cy>=0) and (cy<dimy)) :
        # safe to check
        if (grid[cy,cx]>10000) :
          pass # space is open
        else :
          openspace=False;

      else :
        openspace=False;
      
    
    # draw sand painter
    self.sp.render(rx,ry,self.x,self.y);

class SandPainter :

  #color c;
  #float g;

  def __init__(self):

    self.cr, self.cg, self.cb = somecolor();
    self.g = random.uniform(0.01,0.1);
  
  def render(self, x:float, y:float, ox:float, oy:float):
    # modulate gain
    self.g+=random.uniform(-0.050,0.050);
    maxg = 1.0;
    if (self.g<0): self.g=0.0;
    if (self.g>maxg): self.g=maxg;
    
    # calculate grains by distance
    #int grains = int(sqrt((ox-x)*(ox-x)+(oy-y)*(oy-y)));
    grains = 64;

    # lay down grains of sand (transparent pixels)
    w = self.g/(grains-1);
    for i in range(grains):
      a = 0.1-i/(grains*10.0);
      rgba = (self.cr, self.cg, self.cb,int(a*256))
      point(ox+(x-ox)*math.sin(math.sin(i*w)), oy+(y-oy)*math.sin(math.sin(i*w)), rgba)




# MAIN METHODS ---------------------------------------------
import pygame

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

screen.fill((255,255,255, 255))
grid = np.full((HEIGHT, WIDTH), 10001, dtype=np.int16)

#cracks = [None for _ in range(maxnum)] 

palette = PALETTES[CHOSEN_PALETTE]

begin() 



running = True
while running:

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    elif event.type == pygame.KEYDOWN:
      if event.key == pygame.K_s:
        pygame.image.save(screen, savedir+"/{:03d}.png".format(ssid))
        ssid += 1

  for _ in range(speed_int): 
    # update cracks
    for crack in cracks:
      if crack is not None:
        crack.move()

  pygame.display.flip()
  clock.tick(TARGET_FPS)

pygame.quit()







# j.tarbell   June, 2004
# Albuquerque, New Mexico
# complexification.net
