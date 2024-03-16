#  PyForge ©️
#  2023-2024 Izaiyah Stokes <setoichi.dev@gmail.com>
#
#  This software is provided 'as-is', without any express or implied
#  warranty.  In no event will the authors be held liable for any damages
#  arising from the use of this software.
#
#  Permission is granted to anyone to use this software for any purpose,
#  including commercial applications, and to alter it and redistribute it
#  freely, subject to the following restrictions:
#
#  1. The origin of this software must not be misrepresented; you must not
#     claim that you wrote the original software. If you use this software
#     in a product, an acknowledgment in the product documentation would be
#     appreciated but is not required.
#  2. Altered source versions must be plainly marked as such, and must not be
#     misrepresented as being the original software.
#  3. This notice may not be removed or altered from any source distribution.

import pygame as pg

INIT_ALL = pg.init
INIT_FONTS = pg.font.init
INIT_AUDIO = pg.mixer.init
EVENT = pg.event.Event

KEYDOWN = 768
KEYUP = 769

MOUSEMOTION = 1024
MOUSEBUTTONDOWN = 1025
MOUSEBUTTONUP = 1026

JOYAXISMOTION = 1536
JOYBALLMOTION = 1537
JOYHATMOTION = 1538
JOYBUTTONDOWN = 1539
JOYBUTTONUP = 1540

QUIT = 32787
ACTIVEEVENT = 512
VIDEORESIZE = 32768
VIDEOEXPOSE = 32774

Vector2 = pg.math.Vector2
Vector3 = pg.math.Vector3

Rect = pg.Rect
Surface = pg.Surface
Sprite = pg.sprite.Sprite


class Mouse:
    LeftClick = 1
    WheelClick = 2
    RightClick = 3
    WheelUp = 4
    WheelDown = 5

