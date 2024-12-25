from cmath import tan
from pickle import FALSE
from string import whitespace
import pygame as pg
from pygame import mixer
import random
import math
import pygame_widgets as pw
from pygame_widgets.button import Button


pg.init()

screen = pg.display.set_mode((1100,630)) # set dimensions of screen
fpsLimit = 30  # limiting frames per sec
displaycentreX = displaycentreY = 300
circleradius = 270
clock = pg.time.Clock() # inetializing clock
pg.display.set_caption("RADAR SIMULATOR")
ownShipMoves = otherShipMoves = 1000 #ships are moved in 1000 ms
# can be made to change 
displayrange = 12 # nm
copiedRange = displayrange
vectorTime = 12 #min

# defining diff fonts , number id the size
font = pg.font.SysFont(None, 40)
font1 = pg.font.SysFont(None, 15)
font2 = pg.font.SysFont(None, 28)

# loading images and their path
shipImage = pg.image.load('./ship.png')
othershipimage = pg.image.load('./othership.png')
#seahorseimage = pg.image.load('e:/PYTHON/Radar simulator/sea.png')
# dot = pg.image.load('e:/PYTHON/Radar simulator/dot.png')
backgroundimage = pg.image.load('./background2.png')

relmotionimage = font2.render('RM', True, (28,179,2))
truemotionimage = font2.render('TM', True, (28,179,2))
relativevectorimage = font.render("R", True, (28,179,2))
truevectorimage = font.render("T", True, (28,179,2))

# added to match the centre of ship image
ownshipimageparallexX = 32/2
ownshipimageparallexY = 45/2

ownShipX = 300 - ownshipimageparallexX
ownShipY = 300 - ownshipimageparallexY

# inetializing own ship course and spead
ownshipspead = 15  # knots 
ownshipcoursedegree = 340
ownshipcourse = math.radians(ownshipcoursedegree)

othershiprange = 12 #in nm
othershipbearing = math.radians(20) # number is true bearing in degrees

rangechange = 0
def decreaseDisplayRange():
    global Button
    Button = ()
    global displayrange, rangechange
    if displayrange > 0.75:
        displayrange = displayrange / 2
        rangechange = -1
        resetTargetAfterRangeChange()

def increaseDisplayRange():
    global Button
    Button = ()
    global displayrange, rangechange
    #displayrange = displayrange * 2
    #print ("incr")
    if displayrange < 49:
        displayrange = displayrange * 2
        rangechange = 1
        resetTargetAfterRangeChange()

def resetTargetAfterRangeChange():
    global othership1X, othership1Y, oneMile, ownShipSpeadPixel, rangechange
    oneMile = circleradius/displayrange # in pexel
    ownShipSpeadPixel = oneMile*ownshipspead #pixel per hour
    ownShipSheedVector = (ownShipSpeadPixel*60)*vectorTime
    if rangechange == 1:
        othership1X = displaycentreX+((othership1X- displaycentreX)/2)
        othership1Y = displaycentreY+((othership1Y- displaycentreY)/2)
    elif rangechange == -1:
        othership1X = displaycentreX+((othership1X- displaycentreX)*2)
        othership1Y = displaycentreY+((othership1Y- displaycentreY)*2)
    rangechange = 0
    #print("hi hi")






oneMile = circleradius/displayrange # in pexel
ownShipSpeadPixel = oneMile*ownshipspead #pixel per hour
ownShipSheedVector = (ownShipSpeadPixel*60)*vectorTime

 # display own ship hdg and spead
hdgimage = font.render(f"{ownshipcoursedegree}", True, (28,179,2))
spdimage = font.render(f"{ownshipspead}", True, (28,179,2))

# display target
othership1X = 300+(oneMile*othershiprange)*math.sin(othershipbearing)
othership1Y = 300-(oneMile*othershiprange)*math.cos(othershipbearing)

othershipspeedkn = 12.5 # kn
othership1_spead = (oneMile*othershipspeedkn) # pixel per hr
othership1_spd_vectortime = (othership1_spead/60)*vectorTime
othership1_course = math.radians(273) # number is true bearing in degrees

