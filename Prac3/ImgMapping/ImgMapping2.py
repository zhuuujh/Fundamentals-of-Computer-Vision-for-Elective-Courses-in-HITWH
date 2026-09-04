import cv2
import numpy as np

# 1. 读取汽车图像（彩色）
car_img = cv2.imread('img1.jpg', cv2.IMREAD_COLOR)
h_car, w_car, _ = car_img.shape

# 2. 手工设置广告区域的四个点 (x, y)
ad_points_car = np.array([
    [502, 324],  # 左上
    [645, 306],  # 右上
    [649, 364],  # 右下
    [504, 396]   # 左下
], dtype=np.float32)

# 3. 创建广告区域掩模
mask = np.zeros((h_car, w_car), dtype=np.uint8)
cv2.fillPoly(mask, [ad_points_car.astype(np.int32)], 255)
mask_3ch = cv2.merge([mask, mask, mask])

# 4. 提取广告区域图像（保留彩色）
ad_region_img = np.zeros_like(car_img)
ad_region_img = np.where(mask_3ch == 255, car_img, 0)

# 保存提取的广告区域图像
cv2.imwrite('2_ExtractedAdImg.jpg', ad_region_img)

# 5. 计算透视变换，把广告区域矫正成矩形
# 目标矩形的宽高
rect_width = int(max(np.linalg.norm(ad_points_car[0]-ad_points_car[1]),
                     np.linalg.norm(ad_points_car[2]-ad_points_car[3])))
rect_height = int(max(np.linalg.norm(ad_points_car[0]-ad_points_car[3]),
                      np.linalg.norm(ad_points_car[1]-ad_points_car[2])))

# 矩形四个点 (左上, 右上, 右下, 左下)
rect_points = np.array([
    [0, 0],
    [rect_width-1, 0],
    [rect_width-1, rect_height-1],
    [0, rect_height-1]
], dtype=np.float32)

# 计算透视变换矩阵
M = cv2.getPerspectiveTransform(ad_points_car, rect_points)

# 应用透视变换，将广告区域恢复为长方形
ad_rectified = cv2.warpPerspective(car_img, M, (rect_width, rect_height))

# 6. 显示结果
cv2.imshow('Car Image', car_img)
cv2.imshow('Extracted Ad Region', ad_region_img)
cv2.imshow('Rectified Ad Region', ad_rectified)

# 保存恢复后的长方形广告图像
cv2.imwrite('2_ADRectified.jpg', ad_rectified)

cv2.waitKey(0)
cv2.destroyAllWindows()

