import time
import pyautogui
import cv2
import keyboard

# define global booleans for control flow
global run 
run = False
global quitLoop
quitLoop = False


#define hotkey functions
def changeRun():
    global run
    run = not run
# END DEF

def stopLoop():
    global quitLoop
    quitLoop = True
# END DEF


# function to take screenshots of corrent region for use for openCV testing
global ssNum
ssNum = 0
def getSaveSS():
    global ssNum

    image = pyautogui.screenshot(region=(750, 514, 320, 100))
    image.save("testImage" + str(ssNum) + ".png")
    ssNum += 1
# END DEF


# set hotkeys
keyboard.add_hotkey("p", lambda: changeRun())
keyboard.add_hotkey("l", lambda: stopLoop())
keyboard.add_hotkey("o", lambda: getSaveSS())


# main function
def main():
    # add global variables
    global run, quitLoop

    # # initialise position variables
    # leftPos = 0
    # rightPos = 0

    # start loop
    while not quitLoop:
        if run:
            print("running")

            ##### do calculations

            # get image
            # image = pyautogui.screenshot(region=(750, 514, 320, 100))

            # process image

            # determine action

            # do action

        else:
            print("not running")
        # END IF

        time.sleep(0.2)
    # END WHILE
# END DEF

main()