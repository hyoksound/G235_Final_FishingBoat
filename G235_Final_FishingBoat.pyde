# ------------- FISHING GAME--------------------------------
# Catch as many fish as you can within the time limit.
# CONTROLS -------------------------------------------------
#          SPACE BAR        = lower rod / RELEASE SPACE BAR = raise rod
#           S KEY           = continue / restart game
# LEFT AND RIGHT ARROW KEYS = Move the boat 
#-----------------------------------------------------------
# Global variables
boatX = 0 
boatY = 0
boatWidth, boatHeight = 60, 30
boatSpeed = 6
boatVelocity = 0
boatSprite = None
rodLowering = False  
rodLength = 0
maxRodLength = 300
ROD_SPEED = 1
seaLevelY = 0
fishCaught = 0
gameState = "TITLE"  

# Variables Handling Time
currentFrameTime = 0
lastFrameTime = 0
runningTime = 61000  # time left for player, + 1 second for the sake of seeing 120 seconds countdown, in milliseconds 
deltaTime = 0
timeUntilFish = 500  # start with 0.5 seconds before fish spawn, in milliseconds
fishTime = 0  # timer that keeps track of how many seconds has passed - needed to spawn more fish

# Fish Variables
fishList = []
fishType = 0

# Fish Image Sprites
tunaSprite = None
codSprite = None
mahiMahiSprite = None

# Fish Types
TUNA = 0
COD = 1
MAHI_MAHI = 2

def setup():
    global boatX, boatY, seaLevelY, FISH_SPRITE_SIZE, tunaSprite, codSprite, mahiMahiSprite, boatSprite
    size(640, 480)
    boatX = width / 2
    seaLevelY = height * 30 / 100  # Adjusting sea level to 70%
    boatY = seaLevelY - boatHeight / 2
    
    # Handle Fish Sprites
    FISH_SPRITE_SIZE = PVector(120, 68)  # Constant size for fish sprites
    tunaSprite = loadImage("Sprites/Tuna.png")
    codSprite = loadImage("Sprites/Cod.png")
    mahiMahiSprite = loadImage("Sprites/MahiMahi.png")
    
    # Handle Boat Sprite
    boatSprite = loadImage("Sprites/Boat.png")

def draw():
    global deltaTime
    if gameState == "TITLE":
        drawTitleScreen()
    elif gameState == "GAME":
        runGame()
        drawFishCount()
    elif gameState == "GAMEOVER":
        drawGameOverScreen()

    # Delta Time
    deltaTime = getLastFrameTime()
    
def drawTitleScreen():
    background(300)
    textSize(32)
    textAlign(CENTER, CENTER)
    text("Boat Game", width / 2, height / 2 - 16)
    textSize(20)
    text("Press S to Start", width / 2, height / 2 + 50)  
    
    # Drawing Fish + Boat for title screen
    pushStyle()
    imageMode(CENTER)
    image(boatSprite, width / 2, height * 4 / 5)
    image(tunaSprite, width / 2, height * 1 / 4)
    pushMatrix()
    translate(width * 3 / 4, height / 2)
    rotate(-PI/6)
    image(mahiMahiSprite, 0, 0)
    popMatrix()
    
    pushMatrix()
    translate(width * 1 / 4, height / 2)
    rotate(PI/5)
    image(codSprite, 0, 0)
    popMatrix()
    
    popStyle()
    

def runGame():
    global boatVelocity, rodLength
    background(120, 200, 200)
    drawSea()
    drawBoat()
    drawRemainingTime()

    if rodLowering:
        rodLength = min(rodLength + ROD_SPEED, maxRodLength)
    else:
        rodLength = max(rodLength - ROD_SPEED, 0)

    drawRod()
    if not rodLowering:
        moveBoat()
    # fish are flickering - idk maybe i can ask Zac abt it on Thursday
    timeToAddFish() # Starts fish timer which will then call addFish() once specified amount of time has passed
    drawFish()
    # DEBUG TEXT ----------------------------
    #fill(255)
    #textAlign(LEFT)
    #text("Number of Fish: " + str(len(fishList)), 20, 40)
    # ---------------------------------------

def drawGameOverScreen():
    background(0)
    fill(255, 0, 0)
    textSize(32)
    textAlign(CENTER, CENTER)
    text("Game Over", width / 2, height / 2 - 16)
    text("You caught " + str(fishCaught) + " fish", width / 2, height / 2 + 40)
    textSize(20)
    text("Press S to Restart", width / 2, height / 2 + 80) 
    pushStyle()
    imageMode(CENTER)
    image(tunaSprite, width / 2, height - FISH_SPRITE_SIZE.y * 4 / 3)
    popStyle()

def drawSea():
    pushStyle()
    noStroke()
    fill(0, 100, 150)
    rect(0, seaLevelY, width, height - seaLevelY)
    popStyle()

