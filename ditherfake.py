#all hail king pygame
import pygame



#imports
import numpy as np

#copy this into cmd:   "pip install numpy keyboard pyopencl"

import math, keyboard
import pyopencl as cl



#gpu shader code. uses opencl and then some c code to run on the gpu. makes this box blur code a lot faster, by a factor of about 60x
platforms = cl.get_platforms()
ctx = cl.Context(
    dev_type = cl.device_type.ALL,
    properties=[(cl.context_properties.PLATFORM, platforms[0])]
)
"""
    +----------------------------------+
   /                                  /
  /                                  x
 /                                  /
+----------------------------------+
|                                  |
|                                  |
y                                  |
|                                  |
|                                  |
+----------------c-----------------+
"""


prg = cl.Program(ctx, """
    __kernel void balls(
        __global const uchar *arraying, __global uchar *res_g
        ) {
            int width = get_global_size(0);
            int height = get_global_size(1);
            int channels = get_global_size(2);
            int weird_size = height * channels;

            int x = get_global_id(0);
            int y = get_global_id(1);
            int c = get_global_id(2);

            int id = c + y*channels + x*weird_size;


            int lolr = 0;

            for (int ex = (x-2); ex <= (x+2); ex++)
            for (int wh = (y-2); wh <= (y+2); wh++)
                lolr += arraying[c + wh*channels + ex*weird_size];



            lolr /= 25;

            res_g[id] = lolr;
            //res_g[id] = (uchar)id;

        }
    __kernel void balls2(
        __global const uchar *arraying, __global uchar *res_g
        ) {
            int width = get_global_size(0);
            int height = get_global_size(1);
            int channels = get_global_size(2);
            int weird_size = height * channels;

            int x = get_global_id(0);
            int y = get_global_id(1);
            int c = get_global_id(2);

            int id = c + y*channels + x*weird_size;


            int lolr = 0;

            for (int ex = (x-1); ex <= (x); ex++)
            for (int wh = (y-1); wh <= (y); wh++)
                lolr = arraying[c + wh*channels + ex*weird_size];
                res_g[id] = ((lolr << 1) * 2) >> 1;
            //res_g[id] = (uchar)id;

        }
    """).build()

queue = cl.CommandQueue(ctx)
mf = cl.mem_flags


#initialize pygame
pygame.init()

#calculate where to place pixels for the line / drawing method
def calculation(n, pos1, xdeviance, ydeviance,sample):
                return abs(math.ceil(pos1[0] + xdeviance*(n/(sample*2)))), abs(math.ceil(pos1[1] + (ydeviance*(n/(sample*2)))))
#the box blue shader effect (todo: make it run on the gpu)


def blur(array):
    arraying = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=array)
    res_g = cl.Buffer(ctx, mf.WRITE_ONLY, array.nbytes)
    knl = prg.balls
    knl(queue, array.shape, None, arraying, res_g)

    res_np = np.empty_like(array)
    cl.enqueue_copy(queue,res_np,res_g)

    nuts = res_np.reshape(array.shape, order='C').astype('uint8')
    return nuts


    """
    array_bad = array.ravel()
    width = array.shape[0]
    height = array.shape[1]
    channels = array.shape[2]
    weird_size = height * channels
    for x in range(width-1):
        for y in range(height-1):
            for c in range(channels):
                    lolr = 0
                    for ex in range(x-1, x+2):
                        for wh in range(y-1, y+2):
                            lolr += array_bad[c + wh*channels + ex*weird_size]
                    lolr /= 9
                    array_bad[c + y*channels + x*weird_size] = lolr

    return array_bad.reshape(array.shape)
    """

def dither(array):
    arraying = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=array)
    res_g = cl.Buffer(ctx, mf.WRITE_ONLY, array.nbytes)
    knl = prg.balls2
    knl(queue, array.shape, None, arraying, res_g)

    res_np = np.empty_like(array)
    cl.enqueue_copy(queue,res_np,res_g)

    nuts = res_np.reshape(array.shape, order='C').astype('uint8')
    return nuts

