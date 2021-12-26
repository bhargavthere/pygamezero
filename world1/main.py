import pgzrun
import random

HEIGHT = 1000
WIDTH = 1800

def toss(percent):
    num = random.randint(1,100)
    return(num < percent)
  
class lt(Actor):
  list = []
  id = 0
  update_cycle = 0
  mowcycle = 0

  def __init__(self,imagefile,maxage,minage,maxspeed, minspeed,name):
    Actor.__init__(self,imagefile)
    type(self).list.append(self)
    self.myidx = type(self).id
    self.birth_cycle = 0
    self.minage = minage
    self.maxage = maxage
    self.minspeed = minspeed
    self.maxspeed = maxspeed
    self.agetodie = random.randint(minage,maxage)
    self.xspeed = random.randint(minspeed,maxspeed)
    self.yspeed = random.randint(minspeed,maxspeed)
    self.xfwd = True
    self.yfwd = True
    self.x = random.randint(10,WIDTH-10)
    self.y = random.randint(10,HEIGHT-10)
    self.name = name
    self.alive = True
    type(self).id = type(self).id + 1

  def move(self):
    
    if(self.xfwd):
      self.x = self.x + self.xspeed
    else:
      self.x = self.x - self.xspeed

    if(self.x > WIDTH):
      self.xfwd = False
    elif (self.x < 0):
      self.xfwd = True
    
    if(self.yfwd):
      self.y = self.y + self.yspeed
    else:
      self.y = self.y - self.yspeed

    if(self.y > HEIGHT):
      self.yfwd = False
    elif (self.y < 0):
      self.yfwd = True

    
  def death_schedule(self):
    #self.agetodie = self.agetodie - 1
    #if (self.agetodie == 0):
    #  self.image = ('dead.png')
    #elif (self.agetodie < -5):
    self.alive = False
    if self in type(self).list:
      type(self).list.remove(self)

  def ltdraw():
    for t in lt.list:
      t.draw()

  def ltupdate():
    list_tree = []
    list_nontree = []
    lt.update_cycle = lt.update_cycle + 1
    mowerAlive = False
    
    for t in lt.list:
      t.move()
      if(t.name == 'tree'):
        list_tree.append(t)
      else:
        if(t.name == 'mower'):
          mowerH = t
          mowerAlive = True
        list_nontree.append(t)

    curr_population = len(list_nontree)
    
    if ((curr_population > 27) and not mowerAlive):
      lt('lawnmower.jpeg',1000,750,7,3,'mower')
      lt.mowcycle = lt.update_cycle

    if (mowerAlive):
        if(lt.mowcycle < (lt.update_cycle - 1000 )):
            mowerH.death_schedule()
      
    for nt in list_nontree:
      if(nt.collidelist(list_tree) != -1):
        nt.xfwd = not nt.xfwd
        nt.yfwd = not nt.yfwd
        music.play('muic.wav')
        
      collidedlist = nt.collidelistall(list_nontree)
      for cidx in collidedlist:
        ont = list_nontree[cidx]
        if((nt.name == 'elephant') and (nt.myidx != ont.myidx)):
          if(ont.name == 'gorilla'): #Elephant collides with Gorilla fifty fifty chance
              if (toss(50)):
                  ont.death_schedule()
           #nt.xfwd = not nt.xfwd
           #nt.yfwd = not nt.yfwd
            #ont.xfwd = not ont.xfwd
            #ont.yfwd = not ont.yfwd
          elif(ont.name == 'mower'):
              nt.death_schedule()
          elif((ont.name == 'frog1') or (ont.name == 'frog2')):
            if(toss(50)): #50% chance Elephant wins
              ont.death_schedule()
            else:
              nt.death_schedule()
          elif(ont.name == 'snake'):
            if(toss(50)): #50% chance Elephant wins
              ont.death_schedule()
            else:
              nt.death_schedule()
          elif(ont.name == 'elephant'): #Elephant meets Elephant
            if(toss(5)): #Spawn new elephant 5% of time
                if(nt.birth_cycle < (lt.update_cycle - 100)):
                  nt.birth_cycle = lt.update_cycle
                  lt(nt.image,nt.maxage,nt.minage,nt.maxspeed,nt.minspeed,nt.name)
              
        if((nt.name == 'gorilla') and (nt.myidx != ont.myidx)):
          if((ont.name == 'frog1') or (ont.name == 'frog2')):
            if(toss(50)): #50% chance Gorilla wins
              ont.death_schedule()
            else:
              nt.death_schedule()
          elif(ont.name == 'snake'):
            if(toss(50)): #50% chance Gorilla wins
              ont.death_schedule()
            else:
              nt.death_schedule()
          elif(ont.name == 'gorilla'): #Gorilla meets Gorilla
            if(toss(5)): #Spawn new gorilla 5% of time
              if(nt.birth_cycle < (lt.update_cycle - 100)):
                nt.birth_cycle = lt.update_cycle
                lt(nt.image,nt.maxage,nt.minage,nt.maxspeed,nt.minspeed,nt.name)
          elif(ont.name == 'mower'):
              nt.death_schedule()
                     
        if((nt.name == 'snake') and (nt.myidx != ont.myidx)):
          if((ont.name == 'frog1') or (ont.name == 'frog2')):
            if(toss(50)): #50% chance snake wins
              ont.death_schedule()
            else:
              nt.death_schedule()
          elif(ont.name == 'snake'): #snake meets snake
            if(toss(2.5)): #Spawn new snake 2.5% of time
              if(nt.birth_cycle < (lt.update_cycle - 100)):
                nt.birth_cycle = lt.update_cycle
                lt(nt.image,nt.maxage,nt.minage,nt.maxspeed,nt.minspeed,nt.name)
          elif(ont.name == 'mower'):
              nt.death_schedule()
                            
        if(((nt.name == 'frog1') or (nt.name == 'frog2')) and (nt.myidx != ont.myidx)):
          if((ont.name == 'frog1') or (ont.name == 'frog2')):
            if(toss(5)): #Spawn new frog 5% of time
              if(nt.birth_cycle < (lt.update_cycle - 100)):
                nt.birth_cycle = lt.update_cycle
                lt(nt.image,nt.maxage,nt.minage,nt.maxspeed,nt.minspeed,nt.name)
          elif(ont.name == 'mower'):
              nt.death_schedule()
                        
        
      