def drawBoat():
    #fill(255, 50, 0)
    #rect(boatX - boatWidth / 2, boatY - boatHeight / 2, boatWidth, boatHeight)
    pushStyle()
    imageMode(CENTER)
    image(boatSprite, boatX, boatY - 12) 
    popStyle()

def moveBoat():
    global boatX
    boatX += boatVelocity
    boatX = max(min(boatX, width - boatWidth / 2), boatWidth / 2)
    
# FISH FUNCTIONS -------------------------------------------------------------------------------------
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
            tempScale = -1  # flip sprite horizontally 
            tempVelocity = random(2, 7) * -1
            tempPosX = width
        
        tempPos = PVector(tempPosX, random(seaLevelY, height - FISH_SPRITE_SIZE.y))
       
        # Determine what type of fish -------- 
        tempType = int(random(0, 3))
        if tempType == TUNA:
            tempSprite = tunaSprite
        elif tempType == COD:
            tempSprite = codSprite
        elif tempType == MAHI_MAHI:
            tempSprite = mahiMahiSprite

        fishList.append(Fish(tempPos, tempScale, tempVelocity, tempSprite, tempType))

# Starts fish timer, calls addFish when specified amount of time has passed
def timeToAddFish():
    global fishTime
    fishTime += deltaTime
    if fishTime >= timeUntilFish:
        addFish(int(random(1, 3)))
        fishTime = 0
        
# Render the fish
def drawFish():
    for fish in fishList:
        fish.update()
        fish.render()
        
#-----------------------------------------------------------------------------------------------------
def keyPressed():
    global boatVelocity, rodLowering, rodLength, gameState, runningTime, fishCaught, fishList, fishTime
    if gameState == "TITLE" and key == 's':
        gameState = "GAME"
    elif gameState == "GAME":
        if key == ' ':
            rodLowering = True
        if not rodLowering and rodLength <= 10: # can only move when the rod is almost completely retracted
            if keyCode == LEFT:
                boatVelocity = -boatSpeed
            elif keyCode == RIGHT:
                boatVelocity = boatSpeed
    elif gameState == "GAMEOVER" and key == 's':
        gameState = "GAME"
        runningTime = 61000
        fishCaught = 0
        fishList = []
        fishTime = 0
        boatVelocity = 0
        rodLowering = False
        rodLength = 0

def keyReleased():
    global boatVelocity, rodLowering
    if gameState == "GAME":
        if key == ' ':
            rodLowering = False
        if keyCode in [LEFT, RIGHT]:
            boatVelocity = 0
#-----------------------------------------------------------------------------------------------------

def drawRod():
    stroke(150)
    line(boatX, boatY, boatX, boatY + rodLength)
    
# UI -------------------------------------------------------------------------------------------------
def drawRemainingTime():
    global runningTime, gameState 
    textAlign(RIGHT)
    fill(255)
    runningTime -= deltaTime
    if runningTime <= 0:
        gameState = "GAMEOVER"
        return
    text("Seconds Remaining: " + nf(runningTime / 1000, 2), width - 15, 40) # Will format this better, but it does work

def drawFishCount():
    textAlign(LEFT)
    fill(255)
    text(str(fishCaught) + " fish caught", 10, 30)

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
        self.isCaught = False 
        
    def update(self):
        # MINOR BUG: selfDeletion() running?? causes some fish sprites to flicker ? 
        self.selfDeletion()
        if not self.isCaught:
            self.pos.x += self.velocity
            self.collide()
        else:
            self.pos.y -= ROD_SPEED # fish moves up with the rod once caught
            
    def collide(self): # fish is in range of tip of rod
        if self.pos.x <= boatX and (self.pos.x + FISH_SPRITE_SIZE.x) >= boatX: 
            if self.pos.y <= (boatY + rodLength) and (self.pos.y + FISH_SPRITE_SIZE.y) >= (rodLength + boatY):
                self.isCaught = True
                
    def render(self):
        if self.scal > 0: # facing right
            image(self.sprite, self.pos.x, self.pos.y)
        else: # facing left, flip the sprite horizontally
            # Credit to https://discourse.processing.org/t/solved-question-about-flipping-images/7391
            pushMatrix()
            translate(self.pos.x + FISH_SPRITE_SIZE.x, self.pos.y)
            scale(self.scal, 1)
            image(self.sprite, 0, 0)
            popMatrix()
        #circle(self.pos.x, self.pos.y, self.sprite.height)
        if self.scal == 0:
            print("SCALE IS 0")
        
    def selfDeletion(self):
        global fishCaught
        if self.pos.x > width and self.velocity > 0 and self in fishList: # fish out of bounds to the right
            fishList.remove(self)
        elif self.pos.x < -FISH_SPRITE_SIZE.x and self.velocity < 0 and self in fishList: # fish out of bounds to the left
            fishList.remove(self)
        if (self.pos.y + FISH_SPRITE_SIZE.y / 2) <= boatY and self.isCaught and self in fishList: # fish reached the boat
            fishCaught += 1
            fishList.remove(self)
