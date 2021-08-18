1 # -*- coding:utf-8 -*-
  2
  3 import win32gui
  4 import time
  5 from PIL import ImageGrab, Image
  6 import numpy as np
  7 import operator
  8 from pymouse import PyMouse
  9
 10
 11 class GameAssist:
 12
 13     def __init__(self, wdname):
 14         """初始化"""
 15
 16         # 取得窗口句柄
 17         self.hwnd = win32gui.FindWindow(0, wdname)
 18         if not self.hwnd:
 19             print("窗口找不到，请确认窗口句柄名称：【%s】" % wdname )
 20             exit()
 21
 22         # 窗口显示最前面
 23         win32gui.SetForegroundWindow(self.hwnd)
 24
 25         # 小图标编号矩阵
 26         self.im2num_arr = []
 27
 28         # 主截图的左上角坐标和右下角坐标
 29         self.scree_left_and_right_point = (299, 251, 768, 564)
 30         # 小图标宽高
 31         self.im_width = 39
 32
 33         # PyMouse对象，鼠标点击
 34         self.mouse = PyMouse()
 35
 36     def screenshot(self):
 37         """屏幕截图"""
 38
 39         # 1、用grab函数截图，参数为左上角和右下角左标
 40         # image = ImageGrab.grab((417, 257, 885, 569))
 41         image = ImageGrab.grab(self.scree_left_and_right_point)
 42
 43         # 2、分切小图
 44         # exit()
 45         image_list = {}
 46         offset = self.im_width  # 39
 47
 48         # 8行12列
 49         for x in range(8):
 50             image_list[x] = {}
 51             for y in range(12):
 52                 # print("show",x, y)
 53                 # exit()
 54                 top = x * offset
 55                 left = y * offset
 56                 right = (y + 1) * offset
 57                 bottom = (x + 1) * offset
 58
 59                 # 用crop函数切割成小图标，参数为图标的左上角和右下角左边
 60                 im = image.crop((left, top, right, bottom))
 61                 # 将切割好的图标存入对应的位置
 62                 image_list[x][y] = im
 63
 64         return image_list
 65
 66     def image2num(self, image_list):
 67         """将图标矩阵转换成数字矩阵"""
 68
 69         # 1、创建全零矩阵和空的一维数组
 70         arr = np.zeros((10, 14), dtype=np.int32)    # 以数字代替图片
 71         image_type_list = []
 72
 73         # 2、识别出不同的图片，将图片矩阵转换成数字矩阵
 74         for i in range(len(image_list)):
 75             for j in range(len(image_list[0])):
 76                 im = image_list[i][j]
 77
 78                 # 验证当前图标是否已存入
 79                 index = self.getIndex(im, image_type_list)
 80
 81                 # 不存在image_type_list
 82                 if index < 0:
 83                     image_type_list.append(im)
 84                     arr[i + 1][j + 1] = len(image_type_list)
 85                 else:
 86                     arr[i + 1][j + 1] = index + 1
 87
 88         print("图标数：", len(image_type_list))
 89
 90         self.im2num_arr = arr
 91         return arr
 92
 93     # 检查数组中是否有图标,如果有则返回索引下表
 94     def getIndex(self,im, im_list):
 95         for i in range(len(im_list)):
 96             if self.isMatch(im, im_list[i]):
 97                 return i
 98
 99         return -1
