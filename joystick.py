#!/usr/bin/env python
"""
Joystick Graph Readout Utility for Pygame v0.1.0
By Temia Eszteri -- http://prerisoft.cleverpun.com/

Originally written within an hour, cleaning it up for general use took another
half.

SDL Debug code? Pipe stdout to /dev/null or NUL! At the time of writing
(7/3/2013), SDL's joystick support was compiled in debug mode for Pygame on
multiple platforms for some reason (tested in both Arch Linux ARM and Windows),
and calling the get methods in this code will cause a LOT of debug spam!

Released under Poul-Henning Kamp's Beer-Ware License
"""

import sys, pygame, argparse

parser = argparse.ArgumentParser(description="Joystick Readout for Pygame")
parser.add_argument("-j", "--joystick", nargs=1, metavar="#", type=int,
                    default=0, dest="joys",
                    help="Select a particular joystick")
parser.add_argument("-w", "--width", nargs=1, metavar="#", type=int,
                    default=640, dest="width",
                    help="Sets the window to a specific width")
parsee = parser.parse_args()

pygame.display.init()
pygame.joystick.init()
pygame.font.init()

clock = pygame.time.Clock()
assert pygame.joystick.get_count(), "No joysticks detected by SDL"
joystick = pygame.joystick.Joystick(parsee.joys % pygame.joystick.get_count())
joystick.init()

pygame.event.set_allowed(None)
pygame.event.set_allowed([pygame.JOYAXISMOTION,
                          pygame.JOYHATMOTION,
                          pygame.JOYBUTTONDOWN,
                          pygame.JOYBUTTONUP,
                          pygame.QUIT])

total_y = ((100 * joystick.get_numaxes()) + (32 * joystick.get_numhats()) +
           (12 * joystick.get_numbuttons()))

if isinstance(parsee.width, list): total_x = parsee.width[0]
else: total_x = parsee.width
screen = pygame.display.set_mode((total_x, total_y))
graph = pygame.Surface((total_x, total_y))
overlay = pygame.Surface((total_x, total_y))
overlay.fill((0xC0, 0xFF, 0xEE))
overlay.set_colorkey((0xC0, 0xFF, 0xEE))
font = pygame.font.SysFont(None, 12)
font_draw = lambda x, y: overlay.blit(font.render(x, False, (0xA0, 0xA0, 0xA0),
                                               (0xC0, 0xFF, 0xEE)), (2, y + 2))
clean_rect = pygame.Rect((total_x - 1, 0), (1, total_y))

class AxisArtist(object):
    def __init__(self, axis_num, y, gain = 1.0):
        self.axis = axis_num
        self.base_y = y
        self.position_new = 0
        self.position_old = 0
        self.gain = gain
    def __call__(self):
        self.position_old = self.position_new
        self.position_new = joystick.get_axis(self.axis) * 50
        self.position_new = self.position_new * self.gain
        pygame.draw.line(graph, (0x00, 0xFF, 0x00),
                         (total_x - 2, self.base_y + 50 + self.position_old),
                         (total_x - 1, self.base_y + 50 + self.position_new))

class HatArtist(object):
    def __init__(self, hat_num, y):
        self.up_rect = pygame.Rect((total_x - 1, y), (1, 8))
        self.left_rect = pygame.Rect((total_x - 1, y + 8), (1, 8))
        self.right_rect = pygame.Rect((total_x - 1, y + 16), (1, 8))
        self.down_rect = pygame.Rect((total_x - 1, y + 24), (1, 8))
        self.hat = hat_num
    def __call__(self):
        x, y = joystick.get_hat(self.hat)
        if x < 0: graph.fill((0xFF, 0xFF, 0x00), self.left_rect)
        if x > 0: graph.fill((0xFF, 0xFF, 0x00), self.right_rect)
        if y < 0: graph.fill((0xFF, 0xFF, 0x00), self.down_rect)
        if y > 0: graph.fill((0xFF, 0xFF, 0x00), self.up_rect)

class ButtonArtist(object):
    def __init__(self, button_num, y):
        self.button = button_num
        self.rect = pygame.Rect((total_x - 1, y), (1, 12))
    def __call__(self):
        if joystick.get_button(self.button):
            graph.fill((0xFF, 0x00, 0x00), self.rect)

def make_functions():
    global functions, overlay
    functions = []
    base_y = 0
    for axis in range(joystick.get_numaxes()):
        if axis == 0 or axis == 1:
            functions.append(AxisArtist(axis, base_y, gain=1.5))
        else:
            functions.append(AxisArtist(axis, base_y))

        font_draw("Axis {}".format(axis), base_y)
        base_y += 100
    #for hat in range(joystick.get_numhats()):
    #    functions.append(HatArtist(hat, base_y))
    #    font_draw("Hat {}".format(hat), base_y)
    #    base_y += 32
    for button in range(joystick.get_numbuttons()):
        functions.append(ButtonArtist(button, base_y))
        font_draw("Button {}".format(button), base_y)
        base_y += 12
    print functions
make_functions()
pygame.display.set_caption("Joystick Tester: {} (#{})".format(
                                       joystick.get_name(), joystick.get_id()))

while 1:
    if pygame.event.get(pygame.QUIT):
        pygame.quit()
        sys.exit()
    graph.scroll(-1, 0)
    graph.fill((0x00, 0x00, 0x00), clean_rect)
    for i in functions:
        i()
    pygame.event.clear()
    screen.blit(graph, (0, 0))
    screen.blit(overlay, (0, 0))
    clock.tick(60)
    pygame.display.flip()
    print joystick.get_button(0)