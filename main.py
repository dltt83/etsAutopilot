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


def updateDisplay(win, frame, aveXL, aveXR):
    win.fill((0, 0, 0))

    img = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
    im_pil = Image.fromarray(img)

    py_image = pygame.image.fromstring(im_pil.tobytes(), im_pil.size, im_pil.mode)

    win.blit(py_image, (0,0))

    pygame.draw.rect(win, (255, 0, 0), pygame.Rect(aveXL, 0, 1, 100))
    pygame.draw.rect(win, (0, 255, 0), pygame.Rect(aveXR+200, 0, 1, 100))
    pygame.draw.rect(win, (0, 0, 255), pygame.Rect(200, 0, 1, 100))
    
    pygame.display.update()
# END DEF


def processImage(frame, win):
    (thresh, frameBW) = cv2.threshold(frame, 180, 255, cv2.THRESH_BINARY)


    leftSide = frameBW[0:100, 0:200]
    rightSide = frameBW[0:100, 201:320]

    # find average x position of white pixels
    aveXL = 0
    whtNumL = 0
    for y in range(len(leftSide)):
        for x in range(len(leftSide[0])):
            if leftSide[y][x] == 255:
                aveXL = aveXL + x
                whtNumL += 1
    #END FOR

    aveXR = 0
    whtNumR = 0
    for y in range(len(rightSide)):
        for x in range(len(rightSide[0])):
            if rightSide[y][x] == 255:
                aveXR = aveXR + x
                whtNumR += 1
    # END FOR

    if whtNumL > 0:
        aveXL = aveXL / whtNumL
    else:
        aveXL = LEFT_BASE
    # END IF
    if whtNumR > 0:
        aveXR = aveXR / whtNumR
    else:
        aveXR = RIGHT_BASE
    # END IF

    updateDisplay(win, frameBW, aveXL, aveXR)
    return aveXL, aveXR #, frameBW
# END DEF


def processImageForLines(frame, win):
    # apply gaussian blur to image
    kernel_size = 5
    blurFrame = cv2.GaussianBlur(frame ,(kernel_size, kernel_size),0)

    # convert image to binary black and white
    (thresh, frameBW) = cv2.threshold(blurFrame, 180, 255, cv2.THRESH_BINARY)

    # use canny edge detection
    low_threshold = 50
    high_threshold = 150
    edges = cv2.Canny(frameBW, low_threshold, high_threshold)

    rho = 1  # distance resolution in pixels of the Hough grid
    theta = np.pi / 180  # angular resolution in radians of the Hough grid
    threshold = 15  # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 20  # minimum number of pixels making up a line
    max_line_gap = 60  # maximum gap in pixels between connectable line segments
    line_image = np.copy(frameBW) * 0  # creating a blank to draw lines on

    # Run Hough on edge detected image
    # Output "lines" is an array containing endpoints of detected line segments
    lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]), min_line_length, max_line_gap)

    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),5)
    
    lines_edges = cv2.addWeighted(frameBW, 0.8, line_image, 1, 0)

    
    # update pygame window with information
    win.fill((0, 0, 0))

    # img = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
    im_pil = Image.fromarray(lines_edges)

    py_image = pygame.image.fromstring(im_pil.tobytes(), im_pil.size, im_pil.mode)

    win.blit(py_image, (0,0))

    # pygame.draw.rect(win, (255, 0, 0), pygame.Rect(aveXL, 0, 1, 100))
    # pygame.draw.rect(win, (0, 255, 0), pygame.Rect(aveXR+200, 0, 1, 100))
    # pygame.draw.rect(win, (0, 0, 255), pygame.Rect(200, 0, 1, 100))
    
    pygame.display.update()
# END DEF


# set hotkeys
keyboard.add_hotkey("#", lambda: changeRun())
keyboard.add_hotkey("l", lambda: stopLoop())


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
            # get image
            screenshot = pyautogui.screenshot(region=(750, 514, 320, 100))
            # convert to np and grayscale
            frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

            # # ==========
            # # process image
            # aveXL, aveXR = processImage(frame, win)

            # # determine action
            # lOffset = aveXL - LEFT_BASE
            # rOffset = aveXR - RIGHT_BASE

            # netOffset = lOffset + rOffset
            # print(aveXL, aveXR)
            # print(netOffset)

            # # do action
            # if netOffset < -50:
            #     keyboard.press("a")
            # elif netOffset > 50:
            #     keyboard.press("d")
            # # END IF
            # # ==========

            processImageForLines(frame, win)
        else:
            print("not running")
        # END IF

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # stops loop and closes window
                pygame.quit()
        # END FOR

        time.sleep(0.03)
        keyboard.release("a")
        keyboard.release("d")
        time.sleep(0.17)
    # END WHILE
# END DEF

main()