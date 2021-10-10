from ctypes import windll, byref
from ctypes.wintypes import HWND, POINT
import time

Mouse_Event = windll.user32.mouse_event
ClientToScreen = windll.user32.ClientToScreen

WM_MOUSEMOVE = 0x0200
WM_LBUTTONDOWN = 0x0201
WM_LBUTTONUP = 0x202
WM_MOUSEWHEEL = 0x020A
WHEEL_DELTA = 120
MOUSEEVENTF_MOVE = 0x0001;      #移动鼠标
MOUSEEVENTF_LEFTDOWN = 0x0002; #模拟鼠标左键按下
MOUSEEVENTF_LEFTUP = 0x0004; #模拟鼠标左键抬起
MOUSEEVENTF_RIGHTDOWN = 0x0008;# 模拟鼠标右键按下
MOUSEEVENTF_RIGHTUP = 0x0010; #模拟鼠标右键抬起
MOUSEEVENTF_MIDDLEDOWN = 0x0020;# 模拟鼠标中键按下
MOUSEEVENTF_MIDDLEUP = 0x0040; #模拟鼠标中键抬起
MOUSEEVENTF_ABSOLUTE = 0x8000;# 标示是否采用绝对坐标

#1920X1080的屏幕，对应于鼠标移动参数的换算
MOVE_PERCENT_X=int(65550/1080)
MOVE_PERCENT_Y=int(65530/1920)
def move_to( x: int, y: int):
    Mouse_Event(MOUSEEVENTF_MOVE|MOUSEEVENTF_ABSOLUTE, MOVE_PERCENT_X*x, MOVE_PERCENT_Y*y, 0, 0);
    time.sleep(0.1)


def left_down():
    Mouse_Event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0);
    time.sleep(0.1)
def left_up():
    Mouse_Event(MOUSEEVENTF_LEFTUP|MOUSEEVENTF_ABSOLUTE, 0, 0, 0, 0);
    time.sleep(0.1)

def right_down():
    Mouse_Event(MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0);
    time.sleep(0.1)
def right_up():
    Mouse_Event(MOUSEEVENTF_RIGHTUP|MOUSEEVENTF_ABSOLUTE, 0, 0, 0, 0);
    time.sleep(0.1)

#鼠标右键的移动和点击
def mouse_right_click( x: int, y: int):
    move_to(x,y)
    right_down()
    right_up()
#鼠标左键的移动和点击
def mouse_left_click(x:int,y:int):
    move_to(x,y)
    left_down()
    left_up()

if __name__ == "__main__":
    mouse_left_click(2000,900)
