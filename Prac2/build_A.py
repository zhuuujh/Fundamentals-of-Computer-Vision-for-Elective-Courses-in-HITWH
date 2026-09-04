# -*- coding: utf-8 -*-
"""
任务2 步骤1：从 homework1.png 中提取学号姓名拼音用到的字符，生成图像 A.png
学号: 2025210515  姓名拼音: ZHUJIAHE
"""
import cv2
import numpy as np

src = cv2.imread("homework1.png", cv2.IMREAD_GRAYSCALE)
_, bw = cv2.threshold(src, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
# 轻度形态学闭运算，把同一字符可能断开的部分接起来
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
bw = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel)

num, labels, stats, centroids = cv2.connectedComponentsWithStats(bw)
comps = []
for i in range(1, num):
    x, y, w, h, area = stats[i]
    if area > 150:
        comps.append((centroids[i][1], centroids[i][0], x, y, w, h))

# 按行聚类：用 y 中给每行定义字符模板
def assign_row(cy):
    if cy < 130:
        return 0          # 第1行: 数字 0-9
    if cy < 320:
        return 1          # 第2行: 字母 A-N
    return 2              # 第3行: 字母 O-Z

row_chars = {0: "0123456789", 1: "ABCDEFGHIJKLMN", 2: "OPQRSTUVWXYZ"}
grouped = {0: [], 1: [], 2: []}
for cy, cx, x, y, w, h in comps:
    r = assign_row(cy)
    grouped[r].append((cx, x, y, w, h))

# 每行按 x 从左到右排序，映射成字符
char_map = {}   # 字符 -> (x,y,w,h)
for r, lst in grouped.items():
    lst.sort(key=lambda t: t[0])
    assert len(lst) == len(row_chars[r]), f"第{r}行字符数异常: {len(lst)} != {len(row_chars[r])}"
    for (cx, x, y, w, h), ch in zip(lst, row_chars[r]):
        char_map[ch] = (x, y, w, h)

def crop_char(ch, pad=6):
    x, y, w, h = char_map[ch]
    x0 = max(0, x - pad); y0 = max(0, y - pad)
    x1 = min(src.shape[1], x + w + pad); y1 = min(src.shape[0], y + h + pad)
    return src[y0:y1, x0:x1]

def make_row(text, H=130):
    """把一串字符拼成一行（白底黑字），返回单行图"""
    pieces = []
    for ch in text:
        c = crop_char(ch)
        c = cv2.copyMakeBorder(c, 4, 4, 4, 4, cv2.BORDER_CONSTANT, value=255)
        c = cv2.resize(c, (int(c.shape[1] * H / c.shape[0]), H), interpolation=cv2.INTER_CUBIC)
        if c.shape[0] < H:
            c = cv2.copyMakeBorder(c, 0, H - c.shape[0], 0, 0, cv2.BORDER_CONSTANT, value=255)
        pieces.append(c)
    gap = 16
    w = sum(p.shape[1] for p in pieces) + gap * (len(pieces) - 1)
    line = np.full((H, w), 255, np.uint8)
    cx = 0
    for p in pieces:
        line[0:H, cx:cx + p.shape[1]] = p
        cx += p.shape[1] + gap
    return line

# 学号一行、姓名拼音一行（内容仍是“学号姓名拼音”，两行更紧凑、叠加到图上可读）
s_id = "2025210515"
s_name = "ZHUJIAHE"

row1 = make_row(s_id)
row2 = make_row(s_name)
hline = max(row1.shape[1], row2.shape[1])
# 补齐等宽，行间留白
pad1 = np.full((row1.shape[0], hline - row1.shape[1]), 255, np.uint8)
pad2 = np.full((row2.shape[0], hline - row2.shape[1]), 255, np.uint8)
row1 = np.hstack([row1, pad1])
row2 = np.hstack([row2, pad2])
vgap = 22
A = np.vstack([row1, np.full((vgap, hline), 255, np.uint8), row2])
# 右侧留白让边缘更整洁
A = np.hstack([A, np.full((A.shape[0], 16), 255, np.uint8)])

cv2.imwrite("A.png", A)
print("已生成 A.png，内容:", s_id + " / " + s_name, " 尺寸:", A.shape)
