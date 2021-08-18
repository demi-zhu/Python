import cv2
import numpy as np

# 读取图片，丢弃Alpha通道，转为灰度图
a = cv2.imread('123.png', cv2.IMREAD_GRAYSCALE)
# 读取图片，并保留Alpha通道
b = cv2.imread('12.png', cv2.IMREAD_UNCHANGED)
# 取出Alpha通道
alpha = b[:,:,3]
# 将透明点置0
a = cv2.bitwise_and(a, alpha)
b = cv2.bitwise_and(cv2.cvtColor(b, cv2.COLOR_BGRA2GRAY), alpha)
# 比较两张图，打印不相等的像素个数
print(np.count_nonzero(cv2.compare(a, b, cv2.CMP_NE)))
