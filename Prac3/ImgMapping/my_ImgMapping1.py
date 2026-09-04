# -*- coding: utf-8 -*-
"""
实践任务3 - 例程1（自选图版）：
把艺术作品 myArt.jpg 通过透视变换贴到公交车 myCar.jpg 的广告区域上。
与 ImgMapping1.py 逻辑一致，仅替换了图像与广告区角点。
"""
import cv2
import numpy as np

# 1. 读取彩色图像
art_img = cv2.imread('myArt.jpg', cv2.IMREAD_COLOR)      # 艺术作品
car_img = cv2.imread('myCar.jpg', cv2.IMREAD_COLOR)      # 公交车

h_art, w_art, _ = art_img.shape
h_car, w_car, _ = car_img.shape

# 2. 扩展艺术图像到公交车大小
expanded_art = np.zeros_like(car_img)
expanded_art[0:h_art, 0:w_art, :] = art_img

# 3. 手工设置广告区域的四个点 (x, y) —— 对应我生成的公交车梯形广告牌
ad_points_car = np.array([
    [315, 250],   # 左上
    [640, 232],   # 右上
    [662, 372],   # 右下
    [330, 385]    # 左下
], dtype=np.float32)

# 4. 对应艺术作品四个点（稍微内缩8像素）
art_points = np.array([
    [8, 8],
    [w_art - 8, 8],
    [w_art - 8, h_art - 8],
    [8, h_art - 8]
], dtype=np.float32)

# OpenCV坐标是 (x, y)
art_points_cv = np.array([[p[0], p[1]] for p in art_points], dtype=np.float32)
ad_points_cv = np.array([[p[0], p[1]] for p in ad_points_car], dtype=np.float32)

# 5. 计算透视变换矩阵
M = cv2.getPerspectiveTransform(art_points_cv, ad_points_cv)

# 6. 应用透视变换
warped_art = cv2.warpPerspective(expanded_art, M, (w_car, h_car))

# 7. 创建广告区域掩膜（三通道）
mask = np.zeros((h_car, w_car), dtype=np.uint8)
cv2.fillPoly(mask, [ad_points_car.astype(np.int32)], 255)
mask_3ch = cv2.merge([mask, mask, mask])

# 8. 将变换后的艺术图贴到公交车广告区域
result_img = car_img.copy()
result_img = np.where(mask_3ch == 255, warped_art, result_img)

# 9. 保存中间结果与最终结果
cv2.imwrite('1_ExpandedArt.jpg', expanded_art)     # 扩展后的艺术图(中间)
cv2.imwrite('1_WarpedArt.jpg', warped_art)         # 透视变换后的艺术图(中间)
cv2.imwrite('1_BusArt.jpg', result_img)            # 最终结果：公交+艺术广告
print("已保存 1_ExpandedArt.jpg / 1_WarpedArt.jpg / 1_BusArt.jpg")
