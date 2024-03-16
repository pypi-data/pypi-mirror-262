import os
import sys
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
pygame.init()
    
def get_keys():
    key_pressed = pygame.key.get_pressed()
    all_keys = {
        "backspace": key_pressed[pygame.K_BACKSPACE],
        "tab": key_pressed[pygame.K_TAB],
        "return": key_pressed[pygame.K_RETURN],
        "escape": key_pressed[pygame.K_ESCAPE],
        "space": key_pressed[pygame.K_SPACE],
        "exclaim": key_pressed[pygame.K_EXCLAIM],
        "quotedbl": key_pressed[pygame.K_QUOTEDBL],
        "hash": key_pressed[pygame.K_HASH],
        "dollar": key_pressed[pygame.K_DOLLAR],
        "ampersand": key_pressed[pygame.K_AMPERSAND],
        "quote": key_pressed[pygame.K_QUOTE],
        "leftparen": key_pressed[pygame.K_LEFTPAREN],
        "rightparen": key_pressed[pygame.K_RIGHTPAREN],
        "asterisk": key_pressed[pygame.K_ASTERISK],
        "plus": key_pressed[pygame.K_PLUS],
        "comma": key_pressed[pygame.K_COMMA],
        "minus": key_pressed[pygame.K_MINUS],
        "period": key_pressed[pygame.K_PERIOD],
        "slash": key_pressed[pygame.K_SLASH],
        "0": key_pressed[pygame.K_0],
        "1": key_pressed[pygame.K_1],
        "2": key_pressed[pygame.K_2],
        "3": key_pressed[pygame.K_3],
        "4": key_pressed[pygame.K_4],
        "5": key_pressed[pygame.K_5],
        "6": key_pressed[pygame.K_6],
        "7": key_pressed[pygame.K_7],
        "8": key_pressed[pygame.K_8],
        "9": key_pressed[pygame.K_9],
        "colon": key_pressed[pygame.K_COLON],
        "semicolon": key_pressed[pygame.K_SEMICOLON],
        "less": key_pressed[pygame.K_LESS],
        "equals": key_pressed[pygame.K_EQUALS],
        "greater": key_pressed[pygame.K_GREATER],
        "question": key_pressed[pygame.K_QUESTION],
        "at": key_pressed[pygame.K_AT],
        "leftbracket": key_pressed[pygame.K_LEFTBRACKET],
        "backslash": key_pressed[pygame.K_BACKSLASH],
        "rightbracket": key_pressed[pygame.K_RIGHTBRACKET],
        "caret": key_pressed[pygame.K_CARET],
        "underscore": key_pressed[pygame.K_UNDERSCORE],
        "backquote": key_pressed[pygame.K_BACKQUOTE],
        "a": key_pressed[pygame.K_a],
        "b": key_pressed[pygame.K_b],
        "c": key_pressed[pygame.K_c],
        "d": key_pressed[pygame.K_d],
        "e": key_pressed[pygame.K_e],
        "f": key_pressed[pygame.K_f],
        "g": key_pressed[pygame.K_g],
        "h": key_pressed[pygame.K_h],
        "i": key_pressed[pygame.K_i],
        "j": key_pressed[pygame.K_j],
        "k": key_pressed[pygame.K_k],
        "l": key_pressed[pygame.K_l],
        "m": key_pressed[pygame.K_m],
        "n": key_pressed[pygame.K_n],
        "o": key_pressed[pygame.K_o],
        "p": key_pressed[pygame.K_p],
        "q": key_pressed[pygame.K_q],
        "r": key_pressed[pygame.K_r],
        "s": key_pressed[pygame.K_s],
        "t": key_pressed[pygame.K_t],
        "u": key_pressed[pygame.K_u],
        "v": key_pressed[pygame.K_v],
        "w": key_pressed[pygame.K_w],
        "x": key_pressed[pygame.K_x],
        "y": key_pressed[pygame.K_y],
        "z": key_pressed[pygame.K_z],
        "delete": key_pressed[pygame.K_DELETE],
        "kp0": key_pressed[pygame.K_KP0],
        "kp1": key_pressed[pygame.K_KP1],
        "kp2": key_pressed[pygame.K_KP2],
        "kp3": key_pressed[pygame.K_KP3],
        "kp4": key_pressed[pygame.K_KP4],
        "kp5": key_pressed[pygame.K_KP5],
        "kp6": key_pressed[pygame.K_KP6],
        "kp7": key_pressed[pygame.K_KP7],
        "kp8": key_pressed[pygame.K_KP8],
        "kp9": key_pressed[pygame.K_KP9],
        "kp_period": key_pressed[pygame.K_KP_PERIOD],
        "kp_divide": key_pressed[pygame.K_KP_DIVIDE],
        "kp_multiply": key_pressed[pygame.K_KP_MULTIPLY],
        "kp_minus": key_pressed[pygame.K_KP_MINUS],
        "kp_plus": key_pressed[pygame.K_KP_PLUS],
        "kp_enter": key_pressed[pygame.K_KP_ENTER],
        "kp_equals": key_pressed[pygame.K_KP_EQUALS],
        "up": key_pressed[pygame.K_UP],
        "down": key_pressed[pygame.K_DOWN],
        "left": key_pressed[pygame.K_LEFT],
        "right": key_pressed[pygame.K_RIGHT],
        "insert": key_pressed[pygame.K_INSERT],
        "home": key_pressed[pygame.K_HOME],
        "end": key_pressed[pygame.K_END],
        "pageup": key_pressed[pygame.K_PAGEUP],
        "pagedown": key_pressed[pygame.K_PAGEDOWN],
        "f1": key_pressed[pygame.K_F1],
        "f2": key_pressed[pygame.K_F2],
        "f3": key_pressed[pygame.K_F3],
        "f4": key_pressed[pygame.K_F4],
        "f5": key_pressed[pygame.K_F5],
        "f6": key_pressed[pygame.K_F6],
        "f7": key_pressed[pygame.K_F7],
        "f8": key_pressed[pygame.K_F8],
        "f9": key_pressed[pygame.K_F9],
        "f10": key_pressed[pygame.K_F10],
        "f11": key_pressed[pygame.K_F11],
        "f12": key_pressed[pygame.K_F12],
        "numlock": key_pressed[pygame.K_NUMLOCK],
        "capslock": key_pressed[pygame.K_CAPSLOCK],
        "scrollock": key_pressed[pygame.K_SCROLLOCK],
        "rshift": key_pressed[pygame.K_RSHIFT],
        "lshift": key_pressed[pygame.K_LSHIFT],
        "rctrl": key_pressed[pygame.K_RCTRL],
        "lctrl": key_pressed[pygame.K_LCTRL],
        "ralt": key_pressed[pygame.K_RALT],
        "lalt": key_pressed[pygame.K_LALT],
        "rmeta": key_pressed[pygame.K_RMETA],
        "lmeta": key_pressed[pygame.K_LMETA],
        "lsuper": key_pressed[pygame.K_LSUPER],
        "rsuper": key_pressed[pygame.K_RSUPER],
        "mode": key_pressed[pygame.K_MODE],
        "help": key_pressed[pygame.K_HELP],
        "print": key_pressed[pygame.K_PRINT],
        "sysreq": key_pressed[pygame.K_SYSREQ],
        "break": key_pressed[pygame.K_BREAK],
        "menu": key_pressed[pygame.K_MENU],
        "power": key_pressed[pygame.K_POWER],
        "euro": key_pressed[pygame.K_EURO]}

