from ctypes import windll
from ctypes.wintypes import HWND
import string
import time
import mouse as mouse
Keboard_Event = windll.user32.keybd_event
MapVirtualKeyW = windll.user32.MapVirtualKeyW
VkKeyScanA = windll.user32.VkKeyScanA

WM_KEYDOWN = 0x100
WM_KEYUP = 0x101

# https://docs.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes
VkCode = {
    "backspace":  0x2a,
    "tab":  0x2b,
    "return":  0x28,
    "esc":  0x29,
    "space":  0x2c,
    "pageup":0x4b,
    "pagedown":0x4e,
    "end":  0x4d,
    "home":  0x4a,
    "left":  0x50,
    "up":  0x52,
    "right":  0x4f,
    "down":  0x51,
    "insert":  0x49,
    "delete":  0x4c,
    '0': 0x27,
    '1': 0x1e,
    '2': 0x1f,
    '3': 0x20,
    '4': 0x21,
    '5': 0x22,
    '6': 0x23,
    '7': 0x24,
    '8': 0x25,
    '9': 0x26,
    'a': 0x04,
    'b': 0x05,
    'c': 0x06,
    'd': 0x07,
    'e': 0x08,
    'f': 0x09,
    'g': 0x0a,
    'h': 0x0b,
    'i': 0x0c,
    'j': 0x0d,
    'k': 0x0e,
    'l': 0x0f,
    'm': 0x10,
    'n': 0x11,
    'o': 0x12,
    'p': 0x13,
    'q': 0x14,
    'r': 0x15,
    's': 0x16,
    't': 0x17,
    'u': 0x18,
    'v': 0x19,
    'w': 0x1a,
    'x': 0x1b,
    'y': 0x1c,
    'z': 0x1d,
    "lwin":  0xe3,
    "rwin":  0xe7,
    "numpad0":  0x62,
    "numpad1":  0x59,
    "numpad2":  0x5a,
    "numpad3":  0x5b,
    "numpad4":  0x5c,
    "numpad5":  0x5d,
    "numpad6":  0x5e,
    "numpad7":  0x5f,
    "numpad8":  0x60,
    "numpad9":  0x61,
    "f1":  0x3a,
    "f2":  0x3b,
    "f3":  0x3c,
    "f4":  0x3d,
    "f5":  0x3e,
    "f6":  0x3f,
    "f7":  0x40,
    "f8":  0x41,
    "f9":  0x42,
    "f10":  0x43,
    "f11":  0x44,
    "f12":  0x45,
    "lshift":  0xe1,
    "rshift":  0xe5,
    "lcontrol":  0xe0,
    "rcontrol":  0xe4,

}


def get_virtual_keycode(key: str):
    """根据按键名获取虚拟按键码

    Args:
        key (str): 按键名

    Returns:
        int: 虚拟按键码
    """
    if len(key) == 1 and key in string.printable:
        # https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-vkkeyscana
        return VkKeyScanA(ord(key)) & 0xff
    else:
        return VkCode[key]


def key_down(key: str):
    """按下指定按键

    Args:
        handle (HWND): 窗口句柄
        key (str): 按键名
    """
    vk_code = get_virtual_keycode(key)
    scan_code = MapVirtualKeyW(vk_code, 0)
    Keboard_Event(vk_code, scan_code, 0, 0)


def key_up( key: str):
    """放开指定按键

    Args:
        handle (HWND): 窗口句柄
        key (str): 按键名
    """
    vk_code = get_virtual_keycode(key)
    scan_code = MapVirtualKeyW(vk_code, 0)
    Keboard_Event(vk_code, scan_code, 1, 0)

def keyboard_down_up(key:str):
    key_down(key)
    time.sleep(0.5)
    key_up(key)
if __name__ == "__main__":
    mouse.mouse_left_click(2000,700)
    keyboard_down_up('a')