# starting with relative motion
relativemotion = True

# MOTION CHANGEOVER FROM RELATIVE TO TRUE
def toggletruerelative():
    global Button
    Button = ()
    global relativemotion
    if relativemotion == False:
        relativemotion = True
        resetaftertruemontion()
    else:
        relativemotion = False
 #XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX NEEDS ATTENTION   
def resetaftertruemontion():
    global ownShipX, ownShipY, othership1X, othership1Y
    resetdragX = ownShipX - (displaycentreX)
    resetdragY = (displaycentreY) - ownShipY
    ownShipX = ownShipX - resetdragX #- ownshipimageparallexX
    ownShipY = ownShipY + resetdragY #- ownshipimageparallexY
    othership1X = othership1X - resetdragX
    othership1Y = othership1Y + resetdragY

if relativemotion == True:
    t = 'Now Relative Motion'
else: 
    t = 'Now True Motion'

# BUTTONS XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# FOR MOTION CHANGE
button = Button(
        screen, 111, 30, 30, 20, text='TM/RM', textColour = (250,250,250),
        fontSize=15, margin=10,
        inactiveColour=(40, 40, 40),
        pressedColour=(40, 40, 60), radius=0,
        onClick= lambda: toggletruerelative() )
# FOR VECTOR CHANGE
button2 = Button(
        screen, 626, 360, 20, 20, text='T/R', textColour = (28,179,2),
        fontSize=18, margin=2,
        inactiveColour=(0, 40, 0),
        pressedColour=(0, 40, 0), radius=0,
        onClick= lambda: togglevector() )
# VRM ON/OFF
button3 = Button(
        screen, 408, 571, 20, 15, text='ON/OFF', textColour = (28,179,2),
        fontSize=13, margin=2,
        inactiveColour=(0, 40, 0),
        pressedColour=(0, 40, 0), radius=0,
        onClick= lambda: toggleVrm() )
# VRM INCR
button4 = Button(
        screen, 569, 573, 30, 20, text='incr', textColour = (28,179,2),
        fontSize=18, margin=2,
        inactiveColour=(0, 40, 0),
        pressedColour=(0, 40, 0), radius=0,
        onClick= lambda: increaseVrm() )
 # VRM DECREASE
button5 = Button(
        screen, 483, 573, 30, 20, text='decr', textColour = (28,179,2),
        fontSize=18, margin=2,
        inactiveColour=(0, 40, 0),
        pressedColour=(0, 40, 0), radius=0,
        onClick= lambda: decreaseVrm() )

# INCREASE DISPLAY RANGE
button6 = Button(
        screen, 5, 10, 20, 10, text='decr', textColour = (28,179,2),
        fontSize=18, margin=2,
        inactiveColour=(0, 40, 0),
        pressedColour=(0, 40, 0), radius=0,
        onClick= lambda: decreaseDisplayRange() )
# DECREASE DISPLAY RANGE
button7 = Button(
        screen, 5, 20, 20, 10, text='incr', textColour = (28,179,2),
        fontSize=18, margin=2,
        inactiveColour=(0, 40, 0),
        pressedColour=(0, 40, 0), radius=0,
        onClick= lambda: increaseDisplayRange() )







relativevector = False 
def togglevector():
    global relativevector
    if relativevector == False:
        relativevector = True
    else:
        relativevector = False

def targetvector(x, y , relIncrimentX , relIncrimentY):
    endX = x + (othership1_spd_vectortime * math.sin(othership1_course))
    endY = y + (othership1_spd_vectortime * math.cos(othership1_course))
    
    pg.draw.circle(screen, (255,255,255), (x, y), 7, 2)
    # NEEDS RETHINKING XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    if relativevector:
        endX = x - (relIncrimentX * fpsLimit * 60 * vectorTime)
        endY = y - (relIncrimentY * fpsLimit * 60 * vectorTime)
        
    pg.draw.line(screen, (255,255,255),(x, y), (endX, endY), 2)


