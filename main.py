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

#define hotkey functions
def changeRun():
    global run
    run = not run
    print("running", run)
# END DEF

def stopLoop():
    global quitLoop
    quitLoop = True
# END DEF


# set hotkeys
keyboard.add_hotkey("#", lambda: changeRun())
keyboard.add_hotkey("l", lambda: stopLoop())


def updateDisplay(frame, win, wheelPos):
    # update pygame window with information
    win.fill((0, 0, 0))

    # img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    im_pil = Image.fromarray(frame)

    py_image = pygame.image.fromstring(im_pil.tobytes(), im_pil.size, im_pil.mode)

    win.blit(py_image, (0,0))

    if wheelPos < 0:
        pygame.draw.rect(win, (255, 0, 0), pygame.Rect((210+wheelPos*10), 158, wheelPos*-10, 30))
    elif wheelPos > 0:
        pygame.draw.rect(win, (255, 0, 0), pygame.Rect(210, 158, wheelPos*10, 30))
    # END IF

    
    pygame.display.update()
# END DEF


def processImageForLines(frame, win):
    print("processing")
# END DEF

def getWheelPosition(frame):
    # checkpoints array from wheel positions.py
    checkpoints = [[472, 254], [479, 262], [487, 271], [495, 279], [503, 288], [510, 296], [518, 305], [526, 314], [534, 323], [541, 331], [549, 340], [557, 348], [565, 357], [573, 365], [581, 374], [589, 383], [597, 392], [601, 404], [605, 416], [609, 428], [613, 441], [617, 453], [621, 465], [625, 477], [630, 490], [634, 502], [638, 514], [642, 526], [647, 539], [651, 551], [655, 563], [659, 575], [664, 588]]

    threshhold = 20

    result = []
    for position in checkpoints:
        point = frame[position[1]][position[0]]
        if sum(point) / 3 > threshhold:
            result.append(1)
        else:
            result.append(0)
        # END IF
    # END FOR

    return sum(result) - 16
# END DEF


# main function
def main():
    screenshotDimensions = (700, 450, 700, 600)

    # start pygame display
    pygame.init()
    win = pygame.display.set_mode((420, 188)) # frame is 420x158 + 30 at bottom for inidcator
    pygame.display.update()

    # add global variables
    global run, quitLoop

    badFrames = 0

    # start loop
    while not quitLoop:
        if run:
            # get image
            screenshot = pyautogui.screenshot(region=screenshotDimensions)
            # convert to np and grayscale
            frame = np.array(screenshot)

            # print(sum(frame[508][176]))
            if sum(frame[508][176]) == 0:
                badFrames += 1
                print("badFrame", badFrames)
            else:
                roadFrame = frame[0:158, 0:420]
                # processImageForLines(roadFrame, win)
                wheelPos = getWheelPosition(frame)

                updateDisplay(roadFrame, win, wheelPos)
            # END IF
        # END IF

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # stops loop and closes window
                pygame.quit()
        # END FOR
    # END WHILE
# END DEF

main()


# =================================================================