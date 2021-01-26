import random 
import sys
import pygame
from pygame.locals import *

#Global variables initialisation  
FPS=32
SCREENWIDTH=289
SCREENHEIGHT=511
SCREEN=pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY=SCREENHEIGHT * 0.8
SPRITES={}
SOUNDS={}
PLAYER='gallery/sprites/bird.png'
BACKGROUND='gallery/sprites/background.png'
PIPE='gallery/sprites/pipe.png'

def welcomeScreen():
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - SPRITES['player'].get_height())/2)
    messagex = int((SCREENWIDTH - SPRITES['message'].get_width())/2) 
    messagey = int(SCREENHEIGHT*0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type== KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP ):
                return
            else:
                SCREEN.blit(SPRITES['background'],(0,0))
                SCREEN.blit(SPRITES['player'],(playerx , playery))
                SCREEN.blit(SPRITES['message'],(messagex, messagey))
                SCREEN.blit(SPRITES['base'],(basex , GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def mainGame():
    score= 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENHEIGHT/2)
    basex  = 0

    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    upperPipes = [
        {'x':SCREENWIDTH+200,'y':newPipe1[0]['y']},
        {'x':SCREENWIDTH+200+(SCREENWIDTH/2),'y':newPipe2[0]['y']},
    ]                
    lowerPipes = [
        {'x':SCREENWIDTH+200,'y':newPipe1[1]['y']},
        {'x':SCREENWIDTH+200+(SCREENWIDTH/2),'y':newPipe2[1]['y']},
    ] 

    pipeVelX = -4
    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1
    playerFlapAccv = -8
    playerFlapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    SOUNDS['wing'].play()

        crashTest = isCollide(playerx,playery,upperPipes,lowerPipes)
        if crashTest:
            return

        playerMidPos = playerx + SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + SPRITES['pipe'][0].get_width()/2
            if pipMidPos<= playerMidPos < pipeMidPos + 4:
                score +=1
                print(f"your score is {score}")
                SOUNDS['point'].play()
        if playerVelY <playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False            
        playerHeight = SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        # move pipes to the left
        for upperPipe , lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0<upperPipes[0]['x']<5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        # if the pipe is out of the screen, remove it
        if upperPipes[0]['x'] < -SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)
        
        # Lets blit our sprites now
        SCREEN.blit(SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(SPRITES['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
            Xoffset += SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery> GROUNDY - 25  or playery<0:
        SOUNDS['hit'].play()
        return True
    
    for pipe in upperPipes:
        pipeHeight = SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < SPRITES['pipe'][0].get_width()):
            SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < SPRITES['pipe'][0].get_width():
            SOUNDS['hit'].play()
            return True

    return False

def getRandomPipe():
    """
    Generate positions of two pipes(one bottom straight and one top rotated ) for blitting on the screen
    """
    pipeHeight = SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - SPRITES['base'].get_height()  - 1.2 *offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1}, #upper Pipe
        {'x': pipeX, 'y': y2} #lower Pipe
    ]
    return pipe


        



if __name__ == "__main__":
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Aniket chi Game!!')
    SPRITES['numbers'] = (
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha()
        
    )
    SPRITES['message']=pygame.image.load('gallery/sprites/message.png').convert_alpha()
    SPRITES['base']=pygame.image.load('gallery/sprites/base.png').convert_alpha()
    SPRITES['pipe']=(pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha() , 180),
    pygame.image.load(PIPE).convert_alpha()
    )
    SPRITES['background']=pygame.image.load(BACKGROUND).convert()
    SPRITES['message']=pygame.image.load(PLAYER).convert_alpha()    

    SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

    while True:
        welcomeScreen()
        mainGame()


    