vrm = False
vrmRange = circleradius / 2
vrmRangeDisplayed = (displayrange/circleradius) * vrmRange
incrDecre = 3 # pixel

def increaseVrm():
    global Button
    Button = ()
    global vrmRange , vrmRangeDisplayed , circleradius , displayrange , incrDecre
    
    if vrmRange < circleradius :
        vrmRange += incrDecre
        vrmRangeDisplayed +=  (displayrange/circleradius) * incrDecre

def decreaseVrm():
    global Button
    Button = ()
    global vrmRange , vrmRangeDisplayed , circleradius , displayrange , incrDecre
    
    if vrmRange > 0 :
        vrmRange -= incrDecre
        vrmRangeDisplayed -=  (displayrange/circleradius) * incrDecre


def toggleVrm():
    global Button
    Button = ()
    global vrm
    if vrm == False:
        vrm = True        
    else: vrm = False

#vrmImage = font.render(f"{round(vrmRangeDisplayed , 2)}", True, (28,179,2))

def drawVrm():
    global vrm, displaycentreX, displaycentreY, vrmRange , vrmImage
    if vrm == True:
        pg.draw.circle(screen, (28,179,2), (displaycentreX, displaycentreY), vrmRange, 1)
        vrmImage = font.render(f"{round(vrmRangeDisplayed , 2)}", True, (28,179,2))
        screen.blit(vrmImage, (512, 570))

def rangeRings():
    global displaycentreX, displaycentreY, circleradius
    x = 1
    while x < 6:
        pg.draw.circle(screen, (255,255,255), (displaycentreX, displaycentreY), (circleradius/6)*x, 1)
        x += 1


def circle():
    global displaycentreX, displaycentreY, circleradius

    pg.draw.circle(screen, (255,255,255), (displaycentreX, displaycentreY), circleradius, 1)
    northangle = 0
    while northangle < 360:
        angle = math.radians(northangle)
        startX = 300 + (circleradius * math.sin(angle))
        startY = 30 + circleradius- (circleradius * math.cos(angle)) 
        endX = 300 + ((circleradius+10) * math.sin(angle))
        endY = 30-10 + (circleradius+10)- ((circleradius+10) * math.cos(angle))
        textX = 300-10 + ((circleradius+20) * math.sin(angle))
        textY = 30-20 + (circleradius+20)- ((circleradius+20) * math.cos(angle))
        pg.draw.line(screen, (255,255,255),(startX, startY), (endX, endY), 2)
        
        screen.blit(font1.render(f"{northangle}", True, (25,25,255)), (textX, textY))
        northangle += 10
    
    northangle = 0
    while northangle < 360:
        angle = math.radians(northangle)
        startX = 300 + (circleradius * math.sin(angle))
        startY = 30 + circleradius- (circleradius * math.cos(angle)) 
        endX = 300 + ((circleradius+6) * math.sin(angle))
        endY = 30-6 + (circleradius+6)- ((circleradius+6) * math.cos(angle))
        pg.draw.line(screen, (255,255,255),(startX, startY), (endX, endY), 2)
        northangle += 5

    northangle = 0
    while northangle < 360:
        angle = math.radians(northangle)
        startX = 300 + (circleradius * math.sin(angle))
        startY = 30 + circleradius- (circleradius * math.cos(angle)) 
        endX = 300 + ((circleradius+3) * math.sin(angle))
        endY = 30-3 + (circleradius+3)- ((circleradius+3) * math.cos(angle))
        pg.draw.line(screen, (255,255,255),(startX, startY), (endX, endY), 2)
        northangle += 1


def headline():
    endX = 300 + (circleradius * math.sin(ownshipcourse))
    endY = 30 + circleradius- (circleradius * math.cos(ownshipcourse))
    startX = ownShipX + ownshipimageparallexX
    startY = ownShipY + ownshipimageparallexY
    pg.draw.line(screen, (255,255,255), (startX , startY), (endX, endY), 1) # head line
    pg.draw.line(screen, (255,255,255), (startX - 10, startY), (startX+ 10, startY), 1)  # vertical line of cross
    pg.draw.line(screen, (255,255,255), (startX , startY - 10), (startX , startY+ 10), 1) # horizontal line of cross

