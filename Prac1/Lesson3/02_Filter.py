import cv2
import numpy as np
import time

# 定义常量，表示不同的滤镜模式
PREVIEW  = 0  # Preview Mode 预览模式
BLUR     = 1  # Blurring Filter 高斯模糊
CANNY    = 2  # Canny Edge Detector 边缘检测
EMBOSS   = 3  # Emboss 浮雕效果
SKETCH   = 4  # Pencil Sketch 素描效果
MOSAIC   = 5  # Mosaic 马赛克效果

s = 0

# 设置默认滤镜模式
image_filter = PREVIEW
#image_filter = CANNY
#image_filter = BLUR

alive = True

# 设置窗口名，创建窗口
win_name = "Camera Filters"
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
result = None

# 打开摄像头，获取视频流
source = cv2.VideoCapture(s)

# 用于给截图文件加时间戳
snap_count = 0

# ---- 浮雕效果使用的 3x3 卷积核 ----
# 对角线方向明暗不同，产生凹凸立体感，+128 保证像素值在 0~255 范围内
emboss_kernel = np.array([[-1, -1,  0],
                          [-1,  0,  1],
                          [ 0,  1,  1]])
# 用 filter2D 对一帧图像做浮雕处理
def emboss(frame):
    return cv2.filter2D(frame, -1, emboss_kernel, delta=128)

# ---- 素描效果：灰度->反色->高斯模糊->颜色减淡(color dodge) ----
def sketch(frame):
    gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)          # 1. 灰度化
    inv   = 255 - gray                                       # 2. 反色
    blur  = cv2.GaussianBlur(inv, (13, 13), 0)               # 3. 高斯模糊
    # 4. 颜色减淡：gray * 255 / (255 - blur)，避免除零加 1e-3
    #    统一转成 float32，避免 cv2.divide 的数组类型不匹配报错
    gray_f = gray.astype(np.float32)
    denom  = (255 - blur).astype(np.float32) + 1e-3
    return cv2.divide(gray_f, denom, scale=255).astype(np.uint8)

# ---- 马赛克效果：缩小后最近邻放大成像素方块 ----
def mosaic(frame, block=25):
    h, w = frame.shape[:2]
    small = cv2.resize(frame, (w // block, h // block), interpolation=cv2.INTER_NEAREST)
    return cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)

# while循环
while alive:
    # 获取视频帧
    has_frame, frame = source.read()

    # 如果没有视频帧，退出循环
    if not has_frame:
        break

    # 翻转视频帧
    frame = cv2.flip(frame, 1)

    # 处理视频帧
    # 预览模式，直接显示原图
    if image_filter == PREVIEW:
        result = frame

    # 边缘检测模式，使用Canny边缘检测,参数为(80,150)，表示低阈值和高阈值
    elif image_filter == CANNY:
        result = cv2.Canny(frame, 80, 150)

    # 滤波模式，使用高斯模糊滤波，参数为(13,13)，表示高斯核大小
    elif image_filter == BLUR:
        result = cv2.blur(frame, (13, 13))

    # 浮雕模式，使用上面定义的卷积核做卷积
    elif image_filter == EMBOSS:
        result = emboss(frame)

    # 素描模式，使用灰度+颜色减淡算法
    elif image_filter == SKETCH:
        result = sketch(frame)

    # 马赛克模式，缩小再放大的像素化效果
    elif image_filter == MOSAIC:
        result = mosaic(frame)

    # 显示结果
    cv2.imshow(win_name, result)

    # 获取键盘输入
    key = cv2.waitKey(1)
    # 按下“Q”或“q”或Esc键，退出循环
    if key == ord("Q") or key == ord("q") or key == 27:
        alive = False

    # 按下“C”或“c”键，切换到Canny边缘检测模式
    elif key == ord("C") or key == ord("c"):
        image_filter = CANNY

    # 按下“B”或“b”键，切换到高斯模糊滤波模式
    elif key == ord("B") or key == ord("b"):
        image_filter = BLUR

    # 按下“P”或“p”键，切换到预览模式
    elif key == ord("P") or key == ord("p"):
        image_filter = PREVIEW

    # 按下“E”或“e”键，切换到浮雕模式
    elif key == ord("E") or key == ord("e"):
        image_filter = EMBOSS

    # 按下“K”或“k”键，切换到素描模式
    elif key == ord("K") or key == ord("k"):
        image_filter = SKETCH

    # 按下“M”或“m”键，切换到马赛克模式
    elif key == ord("M") or key == ord("m"):
        image_filter = MOSAIC

    # 按下“S”或“s”键，保存当前帧截图，用于撰写Word报告
    elif key == ord("S") or key == ord("s"):
        snap_count += 1
        name = "snapshot_%d.png" % snap_count
        cv2.imwrite(name, result)
        print("已保存截图: " + name)

source.release()  # 释放摄像头
cv2.destroyWindow(win_name)  # 关闭窗口
