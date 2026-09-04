# -*- coding: utf-8 -*-
"""
实践任务3 - 例程2（自选图版）：
从公交车 myCar.jpg 中提取梯形广告区域，并透视矫正成规则矩形。
与 ImgMapping2.py 逻辑一致，仅替换了图像与广告区角点。
"""
import cv2
import numpy as np

# 1. 读取公交车图像（彩色）
car_img = cv2.imread('myCar.jpg', cv2.IMREAD_COLOR)
h_car, w_car, _ = car_img.shape

# 2. 手工设置广告区域的四个点 (x, y)
ad_points_car = np.array([
    [315, 250],   # 左上
    [640, 232],   # 右上
    [662, 372],   # 右下
    [330, 385]    # 左下
], dtype=np.float32)

# 3. 创建广告区域掩模
mask = np.zeros((h_car, w_car), dtype=np.uint8)
cv2.fillPoly(mask, [ad_points_car.astype(np.int32)], 255)
mask_3ch = cv2.merge([mask, mask, mask])

# 4. 提取广告区域图像（保留彩色）
ad_region_img = np.zeros_like(car_img)
ad_region_img = np.where(mask_3ch == 255, car_img, 0)
cv2.imwrite('2_ExtractedAdImg.jpg', ad_region_img)

# 5. 计算透视变换，把广告区域矫正成矩形
rect_width = int(max(np.linalg.norm(ad_points_car[0] - ad_points_car[1]),
                     np.linalg.norm(ad_points_car[2] - ad_points_car[3])))
rect_height = int(max(np.linalg.norm(ad_points_car[0] - ad_points_car[3]),
                      np.linalg.norm(ad_points_car[1] - ad_points_car[2])))

rect_points = np.array([
    [0, 0],
    [rect_width - 1, 0],
    [rect_width - 1, rect_height - 1],
    [0, rect_height - 1]
], dtype=np.float32)

M = cv2.getPerspectiveTransform(ad_points_car, rect_points)
ad_rectified = cv2.warpPerspective(car_img, M, (rect_width, rect_height))
cv2.imwrite('2_ADRectified.jpg', ad_rectified)

print("已保存 2_ExtractedAdImg.jpg / 2_ADRectified.jpg")