100
101     # 汉明距离判断两个图标是否一样
102     def isMatch(self, im1, im2):
103
104         # 缩小图标，转成灰度
105         image1 = im1.resize((20, 20), Image.ANTIALIAS).convert("L")
106         image2 = im2.resize((20, 20), Image.ANTIALIAS).convert("L")
107
108         # 将灰度图标转成01串,即系二进制数据
109         pixels1 = list(image1.getdata())
110         pixels2 = list(image2.getdata())
111
112         avg1 = sum(pixels1) / len(pixels1)
113         avg2 = sum(pixels2) / len(pixels2)
114         hash1 = "".join(map(lambda p: "1" if p > avg1 else "0", pixels1))
115         hash2 = "".join(map(lambda p: "1" if p > avg2 else "0", pixels2))
116
117         # 统计两个01串不同数字的个数
118         match = sum(map(operator.ne, hash1, hash2))
119
120         # 阀值设为10
121         return match < 10
122
123     # 判断矩阵是否全为0
124     def isAllZero(self, arr):
125         for i in range(1, 9):
126             for j in range(1, 13):
127                 if arr[i][j] != 0:
128                     return False
129         return True
130
131     # 是否为同行或同列且可连
132     def isReachable(self, x1, y1, x2, y2):
133         # 1、先判断值是否相同
134         if self.im2num_arr[x1][y1] != self.im2num_arr[x2][y2]:
135             return False
136
137         # 1、分别获取两个坐标同行或同列可连的坐标数组
138         list1 = self.getDirectConnectList(x1, y1)
139         list2 = self.getDirectConnectList(x2, y2)
140         # print(x1, y1, list1)
141         # print(x2, y2, list2)
142
143         # exit()
144
145         # 2、比较坐标数组中是否可连
146         for x1, y1 in list1:
147             for x2, y2 in list2:
148                 if self.isDirectConnect(x1, y1, x2, y2):
149                     return True
150         return False
151
152     # 获取同行或同列可连的坐标数组
153     def getDirectConnectList(self, x, y):
154
155         plist = []
156         for px in range(0, 10):
157             for py in range(0, 14):
158                 # 获取同行或同列且为0的坐标
159                 if self.im2num_arr[px][py] == 0 and self.isDirectConnect(x, y, px, py):
160                     plist.append([px, py])
161
162         return plist
163
164     # 是否为同行或同列且可连
165     def isDirectConnect(self, x1, y1, x2, y2):
166         # 1、位置完全相同
167         if x1 == x2 and y1 == y2:
168             return False
169
170         # 2、行列都不同的
171         if x1 != x2 and y1 != y2:
172             return False
173
174         # 3、同行
175         if x1 == x2 and self.isRowConnect(x1, y1, y2):
176             return True
177
178         # 4、同列
179         if y1 == y2 and self.isColConnect(y1, x1, x2):
180             return True
181
182         return False
183
184     # 判断同行是否可连
185     def isRowConnect(self, x, y1, y2):
186         minY = min(y1, y2)
187         maxY = max(y1, y2)
188
189         # 相邻直接可连
190         if maxY - minY == 1:
191             return True
192
193         # 判断两个坐标之间是否全为0
194         for y0 in range(minY + 1, maxY):
195             if self.im2num_arr[x][y0] != 0:
196                 return False
197         return True
198
199     # 判断同列是否可连
200     def isColConnect(self, y, x1, x2):
201         minX = min(x1, x2)
202         maxX = max(x1, x2)
203
204         # 相邻直接可连
205         if maxX - minX == 1:
206             return True
207
208         # 判断两个坐标之间是否全为0
209         for x0 in range(minX + 1, maxX):
210             if self.im2num_arr[x0][y] != 0:
211                 return False
212         return True
213
214     # 点击事件并设置数组为0
215     def clickAndSetZero(self, x1, y1, x2, y2):
216         # print("click", x1, y1, x2, y2)
217
218         # (299, 251, 768, 564)
219         # 原理：左上角图标中点 + 偏移量
220         p1_x = int(self.scree_left_and_right_point[0] + (y1 - 1)*self.im_width + (self.im_width / 2))
221         p1_y = int(self.scree_left_and_right_point[1] + (x1 - 1)*self.im_width + (self.im_width / 2))
222
223         p2_x = int(self.scree_left_and_right_point[0] + (y2 - 1)*self.im_width + (self.im_width / 2))
224         p2_y = int(self.scree_left_and_right_point[1] + (x2 - 1)*self.im_width + (self.im_width / 2))
225
226         time.sleep(0.2)
227         self.mouse.click(p1_x, p1_y)
228         time.sleep(0.2)
229         self.mouse.click(p2_x, p2_y)
230
231         # 设置矩阵值为0
232         self.im2num_arr[x1][y1] = 0
233         self.im2num_arr[x2][y2] = 0
234
235         print("消除：(%d, %d) (%d, %d)" % (x1, y1, x2, y2))
236         # exit()
237
238     # 程序入口、控制中心
239     def start(self):
240
241         # 1、先截取游戏区域大图，然后分切每个小图
242         image_list = self.screenshot()
243
244         # 2、识别小图标，收集编号
245         self.image2num(image_list)
246
247         print(self.im2num_arr)
248
249         # 3、遍历查找可以相连的坐标
250         while not self.isAllZero(self.im2num_arr):
251             for x1 in range(1, 9):
252                 for y1 in range(1, 13):
253                     if self.im2num_arr[x1][y1] == 0:
254                         continue
255
256                     for x2 in range(1, 9):
257                         for y2 in range(1, 13):
258                             # 跳过为0 或者同一个
259                             if self.im2num_arr[x2][y2] == 0 or (x1 == x2 and y1 == y2):
260                                 continue
261                             if self.isReachable(x1, y1, x2, y2):
262                                 self.clickAndSetZero(x1, y1, x2, y2)
263
264
265 if __name__ == "__main__":
266     # wdname 为连连看窗口的名称，必须写完整
267     wdname = u'宠物连连看经典版2,宠物连连看经典版2小游戏,4399小游戏 www.4399.com - Google Chrome'
268
269     demo = GameAssist(wdname)
270     demo.start()

GameAssist.py
