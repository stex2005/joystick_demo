# -*- coding: utf-8 -*-
import threading, time
import pygame
import math
import sys
import os


Gain                = 1.1
AxisOffset          = [-0.273468017578 , -0.257843017578]
joystick_axisval    = [0.0, 0.0]


if __name__ == "__main__":


    try:
        os.environ["SDL_VIDEODRIVER"] = "dummy"
        pygame.init()
        pygame.display.init()

        if pygame.joystick.get_count() != 0:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()            
        else:
            print '# No Joystick found.'
            sys.exit()
    except:
        print '# Joystick initialization failed.'
        sys.exit()


    MainThreadRun = True
    
    while MainThreadRun:
        
        try:

            pygame.event.get()

            for i in range (0,2):
                joystick_axisval[i] = (joystick.get_axis(i) - AxisOffset[i]) * Gain

            Mode                 = joystick.get_button(1)
            SavePosition         = joystick.get_button(2)
            GotoSavedPosition    = joystick.get_button(3)
            Alarm                = joystick.get_button(4)

            print "%.3f %.3f - M: %d | Save: %d | GoTo: %d | Alarm: %d" % (joystick_axisval[0], joystick_axisval[1], Mode, SavePosition, GotoSavedPosition, Alarm)

            time.sleep(0.1)
        except (KeyboardInterrupt, SystemExit):
            MainThreadRun = False
            print '\n# Ctrl-C detected\n'
    
    time.sleep(1)

    print '* Bye bye'
