#all hail king pygame
import pygame

#imports
import keyboard, math, random, time, win32api


#initialize pygame
pygame.init()

#calculate where to place pixels for the line / drawing method
def calculation(n, pos1, xdeviance, ydeviance,sample):
                return abs(math.ceil(pos1[0] + xdeviance*(n/(sample*2)))), abs(math.ceil(pos1[1] + (ydeviance*(n/(sample*2)))))
#the box blue shader effect (todo: make it run on the gpu)
def blur(grid):
    for wh in range(len(grid)-1):
            for ex in range(len(grid[wh])-1):
                lolr = 0
                lolg = 0
                lolb = 0
                for x in range(3):
                    for y in range(3):
                        lolr += grid[wh+(x-1)][ex+(y-1)][0]
                        lolg += grid[wh+(x-1)][ex+(y-1)][1]
                        lolb += grid[wh+(x-1)][ex+(y-1)][2]
                lolr /= 9
                lolg /= 9
                lolb /= 9
                grid[wh][ex][0] = lolr
                grid[wh][ex][1] = lolg
                grid[wh][ex][2] = lolb

#do some math to find the shit. probably dosent need its own function lol
def drawline(pos1,pos2,r,g,b):

    #editable variables
    samplesize = 50

    xdeviance = pos2[0] - pos1[0]
    ydeviance = pos2[1] - pos1[1]

    for n in range(samplesize*2):
        drawatlocation(calculation(n+1, pos1, xdeviance,ydeviance,samplesize),r,g,b)

#draw a square of size brush at specified location
def drawatlocation(position,r1,g1,b1):
    global grid
    global brush
    #bla bla bla 
    if not position[0] > len(grid)-math.ceil(brush/2) and not position[1] > len(grid[1])-math.ceil(brush/2):
        for x in range(brush):
            for y in range(brush):
                if not keyboard.is_pressed('b'):
                    grid[position[0]+(x-math.floor(brush/2))][position[1]+(y-math.floor(brush/2))] = [r1,g1,b1]
                else:
                    grid[position[0]+(x-math.floor(brush/2))][position[1]+(y-math.floor(brush/2))] = [0,0,0]

                    
#global vars here
fps = 60
#i hate pygame. all hail pygame
fpsClock = pygame.time.Clock()
#screen dimentions. you can change these and nothing breaks :)
width, height = 1080, 720

#initialize screen in pygame
screen = pygame.display.set_mode((width, height))

#set default brush colours
r1,g1,b1 = 0,0,255

#user set variables. pixel with margin is for convinience and sets how large the grid will eventually be. margin is margin and brush is brush size (slightly broken)
pixeltotal = 8
margin = 0
brush = 3

#some math. breaks if this isnt here
clickpos = pygame.mouse.get_pos()
ecks = math.floor(clickpos[0]/pixeltotal)
why = math.floor(clickpos[1]/pixeltotal)
cursorpos1 = [ecks,why]

#initialize the array with x and y, and set all the colours to white. able to adapt to new pixel sizes and screen widths/ heights
grid = []
for y in range(math.ceil(width/pixeltotal)+math.ceil(brush/2)+1):
    grid.append([])
    for x in range(math.ceil(height/pixeltotal)+math.ceil(brush/2)+1):
        #change this to [0,0,0] for a black background
        grid[y].append([255,255,255])


ticker = 0

# Game loop.
while True:
    #fill screen with black
    screen.fill((0, 0, 0))
    #check if user quits
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    #holy shit i am horrible at variable names
    #do this once every frame vs like 0 to 3827 times per frame
    clickpos = pygame.mouse.get_pos()
    ecks = math.floor(clickpos[0]/pixeltotal)
    why = math.floor(clickpos[1]/pixeltotal)
    cursorpos = [ecks,why]

    #if q, w, or e pressed, change brush colour to red, green or blue accordingly.
    if keyboard.is_pressed("q"):
        r1,g1,b1 = 255,0,0
    if keyboard.is_pressed("w"):
        r1,g1,b1 = 0,255,0
    if keyboard.is_pressed("e"):
        r1,g1,b1 = 0,0,255


    if pygame.mouse.get_pressed()[0]:
        if ticker < 0:
            cursorpos1 = cursorpos
            ticker = 10
        cursorpos2 = cursorpos
        drawline(cursorpos1,cursorpos2,r1,g1,b1)
        cursorpos1 = cursorpos2

    #god i hate pygame. sometimes pygame.mouse.getpressed just fuckin kills itself so i have to use this. also makes this windows only lmfao
    if win32api.GetKeyState(0x01)<0: #if mouse left button is pressed
        ticker = 5
    #tick the ticker
    if ticker >= 0:
        ticker -= 1



    #custom post processing algorithm. when space pressed iterate through each pixel and average the pixels around it in a box (box blur)
    if keyboard.is_pressed("space"):
        for wh in range(len(grid)-1):
            for ex in range(len(grid[wh])-1):
                #probably a way to do this in python without doing it 3 times per colour channel but im lazy
                lolr = 0
                lolg = 0
                lolb = 0
                for x in range(3):
                    for y in range(3):
                        lolr += grid[wh+(x-1)][ex+(y-1)][0]
                        lolg += grid[wh+(x-1)][ex+(y-1)][1]
                        lolb += grid[wh+(x-1)][ex+(y-1)][2]
                lolr /= 9
                lolg /= 9
                lolb /= 9
                grid[wh][ex][0] = lolr
                grid[wh][ex][1] = lolg
                grid[wh][ex][2] = lolb

    #draw the grid bla bla bla (should also be ran on gpu lol
    ycounter = 0
    for y in range(math.ceil(width/pixeltotal)):
        xcounter = 0
        for x in range(math.ceil(height/pixeltotal)):
            pygame.draw.rect(screen,grid[ycounter][xcounter],(1+(pixeltotal*y),(1+(x*pixeltotal)),pixeltotal-margin,pixeltotal-margin))
            xcounter += 1
        ycounter += 1

    #also draw brush colour in top left.
    pygame.draw.circle(screen, (r1,g1,b1), (20,20), 10)


    pygame.display.flip()
    fpsClock.tick(fps)
