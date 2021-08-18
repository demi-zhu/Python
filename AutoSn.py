import win32gui
import win32api
import win32con
import sys, os
from tkinter import *
from tkinter import ttk
import time
import random
global Serial
global batch
def GotVersion():
    return cmb.get()
def Got_Windows():
    classname = "BartendWindowClass"
    titlename = "BarTender Professional - [demo.btw *]"
    #获取句柄
    hwnd= win32gui.FindWindow(classname, titlename)
    win32gui.SetForegroundWindow(hwnd)


def Got_Tool():
    classname = "TkTopLevel"
    titlename = "SN打印工具     v1.0.0"
    #获取句柄
    hwnd= win32gui.FindWindow(classname, titlename)
    win32gui.SetForegroundWindow(hwnd)

def Gerate_SN(Serial):
    global batch
    this_dir = os.path.split(sys.argv[0])[0] #获取当前路径
    source=os.path.join(this_dir, "source.txt")
    print("patch:",source)
    randomInt=random.randint(0,9)
    f = open(source,'w',encoding='utf-8')
    auxiliary=sum([int(i) for i in list(batch)])
    auxiliary1=sum([int(i) for i in list(Serial)])
    print("auxiliary auxiliary1",auxiliary,auxiliary1)
    lrc=sum([int(i) for i in list(batch)]) +sum([int(i) for i in list(Serial)])+randomInt+1
    print("randomInt",randomInt)
    print("lrc:",lrc)
    print("batch:",batch)
    version =GotVersion()
    print("version:",version)
    if version=="单4G版本":
        f.write('demo'+"\r"+"A01"+batch+Serial+str(randomInt)+str(lrc)[-1])
    else:
        f.write('demo'+"\r"+"https://cloudspeaker.chinaums.com/airkiss.html?sn=A01"+batch+Serial+str(randomInt)+str(lrc)[-1])
    f.close()
    print(source)

# 返回批次号
def inputBatch_click():
    global batch
    batch = inputBatch.get()
# 返回流水号
def inputSerial_click():
    global Serial
    Serial= inputSerial.get()

def PrintSN_click():
    global Serial
    Serial=str(int(Serial)+1).zfill(5)
    print("Serial:",Serial)
    Gerate_SN(Serial)
    Got_Windows()
    time.sleep(1)
    win32api.keybd_event(17,0,0,0)      # Contrl
    time.sleep(1)
    win32api.keybd_event(80,0,0,0)     # P
    time.sleep(1)
    win32api.keybd_event(80,0,win32con.KEYEVENTF_KEYUP,0)  #释放按键
    time.sleep(1)
    win32api.keybd_event(17,0,win32con.KEYEVENTF_KEYUP,0)
    time.sleep(5)
    win32api.keybd_event(13,0,0,0)     # enter
    time.sleep(1)
    win32api.keybd_event(13,0,win32con.KEYEVENTF_KEYUP,0)
    time.sleep(5)
    Got_Tool()


root =Tk()
root.title('SN打印工具     v1.0.0')
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
size = '%dx%d+%d+%d' % (600, 400, (screenwidth - 600) / 2, (screenheight - 400) / 2)
root.geometry(size)


lb1 = Label(root, text='批次(日期):',bg='#d3fbfb',fg='blue',font=('微软雅黑',15))
lb1.place(relx=0.1, rely=0.2, relwidth=0.2, relheight=0.1)
inputBatch=Entry(root)
inputBatch.place(relx=0.3, rely=0.2, relwidth=0.5, relheight=0.1)

button =Button(root, text="提交批次",command=inputBatch_click,font=('微软雅黑',15),fg='green')
button.place(relx=0.8, rely=0.2, relwidth=0.2, relheight=0.1)



lb1 = Label(root, text='起始流水号:',bg='#d3fbfb',fg='blue',font=('微软雅黑',15))
lb1.place(relx=0.1, rely=0.4, relwidth=0.2, relheight=0.1)
inputSerial=Entry(root)
inputSerial.place(relx=0.3, rely=0.4, relwidth=0.5, relheight=0.1)


button =Button(root, text="提交流水",command=inputSerial_click,font=('微软雅黑',15),fg='green')
button.place(relx=0.8, rely=0.4, relwidth=0.2, relheight=0.1)


button =Button(root, text="打印SN",command=PrintSN_click,font=('微软雅黑',25),fg='black')
button.place(relx=0.3, rely=0.6, relwidth=0.4, relheight=0.2)

note =Label(root,text="注意：",font=('微软雅黑',12))
note.place(relx=0, rely=0.7, width=50, relheight=0.1)



note1 =Label(root,text="批次格式为年月日,例:20210708",font=('微软雅黑',10))
note1.place(relx=0, rely=0.8, width=235, relheight=0.1)

note2 =Label(root,text="请务必先提交批次和流水后再点击打印SN!",font=('微软雅黑',10))
note2.place(relx=0, rely=0.9, width=290, relheight=0.1)
lb1 = Label(root, text='Author:Ou Yiwen',font=('微软雅黑',8))
lb1.place(relx=0.8, rely=0.9, relwidth=0.2, relheight=0.1)

lb1 = Label(root, text='选择版本:',bg='#d3fbfb',fg='blue',font=('微软雅黑',15))
lb1.place(relx=0.1, rely=0, relwidth=0.2, relheight=0.1)
cmb=ttk.Combobox(root,font=('微软雅黑',15),state= "readonly",justify="center",)
cmb.place(relx=0.3, rely=0, relwidth=0.5, relheight=0.1)
# combostyle = ttk.Style()
# combostyle.theme_create('combostyle', parent='alt',
#                                 settings={'TCombobox':
#                                     {'configure':
#                                         {
                                            # 'foreground': 'black',  # 前景色
                                            # 'selectbackground': 'blue',  # 选择后的背景颜色
                                            # 'fieldbackground': 'white',  # 下拉框颜色
                                            # 'background': 'pink',  # 下拉按钮颜色
#                                         }}}
#                                 )
# combostyle.theme_use('combostyle')
cmb['value'] = ('单4G版本','4G+WIFI版本')
cmb.bind("<<ComboboxSelected>>",GotVersion)
# cmb.current(0)
root.mainloop()
