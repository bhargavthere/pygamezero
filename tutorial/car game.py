import random

WIDTH = 1800
HEIGHT = 1000
PUMPFREQ = 25

min_speed = 10
max_speed = 135
roadslice_count = 0
fuel_overlap = False 
curr_speed = min_speed
carcolors = ['blue', 'silver', 'yellow']
cars = []
carloc = 800

for carcolor in carcolors:
    temp = Actor(carcolor)
    temp.bottomright = carloc,900
    carloc += 400
    cars.append(temp)
    

player = Actor('car')
player.bottomright = 400, 900
player_fuel = 310

fuel_pump = Actor ('fuel_pump') 
fuel_pump.topleft = random.randrange(100,1600), 0

roadslice1 = Actor('roadslice')
roadslice2 = Actor('roadslice')
roadslice1.topleft = 0,0 
roadslice2.topleft = 0,1000

def draw():
    screen.fill((0,0,0))
    roadslice1.draw()
    roadslice2.draw()
    player.draw()
    for car in cars:
        car.draw()
    fuel_pump.draw()
    screen.draw.text("Fuel:"+str(player_fuel), (20, 100))
    

def update():
    global roadslice_count, player_fuel, fuel_overlap
    
    roadslice1.y += curr_speed
    roadslice2.y += curr_speed
    
    if roadslice1.top > HEIGHT:
       roadslice1.bottomleft = 0,0
       roadslice_count = roadslice_count + 1
       player_fuel = player_fuel - 1
    
    if roadslice2.top > HEIGHT:
       roadslice2.bottomleft = 0,0
       roadslice_count = roadslice_count + 1
       player_fuel = player_fuel - 1

    if roadslice_count == PUMPFREQ:
        roadslice_count = 0
        fuel_pump.topleft = random.randrange(100,1600), 0

    fuel_pump.y += curr_speed
    if (((player.topleft[0] > fuel_pump.topleft[0]) and (player.topleft[0] < fuel_pump.topright[0])) and
        ((player.topleft[1] > fuel_pump.topleft[1]) and (player.topleft[1] < fuel_pump.bottomleft[1]))):
        if(fuel_overlap == False):
            player_fuel = player_fuel + 110
            fuel_overlap = True
    else:
        fuel_overlap = False
                

def on_key_down(key):   
    global curr_speed
    if key == keys.UP:
        curr_speed = curr_speed + 10
        if curr_speed > max_speed:
           curr_speed = max_speed
        

    if key == keys.DOWN:
        curr_speed = curr_speed - 10
        if curr_speed < min_speed:
            curr_speed = min_speed
        
    if key == keys.RIGHT:
        player.x += 100
        if player.x > (WIDTH - 200):
            player.x = (WIDTH - 200)
   
    if key == keys.LEFT:
        player.x -= 100
        if player.x < 100:
            player.x = 100


