import pygame
import random

########################################
#         Changeable Variables         #
########################################

#Size of the blobs
blobSize = 10

#Enable Random Coloured Blobs
randomColours = True

#Enable Random Trail Length (Has weird results)
randomTrailLength = False

#Enable Trail Fading
fadeTrail = False

#Remove Trail After x Trail Pixels
removeTrail = True
removeTrailAfter = 5

#Number of Blobs to create
numBlobs = 10

#Size of the Screen (px) - X
wSizeX = 1000

#Size of the Screen (px) - Y
wSizeY = 700

#Colour of the Background
bgColour = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
#bgColour = (255,255,255)

#Length of the Trail (Higher number = shorter)
#Will not be used if randomTrailLength is True
#Minimum value being 1
reduceInt = 1

########################################
#      End Of Changeable Variables     #
########################################


class Blob:
    def __init__(self, window, x, y, colour, size):
        self.window = window
        self.x = x
        self.y = y
        self.colour = colour
        self.size = size
        self.directx = 1
        self.directy = 1
        self.stepX = 5
        self.stepY = 5

    def draw(self):
        self.blob = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
        pygame.draw.rect(self.window, self.colour, self.blob)

    def makeTrail(self, reduceInt, fadeTrail):
        t = Trail(self.window, self.x, self.y, self.colour, self.size, reduceInt, fadeTrail)

    def move(self):
        self.x += self.stepX * self.directx
        self.y += self.stepY * self.directy

    def alterX(self):
        self.directx *= -1
        xOffset = random.randint(-2,2)
        if self.directx == -1: self.stepX -= xOffset
        else: self.stepX += xOffset
        if self.stepX >= 10: self.stepX -= random.randint(0,4)
        elif self.stepX <= -10: self.stepX += random.randint(0,4)
        
    def alterY(self):
        self.directy *= -1
        yOffset = random.randint(-2,2)
        if self.directy == -1: self.stepY -= yOffset
        else: self.stepY += yOffset
        if self.stepY >= 10: self.stepY -= random.randint(0,4)
        elif self.stepY <= -10: self.stepY += random.randint(0,4)

class Trail:
    trails = []
    def __init__(self, window, x, y, colour, size, reduceInt, fadable):
        self.window = window
        self.x = x
        self.y = y
        Trail.trails.append(self)
        self.colour = colour
        self.reduceInt = reduceInt
        self.trail=pygame.Rect(self.x, self.y, size[0], size[1])
        self.fadable = fadable
        self.fading = False
        if self.fadable: self.origColour = self.colour
        else: self.origColour = None

    def reduceColour(self):
        if not self.fadable:
            if (self.colour[0] <= 0) or (self.colour[1] <= 0) or (self.colour[2] <= 0): Trail.trails.remove(self)
            else:
                newC1 = self.colour[0] - self.reduceInt
                newC2 = self.colour[1] - self.reduceInt
                newC3 = self.colour[2] - self.reduceInt
                self.colour = (newC1, newC2, newC3)
            if (self.colour[0] <= 0) or (self.colour[1] <= 0) or (self.colour[2] <= 0):
                self.colour = (0,0,0)
            elif (self.colour[0] > 255) or (self.colour[1] > 255) or (self.colour[2] > 255):
                self.colour = (0,0,0)
        else:
            if self.fading and self.colour == self.origColour: Trail.trails.remove(self)
            elif self.fading and not self.colour == self.origColour:
                newC1 = self.colour[0] + self.reduceInt
                newC2 = self.colour[1] + self.reduceInt
                newC3 = self.colour[2] + self.reduceInt
                self.colour = (newC1, newC2, newC3)
            else:
                newC1 = self.colour[0] - self.reduceInt
                newC2 = self.colour[1] - self.reduceInt
                newC3 = self.colour[2] - self.reduceInt
                self.colour = (newC1, newC2, newC3)

            if not self.fading and ((self.colour[0] <= 0) or (self.colour[1] <= 0) or (self.colour[2] <= 0)) or ((self.colour[0] > 255) or (self.colour[1] > 255) or (self.colour[2] > 255)):
                self.fading = True
            

    def draw(self):
        self.reduceColour()
        pygame.draw.rect(self.window, self.colour, self.trail)


pygame.init()

window = pygame.display.set_mode((wSizeX, wSizeY))

blobs = []

def clearBoard():
    Trail.trails = []



for i in range(numBlobs):
    x, y = random.randint(10, wSizeX-10), random.randint(10, wSizeY-10)
    if randomColours:
        c = (random.randint(50,255),random.randint(50,255),random.randint(50,255))
    else: c = (255,255,255)

    #Give blobs random starting direction
    blobs.append(Blob(window, x, y, c, (blobSize, blobSize)))
    if random.randint(0,1) == 1:
        blobs[-1].directx *= -1
    if random.randint(0,1) == 1:
        blobs[-1].directy *= -1

def drawBlob(blobs, wsx, wsy):
    for blob in blobs:

        #Blob hits a wall, change the direction the blob moved (+ to - or - to +)
        if (blob.x+blobSize >= wSizeX) or (blob.x <= 0): blob.alterX()
        if (blob.y+blobSize >= wSizeY) or (blob.y <= 0): blob.alterY()
        
    
        blob.draw()
        blob.move()
        if randomTrailLength:
            blob.makeTrail(random.randint(0,5), fadeTrail)
        else: blob.makeTrail(reduceInt, fadeTrail)

def drawTrail():
    for trail in Trail.trails:
        trail.draw()

run = True
while run:
    pygame.time.Clock().tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c: clearBoard()
            elif event.key == pygame.K_q: run = False

    window.fill(bgColour)

    drawBlob(blobs, wSizeX, wSizeY)
    if removeTrail:
        if int(len(Trail.trails) / numBlobs) >= removeTrailAfter:
            clearBoard()
    
    drawTrail()

            
    pygame.display.flip()
pygame.quit()