class Keyboard:
    # Letter keys
    A = pg.K_a
    B = pg.K_b
    C = pg.K_c
    D = pg.K_d
    E = pg.K_e
    F = pg.K_f
    G = pg.K_g
    H = pg.K_h
    I = pg.K_i
    J = pg.K_j
    K = pg.K_k
    L = pg.K_l
    M = pg.K_m
    N = pg.K_n
    O = pg.K_o
    P = pg.K_p
    Q = pg.K_q
    R = pg.K_r
    S = pg.K_s
    T = pg.K_t
    U = pg.K_u
    V = pg.K_v
    W = pg.K_w
    X = pg.K_x
    Y = pg.K_y
    Z = pg.K_z

    # Number keys
    Num0 = pg.K_0
    Num1 = pg.K_1
    Num2 = pg.K_2
    Num3 = pg.K_3
    Num4 = pg.K_4
    Num5 = pg.K_5
    Num6 = pg.K_6
    Num7 = pg.K_7
    Num8 = pg.K_8
    Num9 = pg.K_9

    # Function keys
    F1 = pg.K_F1
    F2 = pg.K_F2
    F3 = pg.K_F3
    F4 = pg.K_F4
    F5 = pg.K_F5
    F6 = pg.K_F6
    F7 = pg.K_F7
    F8 = pg.K_F8
    F9 = pg.K_F9
    F10 = pg.K_F10
    F11 = pg.K_F11
    F12 = pg.K_F12

    # Special keys
    Space = pg.K_SPACE
    Escape = pg.K_ESCAPE
    Enter = pg.K_RETURN
    Tab = pg.K_TAB
    Shift = pg.K_LSHIFT  # Left Shift
    Ctrl = pg.K_LCTRL    # Left Control
    Alt = pg.K_LALT      # Left Alt
    RShift = pg.K_RSHIFT  # Right Shift
    RCtrl = pg.K_RCTRL    # Right Control
    RAlt = pg.K_RALT      # Right Alt

    # Arrow keys
    Up = pg.K_UP
    Down = pg.K_DOWN
    Left = pg.K_LEFT
    Right = pg.K_RIGHT

    # Numpad keys
    NumPad0 = pg.K_KP0
    NumPad1 = pg.K_KP1
    NumPad2 = pg.K_KP2
    NumPad3 = pg.K_KP3
    NumPad4 = pg.K_KP4
    NumPad5 = pg.K_KP5
    NumPad6 = pg.K_KP6
    NumPad7 = pg.K_KP7
    NumPad8 = pg.K_KP8
    NumPad9 = pg.K_KP9
    NumPadDivide = pg.K_KP_DIVIDE
    NumPadMultiply = pg.K_KP_MULTIPLY
    NumPadSubtract = pg.K_KP_MINUS
    NumPadAdd = pg.K_KP_PLUS
    NumPadEnter = pg.K_KP_ENTER
    NumPadDecimal = pg.K_KP_PERIOD

    # Modifier keys
    LShift = pg.K_LSHIFT
    RShift = pg.K_RSHIFT
    LCtrl = pg.K_LCTRL
    RCtrl = pg.K_RCTRL
    LAlt = pg.K_LALT
    RAlt = pg.K_RALT
    LMeta = pg.K_LMETA
    RMeta = pg.K_RMETA
    LSuper = pg.K_LSUPER  # Windows key for left
    RSuper = pg.K_RSUPER  # Windows key for right

    # Miscellaneous keys
    CapsLock = pg.K_CAPSLOCK
    NumLock = pg.K_NUMLOCK
    ScrollLock = pg.K_SCROLLOCK
    PrintScreen = pg.K_PRINT
    Pause = pg.K_PAUSE
    Insert = pg.K_INSERT
    Delete = pg.K_DELETE
    Home = pg.K_HOME
    End = pg.K_END
    PageUp = pg.K_PAGEUP
    PageDown = pg.K_PAGEDOWN

    # Symbol keys
    Grave = pg.K_BACKQUOTE  # `~
    Minus = pg.K_MINUS      # -_
    Equals = pg.K_EQUALS    # =+
    LeftBracket = pg.K_LEFTBRACKET   # [{
    RightBracket = pg.K_RIGHTBRACKET # ]}
    Backslash = pg.K_BACKSLASH       # \|
    Semicolon = pg.K_SEMICOLON       # ;:
    Quote = pg.K_QUOTE               # '"
    Comma = pg.K_COMMA               # ,<
    Period = pg.K_PERIOD             # .>
    Slash = pg.K_SLASH               # /?
    BackSpace = pg.K_BACKSPACE
    Tab = pg.K_TAB
    Enter = pg.K_RETURN
    Menu = pg.K_MENU

class Controller:
    # Buttons
    A = pg.CONTROLLER_BUTTON_A
    B = pg.CONTROLLER_BUTTON_B
    X = pg.CONTROLLER_BUTTON_X
    Y = pg.CONTROLLER_BUTTON_Y
    Back = pg.CONTROLLER_BUTTON_BACK
    Guide = pg.CONTROLLER_BUTTON_GUIDE
    Start = pg.CONTROLLER_BUTTON_START
    LeftStick = pg.CONTROLLER_BUTTON_LEFTSTICK
    RightStick = pg.CONTROLLER_BUTTON_RIGHTSTICK
    LeftShoulder = pg.CONTROLLER_BUTTON_LEFTSHOULDER
    RightShoulder = pg.CONTROLLER_BUTTON_RIGHTSHOULDER
    DpadUp = pg.CONTROLLER_BUTTON_DPAD_UP
    DpadDown = pg.CONTROLLER_BUTTON_DPAD_DOWN
    DpadLeft = pg.CONTROLLER_BUTTON_DPAD_LEFT
    DpadRight = pg.CONTROLLER_BUTTON_DPAD_RIGHT

    # Axes
    LeftX = pg.CONTROLLER_AXIS_LEFTX
    LeftY = pg.CONTROLLER_AXIS_LEFTY
    RightX = pg.CONTROLLER_AXIS_RIGHTX
    RightY = pg.CONTROLLER_AXIS_RIGHTY
    TriggerLeft = pg.CONTROLLER_AXIS_TRIGGERLEFT
    TriggerRight = pg.CONTROLLER_AXIS_TRIGGERRIGHT
    
    def init(self) -> None:
        pg.joystick.init()

