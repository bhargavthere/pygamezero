import pgzrun
import random
import math
import enum 

HEIGHT = 1080
WIDTH = 540
FINISHLINE = 10000

state = 23
number_of_players = 2
speed = 0
agility = 0
durability = 0
weight = 0
fuel = 0
control = 0
grip = 0
max_players = 2

class TypeOfObstacle(enum.Enum):
    CRACK_IN_ROAD = 0
    CONSTRUCTION_CONE = 1
    BRICK_WALL = 2
    HEAVY_LOAD = 3
    FUEL_DRAINING_SPIKE = 4
    SNOWFALL = 5
    SLEET = 6

class obstacle(Actor):
  list = []
  type_of_obstacle = 0

  def __init__(self):
    global number_of_players
    global max_players
    self.type_of_obstacle = random.randint (0,len(TypeOfObstacle))
    filename = "obs" + str(self.type_of_obstacle + 1) + ".jpeg"
    Actor.__init__(self,filename)
    type(self).list.append(self)
    track = random.randint (1,max_players)
    r = 164 + 19*(track - 1)
    theta = random.randint (0,359)*math.pi/180.0
    self.x = 270 + r*math.cos(theta)
    self.y = 270 + r*math.sin(theta)

  def draw_obstacle(screen):
    for o in obstacle.list:
      o.draw()
      if (o.type_of_obstacle == 0):
        screen.draw.text("s",(o.x,o.y),color="black",fontsize=20)
      if (o.type_of_obstacle == 1):
        screen.draw.text("a",(o.x,o.y),color="black",fontsize=20)
      if (o.type_of_obstacle == 2):
        screen.draw.text("d",(o.x,o.y),color="black",fontsize=20)
      if (o.type_of_obstacle == 3):
        screen.draw.text("w",(o.x,o.y),color="black",fontsize=20)
      if (o.type_of_obstacle == 4):
        screen.draw.text("f",(o.x,o.y),color="black",fontsize=20)
      if (o.type_of_obstacle == 5):
        screen.draw.text("c",(o.x,o.y),color="black",fontsize=20)
      if (o.type_of_obstacle == 6):
        screen.draw.text("g",(o.x,o.y),color="black",fontsize=20)

  def remove_obstacle(self):
    obstacle.list.remove(self)

  def get_type_of_obstacle(self):
    return(self.type_of_obstacle)
  
class car(Actor):
  list = []
  speed = 0
  agility = 0
  durability = 0
  weight = 0
  fuel = 0
  control = 0
  grip = 0
  dt = 0
  num = 0
  theta = 0
  freeze = 0
  extweight = 0
  weighttime = 0
  
  def __init__(self, num_, speed_, agility_, durability_, weight_, fuel_, control_, grip_ ):
    imagefile = "pcar"+str(num_)+".png"
    Actor.__init__(self,imagefile)
    self.speed = speed_
    self.agility = agility_
    self.durability = durability_
    self.weight = weight_
    self.fuel = fuel_
    self.control = control_
    self.grip = grip_
    self.num = num_
    self.theta = 0
    self.dt = 0
    self.freeze = 0
    self.extweight = 0
    self.weighttime = 0
    type(self).list.append(self)

  def update(self):
    if(self.weighttime == 0):
      sp = self.speed - self.weight
    else:
      sp = self.speed - self.weight - self.extweight
      self.weighttime -= 1
    if(self.theta > 2*math.pi):
      self.theta -= 2*math.pi
    r = 164 + 19*(self.num - 1)
    if((self.freeze == 0) and (self.fuel > 0)):
      self.theta = (self.theta + sp/(r*100.0))
      self.dt += (sp/100.0)
      self.fuel -= (sp/(30000.0*self.weight))
    else:
      self.freeze -= 1
    self.x = 270 + r*math.cos(self.theta)
    self.y = 270 + r*math.sin(self.theta)
    self.angle = 90-(self.theta)*180/math.pi
    idx = self.collidelist(obstacle.list)
    if(idx != -1):
      o = obstacle.list[idx]
      okind = o.get_type_of_obstacle()
      o.remove_obstacle()
      if (okind == 0):#speed obstacle
        if (self.speed < 130.1):
          self.freeze = 750
      elif (okind == 1):#agility obstacle
        if (self.agility < 5):
          self.freeze = 750
      elif (okind == 2):#durability obstacle
        self.durability -= 4
      elif (okind == 3):#weight obstacle
        self.extweight = 30
        self.weighttime = 2250
      elif (okind == 4):#fuel ostacle
        if (self.fuel < 4):
          self.fuel -= 2
      elif (okind == 5):#control obstacle
        if (self.control < 3):
          self.freeze = 750
      elif (okind == 6):#grip obstacle 
        if (self.grip < 4):
          self.freeze = 750

  def report(self):
    ret = "num = " + str(self.num) + "\n" \
        + "speed = " + str(self.speed) + "\n" \
        + "agility = " + str(self.agility) + "\n" \
        + "durability = " + str(self.durability) + "\n" \
        + "weight = " + str(self.weight) + "\n" \
        + "control = " + str(self.control) + "\n" \
        + "fuel = " + str(round(self.fuel,2)) + "\n" \
        + "grip = " + str(self.grip) + "\n" \
        + "distance = " + str(round(self.dt,0))
    return(ret)

  def carupdate():
    for c in car.list:
      c.update()

  def cardraw():
    for c in car.list:
      c.draw()

  def findwinner():
    for c in car.list:
      if(c.dt > FINISHLINE):
        return(c.num)
    return(-1)