def background():
    screen.blit(backgroundimage, (0, 0))


def ownShip(x, y):
    screen.blit(shipImage, (x, y))

def othership(x, y):
    screen.blit(othershipimage, (x, y))

#def seahorse():
    #screen.blit(seahorseimage, (seahorseX, seahorseY))

vectorTimeImage = font.render(f"{vectorTime}", True, (28,179,2))
displayrangeimage = font.render(f"{displayrange}", True, (28,179,2))
rangeRingsimage = font2.render(f"{displayrange/6}", True, (28,179,2))

balanceX = 0
balanceY = 0
running = True

while running:
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            running = False 
    background()
    circle()
    headline()
    othership(othership1X, othership1Y)
    #print(displayrange)

    screen.blit(vectorTimeImage , (760, 355))
    screen.blit(displayrangeimage , (30, 7))
    screen.blit(rangeRingsimage , (85, 12))



    if relativemotion:
        screen.blit(relmotionimage, (65, 34))
    else:
        screen.blit(truemotionimage, (65, 34))

    if relativevector:
        screen.blit(relativevectorimage, (866, 355))
    else:
        screen.blit(truevectorimage, (866, 355))

    screen.blit(hdgimage, (670, 10))
    screen.blit(spdimage, (670, 30))

    ownShipSpeedPixelPerFrame = (ownShipSpeadPixel/(3600*fpsLimit))
    otherShip1SpeedPerFrame = (othership1_spead/(3600*fpsLimit))
    
    
    # MOTION OF SHIPS IN RELATIVE MOTION
    if relativemotion:
        courseDiff = abs(math.degrees(ownshipcourse) - math.degrees(othership1_course))
        if courseDiff > 180:
            courseDiff = math.radians(360 - courseDiff) 

        relativespeed = math.sqrt((ownShipSpeedPixelPerFrame**2) + (otherShip1SpeedPerFrame**2) + (2*ownShipSpeedPixelPerFrame*otherShip1SpeedPerFrame))
        #print(relativespeed)
        calculatedApproachAngle = math.asin((otherShip1SpeedPerFrame*math.sin(courseDiff))/relativespeed)
        #print(math.degrees(calculatedApproachAngle))
        # NEEDS RETHINKING XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
        calculatedApproachAngleTrue = ownshipcourse + calculatedApproachAngle + math.radians(180)
        
        #if math.degrees(calculatedApproachAngleTrue) > 360:
            #calculatedApproachAngleTrue = math.radians(calculatedApproachAngleTrue - math.radians(360))

        #balanceX = -ownshipspead * (math.sin(ownshipcourse))
        #balanceY = ownshipspead * (math.cos(ownshipcourse))
        ownShipX = displaycentreX - ownshipimageparallexX
        ownShipY = displaycentreY - ownshipimageparallexY
        otherShipIncrimentX = relativespeed * math.sin(calculatedApproachAngleTrue)
        otherShipIncrimentY = relativespeed * math.cos(calculatedApproachAngleTrue)
        othership1X -= otherShipIncrimentX
        othership1Y -= otherShipIncrimentY
    else:   # MOTION OF SHIPS IN TRUE MOTION
    
        ownShipX += ownShipSpeedPixelPerFrame * (math.sin(ownshipcourse))
        ownShipY -= ownShipSpeedPixelPerFrame * (math.cos(ownshipcourse))

        othership1X += otherShip1SpeedPerFrame * (math.sin(othership1_course))
        othership1Y -= otherShip1SpeedPerFrame * (math.cos(othership1_course))

       
    drawVrm()
    ownShip(ownShipX, ownShipY)
    othership(othership1X, othership1Y)
    targetvector(othership1X + 9, othership1Y + 7 , otherShipIncrimentX , otherShipIncrimentY)
    circle()
    headline()
    #rangeRings()
    # screen.blit(background, (0,0))
    pw.update(events)
    clock.tick(fpsLimit) # set speed to 30 frames per sec
    pg.display.update()
    

running = False
