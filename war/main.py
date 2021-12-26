import pgzrun
import random
import math
import enum 

HEIGHT = 540
WIDTH = 960
state = 0
player1_artillery_units = []
player1_soldier_units = []
player2_artillery_units = []
player2_soldier_units = []
player1_castle = None
player2_castle = None
launcher = None

class TypeOfArtillery(enum.Enum):
    ARCHER  = 0
    CANNON = 1
    CATAPULT = 2
    GUN = 3
    BOMBER = 4
    TANK = 5
    MISSILE_LAUNCHER = 6

class TypeOfSoldierUnit(enum.Enum):
    CAVALRY = 0
    KING = 1
    KNIGHT = 2
    MODERN_SOLDIER = 3
    SPEARMEN = 4
    SWORDMEN = 5

class Projectile(Actor):
    waypoints = []
    List = []
    damage = 0

    def __init__(self, startpos, endpos, firerange, damage):
        x1,y1 = startpos
        xn,yn = endpos
        self.damage = damage
        rangenotenough = False
        if (xn == x1):
            m = 50
        else:
            m = (yn - y1)/(xn - x1)
        if (xn > x1):
            dx = 5
        else:
            dx = -5
        c = y1 - m*x1
        self.waypoints.append((int(x1),int(y1)))
        cx = x1
        cy = y1
        while (((cy - yn)*(cy - yn)) > (dx*dx*m*m)):
            cx = int(cx + dx)
            cy = int(m*cx + c)
            dist2 = ((cx - x1)**2 + (cy - y1)**2)
            firer2 = ((firerange*60)**2)
            if (dist2 < firer2):
                self.waypoints.append((cx,cy))
            else:
                rangenotenough = True
                break
        if(not rangenotenough):       
            self.waypoints.append((int(xn),int(yn)))
        Actor.__init__(self,'artillery/cannonball.png',topleft = (int(x1),int(y1)))
        Projectile.List.append(self)

    def update(self):
        if(len(self.waypoints)==0):        
            Projectile.List.remove(self)
            for u in (player1_artillery_units + player2_artillery_units + player1_soldier_units + player2_soldier_units):
                for e in u.list:
                  if (self.distance_to(e) < 60):
                      e.durability -= self.damage
                      if (e.durability < 0):
                          u.list.remove(e)
                          del (e)
            del(self)
                
        else:
            if(len(self.waypoints)<=2):
                self.image = 'artillery/explosion.gif'
            self.pos = self.waypoints[0]
            del self.waypoints[0]

class Artillery(Actor):

    damage = 0
    mobility = 0
    firerange = 0
    high_ground_bonus = 0
    castle_bonus = 0
    battlement_bonus = 0
    durability = 0
    the_chosen_one = False
    running_mobility = 0
    my_type = 0
    image_folder = "small icons"
    List = []
         
    def __init__(self,damage,mobility,firerange,high_ground_bonus,castle_bonus,battlement_bonus,durability,imagefile):
        self.damage = damage
        self.mobility = mobility
        self.firerange = firerange
        self.high_ground_bonus = high_ground_bonus
        self.castle_bonus = castle_bonus
        self.battlement_bonus = battlement_bonus
        self.durability = durability
        self.the_chosen_one = False
        self.imagefile = imagefile
        self.running_mobility = 0
        filename = str(self.image_folder) + str("/") + str(imagefile)
        Actor.__init__(self,filename)
        Artillery.List.append(self)

    def draw(self):
        Actor.draw(self)
        if (self.the_chosen_one):
            screen.draw.filled_circle(self.pos, 5,(255, 0, 0))

class Soldier(Actor):

  image_folder = "small icons"
  damage = 0
  mobility = 0
  durability = 0
  my_type = 1
  the_chosen_one = False
  running_mobility = 0
  List = []
         
  def __init__(self,damage,mobility,durability,imagefile):
        self.damage = damage
        self.mobility = mobility
        self.durability = durability
        self.the_chosen_one = False
        self.running_mobility = 0
        filename = str(self.image_folder) + str("/") + str(imagefile)
        Actor.__init__(self,filename)
        Soldier.List.append(self)

  def draw(self):
      Actor.draw(self)
      if (self.the_chosen_one):
          screen.draw.filled_circle(self.pos, 5,(255, 0, 0))

