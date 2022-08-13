import csv
import pyautogui
import cv2
import keyboard
import numpy as np
import pygame
from PIL import Image

global run 
global quitLoop
global recording

# define booleans for control flow
run = False
quitLoop = False
recording = False

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

def changeRecording():
    global recording
    recording = not recording
# END DEF


# set hotkeys
keyboard.add_hotkey("#", lambda: changeRun())
keyboard.add_hotkey("l", lambda: stopLoop())
keyboard.add_hotkey("'", lambda: changeRecording())


def updateDisplay(frame, win, wheelPos, lines, goodLines, roadPos):
    global recording

    # update pygame window with information
    win.fill((0, 0, 0))

    # draw lines detected onto frame
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(frame,(x1,y1),(x2,y2),(255,0,0),1)
        # END FOR
    # END FOR

    for line in goodLines:
        for x1,y1,x2,y2 in line:
            cv2.line(frame,(x1,y1),(x2,y2),(0,255,0),1)
        # END FOR
    # END FOR

    # img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    im_pil = Image.fromarray(frame)

    py_image = pygame.image.fromstring(im_pil.tobytes(), im_pil.size, im_pil.mode)

    win.blit(py_image, (0,0))

    if wheelPos < 0:
        pygame.draw.rect(win, (255, 0, 0), pygame.Rect((210+wheelPos*10), 158, wheelPos*-10, 15))
    elif wheelPos > 0:
        pygame.draw.rect(win, (255, 0, 0), pygame.Rect(210, 158, wheelPos*10, 15))
    # END IF

    if roadPos < 0:
        pygame.draw.rect(win, (0, 0, 255), pygame.Rect((210+roadPos*200), 173, roadPos*-200, 15))
    elif roadPos > 0:
        pygame.draw.rect(win, (0, 0, 255), pygame.Rect(210, 173, roadPos*200, 15))
    # END IF

    if recording:
        pygame.draw.rect(win, (0, 255, 0), pygame.Rect(0, 170, 10, 10))
    # END IF
    
    pygame.display.update()
# END DEF


def processImageForLines(frame):
    # apply gaussian blur to image
    kernel_size = 5
    blurFrame = cv2.GaussianBlur(frame ,(kernel_size, kernel_size),0)

    # use canny edge detection
    low_threshold = 50
    high_threshold = 150
    edges = cv2.Canny(blurFrame, low_threshold, high_threshold)

    rho = 1  # distance resolution in pixels of the Hough grid
    theta = np.pi / 180  # angular resolution in radians of the Hough grid
    threshold = 22  # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 20  # minimum number of pixels making up a line
    max_line_gap = 60  # maximum gap in pixels between connectable line segments

    # Run Hough on edge detected image
    # Output "lines" is an array containing endpoints of detected line segments
    lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]), min_line_length, max_line_gap)

    if lines is not None:
        return lines
    else:
        return []
    # END IF
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


def processLines(lines):
    gradientList = []
    goodLines = []

    for line in lines:
        for x1,y1, x2,y2 in line:
            # get gradient of line
            delX = x1-x2
            delY = y1-y2

            if delY != 0:
                gradient = delX/delY
                if abs(gradient) < 1:
                    gradientList.append(gradient)
                    goodLines.append(line)
                # END IF
            # END IF
        # END FOR
    # END FOR

    if len(gradientList) > 0:
        aveGradient = sum(gradientList) / len(gradientList)
        return aveGradient, goodLines
    else:
        return 0, []
    # END IF
# EN DEF


# main function
def main():
    screenshotDimensions = (700, 450, 700, 600)

    # start pygame display
    pygame.init()
    win = pygame.display.set_mode((420, 188)) # frame is 420x158 + 30 at bottom for inidcator
    pygame.display.update()

    # add global variables
    global run, quitLoop, recording

    badFrames = 0

    file = open("steerdata.csv", "a", newline="")
    writer = csv.writer(file)
    

    # start loop
    while not quitLoop:
        if run:
            # get image
            screenshot = pyautogui.screenshot(region=screenshotDimensions)
            # convert to np and grayscale
            frame = np.array(screenshot)

            # check if frame is bad (all black)
            if sum(frame[508][176]) == 0:
                badFrames += 1
                print("badFrame", badFrames)
            else:
                # run processing as frame is good

                # get frame with just road on
                roadFrame = frame[0:158, 0:420]

                # process image to find lines
                lines = processImageForLines(roadFrame)

                # get estimated road direction from lines
                roadPos, goodLines = processLines(lines)

                # get wheel position
                wheelPos = getWheelPosition(frame)

                if recording:
                    writer.writerow([roadPos, wheelPos])
                # END IF

                # update display
                updateDisplay(roadFrame, win, wheelPos, lines, goodLines, roadPos)
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