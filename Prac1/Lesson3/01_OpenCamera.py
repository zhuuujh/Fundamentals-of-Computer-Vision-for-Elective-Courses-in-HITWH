#打开摄像头 并显示图像
#等待按下ESC键退出

import cv2

# 打开摄像头, 0表示第一个摄像头(默认摄像头)
s = 0
source = cv2.VideoCapture(s)

# 定义一个字符串变量，表示窗口的名称（即标题）
win_name = 'Camera Preview'
# 创建一个名为 'Camera Preview' 的窗口，并设置其属性为 可手动调整大小 
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)

# while循环，如果没有接收到键盘的“ESC”按键，则一直不停地显示摄像头的图像。如果想要退出循环，需要按下“ESC”键。

# cv2.waitKey()函数会等待指定的时间（单位：毫秒），如果有按键按下，则立即返回按键的ASCII码，否则返回-1。
# 如果返回-1，表示没有按键按下，如果返回非-1的ASCII码，则表示有按键按下。Esc按键的ASCII码为27


while cv2.waitKey(1) != 27: 
    has_frame, frame = source.read() # 从摄像头读取一帧图像, has_frame表示是否成功读取到图像，frame表示图像数据
    # 如果没有读取到图像，则退出循环
    if not has_frame:
        break
    # 成功读取到图像,显示图像
    cv2.imshow(win_name, frame)

source.release() # 释放摄像头
cv2.destroyWindow(win_name) # 关闭窗口