class SoldierUnit(Actor):
  
  def __init__(self, type_of_soldierunit,playernum):
      self.list = []
      self.playernum = playernum
      if(type_of_soldierunit == TypeOfSoldierUnit.CAVALRY):
          units = 4
          damage = 20
          mobility = 6
          durability = 45
          if (playernum == 1):
              imagefile = "slide29.png"
          else:
              imagefile = "slide44.png"
      elif(type_of_soldierunit == TypeOfSoldierUnit.KING):
          units = 1
          damage = 50
          mobility = 5
          durability = 60
          if (playernum == 1):
              imagefile = "slide30.png"
          else:
              imagefile = "slide45.png"
      elif(type_of_soldierunit == TypeOfSoldierUnit.KNIGHT):
          units = 5
          damage = 25
          mobility = 4
          durability = 50
          if (playernum == 1):
              imagefile = "slide31.png"
          else:
              imagefile = "slide46.png"
      elif(type_of_soldierunit == TypeOfSoldierUnit.MODERN_SOLDIER):
          units = 2
          damage = 40
          mobility = 5
          durability = 67
          if (playernum == 1):
              imagefile = "slide32.png"
          else:
              imagefile = "slide47.png"
      elif(type_of_soldierunit == TypeOfSoldierUnit.SPEARMEN):
          units = 6
          damage = 16
          mobility = 4
          durability = 40
          if (playernum == 1):
              imagefile = "slide33.png"
          else:
              imagefile = "slide48.png"
      elif(type_of_soldierunit == TypeOfSoldierUnit.SWORDMEN):
          units = 6
          damage = 22
          mobility = 3
          durability = 45
          if (playernum == 1):
              imagefile = "slide34.png"
          else:
              imagefile = "slide49.png"
      for i in range(units):
        self.list.append(Soldier(damage,mobility,durability,imagefile))

  def draw(self):
    for s in self.list:
      s.draw()
      screen.draw.text(str("D:")+str(s.durability), (s.pos[0] - 10, s.pos[1]), fontsize = 20)
           
  def setpos(self,x,y,asc):
    if(asc):
      for i,s in enumerate(self.list):
        s.topright = x, (y-i*30-30)
    else:
      for i,s in enumerate(self.list):
        s.bottomleft = x, (y+i*30+30)

