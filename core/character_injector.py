import ctypes
from ctypes import wintypes
import time

# Windows API Structures and Constants
# https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-input

IS_64BIT = ctypes.sizeof(ctypes.c_void_p) == 8

if IS_64BIT:
    ULONG_PTR = ctypes.c_uint64
else:
    ULONG_PTR = ctypes.c_uint32

class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", wintypes.WORD),
        ("wScan", wintypes.WORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ULONG_PTR)
    ]

class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", wintypes.LONG),
        ("dy", wintypes.LONG),
        ("mouseData", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ULONG_PTR)
    ]

class HARDWAREINPUT(ctypes.Structure):
    _fields_ = [
        ("uMsg", wintypes.DWORD),
        ("wParamL", wintypes.WORD),
        ("wParamH", wintypes.WORD)
    ]

class INPUT_I(ctypes.Union):
    _fields_ = [
        ("ki", KEYBDINPUT),
        ("mi", MOUSEINPUT),
        ("hi", HARDWAREINPUT)
    ]

class INPUT(ctypes.Structure):
    _fields_ = [
        ("type", wintypes.DWORD),
        ("ii", INPUT_I)
    ]

# Constants
INPUT_KEYBOARD = 1
KEYEVENTF_UNICODE = 0x0004
KEYEVENTF_KEYUP = 0x0002

VK_BACK = 0x08
VK_RETURN = 0x0D
VK_TAB = 0x09

user32 = ctypes.WinDLL('user32', use_last_error=True)
user32.SendInput.argtypes = [wintypes.UINT, ctypes.POINTER(INPUT), ctypes.c_int]
user32.SendInput.restype = wintypes.UINT

def send_unicode_char(char):
    if not char:
        return

    if char == '\n':
        send_vk(VK_RETURN)
        return
    elif char == '\t':
        send_vk(VK_TAB)
        return
    
    char_code = ord(char)
    inputs = (INPUT * 2)()

    # Key Down
    inputs[0].type = INPUT_KEYBOARD
    inputs[0].ii.ki.wVk = 0
    inputs[0].ii.ki.wScan = char_code
    inputs[0].ii.ki.dwFlags = KEYEVENTF_UNICODE
    
    # Key Up
    inputs[1].type = INPUT_KEYBOARD
    inputs[1].ii.ki.wVk = 0
    inputs[1].ii.ki.wScan = char_code
    inputs[1].ii.ki.dwFlags = KEYEVENTF_UNICODE | KEYEVENTF_KEYUP
    
    user32.SendInput(2, inputs, ctypes.sizeof(INPUT))

def send_vk(vk_code):
    inputs = (INPUT * 2)()

    # Key Down
    inputs[0].type = INPUT_KEYBOARD
    inputs[0].ii.ki.wVk = vk_code
    inputs[0].ii.ki.wScan = 0
    inputs[0].ii.ki.dwFlags = 0
    
    # Key Up
    inputs[1].type = INPUT_KEYBOARD
    inputs[1].ii.ki.wVk = vk_code
    inputs[1].ii.ki.wScan = 0
    inputs[1].ii.ki.dwFlags = KEYEVENTF_KEYUP

    user32.SendInput(2, inputs, ctypes.sizeof(INPUT))

def send_backspace():
    send_vk(VK_BACK)