class Window():
    def __init__(self, res):
        self.res = self.width, self.height = res[0], res[1]
        self.h_width, self.h_height = self.width / 2, self.height / 2
        self.surface = pygame.display.set_mode(self.res)
        self.clock = pygame.time.Clock()
        self.__private_events = {
            'QUIT':            pygame.QUIT,
            'KEYDOWN':         pygame.KEYDOWN,
            'KEYUP':           pygame.KEYUP,
            'MOUSEBUTTONDOWN': pygame.MOUSEBUTTONDOWN,
            'MOUSEBUTTONUP':   pygame.MOUSEBUTTONUP,
            'MOUSEMOTION':     pygame.MOUSEMOTION,
            'VIDEORESIZE':     pygame.VIDEORESIZE,
            'VIDEOEXPOSE':     pygame.VIDEOEXPOSE,
            'USEREVENT':       pygame.USEREVENT
        }

    def exit(self):
        pygame.quit()
        sys.exit()

    def handle_event(self, excepted_event, command):
        for event in pygame.event.get():
            if event.type == self.__private_events[excepted_event.upper()]:
                return command()

    def update(self, fps=60, color=(255, 255, 255)):
        self.surface.fill(color)
        pygame.display.flip()
        self.clock.tick(fps)

try:
    if os.getenv('WINDOWEASY_HIDE_SUPPORT_PROMPT') == '0':
        print('Hello from the WindowEasy! version 1.0, python 3.11.3\n\
    This library utilizes pygame for enhanced functionality. Enjoy coding with WindowEasy!\n\
    our contact: makar.arapov.real@gmail.ru')
    else:
        os.environ['WINDOWEASY_HIDE_SUPPORT_PROMPT'] = '0'
except:
    os.environ['WINDOWEASY_HIDE_SUPPORT_PROMPT'] = '0'