class ArtilleryUnit(): 

  def __init__(self, type_of_artilleryunit,playernum):
      self.list = []
      self.playernum = playernum
      if(type_of_artilleryunit == TypeOfArtillery.TANK):
          units = 2
          damage = 10
          mobility = 4
          firerange = 4*2
          high_ground_bonus = 0
          castle_bonus = 0
          battlement_bonus = 0
          durability = 70
          if (playernum == 1):
              imagefile = "slide28.png"
          else:
              imagefile = "slide43.png"
      elif(type_of_artilleryunit == TypeOfArtillery.MISSILE_LAUNCHER):
          units = 1
          damage = 25
          mobility = 5
          firerange = 6*2
          high_ground_bonus = 0
          castle_bonus = 0
          battlement_bonus = 0
          durability = 1
          if (playernum == 1):
              imagefile = "slide27.png"
          else:
              imagefile = "slide42.png"
      elif(type_of_artilleryunit == TypeOfArtillery.GUN):
          units = 4
          damage = 5
          mobility = 4
          firerange = 3*2
          high_ground_bonus = 0
          castle_bonus = 0
          battlement_bonus = 0
          durability = 50
          if (playernum == 1):
              imagefile = "slide26.png"
          else:
              imagefile = "slide41.png"
      elif(type_of_artilleryunit == TypeOfArtillery.ARCHER ):
          units = 6
          damage = 3
          mobility = 5
          firerange = 3*2
          high_ground_bonus = 0
          castle_bonus = 0
          battlement_bonus = 0
          durability = 10
          if (playernum == 1):
              imagefile = "slide22.png"
          else:
              imagefile = "slide37.png"
      elif(type_of_artilleryunit == TypeOfArtillery.CANNON):
          units = 4
          damage = 7
          mobility = 3
          firerange = 4*2
          high_ground_bonus = 0
          castle_bonus = 0
          battlement_bonus = 0
          durability = 30
          if (playernum == 1):
              imagefile = "slide23.png"
          else:
              imagefile = "slide38.png"
      elif(type_of_artilleryunit == TypeOfArtillery.CATAPULT):
          units = 5
          damage = 5
          mobility = 2
          firerange = 6*2
          high_ground_bonus = 0
          castle_bonus = 0
          battlement_bonus = 0
          durability = 50
          if (playernum == 1):
              imagefile = "slide24.png"
          else:
              imagefile = "slide39.png"
      elif(type_of_artilleryunit == TypeOfArtillery.BOMBER):
          units = 4
          damage = 9
          mobility = 5
          firerange = 2*2
          high_ground_bonus = 0
          castle_bonus = 0
          battlement_bonus = 0
          durability = 35
          if (playernum == 1):
              imagefile = "slide25.png"
          else:
              imagefile = "slide40.png"
      for i in range(units):
        self.list.append(Artillery(damage,mobility,firerange,high_ground_bonus,castle_bonus,battlement_bonus,durability,imagefile))

  def setpos(self,x,y,asc):
    if(asc):
      for i,a in enumerate(self.list):
        a.topright = x, (y-i*30-30)
    else:
      for i,a in enumerate(self.list):
        a.bottomleft = x, (y+i*30+30)

  def draw(self):
    for s in self.list:
      s.draw()
      screen.draw.text(str("D:")+str(s.durability), (s.pos[0] - 10, s.pos[1]), fontsize = 20)

  def GiveCastleBonus(self):
        if(self.type_of_artilleryunit == TypeOfArtillery.CANNON):
            self.damage = 9
        elif(self.type_of_artilleryunit == TypeOfArtillery.TANK):
            self.damage = 11
        elif(self.type_of_artilleryunit == TypeOfArtillery.MISSILE_LAUNCHER):
            self.damage = 27
        elif(self.type_of_artilleryunit == TypeOfArtillery.GUN):
            self.damage = 7
        elif(self.type_of_artilleryunit == TypeOfArtillery.ARCHER ):
            self.damage = 5
        elif(self.type_of_artilleryunit == TypeOfArtillery.CATAPULT):
            self.damage = 7
        elif(self.type_of_artilleryunit == TypeOfArtillery.BOMBER):
            self.damage = 10

  def GiveBattlementBonus(self):
        if(self.type_of_artilleryunit == TypeOfArtillery.CANNON):
            self.damage = 8
        elif(self.type_of_artilleryunit == TypeOfArtillery.TANK):
            self.damage = 10
        elif(self.type_of_artilleryunit == TypeOfArtillery.MISSILE_LAUNCHER):
            self.range = 7
        elif(self.type_of_artilleryunit == TypeOfArtillery.GUN):
            self.damage = 6
        elif(self.type_of_artilleryunit == TypeOfArtillery.ARCHER ):
            self.damage = 4
        elif(self.type_of_artilleryunit == TypeOfArtillery.CATAPULT):
            self.damage = 5
        elif(self.type_of_artilleryunit == TypeOfArtillery.BOMBER):
            self.damage = 9

  def GiveHighGroundBonus(self):
    if(self.type_of_artilleryunit == TypeOfArtillery.CANNON):
        self.range = 5
    elif(self.type_of_artilleryunit == TypeOfArtillery.TANK):
        self.range = 5
    elif(self.type_of_artilleryunit == TypeOfArtillery.MISSILE_LAUNCHER):
        self.range = 7
    elif(self.type_of_artilleryunit == TypeOfArtillery.GUN):
        self.range = 4
    elif(self.type_of_artilleryunit == TypeOfArtillery.ARCHER ):
        self.range = 4
    elif(self.type_of_artilleryunit == TypeOfArtillery.CATAPULT):
        self.range = 7
    elif(self.type_of_artilleryunit == TypeOfArtillery.BOMBER):
        self.range = 2