def draw():
    global state
    if (state != 22):
      screen.fill('white')
    if (state == 23):
      screen.blit('intro1.png',(0,0))
    elif (state == 0):
        screen.blit('racegame.png', (0,0))
    elif (state == 1):
        screen.blit('slide3.png',(0,0))
    elif (state == 2):
        screen.blit('slide4.png',(0,0))
    elif (state == 3):
        screen.blit('slide5.png',(0,0))
    elif (state == 4):
        screen.blit('slide6.png',(0,0))
    elif (state == 5):
        screen.blit('slide7.png',(0,0))
    elif (state == 6):
        screen.blit('slide8.png',(0,0))
    elif (state == 7):
        screen.blit('slide9.png',(0,0))
    elif (state == 8):
        screen.blit('slide10.png',(0,0))
    elif (state == 9):
        screen.blit('slide11.png',(0,0))
    elif (state == 10):
        screen.blit('slide12.png',(0,0))
    elif (state == 11):
        screen.blit('slide13.png',(0,0))
    elif (state == 12):
        screen.blit('slide14.png',(0,0))
    elif (state == 13):
        screen.blit('slide15.png',(0,0))
    elif (state == 14):
        screen.blit('slide16.png',(0,0))
    elif (state == 15):
        screen.blit('slide17.png',(0,0))
    elif (state == 16):
        screen.blit('slide18.png',(0,0))
    elif (state == 17):
        screen.blit('slide19.png',(0,0))
    elif (state == 18):
        screen.blit('slide20.png',(0,0))
    elif (state == 19):
        screen.blit('slide21.png',(0,0))
    elif (state == 20):
        screen.blit('slide22.png',(0,0))
    elif (state == 21):
        screen.blit('race game.png',(0,0))
        if(random.randint(1,100000) > 99200):
          obstacle()
        car.cardraw()
        obstacle.draw_obstacle(screen)
        i = 0
        xarr = [0,180,360,0,180,360]
        yarr = [540,540,540,810,810,810]
        for c in car.list:
          rep = c.report()
          screen.draw.text(rep,(xarr[i],yarr[i]), color = "black")
          i += 1
        winner = car.findwinner()
        if (winner != -1):
          screen.blit ('banner.png',(0,0))
          w = "... and the winner is..." + str(winner) + "!!!"
          screen.draw.text(w,(100,150), color = 'black', fontsize = 40)
          state = 22
          
def update():
  global state
  if(state == 21):
    car.carupdate()

