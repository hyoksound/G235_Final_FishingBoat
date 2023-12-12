# Global variables
boatX= 0 
boatY = 0
boatWidth, boatHeight = 60, 30
boatSpeed = 6
boatVelocity = 0
rodLowering = False  # Indicates if the rod is being lowered
rodLength = 0
maxRodLength = 500
seaLevelY = 0
gameState = "TITLE"  # Game starts with the title screen

# Seconds Counter - Kai ------------------------------------------------------------------------------
currentFrameTime = 0
lastFrameTime = 0
runningTime = 121000 # time left for player, + 1 second for the sake of seeing 120 seconds countdown, in milliseconds 

# Fish Stuff -----------------------------------------------------------------------------------------
fishList = []
fishType = 0

TUNA = 0
COD = 1
MAHI_MAHI = 2
STURGEON = 3


#-----------------------------------------------------------------------------------------------------
def setup():
    global boatX, boatY, seaLevelY, tunaSprite
    size(640, 480)
    boatX = width / 2
    seaLevelY = height * 30 / 100  # Adjusting sea level to 70%
    boatY = seaLevelY - boatHeight / 2
    
#-----------------------------------------------------------------------------------------------------
def draw():
    if gameState == "TITLE":
        drawTitleScreen()
    elif gameState == "GAME":
        runGame()
    
    # FOR DELTA TIME --------
    getLastFrameTime() # Kai - This is weird :( I can rework the time functions later, but this is needed for the countdown in the meantime

def drawTitleScreen():
    background(300)
    textSize(32)
    textAlign(CENTER, CENTER)
    text("Boat Game", width / 2, height / 2)

def runGame():
    global boatVelocity, rodLength
    background(120, 200, 200)  
    drawSea()
    drawBoat()

    drawRemainingTime() # SECONDS COUNTER UI -------

    if rodLowering:  # feel free to modify this part. this works, but doesn't really look pretty/organized I think?
        rodLength = min(rodLength + 1, maxRodLength)
    else:
        rodLength = max(rodLength - 1, 0)

    drawRod()
    if not rodLowering:  # this is to restrict boat from moving while rod is lowering, not sure if this is the most effiecient way
        moveBoat()
#-----------------------------------------------------------------------------------------------------
def drawSea():
    fill(0, 100, 150)  
    rect(0, seaLevelY, width, height - seaLevelY)

def drawBoat():
    fill(255, 50, 0)  
    rect(boatX - boatWidth / 2, boatY - boatHeight / 2, boatWidth, boatHeight)

def moveBoat():
    global boatX
    boatX += boatVelocity
    boatX = max(min(boatX, width - boatWidth / 2), boatWidth / 2)

#-----------------------------------------------------------------------------------------------------
def keyPressed():
    global boatVelocity, rodLowering, gameState, runningTime
    if gameState == "TITLE" and key == 's':
        gameState = "GAME"
    elif gameState == "GAME":
        if key == ' ':
            rodLowering = True
        if not rodLowering:
            if keyCode == LEFT:
                boatVelocity = -boatSpeed
            elif keyCode == RIGHT:
                boatVelocity = boatSpeed
#-----------------------------------------------------------------------------------------------------
def keyReleased():
    global boatVelocity, rodLowering
    if gameState == "GAME":
        if key == ' ':
            rodLowering = False
        if keyCode in [LEFT, RIGHT]:
            boatVelocity = 0

def drawRod():
    stroke(150)
    line(boatX, boatY, boatX, boatY + rodLength)
    
#-----------------------------------------------------------------------------------------------------
# SECONDS COUNTER UI ---------------------------------------------------------------------------------
def drawRemainingTime():
    global runningTime
    textAlign(RIGHT)
    fill(255)
    runningTime -= getLastFrameTime()
    text("Seconds Remaining: " + nf(runningTime/1000, 3), width - 15, 40) # Will format this better, but it does work
    
    # if runningTime/1000 <= 0:
    #     gameState = "GAMEOVER" 
    
# DELTA TIME FUNCTION --------------------------------------------------------------------------------
def getLastFrameTime():
    global currentFrameTime, lastFrameTime
    lastFrameTime = millis() - currentFrameTime
    currentFrameTime = millis()
    return lastFrameTime

# FISH CLASS -----------------------------------------------------------------------------------------
class Fish(object):
    def __init__(self, tempPos, tempDirection, tempVelocity, tempSprite, tempType):
        self.pos = tempPos
        self.direction = tempDirection
        self.velocity = tempVelocity
        self.sprite = tempSprite
        self.type = tempType
