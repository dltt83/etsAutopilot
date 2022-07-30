import time
import pyautogui
import cv2
import keyboard
import numpy as np
import pygame
from PIL import Image

global run 
global quitLoop
global LEFT_BASE
global RIGHT_BASE

# define booleans for control flow
run = False
quitLoop = False
# initialise base position variables as constants
LEFT_BASE = 110
RIGHT_BASE = 42


#define hotkey functions
def changeRun():
    global run
    run = not run
# END DEF

def stopLoop():
    global quitLoop
    quitLoop = True
# END DEF


##### TEST FUNCTION to take screenshots of corrent region for use for openCV testing
global ssNum
ssNum = 0
def getSaveSS():
    global ssNum
    ssNum += 1

    start = time.perf_counter()
    image = pyautogui.screenshot(region=(750, 514, 320, 100))
    image.save("testImage" + str(ssNum) + ".png")

    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    cv2.imwrite("testImageGRAY" + str(ssNum) + ".png", img)

    aveXL, aveXR, frameBW = processImage(img)
    cv2.imwrite("testImageBW" + str(ssNum) + ".png", frameBW)
    end = time.perf_counter()

    print(end-start)
# END DEF

def updateDisplay(win, frame, aveXL, aveXR):
    win.fill((0, 0, 0))

    img = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
    im_pil = Image.fromarray(img)

    py_image = pygame.image.fromstring(im_pil.tobytes(), im_pil.size, im_pil.mode)

    win.blit(py_image, (0,0))

    pygame.draw.rect(win, (255, 0, 0), pygame.Rect(aveXL, 0, 1, 100))
    pygame.draw.rect(win, (255, 0, 0), pygame.Rect(aveXR+200, 0, 1, 100))
    pygame.draw.rect(win, (0, 255, 0), pygame.Rect(200, 0, 1, 100))
    
    pygame.display.update()
# END DEF


def processImage(frame, win):
    (thresh, frameBW) = cv2.threshold(frame, 180, 255, cv2.THRESH_BINARY)


    leftSide = frameBW[0:100, 0:200]
    rightSide = frameBW[0:100, 201:320]

    # find average x position of white pixels
    aveXL = 0
    whtNum = 0
    for y in range(len(leftSide)):
        for x in range(len(leftSide[0])):
            if leftSide[y][x] == 255:
                aveXL = aveXL + x
                whtNum += 1
    #END FOR

    aveXR = 0
    whtNum = 0
    for y in range(len(rightSide)):
        for x in range(len(rightSide[0])):
            if rightSide[y][x] == 255:
                aveXR = aveXR + x
                whtNum += 1
    # END FOR

    if whtNum > 0:
        aveXL = aveXL / whtNum
        aveXR = aveXR / whtNum
    else:
        aveXL = LEFT_BASE
        aveXR = RIGHT_BASE
    # END IF

    updateDisplay(win, frameBW, aveXL, aveXR)
    return aveXL, aveXR #, frameBW
# END DEF


# set hotkeys
keyboard.add_hotkey("p", lambda: changeRun())
keyboard.add_hotkey("l", lambda: stopLoop())
keyboard.add_hotkey("o", lambda: getSaveSS())


# main function
def main():
    # start pygame display
    pygame.init()
    win = pygame.display.set_mode((320, 100))
    pygame.display.update()

    # add global variables
    global run, quitLoop, LEFT_BASE, RIGHT_BASE

    # start loop
    while not quitLoop:
        if run:
            print("running")

            ##### do calculations

            # get image
            screenshot = pyautogui.screenshot(region=(750, 514, 320, 100))
            # convert to np and grayscale
            frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

            # process image
            aveXL, aveXR = processImage(frame, win)

            # determine action
            lOffset = aveXL - LEFT_BASE
            rOffset = aveXR - RIGHT_BASE

            netOffset = lOffset + rOffset
            print(netOffset)

            # do action

        else:
            print("not running")
        # END IF

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # stops loop and closes window
                pygame.quit()
        # END FOR

        time.sleep(0.2)
    # END WHILE
# END DEF

main()