class Castle(Actor):
    list = []
    units = 0
    durability = 0
    maxoccupancy = 0
    occupancy = 0
    local_artilleryunits = []

    def __init__(self,pos):
        self.units = 1
        self.durability = 60
        self.maxoccupancy = 4
        self.occupancy = 0
        filename = "small icons/slide21.png"
        Actor.__init__(self,filename,topleft = pos)
        type(self).list.append(self)
        

    def AddArtilleryUnit(self,artilleryunit):
        if(self.occupancy < self.maxoccupancy):
          local_artilleryunits.append(artilleryunit)
          self.occupancy += 1

class Battlement(Actor):
    list = []
    units = 0
    durability = 0
    maxoccupancy = 0
    occupancy = 0
    local_artilleryunits = []

    def __init__(self):
        self.units = 1
        self.durability = 40
        self.maxoccupancy = 1
        self.occupancy = 0
        filename = "battlement.png"
        Actor.__init__(self,filename)
        type(self).list.append(self)

    def AddArtilleryUnit(self,artilleryunit):
        if(self.occupancy < self.maxoccupancy):
          local_artilleryunits.append(artilleryunit)
          self.occupancy += 1

def draw_elements():
    global state
    if(state >= 21):
      player1_castle.draw()    
      for au in player1_artillery_units:
          au.draw()   
      for su in player1_soldier_units:
          su.draw()
    if(state >= 22):
      player2_castle.draw()
      for au in player2_artillery_units:
          au.draw()
      for su in player2_soldier_units:
          su.draw()
    for p in Projectile.List:
        p.draw()

def update():
    for p in Projectile.List:
        p.update()
        
def draw():
    global state

    if(state == 0):
      screen.blit('slides/slide8.png',(0,0))
    elif(state == 1):
      screen.blit('slides/slide9.png',(0,0))
    elif(state == 2):
      screen.blit('slides/slide10.png',(0,0))
    elif(state == 3):
      screen.blit('slides/slide7.png',(0,0))
    elif(state == 4):
      screen.blit('slides/slide11.png',(0,0))
    elif(state == 5):
      screen.blit('slides/slide5.png',(0,0))
    elif(state == 6):
      screen.blit('slides/slide6.png',(0,0))
    elif(state == 7):
      screen.blit('slides/slide12.png',(0,0))
    elif(state == 8):
      screen.blit('slides/slide13.png',(0,0))
    elif(state == 9):
      screen.blit('slides/slide14.png',(0,0))
    elif(state == 10):
      screen.blit('slides/slide16.png',(0,0))
    elif(state == 11):
      screen.blit('slides/slide15.png',(0,0))
    elif(state == 12):
      screen.blit('slides/slide17.png',(0,0))
    elif(state >= 20):
      screen.blit('slides/battlefield2.png',(0,0))
      gridsize = 30
      
      ##Draw the highgrounds
      HIGH_GROUND_COLOR = 133, 185, 0
      HIGH_GROUNDS = [Rect((0, 0), (WIDTH, 3*gridsize)),
                    Rect((0, 5*gridsize), (WIDTH, gridsize)),
                    Rect((0, HEIGHT-3*gridsize), (WIDTH, HEIGHT)),
                    Rect((0, HEIGHT-6*gridsize), (WIDTH, gridsize))]
      for rects in HIGH_GROUNDS:
        screen.draw.filled_rect(rects, HIGH_GROUND_COLOR)
      
      ##Draw Gridlines 
      horizontal_lines = int(HEIGHT/gridsize)
      vertical_lines = int(WIDTH/gridsize)
      for i in range(0,horizontal_lines):
          screen.draw.line((0, gridsize*i), (WIDTH, gridsize*i), (255, 0, 0))
      for i in range(0,vertical_lines):
          screen.draw.line((gridsize*i,0), (gridsize*i,HEIGHT), (255, 0, 0))

      draw_elements()

def can_i_move(actor_list, chosen_one):
    ret = chosen_one.collidelist(actor_list)
    if (ret != -1):
        if (chosen_one.my_type == 1):
            victim = actor_list[ret]
            victim.durability -= chosen_one.damage
            if (victim.durability < 0):
                for u in (player1_artillery_units + player2_artillery_units + player1_soldier_units + player2_soldier_units):
                    if (u.list.count(victim)>0):
                        u.list.remove(victim)
                del (victim)
        return False
    else:
        return True

