import pygame
import time
import random
pygame.init()

#colors
white = (255,255,255)
black = (0,0,0)
dark_gray = (64,64,64)
gray = (128,128,128)
light_gray = (192,192,192)
red = (255,0,0)
blue = (0,0,255)
green = (0,255,0)
dark_blue = (0,0,102)
dark_green = (0,120,0)

#bounds of the window
display_width = 800
display_height = 600
dis = pygame.display.set_mode((display_width,display_height))

#first update
pygame.display.update()

#title
pygame.display.set_caption('Game')

block_size = 10

clock = pygame.time.Clock()


#display messages
font_style = pygame.font.SysFont(None, 30)

def messageScore(msg,color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [10, 30])

def messageFail1(msg,color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [100, display_height/3])

def messageFail2(msg,color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [100, display_height/2])


#_____________________________________________________________________________________________________________________________________________________________________
#The game
def gameLoop(): 
    
    stage = 1
    points = 0
    game_over = False
    game_close = False

    #INITIALIZING VARIABLES
    #starting location
    x1 = display_width/2
    y1 = display_height/2


    x1_change = 0
    y1_change = 0

    #food
    foodx = round(random.randrange(0, display_width - block_size) / 10.0) * 10.0
    foody = round(random.randrange(0, display_height - block_size) / 10.0) * 10.0


    #create walls
    wallx = 0
    wally = 0
    
    #direction
    up = False
    down = False
    right = False
    left = False
    
    jump = False        

    #block speed
    block_speed = 10

    #looping pygame window so it doesn't instantly close
    while not game_over:
        

        #exiting sequence
        while game_close == True:
            dis.fill(dark_gray)
            messageFail1("Game Over!", red)
            messageFail2("Press Q to quit or E to play again", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_e:
                        gameLoop()


        for event in pygame.event.get():

            #exiting the game
            if event.type == pygame.QUIT:
                game_over = True
            #if a key is pressed
            if event.type == pygame.KEYDOWN:
                #left
                if event.key == pygame.K_a: 
                    x1_change = -block_size
                    y1_change = 0
                    left = True
                    right = False
                    up = False
                    down = False
                #right
                if event.key == pygame.K_d:
                    x1_change = block_size
                    y1_change = 0
                    left = False
                    right = True
                    up = False
                    down = False
                #up and down are inversed for some reason
                #up
                if event.key == pygame.K_w:
                    x1_change = 0
                    y1_change = -block_size 
                    left = False
                    right = False  
                    up = True
                    down = False
                #down
                if event.key == pygame.K_s:
                    x1_change = 0
                    y1_change = block_size
                    left = False
                    right = False  
                    up = False
                    down = True
                
                #jumping
                if event.key == pygame.K_SPACE:
                    if left == True:
                        print("left")
                        x1_change = -(block_size*5)
                        y1_change = 0
                        jump = True
                    elif right == True:
                        print("right")
                        x1_change = block_size*5
                        y1_change = 0
                        jump = True
                    elif up == True:
                        print("up")
                        x1_change = 0
                        y1_change = -(block_size*5)                    
                        jump = True
                    elif down == True:
                        print("down")
                        x1_change = 0
                        y1_change = block_size*5                   
                        jump = True
                    pygame.display.update()
        #if the player runs out of bounds
        if x1 >= display_width or x1 < 0 or y1 >= display_height or y1 < 0:
            game_close = True

        #where the change to the player happens
        x1 += x1_change
        y1 += y1_change

        #returning the speed back to normal after jumping
        if jump == True:
            if left == True:
                x1_change = -block_size
                y1_change = 0
                jump = False
            if right == True:
                x1_change = block_size
                y1_change = 0
                jump = False
            if up == True:
                x1_change = 0
                y1_change = -block_size
                jump = False
            if down == True:
                x1_change = 0
                y1_change = block_size
                jump = False

        #changing the background color
        if points >= 0 and points < 3:
            dis.fill(light_gray)
        elif points >= 3 and points < 5:
            dis.fill(red)
        elif points >= 5 and points < 10:
            dis.fill(white)
        elif points >= 10 and points < 15:
            dis.fill(dark_green)
        elif points >= 15 and points < 20:
            dis.fill(dark_blue)

        #STAGE 1
        if stage == 1:

            messageFail1("Stage 1", green)
            pygame.display.update()
            #starting the wall's movement
            if wallx == 0:
                forward = True
            
            #moving the wall forward at 10 speed
            if forward == True:
                wallx += 10
            
            def theWall():
                for i in range(0, display_height, 40):
                    pygame.draw.rect(dis,dark_gray,[wallx, i, block_size*2, block_size])
                    #if player runs into walls
                    if x1 == wallx and y1 == i or x1 == wallx + 10 and y1 == i:
                        return True

            #once wall reaches end
            if wallx >= display_width:
                forward = False

            if forward == False:
                wallx -= 10

            theWall()

            if theWall() == True:
                game_close = True

            if points == 3:
                stage += 1

        #STAGE 2
        elif stage == 2:
            messageFail1("Stage 2", green)
            pygame.display.update()

            #starting the wall's movement
            if wally == 0:
                forward = True

            #moving the wall forward at 10 speed
            if forward == True:
                wally += 10

            def theWall():
                for i in range(0, display_width, 40):
                    pygame.draw.rect(dis,dark_gray,[i, wally, block_size, block_size*2])
                    #if player runs into walls
                    if x1 == i and y1 == wally or x1 == i and y1 == wally + 10:
                        return True

            #once wall reaches end
            if wally >= display_height:
                forward = False

            if forward == False:
                wally -= 10

            theWall()

            if theWall() == True:
                game_close = True

            if points == 5:
                wallx = 0
                wally = 0
                stage += 1
                block_speed = 10


        #STAGE 3
        elif stage == 3:
            messageFail1("Stage 3", green)
            pygame.display.update()


           #starting the wall's movement
            if wallx == 0:
                forward = True
            
            #moving the wall forward at 10 speed
            if forward == True:
                wallx += 40
            
            #diagonal
            def theWall(xAxis):

                theReturn = False

                for i in range(0, display_height, 40):
                    if theReturn == False:
                        pygame.draw.rect(dis,dark_gray,[xAxis, i, block_size*2, block_size])
                        xAxis +=40

                    elif theReturn == True:
                        pygame.draw.rect(dis,dark_gray,[display_width - xAxis, i, block_size*2, block_size])
                        xAxis -=40

                    #if player runs into walls
                    if x1 == xAxis and y1 == i or x1 == xAxis + 10 and y1 == i:
                        return True

                if xAxis >= display_width:
                    theReturn = True

            #once wall reaches end
            if wallx >= display_width/3-30:
                forward = False

            if forward == False:
                wallx -= 40

            theWall(wallx)
            pygame.display.update()

            if theWall(wallx) == True:
                game_close = True

            if points == 10:
                wallx = 0
                wally = 0
                stage += 1
                block_speed = 10

        #STAGE 4
        elif stage == 4:
            messageFail1("Stage 4", green)
            pygame.display.update()

            #10
            if points >= 10:
                def theWall10():
                    for i in range(0,display_width):
                        pygame.draw.rect(dis,dark_gray,[300, i, block_size, block_size])

                        if x1 == 300 and y1 == i:
                            return True

                pygame.display.update()

                if theWall10() == True:
                    game_close = True

                #11
                if points >= 11:
                    def theWall11():
                        for i in range(0,display_width):
                            pygame.draw.rect(dis,dark_gray,[500, i, block_size, block_size])
                            if x1 == 500 and y1 == i:
                                return True

                    pygame.display.update()

                    if theWall11() == True:
                        game_close = True

                    #12
                    if points >= 12:
                        def theWall12():
                            for i in range(0,display_width):
                                pygame.draw.rect(dis,dark_gray,[i, 300, block_size, block_size])
                                if x1 == i and y1 == 300:
                                    return True

                        pygame.display.update()

                        if theWall12() == True:
                            game_close = True

                        #13
                        if points >= 13:
                            def theWall13():
                                for i in range(0,display_width):
                                    pygame.draw.rect(dis,dark_gray,[i, i, block_size, block_size])
                                    if x1 == i and y1 == i:
                                        return True

                            theWall13()
                            pygame.display.update()

                            if theWall13() == True:
                                game_close = True

                            #14
                            if points >= 14:
                                def theWall14():
                                    for i in range(0,display_width):
                                        pygame.draw.rect(dis,dark_gray,[i, 500, block_size, block_size])
                                        if x1 == i and y1 == 500:
                                            return True

                                pygame.display.update()

                                if theWall14() == True:
                                    game_close = True

                                if points == 15:
                                    block_speed = 10
                                    stage +=1

        #STAGE 5
        elif stage == 5:
            if points == 15:
                block_speed += 1
                if block_speed == 200:
                    block_speed -= 1
            if points == 16:
                block_speed -= 1

        #STAGE 6



        #character
        pygame.draw.rect(dis,black,[x1, y1, block_size, block_size])

        #creating food
        pygame.draw.rect(dis,blue,[foodx, foody, block_size, block_size])

        #updating the score
        pointsInString = str(points)
        pointsVisual = "Score: " + pointsInString
        messageScore(pointsVisual, green)

        pygame.display.update()


        #if the block eats food
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, display_width - block_size) / 10.0) * 10.0
            foody = round(random.randrange(0, display_height - block_size) / 10.0) * 10.0
            block_speed += 5
            points += 1
            pygame.display.update()
            time.sleep(1)


        clock.tick(block_speed)
 
    pygame.quit()
    quit()
gameLoop()