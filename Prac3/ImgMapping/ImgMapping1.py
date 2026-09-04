import cv2
import numpy as np

# 1. 读取彩色图像
van_gogh_img = cv2.imread('img2.jpg', cv2.IMREAD_COLOR)
car_img = cv2.imread('img1.jpg', cv2.IMREAD_COLOR)

# 获取图像尺寸
h_vg, w_vg, _ = van_gogh_img.shape
h_car, w_car, _ = car_img.shape

# 2. 扩展梵高图像到汽车图像大小
expanded_vg = np.zeros_like(car_img)
# 将梵高图像放在左上角
expanded_vg[0:h_vg, 0:w_vg, :] = van_gogh_img

# 3. 手工设置广告区域的四个点 (x, y)
ad_points_car = np.array([
    [502, 324],  # 左上
    [645, 306],  # 右上
    [649, 364],  # 右下
    [504, 396]   # 左下
], dtype=np.float32)

# 4. 对应梵高图像四个点（稍微内缩8像素）
vg_points = np.array([
    [8, 8],                 # 左上
    [w_vg-8, 8],            # 右上
    [w_vg-8, h_vg-8],       # 右下
    [8, h_vg-8]             # 左下
], dtype=np.float32)

# OpenCV坐标是 (x, y)
vg_points_cv = np.array([[p[0], p[1]] for p in vg_points], dtype=np.float32)
ad_points_cv = np.array([[p[0], p[1]] for p in ad_points_car], dtype=np.float32)

# 5. 计算透视变换矩阵
M = cv2.getPerspectiveTransform(vg_points_cv, ad_points_cv)

# 6. 应用透视变换
warped_vg = cv2.warpPerspective(expanded_vg, M, (w_car, h_car))

# 7. 创建广告区域掩膜（三通道）
mask = np.zeros((h_car, w_car), dtype=np.uint8)
cv2.fillPoly(mask, [ad_points_car.astype(np.int32)], 255)
mask_3ch = cv2.merge([mask, mask, mask])  # 扩展为三通道

# 8. 将变换后的梵高画贴到汽车广告区域
result_img = car_img.copy()
# 使用掩膜选择性替换像素
result_img = np.where(mask_3ch == 255, warped_vg, result_img)

# 9. 显示图像
cv2.imshow('Expanded Van Gogh', expanded_vg)
cv2.imshow('Warped Van Gogh', warped_vg)
cv2.imshow('Car Image', car_img)
cv2.imshow('Result Image', result_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 10. 保存结果
cv2.imwrite('1_ExpandedVanGogh.jpg', expanded_vg)
cv2.imwrite('1_WarpedVanGogh.jpg', warped_vg)
cv2.imwrite('1_CarVanGogh.jpg', result_img)
