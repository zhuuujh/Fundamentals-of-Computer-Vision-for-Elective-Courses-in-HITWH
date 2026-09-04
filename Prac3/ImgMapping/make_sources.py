# -*- coding: utf-8 -*-
"""
实践任务3 用到的两张"自己找的"素材图：
  1) myCar.jpg   —— 一辆侧面带广告牌的城市公交车（广告牌为梯形，便于演示透视）
  2) myArt.jpg   —— 一幅彩色艺术作品（落日渐变 + 太阳 + 山影）

同时把广告牌四个角点保存为 ad_points_car，供两个映射脚本使用。
"""
import cv2
import numpy as np

# ================= 场景：城市公交车 =================
W, H = 900, 620
scene = np.zeros((H, W, 3), np.uint8)

# 天空（上浅下深的蓝色渐变）
for y in range(int(H * 0.62)):
    t = y / (H * 0.62)
    c = (int(190 - 60 * t), int(220 - 60 * t), int(240 - 40 * t))
    cv2.line(scene, (0, y), (W, y), c, 1)

# 路面（灰色）
cv2.rectangle(scene, (0, int(H * 0.62)), (W, H), (90, 95, 100), -1)
cv2.rectangle(scene, (0, int(H * 0.62)), (W, int(H * 0.62) + 6), (150, 150, 150), -1)
# 车道虚线
for x in range(0, W, 120):
    cv2.rectangle(scene, (x, int(H * 0.78)), (x + 55, int(H * 0.80)), (200, 200, 200), -1)

# ---- 公交车 ----
bx0, by0, bx1, by1 = 70, 150, 810, 470        # 车身外框
# 车身主体（白/橙）
bus = np.zeros((H, W, 3), np.uint8)
body = np.zeros((3,), np.uint8)                # placeholder
# 车身底色
pts = np.array([[bx0, by0], [bx1, by0], [bx1, by1 - 30], [bx0, by1 - 30]], np.int32)
cv2.fillConvexPoly(scene, pts, (230, 235, 240))            # 白色车身
cv2.rectangle(scene, (bx0, by1 - 30), (bx1, by1), (255, 160, 40), -1)   # 橙色裙边
cv2.rectangle(scene, (bx0, by1 - 6), (bx1, by1), (40, 40, 40), -1)       # 底部深色
# 前窗与后窗
cv2.rectangle(scene, (bx0 + 10, by0 + 15), (bx0 + 95, by1 - 90), (35, 40, 50), -1)
cv2.rectangle(scene, (bx1 - 95, by0 + 15), (bx1 - 10, by1 - 90), (35, 40, 50), -1)
# 侧面一排车窗
for i in range(4):
    wx = bx0 + 130 + i * 135
    cv2.rectangle(scene, (wx, by0 + 18), (wx + 105, by0 + 95), (50, 60, 75), -1)
    cv2.line(scene, (wx + 52, by0 + 18), (wx + 52, by0 + 95), (200, 205, 210), 2)
# 车门
cv2.rectangle(scene, (bx0 + 300, by0 + 30), (bx0 + 420, by1 - 30), (70, 78, 92), -1)
# 车轮
for cx in [bx0 + 150, bx1 - 150]:
    cv2.circle(scene, (cx, by1), 55, (15, 15, 18), -1)
    cv2.circle(scene, (cx, by1), 55, (90, 90, 95), 4)
    cv2.circle(scene, (cx, by1), 16, (60, 60, 65), -1)
# 车头灯
cv2.circle(scene, (bx0 + 30, by1 - 45), 12, (255, 230, 120), -1)
cv2.circle(scene, (bx0 + 62, by1 - 45), 12, (255, 230, 120), -1)

# ---- 广告牌（梯形，右窄左宽 = 透视收缩）----
ad_points_car = np.array([
    [315, 250],   # 左上
    [640, 232],   # 右上
    [662, 372],   # 右下
    [330, 385],   # 左下
], np.float32)
# 广告牌底色（浅色，便于看清映射出的艺术图）
cv2.fillPoly(scene, [ad_points_car.astype(np.int32)], (225, 228, 235))
cv2.polylines(scene, [ad_points_car.astype(np.int32)], True, (60, 60, 65), 3)
cv2.putText(scene, "AD AREA", (430, 320), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (120, 120, 130), 2)

cv2.imwrite("myCar.jpg", scene)
print("已生成 myCar.jpg", scene.shape, "广告角点(左上/右上/右下/左下):")
print(ad_points_car.tolist())

# ================= 艺术作品：落日渐变 =================
aw, ah = 480, 380
art = np.zeros((ah, aw, 3), np.uint8)
# 天空渐变（顶部深橙 -> 中部亮黄）
for y in range(ah):
    t = y / ah
    c = (int(40 + 200 * t), int(80 + 160 * t), int(230 - 60 * t))
    cv2.line(art, (0, y), (aw, y), c, 1)
# 太阳
cv2.circle(art, (int(aw * 0.7), int(ah * 0.42)), 70, (30, 200, 255), -1)
# 山脉（近实远淡）
for i, (col, base) in enumerate([((45, 60, 70), 0.72), ((25, 35, 45), 0.80)]):
    pts = np.array([[0, int(ah * base)],
                    [int(aw * 0.2), int(ah * (base - 0.14))],
                    [int(aw * 0.4), int(ah * base)],
                    [int(aw * 0.6), int(ah * (base - 0.18))],
                    [int(aw * 0.85), int(ah * base)],
                    [aw, int(ah * (base - 0.06))],
                    [aw, ah], [0, ah]], np.int32)
    cv2.fillPoly(art, [pts], col)
# 海面倒影
cv2.rectangle(art, (0, int(ah * 0.9)), (aw, ah), (20, 30, 45), -1)
for x in range(0, aw, 30):
    cv2.line(art, (x, int(ah * 0.92)), (x + 20, int(ah * 0.98)), (30, 170, 230), 2)

cv2.imwrite("myArt.jpg", art)
print("已生成 myArt.jpg", art.shape)