lt('elephant.jpg',1000,500,3,1,'elephant')
lt('elephant.jpg',1000,500,3,1,'elephant')
lt('elephant.jpg',1000,500,3,1,'elephant')
lt('elephant.jpg',1000,500,3,1,'elephant')
lt('elephant.jpg',1000,500,3,1,'elephant')
lt('elephant.jpg',1000,500,3,1,'elephant')
lt('elephant.jpg',1000,500,3,1,'elephant')
lt('elephant.jpg',1000,500,3,1,'elephant')
lt('frog1.jpeg',1000,500,3,1,'frog1')
lt('frog2.jpeg',1000,500,3,1,'frog2')
lt('frog1.jpeg',1000,500,3,1,'frog1')
lt('frog2.jpeg',1000,500,3,1,'frog2')
lt('frog1.jpeg',1000,500,3,1,'frog1')
lt('frog2.jpeg',1000,500,3,1,'frog2')
lt('frog1.jpeg',1000,500,3,1,'frog1')
lt('frog2.jpeg',1000,500,3,1,'frog2')
lt('gorilla.jpg',1000,500,3,1,'gorilla')
lt('gorilla.jpg',1000,500,3,1,'gorilla')
lt('gorilla.jpg',1000,500,3,1,'gorilla')
lt('gorilla.jpg',1000,500,3,1,'gorilla')
lt('gorilla.jpg',1000,500,3,1,'gorilla')
lt('gorilla.jpg',1000,500,3,1,'gorilla')
lt('gorilla.jpg',1000,500,3,1,'gorilla')
lt('gorilla.jpg',1000,500,3,1,'gorilla')
lt('snake.jpg',1000,500,3,1,'snake')
lt('snake.jpg',1000,500,3,1,'snake')
lt('snake.jpg',1000,500,3,1,'snake')
lt('snake.jpg',1000,500,3,1,'snake')
lt('snake.jpg',1000,500,3,1,'snake')
lt('snake.jpg',1000,500,3,1,'snake')
lt('snake.jpg',1000,500,3,1,'snake')
lt('snake.jpg',1000,500,3,1,'snake')
lt('tree.jpeg',1000,500,0,0,'tree')
lt('tree.jpeg',1000,500,0,0,'tree')
#lt('tree.jpeg',1000,500,0,0,'tree')
#lt('tree.jpeg',1000,500,0,0,'tree')
#lt('tree.jpeg',1000,500,0,0,'tree')



def draw():
  screen.blit('bround.jpg', (0,0))
  lt.ltdraw()

def update():
  lt.ltupdate()


pgzrun.go()
