# -*- coding: utf-8 -*-
"""
自动生成《实践任务1 图像滤镜设计》报告 Word 文档
文件名：学号姓名-1.docx  （请自行把文件名改成你的学号+姓名）
"""
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()

def add_img_cell(cell, caption, img_path):
    """在表格单元格中加入「标题段 + 居中图片段」"""
    cap = cell.paragraphs[0]
    cap.text = caption
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.runs[0].bold = True
    pic = cell.add_paragraph()
    pic.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pic.add_run().add_picture(img_path, width=Inches(3.2))

# ---------- 标题 ----------
title = doc.add_heading("实践任务1：图像滤镜设计", level=0)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
pline = doc.add_paragraph("学号姓名：＿＿＿＿＿＿＿＿＿＿＿＿")
pline.runs[0].font.size = Pt(12)

# ---------- 一、任务说明 ----------
doc.add_heading("一、任务说明", level=1)
doc.add_paragraph(
    "在例程 Lesson3 的 02_Filter.py 基础上，新增三种滤镜效果并绑定三个新的按键，"
    "使程序既能显示原有的边缘检测、高斯模糊，也能切换到新添加的三种滤镜模式。"
    "原始程序已有模式：Q/q/Esc 退出、C/c Canny 边缘检测、B/b 高斯模糊、P/p 预览。"
)
doc.add_paragraph("本次新增三种滤镜及对应按键：")
tbl = doc.add_table(rows=5, cols=2)
tbl.style = "Light Grid Accent 1"
for i, (a, b) in enumerate([("按键", "滤镜"), ("E / e", "浮雕 Emboss"),
                            ("K / k", "铅笔素描 Sketch"), ("M / m", "马赛克 Mosaic"),
                            ("S / s", "（辅助）保存当前帧截图")]):
    tbl.rows[i].cells[0].text = a
    tbl.rows[i].cells[1].text = b

# ---------- 二、滤镜1：浮雕 ----------
doc.add_heading("二、滤镜1：浮雕效果（Emboss）", level=1)
doc.add_paragraph("功能：让图像产生类似石刻/模具的三维浮雕立体感，物体边缘一侧发亮、另一侧"
                  "变暗，视觉效果非常明显、有趣。", style="List Bullet")
doc.add_paragraph("实现方法：使用卷积核（后向差分算子）对图像做卷积（cv2.filter2D）。卷积核主对角方向"
                  "取值由 -1 变为 1，用于提取图像沿对角方向的边缘梯度；delta=128 的偏移量保证卷积后的像素值"
                  "落在 0~255 的可见区间。", style="List Bullet")
doc.add_paragraph("核心代码：")
run = doc.add_paragraph().add_run(
    "k = np.array([[-1,-1,0],[-1,0,1],[0,1,1]])\n"
    "result = cv2.filter2D(frame, -1, k, delta=128)")
run.font.name = "Consolas"; run.font.size = Pt(10)
tk1 = doc.add_table(rows=1, cols=2); tk1.style = "Table Grid"
add_img_cell(tk1.rows[0].cells[0], "原图（预览）", "preview.png")
add_img_cell(tk1.rows[0].cells[1], "浮雕效果", "emboss.png")

# ---------- 三、滤镜2：素描 ----------
doc.add_heading("三、滤镜2：铅笔素描效果（Sketch）", level=1)
doc.add_paragraph("功能：把彩色图像转换成黑白铅笔手绘素描的效果，线条清晰、像用铅笔勾勒出来的画，"
                  "风格鲜明。", style="List Bullet")
doc.add_paragraph("实现方法：采用经典素描算法（灰度—反色—模糊—颜色减淡）：先转灰度图，再反色，对反色图"
                  "做高斯模糊，最后用颜色减淡公式 gray*255/(255-blur) 把两幅图相乘，得到明暗交界的素描线条。"
                  "为避免除以 0，分母加了极小量 1e-3，并把结果转回 uint8。", style="List Bullet")
doc.add_paragraph("核心代码：")
run = doc.add_paragraph().add_run(
    "gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)\n"
    "inv  = 255 - gray\n"
    "blur = cv2.GaussianBlur(inv, (13,13), 0)\n"
    "result = cv2.divide(gray.astype(np.float32), (255-blur).astype(np.float32)+1e-3, scale=255)\n"
    "result = result.astype(np.uint8)")
run.font.name = "Consolas"; run.font.size = Pt(10)
tk2 = doc.add_table(rows=1, cols=2); tk2.style = "Table Grid"
add_img_cell(tk2.rows[0].cells[0], "原图（预览）", "preview.png")
add_img_cell(tk2.rows[0].cells[1], "素描效果", "sketch.png")

# ---------- 四、滤镜3：马赛克 ----------
doc.add_heading("四、滤镜3：马赛克效果（Mosaic）", level=1)
doc.add_paragraph("功能：把图像变成由一个个色块组成的像素化马赛克，类似打码或复古像素画效果，非常有趣。",
                  style="List Bullet")
doc.add_paragraph("实现方法：采用「缩小—放大」的思路：先把整幅图按 block 倍缩小（宽高都除以 block），再用"
                  "最近邻插值（INTER_NEAREST）放大回原尺寸。最近邻插值不做平滑，因此放大后每个区域都是整数块"
                  "纯色，形成明显马赛克方块。block 越大，方块越大、效果越强。", style="List Bullet")
doc.add_paragraph("核心代码：")
run = doc.add_paragraph().add_run(
    "h, w = frame.shape[:2]\n"
    "small = cv2.resize(frame, (w//block, h//block), interpolation=cv2.INTER_NEAREST)\n"
    "result = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)   # block=30")
run.font.name = "Consolas"; run.font.size = Pt(10)
tk3 = doc.add_table(rows=1, cols=2); tk3.style = "Table Grid"
add_img_cell(tk3.rows[0].cells[0], "原图（预览）", "preview.png")
add_img_cell(tk3.rows[0].cells[1], "马赛克效果", "mosaic.png")

# ---------- 五、运行与按键说明 ----------
doc.add_heading("五、程序运行与按键说明", level=1)
doc.add_paragraph("运行：python 02_Filter.py （需已安装 opencv-python 和 numpy）")
doc.add_paragraph("按键：")
kt = doc.add_table(rows=7, cols=2); kt.style = "Light Grid Accent 1"
for i, (a, b) in enumerate([("按键", "功能"), ("Q / q / Esc", "退出循环，结束程序"),
                            ("C / c", "Canny 边缘检测"), ("B / b", "高斯模糊"),
                            ("P / p", "预览（原图）"), ("E / e", "浮雕效果（新增）"),
                            ("K / k", "铅笔素描（新增）；M/m 马赛克（新增）")]):
    kt.rows[i].cells[0].text = a
    kt.rows[i].cells[1].text = b

doc.add_heading("六、说明", level=1)
doc.add_paragraph(
    "报告中用于对比的图像为示例图（scanned-form.jpg）。你可以运行程序时按 S/s 键，把你自己摄像头的"
    "「原图」和「滤镜效果图」分别截图，替换本文档中的 preview.png、emboss.png、sketch.png、mosaic.png，"
    "以体现真实摄像头效果。")

doc.save("学号姓名-1.docx")
print("已生成：学号姓名-1.docx")