def on_key_down(key):
    
    global state
    global player1_artillery_units
    global player2_artillery_units
    global player1_soldier_units
    global player2_soldier_units

    player1_artillery_units_done = (len(player1_artillery_units) == 2)
    player1_soldier_units_done = (len(player1_soldier_units) == 2)
    player1_done = player1_artillery_units_done and player1_soldier_units_done

    player2_artillery_units_done = (len(player2_artillery_units) == 2)
    player2_soldier_units_done = (len(player2_soldier_units) == 2)
    player2_done = player2_artillery_units_done and player2_soldier_units_done
    
    if (state == 0):
       if (key == keys.RETURN):#TypeOfArtillery.ARCHER 
           if(not player1_artillery_units_done):
             artillery_unit = ArtilleryUnit(TypeOfArtillery.ARCHER,1 )
             player1_artillery_units.append(artillery_unit)
           else:
             artillery_unit = ArtilleryUnit(TypeOfArtillery.ARCHER,2 )
             player2_artillery_units.append(artillery_unit)
             player2_artillery_units_done = (len(player2_artillery_units) == 2)
           if(player2_artillery_units_done and player1_artillery_units_done):
               state = 7
           else:
               state = 1
       elif (key == keys.DOWN):
            state = 1
    elif (state == 1):
       if (key == keys.RETURN):#TypeOfArtillery.CANNON
           if(not player1_artillery_units_done):
             artillery_unit = ArtilleryUnit(TypeOfArtillery.CANNON,1)
             player1_artillery_units.append(artillery_unit)
           else:
             artillery_unit = ArtilleryUnit(TypeOfArtillery.CANNON,2)
             player2_artillery_units.append(artillery_unit)
             player2_artillery_units_done = (len(player2_artillery_units) == 2)
           if(player2_artillery_units_done and player1_artillery_units_done):
               state = 7
           else:
               state = 2
       elif (key == keys.DOWN):
            state = 2
    elif (state == 2):
       if (key == keys.RETURN):#TypeOfArtillery.CATAPULT
           if(not player1_artillery_units_done):
             artillery_unit = ArtilleryUnit(TypeOfArtillery.CATAPULT,1)
             player1_artillery_units.append(artillery_unit)
           else:
             artillery_unit = ArtilleryUnit(TypeOfArtillery.CATAPULT,2)
             player2_artillery_units.append(artillery_unit)
             player2_artillery_units_done = (len(player2_artillery_units) == 2)
           if(player2_artillery_units_done and player1_artillery_units_done):
               state = 7
           else:
               state = 3
       elif (key == keys.DOWN):
            state = 3
    elif (state == 3):
       if (key == keys.RETURN):#TypeOfArtillery.GUN        
           if(not player1_artillery_units_done):
             artillery_unit = ArtilleryUnit(TypeOfArtillery.GUN,1)
             player1_artillery_units.append(artillery_unit)
           else:
             artillery_unit = ArtilleryUnit(TypeOfArtillery.GUN,2)
             player2_artillery_units.append(artillery_unit)
             player2_artillery_units_done = (len(player2_artillery_units) == 2)
           if(player2_artillery_units_done and player1_artillery_units_done):
               state = 7
           else:
               state = 4
       elif (key == keys.DOWN):
            state = 4
    elif (state == 4):
       if (key == keys.RETURN):#TypeOfArtillery.BOMBER    
           if(not player1_artillery_units_done):
             artillery_unit = ArtilleryUnit(TypeOfArtillery.BOMBER,1)
             player1_artillery_units.append(artillery_unit)
           else:
             artillery_unit = ArtilleryUnit(TypeOfArtillery.BOMBER,2)
             player2_artillery_units.append(artillery_unit)
             player2_artillery_units_done = (len(player2_artillery_units) == 2)
           if(player2_artillery_units_done and player1_artillery_units_done):
               state = 7
           else:
               state = 5
       elif (key == keys.DOWN):
            state = 5
    elif (state == 5):
       if (key == keys.RETURN):#TypeOfArtillery.TANK          
           if(not player1_artillery_units_done):
             artillery_unit = ArtilleryUnit(TypeOfArtillery.TANK,1)
             player1_artillery_units.append(artillery_unit)
           else:
             artillery_unit = ArtilleryUnit(TypeOfArtillery.TANK,2)
             player2_artillery_units.append(artillery_unit)
             player2_artillery_units_done = (len(player2_artillery_units) == 2)
           if(player2_artillery_units_done and player1_artillery_units_done):
               state = 7
           else:
               state = 6
       elif (key == keys.DOWN):
            state = 6
    elif (state == 6):
       if (key == keys.RETURN):#TypeOfArtillery.MISSILE_LAUNCHER          
           if(not player1_artillery_units_done):
             artillery_unit = ArtilleryUnit(TypeOfArtillery.MISSILE_LAUNCHER,1)
             player1_artillery_units.append(artillery_unit)
           else:
             artillery_unit = ArtilleryUnit(TypeOfArtillery.MISSILE_LAUNCHER,2)
             player2_artillery_units.append(artillery_unit)
             player2_artillery_units_done = (len(player2_artillery_units) == 2)
           if(player2_artillery_units_done and player1_artillery_units_done):
               state = 7
           elif(player1_artillery_units_done and player1_soldier_units_done):
               state = 0  
           else:
               state = 7
       elif (key == keys.DOWN):         
            state = 0
    elif (state == 7):##Soldier unit selection starts
       if (key == keys.RETURN):#CAVALRY
           if(not player1_soldier_units_done):
             soldier_unit = SoldierUnit(TypeOfSoldierUnit.CAVALRY,1)
             player1_soldier_units.append(soldier_unit)
           else:
             soldier_unit = SoldierUnit(TypeOfSoldierUnit.CAVALRY,2)
             player2_soldier_units.append(soldier_unit)
             player2_soldier_units_done = (len(player2_soldier_units) == 2)
           if(player2_soldier_units_done and player1_soldier_units_done):
               state = 20 ##Begin game
           else:
               state = 8
       elif (key == keys.DOWN):         
            state = 8
            
    elif (state == 8):##Soldier unit selection starts
       if (key == keys.RETURN):#Knight     
           if(not player1_soldier_units_done):
             soldier_unit = SoldierUnit(TypeOfSoldierUnit.KNIGHT,1)
             player1_soldier_units.append(soldier_unit)
           else:
             soldier_unit = SoldierUnit(TypeOfSoldierUnit.KNIGHT,2)
             player2_soldier_units.append(soldier_unit)
             player2_soldier_units_done = (len(player2_soldier_units) == 2)
           if(player2_soldier_units_done and player1_soldier_units_done):
               state = 20 ##Begin game
           else:
               state = 9
       elif (key == keys.DOWN):         
            state = 9
            
    elif (state == 9):##Soldier unit selection starts
       if (key == keys.RETURN):#MODERN SOLDIER      
           if(not player1_soldier_units_done):
             soldier_unit = SoldierUnit(TypeOfSoldierUnit.MODERN_SOLDIER,1)
             player1_soldier_units.append(soldier_unit)
           else:
             soldier_unit = SoldierUnit(TypeOfSoldierUnit.MODERN_SOLDIER,2)
             player2_soldier_units.append(soldier_unit)
             player2_soldier_units_done = (len(player2_soldier_units) == 2)
           if(player2_soldier_units_done and player1_soldier_units_done):
               state = 20 ##Begin game
           else:
               state = 10
       elif (key == keys.DOWN):         
            state = 10
            
    elif (state == 10):##Soldier unit selection starts
       if (key == keys.RETURN):#SWORDMEN         
           if(not player1_soldier_units_done):
             soldier_unit = SoldierUnit(TypeOfSoldierUnit.SWORDMEN,1)
             player1_soldier_units.append(soldier_unit)
           else:
             soldier_unit = SoldierUnit(TypeOfSoldierUnit.SWORDMEN,2)
             player2_soldier_units.append(soldier_unit)
             player2_soldier_units_done = (len(player2_soldier_units) == 2)
           if(player2_soldier_units_done and player1_soldier_units_done):
               state = 20 ##Begin game
           else:
               state = 11
       elif (key == keys.DOWN):         
            state = 11
    
    elif (state == 11):##Soldier unit selection starts
       if (key == keys.RETURN):#SPEARMEN  
           if(not player1_soldier_units_done):
             soldier_unit = SoldierUnit(TypeOfSoldierUnit.SPEARMEN,1)
             player1_soldier_units.append(soldier_unit)
           else:
             soldier_unit = SoldierUnit(TypeOfSoldierUnit.SPEARMEN,2)
             player2_soldier_units.append(soldier_unit)
             player2_soldier_units_done = (len(player2_soldier_units) == 2)
           if(player2_soldier_units_done and player1_soldier_units_done):
               state = 20 ##Begin game
           else:
               state = 12
       elif (key == keys.DOWN):         
            state = 12

    elif (state == 12):##Soldier unit selection starts
       if (key == keys.RETURN):#KING        
           if(not player1_soldier_units_done):
             soldier_unit = SoldierUnit(TypeOfSoldierUnit.KING,1)
             player1_soldier_units.append(soldier_unit)
           else:
             soldier_unit = SoldierUnit(TypeOfSoldierUnit.KING,2)
             player2_soldier_units.append(soldier_unit)
             player2_soldier_units_done = (len(player2_soldier_units) == 2)
           if(player2_soldier_units_done and player1_soldier_units_done):
               state = 20 ##Begin game
           else:
               state = 7
       elif (key == keys.DOWN):         
            state = 7

    elif (state == 22):
        units = Artillery.List + Soldier.List
        chosen_found = False
        for u in units:
            if (u.the_chosen_one):
                chosen_found = True
                chosen_u = u
                break
        if(chosen_found):
          prev_pos = chosen_u.pos
          if (key == keys.DOWN):
            chosen_u.y = chosen_u.y + 30

          if (key == keys.UP):
            chosen_u.y = chosen_u.y - 30

          if (key == keys.LEFT):
            chosen_u.x = chosen_u.x - 30

          if (key == keys.RIGHT):
            chosen_u.x = chosen_u.x + 30

          if (key == keys.U):
              chosen_u.the_chosen_one = False
              chosen_u.running_mobility = 0
            
          units.remove(chosen_u)
          if (can_i_move(units, chosen_u)== False):
              chosen_u.pos = prev_pos

          if (chosen_u.running_mobility == 1):
              chosen_u.running_mobility = 0
              chosen_u.the_chosen_one = False
          elif (chosen_u.running_mobility > 0):
              chosen_u.running_mobility -= 1
        if(key == keys.L):
            state = 23
    elif (state == 23):
        if(key == keys.E):
            state = 22
    elif (state == 24):
        if(key == keys.E):
            state = 22