def fps_counter():
        fps = str(int(fpsClock.get_fps()))
        fps_t = font.render(fps , 1, pygame.Color("RED"))
        screen.blit(fps_t,(0,30))


#do some math to find the shit. probably dosent need its own function lol
def drawline(pos1,pos2,r,g,b):
    xdeviance = pos2[0] - pos1[0]
    ydeviance = pos2[1] - pos1[1]
    global brush
    #editable variables
    if brush < 9:
        samplesize = 10
    else:
         samplesize = math.ceil(abs(xdeviance+ydeviance)/10)


    for n in range(samplesize*2):
        drawatlocation(calculation(n+1, pos1, xdeviance,ydeviance,samplesize),r,g,b)

#draw a square of size brush at specified location
def drawatlocation(position,r1,g1,b1):
    global array
    global brush
    #bla bla bla
    if not position[0] > len(array)-math.ceil(brush/2) and not position[1] > len(array[1])-math.ceil(brush/2):
        for x in range(brush):
            for y in range(brush):
                if not keyboard.is_pressed('b'):
                    array[position[0]+(x-math.floor(brush/2))][position[1]+(y-math.floor(brush/2))] = [r1,g1,b1]
                else:
                    array[position[0]+(x-math.floor(brush/2))][position[1]+(y-math.floor(brush/2))] = [0,0,0]


#global vars here
fps = 60
#i hate pygame. all hail pygame
fpsClock = pygame.time.Clock()
#screen dimentions. you can change these and nothing breaks :)
width, height = 1080, 720

#initialize screen in pygame
screen = pygame.display.set_mode((width, height))

#set default brush colours
r1,g1,b1 = 122,233,255

#user set variables. pixel with margin is for convinience and sets how large the array will eventually be. margin is margin and brush is brush size (slightly broken)
pixeltotal = 15
margin = 0
brush = 2

#some math. breaks if this isnt here
clickpos = pygame.mouse.get_pos()
ecks = math.floor(clickpos[0]/pixeltotal)
why = math.floor(clickpos[1]/pixeltotal)
cursorpos1 = [ecks,why]

#initialize the array with x and y, and set all the colours to white. able to adapt to new pixel sizes and screen widths/ heights

grid = []
for x in range( width): #math.ceil(width/pixeltotal)+math.ceil(brush/2)+1):
    grid.append([])
    for y in range( height):#math.ceil(height/pixeltotal)+math.ceil(brush/2)+1):
        #change this to [0,0,0] for a black background
        grid[x].append([0,0,0])



array = np.array(grid, dtype="uint8", order='C' )
#array = np.zeros((width, height, 3), dtype="uint8", order='C' )

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
            cursorpos1 = clickpos
            #cursorpos1 = cursorpos
            ticker = 10
        cursorpos2 = clickpos
        drawline(cursorpos1,cursorpos2,r1,g1,b1)
        cursorpos1 = cursorpos2





    if pygame.mouse.get_pressed()[0]: #if mouse left button is pressed
        ticker = 5
    #tick the ticker
    if ticker >= 0:
        ticker -= 1



    #custom post processing algorithm. when space pressed iterate through each pixel and average the pixels around it in a box (box blur)
    if keyboard.is_pressed("space"):
         array = blur(array)

    if keyboard.is_pressed("k"):
         array = dither(array)


    #draw the array bla bla bla (should also be ran on gpu lol)
    """
    ycounter = 0
    for y in range(math.ceil(width/pixeltotal)):
        xcounter = 0
        for x in range(math.ceil(height/pixeltotal)):
            pygame.draw.rect(screen,array[ycounter][xcounter],(1+(pixeltotal*y),(1+(x*pixeltotal)),pixeltotal-margin,pixeltotal-margin))
            xcounter += 1
        ycounter += 1
    """
    pygame.surfarray.blit_array(screen, array)


    #also draw brush colour in top left.
    pygame.draw.circle(screen, (r1,g1,b1), (20,20), 10)
    font = pygame.font.SysFont("Arial" , 18 , bold = True)

    fps_counter()

    pygame.display.flip()
    fpsClock.tick(fps)
