import pygame as pg
from pygame.locals import *
import numpy
from sense_hat import SenseHat
import time
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2

# library initialization
pg.init()
pg.mixer.init()

#             R    G    B
WHITE      = (255, 255, 255)
BLACK      = (  0,   0,   0)
RED        = (255,   0,   0)
GREEN      = (  0, 255,   0)
BLUE       = (  0,   0, 255)
YELLOW     = (255, 255,   0)
PURPLE     = (128,   0, 128)
PINK       = (255, 105, 180)
SANDYBROWN = (244, 164,  96)
LIGHTBLUE  = (173, 206, 230)

pixel = 36 # size of square
x = 0
y = 0
b = pixel
h = pixel
mud = 0
x_ball_old = - pixel
y_ball_old = - pixel
mud_aux = False
score_1 = 0
score_2 = 0
attempts = 0


sense = SenseHat()

# position of the ball in the maze
i_maze = 9
j_maze = 5

maze = numpy.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 1, 5, 0, 1, 1, 1, 1, 1, 4, 0],
                   [0, 6, 0, 0, 0, 1, 0, 13, 0, 0, 0],
                   [0, 1, 6, 6 ,14, 1, 0, 1, 1, 1, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                   [0, 1, 1, 2, 0, 1, 1, 12, 1, 1, 0],
                   [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
                   [0, 1, 0, 1, 1, 1, 0, 3, 0, 6, 0],
                   [0, 1, 0, 1, 0, 1, 0, 1, 0, 6, 0],
                   [0, 1, 1, 1, 0, 20, 0, 1, 1, 1, 0],
                   [0, 0, 0, 0, 0, 15, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

size = [512, 512]
screen = pg.display.set_mode(size) # screen creation
pg.display.set_caption('The Morest Betterest Game Ever') # name of the window


# THE GAME IS GOING TO STAAAAAAAAAAAAAART
pg.mixer.music.load("intro.mp3")
pg.mixer.music.play(-1)

clock = pg.time.Clock()

global FPSCLOCK, DISPLAYSURF, BASICFONT

FPSCLOCK = pg.time.Clock()
DISPLAYSURF = pg.display.set_mode((size[0], size[1]))
BASICFONT = pg.font.Font('freesansbold.ttf', 18)
pg.display.set_caption('The Morest Betterest Game Ever')

titleFont = pg.font.Font('freesansbold.ttf', 40)
titleSurf1 = titleFont.render('     THE MOREST BETTEREST     ', True, RED, BLUE)
titleSurf2 = titleFont.render('GAME EVER!!1!', True, RED)
titleSurf3 = titleFont.render('THE MOREST BTETEREST', True, GREEN)
titleSurf4 = titleFont.render('GAME EVER!!!!', True, GREEN)

degrees1 = 0
degrees3 = 0

#pg.event.get()  # clear out event queue

screen_1 = True # initial screen
while screen_1:
    DISPLAYSURF.fill(BLACK)
    rotatedSurf1 = pg.transform.rotate(titleSurf1, degrees1)
    rotatedRect1 = rotatedSurf1.get_rect()
    rotatedRect1.center = (size[0] / 2, size[1] / 2 - 50)
    DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)
    
    rotatedSurf2 = pg.transform.rotate(titleSurf2, degrees1)
    rotatedRect2 = rotatedSurf2.get_rect()
    rotatedRect2.center = (size[0] / 2, size[1] / 2 + 50)
    DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

    rotatedSurf3 = pg.transform.rotate(titleSurf3, degrees3)
    rotatedRect3 = rotatedSurf3.get_rect()
    rotatedRect3.center = (size[0] / 2, size[1] / 2 - 50)
    DISPLAYSURF.blit(rotatedSurf3, rotatedRect3)
    
    rotatedSurf4 = pg.transform.rotate(titleSurf4, degrees3)
    rotatedRect4 = rotatedSurf4.get_rect()
    rotatedRect4.center = (size[0]/ 2, size[1] / 2 + 50)
    DISPLAYSURF.blit(rotatedSurf4, rotatedRect4)
    
    pg.display.update()
    FPSCLOCK.tick(15)
    degrees1 += 6 # rotate by 7 degrees each frame
    degrees3 += 12 # rotate by 14 degrees each frame
    if degrees1 == 360:
        degrees1 = 0
    if degrees3 == 360:
        degrees3 = 0
        
    events = sense.stick.get_events()
    # to get out the game
    for event in events:
        if event.direction  == "middle":
            screen_1 = False

game_on = True
while game_on:  

    i_maze = 9
    j_maze = 5
    
    maze = numpy.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 1, 5, 0, 1, 1, 1, 1, 1, 4, 0],
                       [0, 6, 0, 0, 0, 1, 0, 13, 0, 0, 0],
                       [0, 1, 6, 6 ,14, 1, 0, 1, 1, 1, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                       [0, 1, 1, 2, 0, 1, 1, 12, 1, 1, 0],
                       [0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
                       [0, 1, 0, 1, 1, 1, 0, 3, 0, 6, 0],
                       [0, 1, 0, 1, 0, 1, 0, 1, 0, 6, 0],
                       [0, 1, 1, 1, 0, 20, 0, 1, 1, 1, 0],
                       [0, 0, 0, 0, 0, 15, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
    
    x = 0
    y = 0
    b = pixel
    h = pixel
    mud = 0
    x_ball_old = - pixel
    y_ball_old = - pixel
    timer = 45 # THIS IS THE TIME, NOTICE ME SENPAI!!!
    timer_aux = 0

             
    clock.tick(10) # the loop is limited to 10
    """
    for event in pg.event.get(): # the user did something
        if event.type == pg.QUIT: # close button pressed
            pg.quit() # aplication close
            sense.clear()"""
    
    screen.fill(LIGHTBLUE) # fill the screen in light blue color
    
    i = 0
    while (i < 11):
        j = 0
        y = (400 - pixel * 11) / 2 + i * pixel
        while (j < 11):
            x = (size[0] - pixel * 11) / 2 + j * pixel
            if maze[i][j] == 0:
                pg.draw.rect(screen, BLACK, [x, y, b, h]) # xmin, xmax, width, heigth
            elif maze[i][j] == 1:
                pg.draw.rect(screen, WHITE, [x, y, b, h])
            elif maze[i][j] == 2:
                pg.draw.rect(screen, WHITE, [x, y, b, h])
                pg.draw.circle(screen, BLUE, [x + pixel / 2, y + pixel / 2], pixel / 2)
            elif maze[i][j] == 3:
                pg.draw.rect(screen, WHITE, [x, y, b, h])
                pg.draw.circle(screen, YELLOW, [x + pixel / 2, y + pixel / 2], pixel / 2)
            elif maze[i][j] == 4:
                pg.draw.rect(screen, WHITE, [x, y, b, h])
                pg.draw.circle(screen, PURPLE, [x + pixel / 2, y + pixel / 2], pixel / 2)
            elif maze[i][j] == 5:
                pg.draw.rect(screen, WHITE, [x, y, b, h])
                pg.draw.circle(screen, GREEN, [x + pixel / 2, y + pixel / 2], + pixel / 2)
            elif maze[i][j] == 6:
                pg.draw.rect(screen, SANDYBROWN, [x, y, b, h])
            elif maze[i][j] == 12:
                pg.draw.rect(screen, BLUE, [x, y, b, h])
            elif maze[i][j] == 13:
                pg.draw.rect(screen, YELLOW, [x, y, b, h])
            elif maze[i][j] == 14:
                pg.draw.rect(screen, PURPLE, [x, y, b, h])
            elif maze[i][j] == 15:
                pg.draw.rect(screen, GREEN, [x, y, b, h])
                x_final = x + pixel / 2
                y_final = y + pixel / 2
            elif maze[i][j] == 20:
                pg.draw.rect(screen, WHITE, [x, y, b, h])
                x_ball = x + pixel / 2
                y_ball = y + pixel / 2
            j += 1
        i += 1
        
    pg.display.flip() # print the previous geometries
    
    
    
    # THE GAME HAS STARTEEEEEED!!
    screen_2 = True
    pg.mixer.music.load("game.mp3")
    pg.mixer.music.play(-1)
    while screen_2: 
    
        """for event in pg.event.get(): # the user did something
                if event.type == pg.QUIT: # close button pressed
                    screen_2 = False"""
                    
        # checks if the ball is in the mud
        if maze[i_maze][j_maze] == 6:
            mud = True
            if mud_aux == False:
                count = 0
                events = sense.stick.get_events()
                # to get out the game
                for event in events:
                    if event.direction  == "middle":
                        screen_2 = False
                        mud = False
                    while (count < 2):
                        events = sense.stick.get_events()
                        # to get out the game
                        for event in events:
                            if event.direction  == "middle":
                                screen_2 = False
                                mud = False
                                count = 2
                            if event.action == "released":
                                while event.action != "released":
                                    superaux = 1
                                count += 1                             
                        time.sleep(0.1)
                        timer_aux += 1
                        if timer_aux == 10:
                            timer -= 1
                            timer_aux = 0
                        pg.draw.rect(screen, LIGHTBLUE, [0, 420, 512, 80])
                        gameOverFont = pg.font.Font('freesansbold.ttf', 30)
                        overSurf = gameOverFont.render('TIME: %s' % (timer), True, WHITE)
                        overRect = overSurf.get_rect()
                        overRect.midtop = (512 / 2, 430)
                        DISPLAYSURF.blit(overSurf, overRect)
                        pg.display.update()
                        if timer == 0:
                            screen_2 = False
                    mud_aux = True
                    
        else:
            mud = 0
        
        # checks if the ball can move, and move it if possible
        events = sense.stick.get_events()  
        
        # to get out the game FATAL ERROR!
        """for event in events:
            if event.direction  == "middle":
                screen_2 = False"""
        if not mud or mud_aux:
            for event in events:
                if event.direction == 'right' and event.action != "released" and (maze[i_maze][j_maze + 1] < 7 and maze[i_maze][j_maze + 1] != 0 or maze[i_maze][j_maze + 1] == 20):
                    j_maze += 1
                    x_ball += pixel
                    mud_aux = False
                elif event.direction == 'up' and event.action != "released" and (maze[i_maze - 1][j_maze] < 7 and maze[i_maze - 1][j_maze] != 0 or maze[i_maze - 1][j_maze] == 20):
                    i_maze -= 1
                    y_ball -= pixel
                    mud_aux = False
                elif event.direction == 'left' and event.action != "released" and (maze[i_maze][j_maze - 1] < 7 and maze[i_maze][j_maze - 1] != 0 or maze[i_maze][j_maze - 1] == 20):
                    j_maze -= 1
                    x_ball -= pixel
                    mud_aux = False
                elif event.direction == 'down' and event.action != "released" and (maze[i_maze + 1][j_maze] < 7 and maze[i_maze + 1][j_maze] != 0 or maze[i_maze + 1][j_maze] == 20):
                    i_maze += 1
                    y_ball += pixel
                    mud_aux = False
             
        # open the door if the key is picked
        i = 0
        while (i < 11):
            j = 0
            while(j < 11):
                if maze[i][j] == maze[i_maze][j_maze] + 10:
                    x = (size[0] - pixel * 11) / 2 + j * pixel
                    y = (400 - pixel * 11) / 2 + i * pixel
                    pg.draw.rect(screen, WHITE, [x, y, b, h])
                    pg.display.flip()
                    maze[i][j] = 1 
                    timer_music_aux = 1
                j += 1
            i += 1
                  
        # print the new circle and delete the previous one
        if x_ball != x_ball_old or y_ball != y_ball_old:
            pg.draw.circle(screen, RED, [x_ball, y_ball], + pixel / 2)
            if not mud:
                pg.draw.circle(screen, WHITE, [x_ball_old, y_ball_old], + pixel / 2)
            else:
                pg.draw.circle(screen, SANDYBROWN, [x_ball_old, y_ball_old], + pixel / 2)
        pg.display.flip()
        x_ball_old = x_ball
        y_ball_old = y_ball

        time.sleep(0.1)
        timer_aux += 1
        if timer_aux == 10:
            timer -= 1
            timer_aux = 0
        
        pg.draw.rect(screen, LIGHTBLUE, [0, 420, 512, 80])
        gameOverFont = pg.font.Font('freesansbold.ttf', 30)
        overSurf = gameOverFont.render('TIME: %s' % (timer), True, WHITE)
        overRect = overSurf.get_rect()
        overRect.midtop = (512 / 2, 430)
        DISPLAYSURF.blit(overSurf, overRect)
        pg.display.update()    
        if x_ball == x_final and y_ball == y_final or timer == 0:
            screen_2 = False
     
     
    # THE GAME HAS ENDEEEEEED!! 
    if not attempts:
        score_1 = timer * 10
    else:
        score_2 = timer * 10
    attempts += 1
    
    if attempts == 1 and not score_1 or attempts == 2 and not score_2:
        pg.mixer.music.load("lose.mp3")
        pg.mixer.music.play()
    else:
        pg.mixer.music.load("victory.mp3")
        pg.mixer.music.play(0, 1.0) 
    
    screen.fill(BLACK)
    pg.display.flip()
    gameOverFont = pg.font.Font('freesansbold.ttf', 40)
    if attempts > 0:
        gameSurf = gameOverFont.render('First try', True, BLUE)
        overSurf = gameOverFont.render('Score 1: %s' % (score_1), True, WHITE)
        gameRect = gameSurf.get_rect()
        overRect = overSurf.get_rect()
        gameRect.midtop = (512 / 2, 60)
        overRect.midtop = (512 / 2, gameRect.height + 60 + 25)
        DISPLAYSURF.blit(gameSurf, gameRect)
        DISPLAYSURF.blit(overSurf, overRect)
        pg.display.update()
    if attempts > 1:
        gameSurf = gameOverFont.render('Second try', True, BLUE)
        overSurf = gameOverFont.render('Score 2: %s' % (score_2), True, WHITE)
        if score_1 >= score_2:
            bestSurf = gameOverFont.render('Your best: %s' % (score_1), True, RED)
        else:
            bestSurf = gameOverFont.render('Your best: %s' % (score_2), True, RED)
        gameRect = gameSurf.get_rect()
        overRect = overSurf.get_rect()
        bestRect = bestSurf.get_rect()
        gameRect.midtop = (512 / 2, 60 + 150)
        overRect.midtop = (512 / 2, gameRect.height + 60 + 175)
        bestRect.midtop = (512 / 2, gameRect.height + 60 + 275)
        DISPLAYSURF.blit(gameSurf, gameRect)
        DISPLAYSURF.blit(overSurf, overRect)
        DISPLAYSURF.blit(bestSurf, bestRect)
        pg.display.update()
    time.sleep(5)
    
    if attempts == 2:
        pg.mixer.music.load("unicorn.mp3")
        pg.mixer.music.play(-1)
        screen.fill(PURPLE)        
        gameOverFont = pg.font.Font('Love_and_Passion.ttf', 40)
        heart1Surf = gameOverFont.render('OoOoOoOoOoOoOoOoOoOoO', True, PINK)
        gameSurf = gameOverFont.render('Follow your heart and', True, PINK)
        overSurf = gameOverFont.render('chase your dreams', True, PINK)
        heart2Surf = gameOverFont.render('OoOoOoOoOoOoOoOoOoOoO', True, PINK)
        heart1Rect = heart1Surf.get_rect()
        gameRect = gameSurf.get_rect()
        overRect = overSurf.get_rect()
        heart2Rect = heart2Surf.get_rect()
        heart1Rect.midtop = (512 / 2, 120 - 75)
        gameRect.midtop = (512 / 2, 120)
        overRect.midtop = (512 / 2, gameRect.height + 120 + 75)
        heart2Rect.midtop = (512 / 2, gameRect.height + 120 + 75 + 75)
        DISPLAYSURF.blit(heart1Surf, heart1Rect)
        DISPLAYSURF.blit(gameSurf, gameRect)
        DISPLAYSURF.blit(overSurf, overRect)
        DISPLAYSURF.blit(heart2Surf, heart2Rect)

        gameOverFont = pg.font.Font('Love_and_Passion.ttf', 90)
        heart3Surf = gameOverFont.render('O', True, PINK)
        heart3Rect = heart3Surf.get_rect()
        heart3Rect.midtop = (512 / 2, gameRect.height + 80)
        DISPLAYSURF.blit(heart3Surf, heart3Rect)
          
        pg.display.flip()
        time.sleep(5)
        
        # picture
        camera = PiCamera()
        camera.resolution = (640, 480)
        camera.framerate = 32
        camera.rotation = 180
        camera.hflip = True
        rawCapture = PiRGBArray(camera, size=(640, 480))
        
        time.sleep(0.1)
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            image = frame.array         
            cv2.imshow("Previsualizacion", image)  
            key = cv2.waitKey(1) & 0xFF  
            rawCapture.truncate(0)
            if key == ord("q"):
                 cv2.imwrite("BestPlayerEver.jpg",image)
                 break
        camera.close()
        cv2.destroyWindow("Previsualizacion") 
        camera.stop_preview()           
        
        screen_3 = True
        while screen_3:
            absolutelyuselessvariable = 0
                
# close aplications
pg.quit()
sense.clear()

"""
# something important
if __name__ == '__main__':
    main()"""
    