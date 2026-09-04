# -*- coding: utf-8 -*-
"""
任务2 步骤2、3：把图像A缩放后，以半透明卡片方式叠加到灰度图、彩色图的右上角
"""
import cv2
import numpy as np

A = cv2.imread("A.png", cv2.IMREAD_GRAYSCALE)

def overlay_a(base, ratio=0.38, margin=18, top=18, alpha=0.78):
    """把A叠加到base右上角，返回叠加后的BGR图像"""
    h, w = base.shape[:2]
    # 1) 按比例缩放A（宽度占原图宽度的 ratio）
    aw = int(w * ratio)
    ah = int(aw * A.shape[0] / A.shape[1])
    a_img = cv2.resize(A, (aw, ah), interpolation=cv2.INTER_AREA)

    # 2) 做一张白色卡片，内含A，便于在不同背景上醒目
    m = 8                       # A在卡片内的留白
    card = np.full((ah + 2 * m, aw + 2 * m, 3), 255, np.uint8)
    card[m:m + ah, m:m + aw] = cv2.cvtColor(a_img, cv2.COLOR_GRAY2BGR)
    # 卡片加一圈细边框
    cv2.rectangle(card, (0, 0), (card.shape[1] - 1, card.shape[0] - 1),
                  (0, 0, 0), 2)

    ch, cw = card.shape[:2]
    left = w - cw - margin
    topy = top
    # 3) 确保卡片在图像范围内
    if left < 0:
        left = 0
    if topy + ch > h:
        topy = h - ch
    region = base[topy:topy + ch, left:left + cw]

    # 4) 半透明混叠：背景微微透出，文字保持清晰
    blended = cv2.addWeighted(card, alpha, region, 1 - alpha, 0)
    base[topy:topy + ch, left:left + cw] = blended
    return base

# ---- 灰度图：lena512.bmp ----
gray = cv2.imread("images/lena512.bmp", cv2.IMREAD_GRAYSCALE)
gray_bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
gray_out = overlay_a(gray_bgr)
cv2.imwrite("gray_overlay_A.png", gray_out)
print("灰度图叠加完成 -> gray_overlay_A.png", gray_out.shape)

# ---- 彩色图：peppers.png ----
color = cv2.imread("images/peppers.png")
color_out = overlay_a(color)
cv2.imwrite("color_overlay_A.png", color_out)
print("彩色图叠加完成 -> color_overlay_A.png", color_out.shape)