def round2(num,gridsize,offset):
    return(((num + gridsize - 1)//gridsize)*gridsize + offset)

def on_mouse_down(pos):
    global state
    global player1_castle
    global player2_castle
    global player1_artillery_units
    global player2_artillery_units
    global player1_soldier_units
    global player2_soldier_units
    global launcher

    x,y = pos
    x = round2(x,30,0)
    y = round2(y,30,0)
    pos_rnd = x,y
    
    if (state == 20):
        player1_castle = Castle(pos_rnd)
        units = player1_artillery_units + player1_soldier_units
        for i,au in enumerate(units):
          units[i].setpos(60+60*i,HEIGHT,True)   
        state = 21
    elif (state == 21):
        player2_castle = Castle(pos_rnd)
        units = player2_artillery_units + player2_soldier_units
        for i,au in enumerate(units):
          units[i].setpos(WIDTH-60-60*i,0,False)   
        state = 22
    elif (state == 23):
        units = Artillery.List + Soldier.List
        dummy = Actor ('black.jpg',center=pos_rnd)
        ret = dummy.collidelist(units)
        if (ret != -1):
            launcher = units[ret]
            state = 24
    elif (state == 24):
        p = Projectile(launcher.pos, pos_rnd, launcher.firerange, launcher.damage) 
    else:
        units = Artillery.List + Soldier.List
        dummy = Actor ('black.jpg',center=pos_rnd)
        ret = dummy.collidelist(units)
        if (ret != -1):
            units[ret].the_chosen_one = True
            units[ret].running_mobility = units[ret].mobility
   
pgzrun.go()
