#若该键盘鼠标的操作被检测到了，可以使用pip install pywinio模块，制作驱动级别的键鼠模拟

from ctypes import windll, byref, c_ubyte
from ctypes.wintypes import RECT, HWND
import numpy as np
import time
# import mouse as mouse
GetDC = windll.user32.GetDC
CreateCompatibleDC = windll.gdi32.CreateCompatibleDC
GetClientRect = windll.user32.GetClientRect
CreateCompatibleBitmap = windll.gdi32.CreateCompatibleBitmap
SelectObject = windll.gdi32.SelectObject
BitBlt = windll.gdi32.BitBlt
SRCCOPY = 0x00CC0020
GetBitmapBits = windll.gdi32.GetBitmapBits
DeleteObject = windll.gdi32.DeleteObject
ReleaseDC = windll.user32.ReleaseDC

# 防止UI放大导致截图不完整
#windll.user32.SetProcessDPIAware()

def capture(handle: HWND):
    """窗口客户区截图

    Args:
        handle (HWND): 要截图的窗口句柄

    Returns:
        numpy.ndarray: 截图数据
    """
    # 获取窗口客户区的大小
    r = RECT()
    GetClientRect(handle, byref(r))
    width, height = r.right, r.bottom
    # 开始截图
    dc = GetDC(handle)
    cdc = CreateCompatibleDC(dc)
    bitmap = CreateCompatibleBitmap(dc, width, height)
    SelectObject(cdc, bitmap)
    BitBlt(cdc, 0, 0, width, height, dc, 0, 0, SRCCOPY)
    # 截图是BGRA排列，因此总元素个数需要乘以4
    total_bytes = width*height*4
    buffer = bytearray(total_bytes)
    byte_array = c_ubyte*total_bytes
    GetBitmapBits(bitmap, total_bytes, byte_array.from_buffer(buffer))
    DeleteObject(bitmap)
    DeleteObject(cdc)
    ReleaseDC(handle, dc)
    # 返回截图数据为numpy.ndarray
    return np.frombuffer(buffer, dtype=np.uint8).reshape(height, width, 4)

if __name__ == "__main__":
    import cv2
    handle = windll.user32.FindWindowW(None, "dnf怪物_百度图片搜索")
    # 截图时要保证游戏窗口的客户区大小是1334×750
    image = capture(handle)
    # 转为灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
    # 读取图片，并保留Alpha通道,若要排除背景干扰，需要将源对比图背景设置成透明的，即Alpha通道置为0.
    template = cv2.imread('234.bmp', cv2.IMREAD_UNCHANGED)
    # 转为灰度图
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGRA2GRAY)
    # 取出Alpha通道
    alpha = template[:,:,3]

    # 模板匹配，将alpha作为mask，TM_CCORR_NORMED方法的计算结果范围为[0, 1]，越接近1越匹配 TM_CCOEFF_NORMED
    result = cv2.matchTemplate(gray, template_gray, cv2.TM_CCOEFF_NORMED,mask=alpha)

    # TM_SQDIFF 平方差匹配法：该方法采用平方差来进行匹配；最好的匹配值为0；匹配越差，匹配值越大。
    # TM_CCORR 相关匹配法：该方法采用乘法操作；数值越大表明匹配程度越好。
    # TM_CCOEFF 相关系数匹配法：1表示完美的匹配；-1表示最差的匹配。
    # TM_SQDIFF_NORMED 归一化平方差匹配法
    # TM_CCORR_NORMED 归一化相关匹配法
    # TM_CCOEFF_NORMED 归一化相关系数匹配法
    # result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)

    print(cv2.minMaxLoc(result))
    # 获取结果中最大值和最小值以及他们的坐标
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    # 匹配最大值的坐标，左上角
    top_left = max_loc
    # 模板的高度和宽度
    h, w = template.shape[:2]
    # 右下角的坐标
    bottom_right = top_left[0] + w, top_left[1] + h
    # 在窗口截图中匹配位置画红色方框，在image上画出左上角为top_left，右下角为bottom_right的坐标的矩形
    cv2.rectangle(image, top_left, bottom_right, (0,0,255), 2)
    cv2.imshow('Match Template', image)

    cv2.waitKey()


