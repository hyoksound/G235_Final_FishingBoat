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
deltaTime = 0
timeUntilFish = 500 # start with 0.5 seconds before fish spawn, in milliseconds
fishTime = 0 # timer that  keeps track of how many seconds has passed - needed to spawn more fish

# Fish Variables -------------------------------------------------------------------------------------
fishList = []
fishType = 0

tunaSprite = None
codSprite = None
mahiMahiSprite = None

TUNA = 0
COD = 1
MAHI_MAHI = 2
#STURGEON = 3

#-----------------------------------------------------------------------------------------------------
def setup():
    global boatX, boatY, seaLevelY, FISH_SPRITE_SIZE, tunaSprite, codSprite, mahiMahiSprite
    size(640, 480)
    boatX = width / 2
    seaLevelY = height * 30 / 100  # Adjusting sea level to 70%
    boatY = seaLevelY - boatHeight / 2
    
    # Handle Fish Sprites ------------------------------------
    FISH_SPRITE_SIZE = PVector(120, 68) # Constant for size, will need for collision 
    
    tunaSprite = loadImage("Sprites/Tuna.png")
    codSprite = loadImage("Sprites/Cod.png")
    mahiMahiSprite = loadImage("Sprites/MahiMahi.png")
    
#-----------------------------------------------------------------------------------------------------
def draw():
    global deltaTime
    if gameState == "TITLE":
        drawTitleScreen()
    elif gameState == "GAME":
        runGame()
    
    # FOR DELTA TIME --------
    deltaTime = getLastFrameTime() # needed for the countdown / other timing stuff

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
        
    # HAVE TO RENDER FISH LAST OR ELSE THINGS WILL FLICKER?? idk maybe i can ask Zac abt it on Thursday
    timeToAddFish()
    drawFish()
    # DEBUG TEXT ----------------------------
    #fill(255)
    #textAlign(LEFT)
    #text("Number of Fish: " + str(len(fishList)), 20, 40)
    # ---------------------------------------
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

# Add new fish (Kai) ----------------------------------
def addFish(fishCount):
    global fishList
    for i in range(fishCount):
        # Determine which way the fish will face ------
        tempDirection = int(random(1, 3))

        if tempDirection == 1:
            tempScale = 1
            tempVelocity = random(2, 7)
            tempPosX = -FISH_SPRITE_SIZE.x
        else:
            tempScale = -1 # flip sprite horizontally 
            tempVelocity = random(2, 7) * -1 
            tempPosX = width
        
        tempPos = PVector(tempPosX, random(height  * 3/10, height - FISH_SPRITE_SIZE.y)) # above bottom of screen to below sea lvl
        
        # Determine what type of fish --------
        tempType = int(random(0, 3))
        if tempType == TUNA:
            tempSprite = tunaSprite
        elif tempType == COD:
            tempSprite = codSprite
        elif tempType == MAHI_MAHI:
            tempSprite = mahiMahiSprite

        fishList.append(Fish(tempPos, tempScale, tempVelocity, tempSprite, tempType))

def timeToAddFish(): # sorry the name is a bit stupid, needs a timer for adding more fish into the scene
    global fishTime
    fishTime += deltaTime
    if fishTime >= timeUntilFish: # 0.5 seconds has passed, add another fish
        addFish(int(random(1, 3))) # Add between 1-2 fish every 0.5 seconds
        fishTime = 0 # reset timer

# Draw Fish - Kai -----------------------------
def drawFish():
    for fish in fishList:
        fish.render()
        fish.update()
        
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
    runningTime -= deltaTime
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
    def __init__(self, tempPos, tempScale, tempVelocity, tempSprite, tempType):
        self.pos = tempPos
        self.scal = tempScale
        self.velocity = tempVelocity
        self.sprite = tempSprite
        self.type = tempType
        self.isCaught = False # flag for being caught
        
    def update(self):
        # MINOR BUG: selfDeletion() running causes some fish sprites to flicker ? 
        self.selfDeletion()
        
        if not self.isCaught:
            self.pos.x += self.velocity
            self.collide()
        else: 
            self.pos.y -= 1 # fish moves up with the rod, could be a variable so we can adjust the rod speed
            
    def collide(self):
        if self.pos.x <= boatX and (self.pos.x + FISH_SPRITE_SIZE.x) >= boatX:
            if self.pos.y <= (boatY + rodLength) and (self.pos.y + FISH_SPRITE_SIZE.y) >= (rodLength + boatY):
                self.isCaught = True
        
    def render(self):
        if self.scal > 0: # facing right
            image(self.sprite, self.pos.x, self.pos.y)
        else:
            # Credit to https://discourse.processing.org/t/solved-question-about-flipping-images/7391
            pushMatrix()
            translate(self.pos.x + FISH_SPRITE_SIZE.x, self.pos.y)
            scale(self.scal, 1)
            image(self.sprite, 0, 0)
            popMatrix()
        
    def selfDeletion(self):
        if self.pos.x > width + 300 and self in fishList: # moving right
            fishList.remove(self)
        elif self.pos.x < -300 and self in fishList: # moving left
            fishList.remove(self)
            
        if (self.pos.y + FISH_SPRITE_SIZE.y / 2) <= boatY and self.isCaught and self in fishList: 
            # TODO: INCREASE FISH CAUGHT COUNTER  !
            fishList.remove(self)
