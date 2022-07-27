import pygame
import time

def update_display(win, running):
    win.fill((0, 0, 0))

    if running:
        print("running")
        pygame.draw.rect(win, (255, 0, 0), (0, 40, 300, 20))
    # END IF

    pygame.display.update()
# END DEF

def main():
    # create pygame window
    pygame.init()
    win = pygame.display.set_mode((300, 100))

    # define booleans for control flow
    run = False
    quitLoop = False

    # # initialise position variables
    # leftPos = 0
    # rightPos = 0

    # start loop
    while not quitLoop:
        # get key presses
        for event in pygame.event.get():
            # if user closes window
            if event.type == pygame.QUIT:
                # stops loop and closes window
                quitLoop = True
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                # if user presses keypad 1
                if event.key == pygame.K_KP1:
                    # toggle system on/off
                    run = not run
                # END IF
            # END IF
        # END FOR


        # do calculations


        # update display
        update_display(win, run)


        time.sleep(0.2)
    # END WHILE
# END DEF

main()