# -*- coding: utf-8 -*-
"""
实践任务4：
  任务1：设计自己的二维码内容 + 自己的logo，生成带logo的二维码；识别该二维码内容。
  任务2：制作一张含多个二维码的图像，识别并显示所有二维码的内容。
"""
import cv2
import numpy as np
import qrcode
from PIL import Image, ImageDraw, ImageFont

# 用 OpenCV 的解码器（能正确解出中文），替代 pyzbar
detector = cv2.QRCodeDetector()
# Windows 中文字体（微软雅黑），用于绘制中文内容
FONT_CJK = "C:/Windows/Fonts/msyh.ttc"


# ---------------------------------------------------------------
# 任务1 第0步：设计自己的 logo（透明背景，PNG，圆徽标 + 姓名缩写 ZJH）
# ---------------------------------------------------------------
def make_my_logo(size=400):
    """设计自己的logo：蓝色圆形徽标 + 白色姓名缩写 ZJH（透明背景带alpha）"""
    canvas = np.zeros((size, size, 4), np.uint8)   # BGRA，初始全透明
    c = size // 2
    r_out = int(size * 0.40)
    # 外圈描边环
    cv2.circle(canvas, (c, c), r_out, (200, 45, 35, 255), -1)        # 外圈(品牌蓝)
    cv2.circle(canvas, (c, c), r_out, (40, 120, 24, 255), 10)       # 白色描边
    # 内圈
    cv2.circle(canvas, (c, c), int(size * 0.30), (200, 45, 35, 255), -1)
    # 姓名缩写 ZJH
    text = "ZJH"
    font = cv2.FONT_HERSHEY_DUPLEX
    scale = size * 0.20 / 42.0
    thick = int(size * 0.045) + 2
    # 用 getTextSize 居中
    (tw, th), _ = cv2.getTextSize(text, font, scale, thick)
    org = (c - tw // 2, c + th // 2)
    cv2.putText(canvas, text, org, font, scale, (255, 255, 255, 255), thick, cv2.LINE_AA)
    # 下方小星点缀
    cv2.circle(canvas, (c, int(size * 0.80)), 8, (250, 210, 30, 255), -1)
    return canvas

logo = make_my_logo()
cv2.imwrite("1a_my_logo.png", logo)
print("已生成 1a_my_logo.png")

# ---------------------------------------------------------------
# 任务1：生成带logo的二维码
# ---------------------------------------------------------------
qr_content = "2025210515 朱嘉和 ZHUJIAHE"     # 自己设计的二维码内容

qr = qrcode.QRCode(
    version=4,
    error_correction=qrcode.constants.ERROR_CORRECT_H,   # 30%容错，放logo也不影响
    box_size=10,
    border=2,
)
qr.add_data(qr_content)
qr.make(fit=True)

qr_pil = qr.make_image(fill_color="black", back_color="white").convert("RGB")
qr_img = np.array(qr_pil)
qr_img = cv2.cvtColor(qr_img, cv2.COLOR_RGB2BGR)
cv2.imwrite("1b_qrcode_nologo.png", qr_img)   # 中间结果：二维码(无logo)

# 嵌入logo
qr_h, qr_w = qr_img.shape[:2]
logo_size = min(qr_w, qr_h) // 4
l_h, l_w = logo.shape[:2]
scale = logo_size / max(l_w, l_h)
logo_s = cv2.resize(logo, (int(l_w * scale), int(l_h * scale)), interpolation=cv2.INTER_AREA)
s_h, s_w = logo_s.shape[:2]
x_off = (qr_w - s_w) // 2
y_off = (qr_h - s_h) // 2
# alpha 混合（logo有透明通道）
alpha = logo_s[:, :, 3] / 255.0
for ch in range(3):
    qr_img[y_off:y_off + s_h, x_off:x_off + s_w, ch] = (
        alpha * logo_s[:, :, ch] + (1 - alpha) * qr_img[y_off:y_off + s_h, x_off:x_off + s_w, ch]
    )
cv2.imwrite("1c_qrcode_with_logo.png", qr_img)   # 最终结果：带logo的二维码
print("已生成 1c_qrcode_with_logo.png，内容：", qr_content)

# ---------------------------------------------------------------
# 识别二维码并把结果画到图上（任务1、任务2共用）
# ---------------------------------------------------------------
def annotate_qrs(image, output_path, label=""):
    """用 OpenCV 解码图中所有二维码，画框+编号，并在底部显示内容(支持中文)"""
    ret, info, pts, _ = detector.detectAndDecodeMulti(image)
    if not ret or not info:
        print("未检测到二维码")
        return None
    contents = []
    for idx, content in enumerate(info, start=1):
        if not content:
            content = "(无法解码)"
        # 画多边形框
        poly = pts[idx - 1].astype(np.int32).reshape((-1, 1, 2))
        cv2.polylines(image, [poly], True, (0, 255, 0), 3)
        # 左上角编号（ASCII，可用cv2）
        cv2.putText(image, f"#{idx}", (int(poly[0][0][0]), int(poly[0][0][1]) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 255), 2)
        contents.append((idx, content))
        print(f"  {label} 二维码#{idx} 内容:{content}")
    # 底部内容区（用PIL+中文字体，支持中文）
    h, w = image.shape[:2]
    line_h = 34
    ext = np.ones((h + line_h * len(contents) + 16, w, 3), np.uint8) * 255
    ext[:h, :, :] = image
    pil_img = Image.fromarray(cv2.cvtColor(ext, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)
    f = ImageFont.truetype(FONT_CJK, 22)
    for i, (idx, content) in enumerate(contents):
        y = h + 8 + (i + 1) * line_h
        draw.text((12, y), f"#{idx}: {content}", font=f, fill=(0, 0, 0))
    cv2.imwrite(output_path, cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR))
    print(f"  已保存看图结果 {output_path}")
    return contents

# 任务1：识别自己设计的带logo二维码
print("== 任务1：识别自己设计的二维码 ==")
annotate_qrs(cv2.imread("1c_qrcode_with_logo.png"), "1d_qrcode_decoded.png", label="")

# ---------------------------------------------------------------
# 任务2：制作一张含多个二维码的图像，再识别全部内容
# ---------------------------------------------------------------
def make_qr_image(content, box=8, border=3):
    q = qrcode.QRCode(version=4, error_correction=qrcode.constants.ERROR_CORRECT_M,
                      box_size=box, border=border)
    q.add_data(content); q.make(fit=True)
    im = q.make_image(fill_color="black", back_color="white").convert("RGB")
    return cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)

contents2 = [
    "https://www.hitwh.edu.cn",
    "2025210515 朱嘉和",
    "实践任务4 二维码识别演示",
]
qrs = [make_qr_image(c) for c in contents2]
# 拼成一张三连图
gap = 40
h = max(q.shape[0] for q in qrs)
w = sum(q.shape[1] for q in qrs) + gap * (len(qrs) - 1)
canvas = np.full((h, w, 3), 255, np.uint8)
x = 0
for q in qrs:
    canvas[:q.shape[0], x:x + q.shape[1]] = q
    x += q.shape[1] + gap
cv2.imwrite("2a_multi_qrcodes.png", canvas)
print("已生成 2a_multi_qrcodes.png（含", len(qrs), "个二维码）")

print("== 任务2：识别多二维码图像 ==")
annotate_qrs(cv2.imread("2a_multi_qrcodes.png"), "2b_multi_result.png", label="[任务2]")

print("\n全部完成！")