def on_key_down(key):
    
    global state, number_of_players, max_players
    global speed, agility, durability, weight
    global fuel, control, grip

    if (state == 23):
      if (key == keys.RETURN):
        state = 0
    if (state == 0):
        if (key == keys.K_2):
            number_of_players = 2
            max_players = 2
            state = 1
        elif (key == keys.K_3):
            number_of_players = 3
            max_players = 3
            state = 1
        elif (key == keys.K_4):
            number_of_players = 4
            max_players = 4
            state = 1
        elif (key == keys.K_5):
            number_of_players = 5
            max_players = 5
            state = 1
        elif (key == keys.K_6):
            number_of_players = 6
            max_players = 6
            state = 1
    if (state == 1):
        if (key == keys.RETURN):#George engine
            speed = 130
            agility = 1
            durability = 10
            weight = 10
            fuel = 4
            state = 7
        elif (key == keys.DOWN):
            state = 2
    elif (state == 2):
        if (key == keys.RETURN):#Robert enine
            speed = 150
            agility = 0
            durability = 13
            weight = 20
            fuel = 5.5
            state = 7
        elif (key == keys.DOWN):
            state = 3
    elif (state == 3):
        if (key == keys.RETURN):#Jack tack engine
            speed = 170
            agility = -1
            durability = 17
            weight = 30
            fuel = 7
            state = 7
        elif (key == keys.DOWN):
            state = 4
    elif (state == 4):
        if (key == keys.RETURN):#Gregory engine
            speed = 90
            agility = 3
            durability = 8
            weight = 5
            fuel = 3
            state = 7
        elif (key == keys.DOWN):
            state = 5
    elif (state == 5):
        if (key == keys.RETURN):#Micheal engine
            speed = 75
            agility = 5
            durability =7
            weight = 3
            fuel = 1.5
            state = 7
        elif (key == keys.DOWN):
            state = 6
    elif (state == 6):
        if (key == keys.RETURN):#Richard engine
            speed = 65
            agility = 7
            durability = 6
            weight = 1
            fuel = 0.5
            state = 7
        elif (key == keys.DOWN):
            state = 1
    elif (state == 7):
        if (key == keys.RETURN):#car 1
            speed += 10
            agility += 1
            control = 2
            weight += 3
            state = 15
        elif (key == keys.DOWN):
            state = 8
    elif (state == 8):
        if (key == keys.RETURN):#car 2
            speed += 20
            agility += 1
            control = 1
            weight += 3
            state = 15
        elif (key == keys.DOWN):
            state = 9
    elif (state == 9):
        if (key == keys.RETURN):#car 3
            durability += 1
            speed += 30
            agility += 2
            control = 3
            weight += 0
            state = 15
        elif (key == keys.DOWN):
            state = 10
    elif (state == 10):
        if (key == keys.RETURN):#car 4
            speed += 35
            agility += 3
            control = 3
            weight += 3
            state = 15
        elif (key ==  keys.DOWN):
            state = 11
    elif (state == 11):
        if (key == keys.RETURN):#car 5
            speed += 25
            agility += 4
            Control = 3
            weight += 4
            state = 15
        elif (key == keys.DOWN):
            state = 12
    elif (state == 12):
        if (key == keys.RETURN):#car 6
            durability += 1
            speed += 30
            agility += 3
            control = 3
            weight += 3
            state = 15
        elif (key == keys.DOWN):
            state = 13
    elif (state == 13):
        if (key == keys.RETURN):#car 7
            durability += 2
            speed += 10
            agility += 1
            control = 2
            weight += 2
            state = 15
        elif (key == keys.DOWN):
            state = 14
    elif (state == 14):
        if (key == keys.RETURN):#car 8
            durability += 3
            speed += 20
            control = 1
            weight += 5
            state = 15
        elif (key == keys.DOWN):
            state = 7
    elif (state == 15):
        if (key == keys.RETURN):#Off-Road tires
            durability += 0
            grip = 4
            weight += 3
            car(number_of_players, speed, agility, durability, weight, fuel, control, grip)
            number_of_players = number_of_players - 1
            if(number_of_players == 0):
              state = 21 ##Start the game
            else:
              state = 1
        elif (key == keys.DOWN):
            state = 16
    elif (state == 16):
        if (key == keys.RETURN):#Normal tires
            durability += 0
            grip = 3
            weight += 2
            car(number_of_players, speed, agility, durability, weight, fuel, control, grip)
            number_of_players = number_of_players - 1
            if(number_of_players == 0):
              state = 21 ##Start the game
            else:
              state = 1
        elif (key == keys.DOWN):
            state = 17
    elif (state == 17):
        if (key == keys.RETURN):#Wheel 1
            durability += 0
            grip = 5
            weight += 4
            car(number_of_players, speed, agility, durability, weight, fuel, control, grip)
            number_of_players = number_of_players - 1
            if(number_of_players == 0):
              state = 21 ##Start the game
            else:
              state = 1
        elif (key == keys.DOWN):
            state = 18
    elif (state == 18):
        if (key == keys.RETURN):#Michigan tires
            durability += 0
            grip = 2
            weight += 1
            car(number_of_players, speed, agility, durability, weight, fuel, control, grip)
            number_of_players = number_of_players - 1
            if(number_of_players == 0):
              state = 21 ##Start the game
            else:
              state = 1
        elif (key == keys.DOWN):
            state = 19
    elif (state == 19):
        if (key == keys.RETURN):#Wheel 2
            durability += 1
            grip = 2
            weight += 2
            car(number_of_players, speed, agility, durability, weight, fuel, control, grip)
            number_of_players = number_of_players - 1
            if(number_of_players == 0):
              state = 21 ##Start the game
            else:
              state = 1
        elif (key == keys.DOWN):
            state = 20
    elif (state == 20):
        if (key == keys.RETURN):#Deluxe Off-Road tires
            durability += 1
            grip = 5
            weight += 5
            car(number_of_players, speed, agility, durability, weight, fuel, control, grip)
            number_of_players = number_of_players - 1
            if(number_of_players == 0):
              state = 21 ##Start the game
            else:
              state = 1
        elif (key == keys.DOWN):
            state = 15
            
pgzrun.go()
