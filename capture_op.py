from win32com.client import Dispatch
class CAPTURE_PICTURE:
    def __init__(self):
        #创建com对象
        self.op=op=Dispatch("op.opsoft");
        self.op.SetPath(R"C:\Users\YWOU\Desktop")
        self.hwnd=0;
        self.send_hwnd=0;
        print("init");
    def get_picture(self):
        cr=self.op.GetColor(30,30);
        print("color of (30,30):",cr);
        ret=self.op.Capture(250,120,1100,690,"screen.bmp");
        print("op.Capture ret:",ret);
    def find_picture(self,x1:int,y1:int,x2:int,y2:int):
        r,x,y=self.op.FindPic(x1,y1,x2,y2,"12.png","000000",0.8,0);
        print("op.FindPic:",r,x,y);

if __name__ == "__main__":
    capture_FILE=CAPTURE_PICTURE()
    capture_FILE.get_picture()
    capture_FILE.find_picture(250,120,1100,690)
