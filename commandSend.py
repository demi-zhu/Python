
import serial
import time
import binascii
from ctypes import c_ulong, windll, byref
from ctypes.wintypes import HWND, POINT
from serial.serialwin32 import Serial
getMousePos=windll.user32.GetCursorPos
portx = "COM5"
bps = 115200
timex = 5
VkCode = {
    "stopmove":0x00,
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
#将字符串转换成byte字节,字符串的每两个会被当成一个字节，例如data=“04”，则byte为b'\x04'，即十六进制的04，8位一个字节
def strTobytes(data:str):
    byte=bytes.fromhex(data)
    return byte
#与上一个函数相反，将bytes类型的字符转换成string类型
def bytesTostr(data:bytes):
    string=data.hex()
    return string
#bytes类型的变量x，转化为十进制整数
#函数参数：int.from_bytes(bytes, byteorder, *, signed=False)
# byteorder大小端；,小端是低位在前，高位在后。signed=True表示需要考虑符号位。
#int.to_bytes函数是上面的逆过程

#pyserial通过串口发送的数据类型能且仅能是bytes类型
def keySend(key:str,ser:Serial):
    ser.write(b'\x02\xf0\x03')
    virkey="%02x"%(VkCode[key])     #格式化输出，将VkCode[key]的值转换成2位的字符串(原本是int)
    ser.write(strTobytes(virkey))   #将字符串转换成bytes类型并通过串口输出
    ser.write(b'\x2e')
def keyStringSend(key:str,time_s=0.001):         #不同字符之间用空格或者+连接
    ser = serial.Serial(portx, bps, timeout=timex)
    time.sleep(0.05)
    if key.find('+')==-1:
        tmp=key.split()
    else:
        tmp=key.split('+')
    for item in tmp:
        keySend(item,ser)
        time.sleep(time_s)
    ser.close()
def mouseMovesend(x:int,y:int,time_s=0.1):
    ser = serial.Serial(portx, bps, timeout=timex)
    time.sleep(0.05)
    po=POINT()
    getMousePos(byref(po)) #获取当前鼠标位置
    print("MOUSE_POS:",po.x,po.y)
    if x-po.x>0:                #右移
        result_x=divmod(x-po.x,127)
        # print("result:",result_x[0],result_x[1])
        for item in range(result_x[0]):
            ser.write(b'\x02\xf0\x03')
            ser.write(b'\x00\x7f\x00')
            ser.write(b'\x2e')
            time.sleep(time_s)
        ser.write(b'\x02\xf0\x03')
        ser.write(b'\x00')
        if result_x[1]==46 or result_x[1]==21:#避免"!"."的冲突
            result_x[1]=result_x[1]+1
        remainder=strTobytes("%02x"%(result_x[1]))
        # print("remainder:",remainder)
        ser.write(remainder)
        ser.write(b'\x00')
        ser.write(b'\x2e')
    elif x-po.x<0:              #左移
        result_x=divmod(po.x-x,127)
        # print("result:",result_x[0],result_x[1])
        for item in range(result_x[0]):
            ser.write(b'\x02\xf0\x03')
            ser.write(b'\x00\x81\x00')
            ser.write(b'\x2e')
            time.sleep(time_s)
        ser.write(b'\x02\xf0\x03')
        ser.write(b'\x00')
        if result_x[1]==46 or result_x[1]==21:#避免"!"."的冲突
            result_x[1]=result_x[1]+1
        complement=(bin(-result_x[1]&0xff).replace("0b",""))    #计算补码
        # print("compelent:",complement)
        hex_str="%02x"%(int(complement,2))                      #转换成十六进制字符串
        # print("hex_str:",hex_str)
        hex_b=strTobytes(hex_str)                               #转换成字节发送
        # print("hex_b:",hex_b)
        ser.write(hex_b)
        ser.write(b'\x00')
        ser.write(b'\x2e')

    if y-po.y>0:                #下移
        result_y=divmod(y-po.y,127)
        print("result:",result_y[0],result_y[1])
        for item in range(result_y[0]):
            ser.write(b'\x02\xf0\x03')
            ser.write(b'\x00\x00\x7f')
            ser.write(b'\x2e')
            time.sleep(time_s)
        ser.write(b'\x02\xf0\x03')
        ser.write(b'\x00\x00')
        if result_y[1]==46 or result_y[1]==21:#避免"!"."的冲突
            result_y[1]=result_y[1]+1
        remainder=strTobytes("%02x"%(result_y[1]))
        print("remainder:",remainder)
        ser.write(remainder)
        ser.write(b'\x2e')
    elif y-po.y<0:              #上移
        result_y=divmod(po.y-y,127)
        print("result:",result_y[0],result_y[1])
        for item in range(result_y[0]):
            ser.write(b'\x02\xf0\x03')
            ser.write(b'\x00\x00\x81')
            ser.write(b'\x2e')
            time.sleep(time_s)
        ser.write(b'\x02\xf0\x03')
        ser.write(b'\x00\x00')
        if result_y[1]==46 or result_y[1]==21:#避免"!"."的冲突
            result_y[1]=result_y[1]+1
        complement=(bin(-result_y[1]&0xff).replace("0b",""))    #计算补码
        print("compelent:",complement)
        hex_str="%02x"%(int(complement,2))                      #转换成十六进制字符串
        print("hex_str:",hex_str)
        hex_b=strTobytes(hex_str)                               #转换成字节发送
        print("hex_b:",hex_b)
        ser.write(hex_b)
        ser.write(b'\x2e')
    ser.close()
def mouseLeftclick():
    ser = serial.Serial(portx, bps, timeout=timex)
    time.sleep(0.1)
    ser.write(b'\x02\xf0\x03')
    ser.write(b'\x01\x00\x00')
    ser.write(b'\x2e')
    time.sleep(0.05)
    ser.write(b'\x02\xf0\x03')
    ser.write(b'\x00\x00\x00')
    time.sleep(0.05)
    ser.write(b'\x2e')
def mouseRightclick():
    ser = serial.Serial(portx, bps, timeout=timex)
    time.sleep(0.1)
    ser.write(b'\x02\xf0\x03')
    ser.write(b'\x06\x00\x00')
    ser.write(b'\x2e')
    time.sleep(0.05)
    ser.write(b'\x02\xf0\x03')
    ser.write(b'\x00\x00\x00')
    time.sleep(0.05)
    ser.write(b'\x2e')
if __name__ == "__main__":
    mouseRightclick()

